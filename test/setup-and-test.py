#!/usr/bin/env python3
"""
Script de lancement des tests avec vérification et installation automatique des dépendances
Compatible Windows, macOS et Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_colored(message, color="white"):
    """Affichage coloré selon la plateforme"""
    colors = {
        "green": "\033[92m" if platform.system() != "Windows" else "",
        "yellow": "\033[93m" if platform.system() != "Windows" else "",
        "red": "\033[91m" if platform.system() != "Windows" else "",
        "reset": "\033[0m" if platform.system() != "Windows" else "",
    }
    
    color_code = colors.get(color, "")
    reset_code = colors.get("reset", "")
    print(f"{color_code}{message}{reset_code}")

def get_python_executable():
    """Déterminer le bon exécutable Python selon l'OS"""
    if platform.system() == "Windows":
        return Path("venv/Scripts/python.exe")
    else:
        return Path("venv/bin/python")

def get_pip_executable():
    """Déterminer le bon exécutable pip selon l'OS"""
    if platform.system() == "Windows":
        return Path("venv/Scripts/pip.exe")
    else:
        return Path("venv/bin/pip")

def create_venv():
    """Créer l'environnement virtuel s'il n'existe pas"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print_colored("⚠️ Environnement virtuel non trouvé. Création en cours...", "yellow")
        result = subprocess.run([sys.executable, "-m", "venv", "venv"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_colored("✅ Environnement virtuel créé", "green")
        else:
            print_colored(f"❌ Erreur lors de la création de l'environnement virtuel: {result.stderr}", "red")
            sys.exit(1)

def check_dependencies():
    """Vérifier si les dépendances sont installées"""
    python_exe = get_python_executable()
    modules = ["selenium", "requests", "webdriver_manager"]
    missing_modules = []
    
    for module in modules:
        result = subprocess.run([str(python_exe), "-c", f"import {module}"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            missing_modules.append(module)
    
    return missing_modules

def install_dependencies():
    """Installer les dépendances depuis requirements.txt"""
    python_exe = get_python_executable()
    requirements_path = Path("test/requirements.txt")
    
    if not requirements_path.exists():
        print_colored("❌ Fichier requirements.txt non trouvé", "red")
        sys.exit(1)
    
    print_colored("📦 Installation des dépendances...", "yellow")
    result = subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(requirements_path)], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print_colored("✅ Dépendances installées avec succès", "green")
    else:
        print_colored(f"❌ Erreur lors de l'installation: {result.stderr}", "red")
        sys.exit(1)

def run_tests():
    """Lancer les tests"""
    python_exe = get_python_executable()
    test_script = Path("test/run_all_tests.py")
    
    if not test_script.exists():
        print_colored("❌ Script de test non trouvé", "red")
        sys.exit(1)
    
    print_colored("🎯 Lancement des tests...", "green")
    print()  # Ligne vide pour la lisibilité
    
    result = subprocess.run([str(python_exe), str(test_script)])
    sys.exit(result.returncode)

def main():
    """Fonction principale"""
    # Changer vers le répertoire parent (racine du projet) pour les chemins relatifs
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print_colored("🚀 Préparation de l'environnement de test...", "green")
    
    # Vérifier/créer l'environnement virtuel
    create_venv()
    
    # Vérifier les dépendances
    print_colored("🔍 Vérification des dépendances Python...", "yellow")
    missing_modules = check_dependencies()
    
    if missing_modules:
        print_colored(f"📦 Installation des dépendances manquantes: {', '.join(missing_modules)}", "yellow")
        install_dependencies()
    else:
        print_colored("✅ Toutes les dépendances sont déjà installées", "green")
    
    # Lancer les tests
    run_tests()

if __name__ == "__main__":
    main()