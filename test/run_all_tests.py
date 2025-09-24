#!/usr/bin/env python3
"""
Script de lancement pour tous les tests E2E
Vérifie que le serveur de développement est actif avant de lancer les tests
Lance tous les tests disponibles : navigation interne + back-office CMS
"""

import requests
import sys
import time
import subprocess
import importlib.util
import os
from pathlib import Path


def check_server_status(url, max_retries=5, delay=2):
    """Vérifie si le serveur local est accessible"""
    print(f"🔍 Vérification du serveur sur {url}...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Serveur accessible (tentative {attempt + 1})")
                return True
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                print(f"⏳ Serveur non accessible, nouvelle tentative dans {delay}s...")
                time.sleep(delay)
            else:
                print(f"❌ Serveur non accessible après {max_retries} tentatives")
    
    return False


def load_test_module(module_name, file_path):
    """Charge dynamiquement un module de test"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"❌ Erreur lors du chargement du module {module_name}: {e}")
        return None


def run_navigation_test():
    """Lance le test de navigation interne"""
    print("🧭 Lancement du test de navigation interne...")
    print("=" * 60)
    
    try:
        # Charger et exécuter le test de navigation
        current_dir = Path(__file__).parent
        nav_test_path = current_dir / "test_navigation_interne.py"
        
        if not nav_test_path.exists():
            print("⚠️ Fichier test_navigation_interne.py non trouvé")
            return False
            
        # Importer et exécuter la fonction de test
        nav_module = load_test_module("test_navigation_interne", str(nav_test_path))
        if nav_module and hasattr(nav_module, 'test_navigation_interne'):
            nav_module.test_navigation_interne()
            print("✅ Test de navigation terminé avec succès")
            return True
        else:
            print("❌ Fonction test_navigation_interne non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur durant le test de navigation: {e}")
        return False


def run_backoffice_test():
    """Lance le test E2E back-office CMS"""
    print("🎯 Lancement du test E2E Back-Office CMS...")
    print("=" * 60)
    
    try:
        # Charger et exécuter le test back-office
        current_dir = Path(__file__).parent
        cms_test_path = current_dir / "test_backoffice_cms.py"
        
        if not cms_test_path.exists():
            print("⚠️ Fichier test_backoffice_cms.py non trouvé")
            return False
            
        # Importer et exécuter la classe de test
        cms_module = load_test_module("test_backoffice_cms", str(cms_test_path))
        if cms_module and hasattr(cms_module, 'TestBackOfficeCMS'):
            test = cms_module.TestBackOfficeCMS()
            test.run_test()
            print("✅ Test back-office terminé avec succès")
            return True
        else:
            print("❌ Classe TestBackOfficeCMS non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur durant le test back-office: {e}")
        return False


def main():
    """Point d'entrée principal"""
    print("🚀 Lanceur de tests E2E - Suite complète")
    print("=" * 70)
    
    # Configuration
    server_url = "http://localhost:8080"
    admin_url = f"{server_url}/admin/"
    
    # Vérifier que le serveur principal est actif
    if not check_server_status(server_url):
        print()
        print("❌ Le serveur de développement n'est pas accessible.")
        print("🔧 Veuillez lancer 'npm run dev' dans un autre terminal avant de relancer ce test.")
        print()
        return False
    
    # Vérifier que la page admin est accessible
    if not check_server_status(admin_url):
        print()
        print("❌ La page d'administration n'est pas accessible.")
        print("🔧 Vérifiez que Decap CMS est correctement configuré.")
        print()
        return False
    
    print()
    print("✅ Serveurs accessibles, lancement des tests...")
    print()
    
    # Compteurs de résultats
    total_tests = 0
    successful_tests = 0
    
    # Test 1 : Navigation interne
    print("\n" + "🔸" * 70)
    total_tests += 1
    if run_navigation_test():
        successful_tests += 1
        
    print("\n" + "🔸" * 70)
    
    # Attente entre les tests pour laisser le temps au navigateur de se fermer
    print("⏳ Pause entre les tests...")
    time.sleep(3)
    
    # Test 2 : Back-office CMS
    total_tests += 1
    if run_backoffice_test():
        successful_tests += 1
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    print(f"Tests exécutés: {total_tests}")
    print(f"Tests réussis: {successful_tests}")
    print(f"Tests échoués: {total_tests - successful_tests}")
    
    if successful_tests == total_tests:
        print("\n🎉 Tous les tests ont réussi ! 🎉")
        return True
    else:
        print(f"\n⚠️ {total_tests - successful_tests} test(s) ont échoué")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)