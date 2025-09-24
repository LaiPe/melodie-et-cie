import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import des utilitaires de navigation
from navigation_utils import NavigationHelper, CMSHelper


class TestBackOfficeCMS:
    def __init__(self):
        """Initialise le test avec les paramètres du navigateur"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
        
        # Initialiser les helpers
        self.nav_helper = NavigationHelper(self.driver, 10)
        self.cms_helper = CMSHelper(self.driver, 10)
        
        # Configuration du test
        self.base_url = "http://localhost:8080"
        self.admin_url = f"{self.base_url}/admin/"
        self.formations_url = f"{self.base_url}/services/formation/"
        
        # Données de la formation de test (nom unique avec timestamp)
        import time
        timestamp = str(int(time.time()))
        self.test_formation = {
            "emoji": "♪",  # Caractère musical compatible BMP au lieu d'emoji
            "name": f"Cornemuse-Test-{timestamp}",  # Nom unique pour éviter les collisions
            "shortDescription": "Découvrez l'art ancestral de la cornemuse écossaise - Test automatisé",
            "longDescription": "Formation complète pour apprendre la cornemuse, instrument traditionnel aux sonorités uniques. Du débutant au niveau avancé. (Version test)",
            "teachers": ["Marie MacDonald", "Hamish McGregor"],
            "styles": ["Traditionnel écossais", "Folk", "Celtic"],
            "hash": f"cornemuse-test-{timestamp}"
        }
        
        # Chemin du fichier JSON qui sera créé
        self.json_file_path = os.path.join(
            os.getcwd(), 
            "src", "services", "formation", 
            f"{self.test_formation['name'].lower()}.json"
        )
    
    def run_test(self):
        """Lance le test complet"""
        print("🚀 Démarrage du test E2E Back-Office CMS")
        
        try:
            # Étape 1 : Navigation et vérification initiale
            self.navigate_to_formations_page()
            self.verify_formation_not_exists()
            
            # Étape 2 : Création via le back-office
            self.navigate_to_admin()
            self.click_on_cms_login()
            self.create_new_formation()
            
            # Étape 3 : Vérification de la création
            self.navigate_to_formations_page()
            self.verify_formation_exists()
            
            # Étape 4 : Nettoyage
            self.cleanup_created_formation()
            
            print("✅ Test terminé avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur durant le test: {e}")
            self.cleanup_created_formation()  # Nettoyage même en cas d'erreur
            raise
        finally:
            self.driver.quit()
    
    def navigate_to_formations_page(self):
        """Navigue de la home page vers la page des formations"""
        print("📍 Navigation vers la page des formations...")
        
        # Aller à la home page
        self.driver.get(self.base_url)
        self.nav_helper.safe_page_wait(2)
        
        # Navigation DIRECTE vers Formation depuis la page d'accueil
        # Utiliser les liens de la section services de la page d'accueil
        print("🎯 Navigation directe vers Formation depuis l'accueil...")
        
        formation_direct_selectors = [
            # Sélecteur le plus spécifique basé sur ton HTML
            (By.CSS_SELECTOR, "a[href='/services/formation'].service-link"),
            (By.XPATH, "//a[@href='/services/formation' and contains(@class, 'service-link')]"),
            (By.XPATH, "//section[@id='services']//a[contains(@href, 'formation')]"),
            (By.XPATH, "//h3[contains(text(), 'Formation Musicale')]/ancestor::a"),
            (By.XPATH, "//div[contains(text(), '🎓')]/following-sibling::h3[contains(text(), 'Formation')]/ancestor::a"),
            # Fallback sur les anciens sélecteurs
            (By.CSS_SELECTOR, "a.service-link[href*='formation']"),
            (By.LINK_TEXT, "Formation Musicale"),
            (By.PARTIAL_LINK_TEXT, "Formation")
        ]
        
        formation_clicked = False
        for selector_type, selector_value in formation_direct_selectors:
            try:
                formation_link = self.wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                formation_link.click()
                print(f"✅ Lien Formation direct cliqué: {selector_value}")
                formation_clicked = True
                break
            except Exception as e:
                print(f"   ⏳ Sélecteur '{selector_value}' échoué: {str(e)[:50]}")
                continue
        
        if not formation_clicked:
            print("⚠️ Navigation directe échouée, essai via la page Services...")
            # Fallback sur l'ancienne méthode si la navigation directe échoue
            if not self.nav_helper.navigate_to_services_page():
                raise AssertionError("❌ Impossible de naviguer vers Services")
            
            self.nav_helper.safe_page_wait(2)
            
            if not self.nav_helper.navigate_to_formation_page():
                raise AssertionError("❌ Impossible de naviguer vers Formation")
        
        # Vérifier qu'on est sur la bonne page
        self.nav_helper.safe_page_wait(2)
        if self.nav_helper.wait_for_url_contains("/services/formation/"):
            print("✅ Navigation vers formations réussie")
        else:
            raise AssertionError("❌ URL ne contient pas '/services/formation/'")
    
    def verify_formation_not_exists(self):
        """Vérifie que la formation de test n'existe pas"""
        print(f"🔍 Vérification de l'absence de la formation {self.test_formation['name']}...")
        
        try:
            # Chercher le nom exact de notre formation de test
            test_formation_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{self.test_formation['name']}')]")
            
            if len(test_formation_elements) == 0:
                print(f"✅ Confirmation: la formation {self.test_formation['name']} n'existe pas")
            else:
                # Si elle existe, on la supprime avant de commencer le test
                print(f"⚠️ La formation {self.test_formation['name']} existe déjà, nettoyage préventif...")
                self.cleanup_created_formation()
                # Attendre qu'Eleventy recharge la page
                print("⏳ Attente du rechargement d'Eleventy...")
                self.nav_helper.safe_page_wait(5)
                self.driver.refresh()
                self.nav_helper.safe_page_wait(3)
                
                # Re-vérifier
                test_formation_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{self.test_formation['name']}')]")
                if len(test_formation_elements) > 0:
                    print(f"⚠️ Formation toujours présente après nettoyage, elle sera écrasée")
                else:
                    print(f"✅ Formation nettoyée avec succès")
                
        except NoSuchElementException:
            print(f"✅ Confirmation: la formation {self.test_formation['name']} n'existe pas")
    
    def navigate_to_admin(self):
        """Navigue vers la page d'administration"""
        print("🔧 Navigation vers le back-office...")
        
        self.driver.get(self.admin_url)
        
        # Attendre que Decap CMS soit chargé avec les helpers
        if self.cms_helper.wait_for_cms_load():
            print("✅ Back-office chargé")
        else:
            print("⚠️ Back-office possiblement chargé mais non confirmé")
    
    def click_on_cms_login(self):
        """Se connecter au CMS (backend local ou authentification)"""
        print("🔑 Tentative de connexion au CMS...")
        
        # En mode local backend, il peut y avoir un bouton de connexion rapide
        # ou pas d'authentification nécessaire
        
        # Attendre un peu pour que la page se stabilise
        self.nav_helper.safe_page_wait(2)
        
        # Vérifier si on a déjà accès au CMS (backend local)
        try:
            # Chercher des éléments qui indiquent qu'on est déjà connecté
            dashboard_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Formation') or contains(text(), 'Collections')]")
            
            if len(dashboard_elements) > 0:
                print("✅ Déjà connecté au CMS (backend local)")
                return True
                
        except Exception as e:
            print(f"Debug: Erreur lors de la vérification de connexion: {e}")
        
        # Chercher un bouton de login/connexion
        login_button_selectors = [
            (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Connexion') or contains(text(), 'Se connecter')]"),
            (By.CSS_SELECTOR, "button[data-testid='login-button']"),
            (By.CSS_SELECTOR, "button.login-button"),
            (By.XPATH, "//button[contains(@class, 'login') or contains(@class, 'auth')]"),
            (By.XPATH, "//a[contains(text(), 'Login') or contains(text(), 'Connexion')]"),
        ]
        
        login_clicked = False
        for selector_type, selector_value in login_button_selectors:
            try:
                login_element = self.wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                login_element.click()
                print(f"✅ Bouton de connexion cliqué: {selector_value}")
                login_clicked = True
                break
            except Exception as e:
                print(f"Debug: Sélecteur '{selector_value}' non trouvé: {e}")
                continue
        
        if login_clicked:
            # Attendre après le clic sur login
            self.nav_helper.safe_page_wait(3)
            
            # Vérifier que la connexion a réussi
            try:
                dashboard_elements = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Formation') or contains(text(), 'Collections')]"))
                )
                print("✅ Connexion au CMS réussie")
                return True
            except TimeoutException:
                print("⚠️ Connexion incertaine, on continue...")
                return True
        else:
            print("ℹ️ Pas de bouton de connexion trouvé, probablement déjà connecté (backend local)")
            return True
    
    def create_new_formation(self):
        """Crée une nouvelle formation via le CMS"""
        print("➕ Création d'une nouvelle formation...")
        
        # Cliquer sur l'onglet "Formation" avec stratégies multiples
        if not self.cms_helper.click_cms_button(
            ["Formation", "formation"], 
            "onglet Formation"
        ):
            raise AssertionError("❌ Impossible de cliquer sur l'onglet Formation")
        
        self.nav_helper.safe_page_wait(2)
        
        # Cliquer sur "New Formation" avec stratégies multiples
        if not self.cms_helper.click_cms_button(
            ["New", "Nouveau", "Nouvelle", "Add", "Ajouter", "+"], 
            "bouton Nouvelle Formation"
        ):
            raise AssertionError("❌ Impossible de cliquer sur 'Nouvelle Formation'")
        
        self.nav_helper.safe_page_wait(2)
        
        # Remplir le formulaire
        self.fill_formation_form()
        
        # Sauvegarder avec stratégies multiples
        if not self.cms_helper.click_cms_button(
            ["Publish", "Save", "Publier", "Sauvegarder", "Enregistrer"], 
            "bouton Sauvegarder"
        ):
            raise AssertionError("❌ Impossible de sauvegarder la formation")
        
        # Attendre la confirmation
        self.nav_helper.safe_page_wait(3)
        print("✅ Formation créée avec succès")
    
    def fill_formation_form(self):
        """Remplit le formulaire de création de formation"""
        print("📝 Remplissage du formulaire...")
        
        # Utiliser les helpers pour remplir les champs basiques
        fields_to_fill = [
            ("emoji", self.test_formation["emoji"], "champ Emoji"),
            ("name", self.test_formation["name"], "nom de la formation"),
            ("shortDescription", self.test_formation["shortDescription"], "description courte"),
            ("longDescription", self.test_formation["longDescription"], "description longue"),
            ("hash", self.test_formation["hash"], "hash de la formation")
        ]
        
        for field_name, field_value, field_desc in fields_to_fill:
            if not self.cms_helper.fill_input_field(field_name, field_value, field_desc):
                print(f"⚠️ Impossible de remplir le {field_desc}")
        
        # Professeurs (string séparée par virgules dans le formulaire)
        print("📝 Ajout des professeurs...")
        teachers_string = ", ".join(self.test_formation["teachers"])
        if not self.cms_helper.fill_input_field("teachers", teachers_string, "champ Professeurs"):
            print("⚠️ Impossible de remplir le champ Professeurs")
        
        # Styles (string séparée par virgules dans le formulaire)  
        print("📝 Ajout des styles...")
        styles_string = ", ".join(self.test_formation["styles"])
        if not self.cms_helper.fill_input_field("styles", styles_string, "champ Styles"):
            print("⚠️ Impossible de remplir le champ Styles")
        
        self.nav_helper.safe_page_wait(1)
        print("✅ Formulaire rempli")
    
    def verify_formation_exists(self):
        """Vérifie que la formation a été créée et apparaît sur la page"""
        print("🔍 Vérification de la présence de la formation...")
        
        # Attendre qu'Eleventy recharge la page avec les nouvelles données
        print("⏳ Attente du rechargement d'Eleventy...")
        self.nav_helper.safe_page_wait(8)  # Plus de temps pour qu'Eleventy détecte le changement
        
        # Actualiser la page pour voir les changements
        print("🔄 Actualisation de la page...")
        self.driver.refresh()
        self.nav_helper.safe_page_wait(3)
        
        # Chercher la formation sur la page
        try:
            formation_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.test_formation['name']}')]"))
            )
            print(f"✅ Formation {self.test_formation['name']} trouvée sur la page des formations")
            
            # Vérifier aussi la description courte
            try:
                desc_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), 'Test automatisé')]")
                print("✅ Description de la formation également présente")
            except NoSuchElementException:
                print("⚠️ Description complète non trouvée, mais formation présente")
            
        except TimeoutException:
            print("❌ Formation non trouvée immédiatement, tentative de rechargement...")
            # Second essai après un rechargement plus long
            self.nav_helper.safe_page_wait(5)
            self.driver.refresh()
            self.nav_helper.safe_page_wait(3)
            
            try:
                formation_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.test_formation['name']}')]"))
                )
                print(f"✅ Formation {self.test_formation['name']} trouvée après second rechargement")
            except TimeoutException:
                raise AssertionError(f"❌ La formation {self.test_formation['name']} n'a pas été trouvée sur la page")
    
    def cleanup_created_formation(self):
        """Supprime le fichier JSON de la formation créée"""
        print("🧹 Nettoyage - suppression du fichier de formation...")
        
        try:
            if os.path.exists(self.json_file_path):
                os.remove(self.json_file_path)
                print(f"✅ Fichier supprimé: {self.json_file_path}")
            else:
                print("ℹ️ Aucun fichier à supprimer")
                
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression du fichier: {e}")


def main():
    """Point d'entrée principal du test"""
    print("🎯 Test E2E Back-Office CMS - Formation Cornemuse")
    print("=" * 60)
    
    # Vérifier que le serveur local tourne
    print("ℹ️ Assurez-vous que 'npm run dev' est actif avant de lancer ce test")
    input("Appuyez sur Entrée pour continuer...")
    
    # Lancer le test
    test = TestBackOfficeCMS()
    test.run_test()


if __name__ == "__main__":
    main()