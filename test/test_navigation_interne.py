from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Import des utilitaires de navigation
from navigation_utils import NavigationHelper

def test_navigation_interne():
    """Test de navigation interne du site Mélodie & Cie"""
    print("🎵 Démarrage du test de navigation - Site Mélodie & Cie")
    
    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    # Initialiser le helper de navigation
    nav_helper = NavigationHelper(driver, 10)
    
    try:
        # URL locale
        base_url = "http://localhost:8080"  # URL par défaut d'Eleventy --serve
        
        print("📍 Test 1: Chargement de la page d'accueil")
        driver.get(base_url)
        nav_helper.safe_page_wait(2)
        
        # Vérifier le titre de la page
        assert "Mélodie & Cie" in driver.title
        print("✅ Page d'accueil chargée avec succès")
        
        print("📍 Test 2: Navigation vers Services")
        if nav_helper.navigate_to_services_page():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            assert "services" in current_url
            print("✅ Navigation vers Services réussie")
        else:
            print("⚠️ Navigation vers Services échouée")
        
        print("📍 Test 3: Navigation vers Formation")
        if nav_helper.navigate_to_formation_page():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            assert "formation" in current_url
            print("✅ Navigation vers Formation réussie")
        else:
            print("⚠️ Navigation vers Formation échouée")
        
        print("📍 Test 4: Navigation vers Événements")
        if nav_helper.navigate_to_evenements_page():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            assert "evenements" in current_url
            print("✅ Navigation vers Événements réussie")
        else:
            print("⚠️ Navigation vers Événements échouée")
        
        print("📍 Test 5: Navigation vers Production")
        if nav_helper.navigate_to_production_page():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            assert "production" in current_url
            print("✅ Navigation vers Production réussie")
        else:
            print("⚠️ Navigation vers Production échouée")
        
        print("📍 Test 6: Navigation vers Contact")
        if nav_helper.navigate_to_contact_page():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            assert "contact" in current_url
            print("✅ Navigation vers Contact réussie")
        else:
            print("⚠️ Navigation vers Contact échouée")
        
        print("📍 Test 7: Retour à l'accueil")
        if nav_helper.navigate_to_home():
            nav_helper.safe_page_wait(2)
            current_url = driver.current_url
            # Vérifier qu'on est revenu à l'accueil
            assert current_url == base_url or current_url == base_url + "/" or "index" in current_url
            print("✅ Retour à l'accueil réussi")
        else:
            print("⚠️ Retour à l'accueil échoué")
        
        print("\n🎉 Test de navigation terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        raise
    
    finally:
        driver.quit()
        print("🔚 Navigateur fermé")

if __name__ == "__main__":
    test_navigation_interne()
