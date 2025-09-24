"""
Utilitaires partagés pour les tests Selenium de Mélodie & Cie
Contient des méthodes communes de navigation et d'interaction avec le site
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NavigationHelper:
    """Classe utilitaire pour la navigation robuste sur le site"""
    
    def __init__(self, driver, wait_timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
    
    def click_with_multiple_strategies(self, selectors_list, element_description="élément", timeout=10):
        """
        Tente de cliquer sur un élément en utilisant plusieurs stratégies de sélection.
        
        Args:
            selectors_list: Liste de tuples (By.TYPE, "selector_value")
            element_description: Description de l'élément pour les logs
            timeout: Délai d'attente pour chaque tentative
        
        Returns:
            bool: True si le clic a réussi, False sinon
        """
        print(f"🔍 Recherche de l'{element_description}...")
        
        for i, (selector_type, selector_value) in enumerate(selectors_list, 1):
            try:
                print(f"   Tentative {i}/{len(selectors_list)}: {selector_type} = '{selector_value}'")
                
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                element.click()
                print(f"✅ {element_description.capitalize()} trouvé et cliqué avec succès !")
                return True
                
            except (TimeoutException, NoSuchElementException) as e:
                print(f"   ⏳ Tentative {i} échouée: {type(e).__name__}")
                continue
        
        print(f"❌ {element_description.capitalize()} non trouvé avec toutes les stratégies")
        return False
    
    def navigate_to_services_page(self):
        """Navigate vers la page Services avec stratégies multiples"""
        services_selectors = [
            (By.CSS_SELECTOR, "a.service-link[href*='services']"),
            (By.LINK_TEXT, "Services"),
            (By.PARTIAL_LINK_TEXT, "Services"),
            (By.XPATH, "//a[contains(@href, 'services')]"),
            (By.CSS_SELECTOR, "a[href='/services/']")
        ]
        
        return self.click_with_multiple_strategies(
            services_selectors, 
            "lien Services"
        )
    
    def navigate_to_formation_page(self):
        """Navigate vers la page Formation avec stratégies multiples"""
        formation_selectors = [
            (By.CSS_SELECTOR, "a.service-link[href*='formation']"),
            (By.LINK_TEXT, "Formation Musicale"),
            (By.PARTIAL_LINK_TEXT, "Formation"),
            (By.XPATH, "//h3[contains(text(), 'Formation')]/ancestor::a[@class='service-link']"),
            (By.XPATH, "//a[contains(@href, 'formation')]"),
            (By.CSS_SELECTOR, "a[href='/services/formation/']")
        ]
        
        return self.click_with_multiple_strategies(
            formation_selectors, 
            "lien Formation"
        )
    
    def navigate_to_evenements_page(self):
        """Navigate vers la page Événements avec stratégies multiples"""
        evenements_selectors = [
            (By.CSS_SELECTOR, "a.service-link[href*='evenements']"),
            (By.LINK_TEXT, "Événements"),
            (By.PARTIAL_LINK_TEXT, "Événements"),
            (By.XPATH, "//h3[contains(text(), 'Événements')]/ancestor::a[@class='service-link']"),
            (By.XPATH, "//a[contains(@href, 'evenements')]"),
            (By.CSS_SELECTOR, "a[href='/services/evenements/']")
        ]
        
        return self.click_with_multiple_strategies(
            evenements_selectors, 
            "lien Événements"
        )
    
    def navigate_to_production_page(self):
        """Navigate vers la page Production avec stratégies multiples"""
        production_selectors = [
            (By.CSS_SELECTOR, "a.service-link[href*='production']"),
            (By.LINK_TEXT, "Production"),
            (By.PARTIAL_LINK_TEXT, "Production"),
            (By.XPATH, "//h3[contains(text(), 'Production')]/ancestor::a[@class='service-link']"),
            (By.XPATH, "//a[contains(@href, 'production')]"),
            (By.CSS_SELECTOR, "a[href='/services/production/']")
        ]
        
        return self.click_with_multiple_strategies(
            production_selectors, 
            "lien Production"
        )
    
    def navigate_to_contact_page(self):
        """Navigate vers la page Contact avec stratégies multiples"""
        contact_selectors = [
            (By.CSS_SELECTOR, "a.service-link[href*='contact']"),
            (By.LINK_TEXT, "Contact"),
            (By.PARTIAL_LINK_TEXT, "Contact"),
            (By.XPATH, "//h3[contains(text(), 'Contact')]/ancestor::a[@class='service-link']"),
            (By.XPATH, "//a[contains(@href, 'contact')]"),
            (By.CSS_SELECTOR, "a[href='/contact/']")
        ]
        
        return self.click_with_multiple_strategies(
            contact_selectors, 
            "lien Contact"
        )
    
    def navigate_to_home(self):
        """Navigate vers la page d'accueil avec stratégies multiples"""
        home_selectors = [
            (By.LINK_TEXT, "Mélodie & Cie"),
            (By.LINK_TEXT, "Accueil"),
            (By.CLASS_NAME, "logo"),
            (By.CSS_SELECTOR, "a[href='/']"),
            (By.CSS_SELECTOR, "a[href='index.html']"),
            (By.XPATH, "//a[@href='/']")
        ]
        
        return self.click_with_multiple_strategies(
            home_selectors, 
            "lien vers l'accueil"
        )
    
    def wait_for_url_contains(self, url_part, timeout=10):
        """Attend que l'URL contienne une partie spécifique"""
        try:
            self.wait.until(EC.url_contains(url_part))
            print(f"✅ URL contient '{url_part}' - Navigation réussie")
            return True
        except TimeoutException:
            print(f"❌ L'URL ne contient toujours pas '{url_part}' après {timeout}s")
            return False
    
    def safe_page_wait(self, seconds=2):
        """Attente sécurisée entre les actions"""
        time.sleep(seconds)


class CMSHelper:
    """Classe utilitaire pour les interactions avec Decap CMS"""
    
    def __init__(self, driver, wait_timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.nav_helper = NavigationHelper(driver, wait_timeout)
    
    def wait_for_cms_load(self, timeout=15):
        """Attend que Decap CMS soit complètement chargé"""
        print("⏳ Attente du chargement complet de Decap CMS...")
        
        cms_selectors = [
            "[data-testid='app']",
            ".nc-app-container", 
            "#nc-root",
            ".cms-app",
            "[role='main']"
        ]
        
        for selector in cms_selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"✅ CMS chargé (détecté via {selector})")
                time.sleep(3)  # Temps supplémentaire pour stabilité
                return True
            except TimeoutException:
                continue
        
        print("⚠️ CMS possiblement chargé mais sélecteurs standards non trouvés")
        time.sleep(5)  # Attente de fallback
        return False
    
    def click_cms_button(self, button_texts, button_description="bouton CMS"):
        """Clique sur un bouton du CMS avec textes multiples"""
        button_selectors = []
        
        # Sélecteurs spécifiques pour l'onglet Formation dans Decap CMS (sidebar navigation)
        if "Formation" in button_texts or "formation" in button_texts:
            if "onglet" in button_description.lower():
                # Sélecteurs UNIQUEMENT pour l'onglet de navigation (pas le bouton New)
                button_selectors.extend([
                    (By.CSS_SELECTOR, "a[data-testid='formations']:not([href*='/new'])"),
                    (By.CSS_SELECTOR, "a[href='#/collections/formations']:not([href*='/new'])"),
                    (By.XPATH, "//a[contains(@href, '/collections/formations') and not(contains(@href, '/new'))]"),
                    (By.XPATH, "//a[contains(@class, 'SidebarNavLink') and contains(text(), 'Formation')]"),
                    (By.CSS_SELECTOR, "a.sidebar-active:not([href*='/new'])"),
                    (By.XPATH, "//nav//a[contains(text(), 'Formation') and not(contains(@href, '/new'))]"),
                    (By.CSS_SELECTOR, "[data-testid='formations'][class*='SidebarNavLink']")
                ])
            else:
                # Sélecteurs pour le bouton "New Formation" 
                button_selectors.extend([
                    (By.CSS_SELECTOR, "a[href*='/collections/formations/new']"),
                    (By.CSS_SELECTOR, "a.CollectionTopNewButton"),
                    (By.XPATH, "//a[contains(@href, '/new') and contains(text(), 'Formation')]"),
                    (By.CSS_SELECTOR, "a[class*='CollectionTopNewButton']")
                ])
        
        # Gestion spéciale pour le bouton Publish (dropdown)
        elif any(text in ["Publish", "Save", "Publier", "Sauvegarder", "Enregistrer"] for text in button_texts):
            print("🎯 Gestion spéciale du bouton Publish (dropdown)")
            return self._handle_publish_dropdown()
        
        # Sélecteurs génériques pour les autres boutons
        for text in button_texts:
            button_selectors.extend([
                (By.XPATH, f"//button[contains(text(), '{text}')]"),
                (By.XPATH, f"//a[contains(text(), '{text}')]"),
                (By.XPATH, f"//button[@aria-label='{text}']"),
                (By.XPATH, f"//*[contains(@class, 'button') and contains(text(), '{text}')]"),
                (By.CSS_SELECTOR, f"[aria-label*='{text}']"),
                (By.XPATH, f"//*[@role='button' and contains(text(), '{text}')]")
            ])
        
        return self.nav_helper.click_with_multiple_strategies(
            button_selectors,
            button_description
        )
    
    def _handle_publish_dropdown(self):
        """Gère spécifiquement le bouton Publish dropdown de Decap CMS"""
        print("📤 Étape 1: Clic sur le bouton Publish principal...")
        
        # Sélecteurs pour le bouton Publish principal
        publish_button_selectors = [
            (By.CSS_SELECTOR, "span.css-1qpwgo3-StyledDropdownButton-button-button-default-default-caret-caret-caretDown-caretDown-DropdownButton-noOverflow-PublishButton"),
            (By.XPATH, "//span[contains(@class, 'PublishButton') and contains(text(), 'Publish')]"),
            (By.XPATH, "//span[@role='button' and contains(text(), 'Publish')]"),
            (By.CSS_SELECTOR, "[class*='PublishButton']"),
            (By.XPATH, "//span[contains(@class, 'StyledDropdownButton') and text()='Publish']")
        ]
        
        # Cliquer sur le bouton Publish principal
        publish_clicked = False
        for selector_type, selector_value in publish_button_selectors:
            try:
                publish_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                publish_btn.click()
                print(f"✅ Bouton Publish principal cliqué: {selector_value}")
                publish_clicked = True
                break
            except Exception as e:
                print(f"   ⏳ Sélecteur Publish '{selector_value}' échoué: {str(e)[:50]}")
                continue
        
        if not publish_clicked:
            print("❌ Impossible de cliquer sur le bouton Publish principal")
            return False
        
        # Attendre que le dropdown s'ouvre
        self.nav_helper.safe_page_wait(1)
        
        print("📤 Étape 2: Clic sur 'Publish now' dans le dropdown...")
        
        # Sélecteurs pour "Publish now" dans le dropdown
        publish_now_selectors = [
            (By.XPATH, "//div[@role='menuitem']//span[contains(text(), 'Publish now')]"),
            (By.XPATH, "//div[@role='menuitem' and contains(., 'Publish now')]"),
            (By.CSS_SELECTOR, "div[role='menuitem'] span:contains('Publish now')"),
            (By.XPATH, "//ul[contains(@class, 'DropdownList')]//span[text()='Publish now']"),
            (By.XPATH, "//div[contains(@class, 'StyledMenuItem')]//span[text()='Publish now']")
        ]
        
        # Cliquer sur "Publish now"
        for selector_type, selector_value in publish_now_selectors:
            try:
                publish_now_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                publish_now_btn.click()
                print(f"✅ 'Publish now' cliqué: {selector_value}")
                return True
            except Exception as e:
                print(f"   ⏳ Sélecteur 'Publish now' '{selector_value}' échoué: {str(e)[:50]}")
                continue
        
        print("❌ Impossible de cliquer sur 'Publish now' dans le dropdown")
        return False
    
    def fill_input_field(self, field_name, value, field_description=None):
        """Remplit un champ d'input avec gestion d'erreurs"""
        if not field_description:
            field_description = f"champ {field_name}"
            
        print(f"📝 Remplissage du {field_description}...")
        
        # Gestion spéciale pour les emojis - fallback si ChromeDriver échoue
        if field_name == "emoji" and any(ord(c) > 0xFFFF for c in str(value)):
            print(f"⚠️ Emoji détecté qui peut poser problème avec ChromeDriver: {value}")
            # Alternatives compatibles BMP
            emoji_fallbacks = {
                "🎺": "♪",  # Note musicale
                "🎵": "♫",  # Notes musicales
                "🎶": "♬",  # Notes musicales multiples
                "🥁": "♩",  # Noire
                "🎹": "♭",  # Bémol
                "🎸": "♯",  # Dièse
            }
            
            original_value = value
            if value in emoji_fallbacks:
                value = emoji_fallbacks[value]
                print(f"  → Remplacement par caractère compatible: {original_value} → {value}")
        
        # Sélecteurs basés sur la structure HTML réelle de Decap CMS
        field_selectors = [
            # Sélecteurs par ID (plus précis)
            (By.CSS_SELECTOR, f"input[id^='{field_name}-field-']"),
            (By.CSS_SELECTOR, f"textarea[id^='{field_name}-field-']"),
            (By.ID, f"{field_name}-field-1"),
            (By.ID, f"{field_name}-field-2"),
            (By.ID, f"{field_name}-field-3"),
            (By.ID, f"{field_name}-field-4"),
            (By.ID, f"{field_name}-field-5"),
            (By.ID, f"{field_name}-field-6"),
            (By.ID, f"{field_name}-field-7"),
            (By.ID, f"{field_name}-field-8"),
            (By.ID, f"{field_name}-field-9"),
            # Sélecteurs génériques de fallback
            (By.NAME, field_name),
            (By.CSS_SELECTOR, f"input[name='{field_name}']"),
            (By.CSS_SELECTOR, f"textarea[name='{field_name}']"),
            (By.XPATH, f"//input[@name='{field_name}']"),
            (By.XPATH, f"//textarea[@name='{field_name}']"),
            # Sélecteurs par label (association label-input)
            (By.XPATH, f"//label[contains(text(), '{field_description}')]/following::input[1]"),
            (By.XPATH, f"//label[contains(text(), '{field_description}')]/following::textarea[1]")
        ]
        
        # Mapping spécifique pour les champs connus
        field_mapping = {
            "emoji": ["emoji-field-1"],
            "name": ["name-field-2"],
            "shortDescription": ["shortDescription-field-3"],
            "longDescription": ["longDescription-field-4"],
            "teachers": ["teachers-field-5"],
            "styles": ["styles-field-7"],
            "hash": ["hash-field-9"]
        }
        
        # Essayer d'abord les IDs mappés spécifiquement
        if field_name in field_mapping:
            for field_id in field_mapping[field_name]:
                try:
                    field = self.driver.find_element(By.ID, field_id)
                    field.clear()
                    field.send_keys(value)
                    print(f"✅ {field_description.capitalize()} rempli via ID '{field_id}': '{value}'")
                    return True
                except Exception as e:
                    print(f"   ⏳ Erreur avec ID '{field_id}': {str(e)[:100]}")
                    continue
        
        # Fallback sur les sélecteurs génériques
        for selector_type, selector_value in field_selectors:
            try:
                field = self.driver.find_element(selector_type, selector_value)
                field.clear()
                field.send_keys(value)
                print(f"✅ {field_description.capitalize()} rempli via '{selector_value}': '{value}'")
                return True
            except Exception as e:
                continue
        
        print(f"❌ {field_description.capitalize()} non trouvé avec aucun sélecteur")
        return False