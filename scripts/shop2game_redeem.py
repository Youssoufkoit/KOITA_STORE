import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class Shop2GameRedeemer:
    """Classe améliorée pour automatiser la recharge sur shop2game.com"""
    
    def __init__(self):
        self.driver = None
        self.base_url = "https://shop2game.com/?channel=299999"
        self.wait_timeout = 15  # secondes
        
    def setup_driver(self):
        """Configuration optimisée du driver Selenium avec ChromeDriver auto-installé"""
        try:
            chrome_options = Options()
            
            # Options pour environnement serveur
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Installation automatique de ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            
            logger.info("✅ Driver Selenium initialisé avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation du driver: {str(e)}")
            return False
        
    def redeem_diamonds(self, free_fire_id, redeem_code):
        """
        Automatise le processus de recharge avec gestion d'erreurs robuste
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Initialisation du driver
            if not self.setup_driver():
                return False, "Impossible d'initialiser le navigateur automatique"
            
            logger.info(f"🔄 Début de la recharge - ID: {free_fire_id}, Code: {redeem_code}")
            
            # Étape 1: Accéder au site
            self.driver.get(self.base_url)
            logger.info(f"✅ Navigation vers {self.base_url}")
            time.sleep(3)  # Attendre le chargement complet
            
            # Étape 2: Trouver et remplir le champ ID
            try:
                # Essayer plusieurs sélecteurs possibles
                id_selectors = [
                    "input[name='id']",
                    "input[placeholder*='Player ID']",
                    "input[placeholder*='Game ID']",
                    "#player-id",
                    "input[type='text'][class*='player']"
                ]
                
                id_input = None
                for selector in id_selectors:
                    try:
                        id_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if id_input:
                            break
                    except TimeoutException:
                        continue
                
                if not id_input:
                    logger.error("❌ Impossible de trouver le champ ID")
                    return False, "Champ ID introuvable sur le site"
                
                id_input.clear()
                id_input.send_keys(free_fire_id)
                logger.info(f"✅ ID Free Fire saisi: {free_fire_id}")
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la saisie de l'ID: {str(e)}")
                return False, f"Impossible de saisir l'ID: {str(e)}"
            
            # Étape 3: Cliquer sur le bouton Redeem/Submit
            try:
                # Essayer plusieurs sélecteurs pour le bouton
                button_selectors = [
                    "button:contains('Redeem')",
                    "button[type='submit']",
                    "button:contains('Submit')",
                    "button:contains('Confirm')",
                    ".redeem-button",
                    "#redeem-btn"
                ]
                
                redeem_clicked = False
                for selector in button_selectors:
                    try:
                        if ':contains' in selector:
                            # Utiliser XPath pour :contains
                            text = selector.split("'")[1]
                            xpath = f"//button[contains(text(), '{text}')]"
                            redeem_button = self.driver.find_element(By.XPATH, xpath)
                        else:
                            redeem_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if redeem_button.is_displayed() and redeem_button.is_enabled():
                            redeem_button.click()
                            redeem_clicked = True
                            logger.info("✅ Clic sur le bouton Redeem")
                            break
                    except (NoSuchElementException, TimeoutException):
                        continue
                
                if not redeem_clicked:
                    logger.warning("⚠️ Bouton Redeem introuvable, tentative directe")
                    # Fallback: soumettre le formulaire
                    id_input.submit()
                
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du clic sur Redeem: {str(e)}")
                return False, f"Impossible de cliquer sur le bouton: {str(e)}"
            
            # Étape 4: Remplir le code REDEEM
            try:
                code_selectors = [
                    "input[name='code']",
                    "input[placeholder*='Redeem']",
                    "input[placeholder*='Code']",
                    "#redeem-code",
                    "input[type='text'][class*='code']"
                ]
                
                code_input = None
                for selector in code_selectors:
                    try:
                        code_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if code_input:
                            break
                    except TimeoutException:
                        continue
                
                if not code_input:
                    logger.error("❌ Impossible de trouver le champ CODE")
                    return False, "Champ CODE REDEEM introuvable"
                
                code_input.clear()
                code_input.send_keys(redeem_code)
                logger.info(f"✅ Code REDEEM saisi: {redeem_code}")
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la saisie du code: {str(e)}")
                return False, f"Impossible de saisir le code: {str(e)}"
            
            # Étape 5: Soumettre le formulaire final
            try:
                submit_selectors = [
                    "button[type='submit']",
                    "button:contains('Submit')",
                    "button:contains('Confirm')",
                    "button:contains('Claim')",
                    ".submit-button"
                ]
                
                for selector in submit_selectors:
                    try:
                        if ':contains' in selector:
                            text = selector.split("'")[1]
                            xpath = f"//button[contains(text(), '{text}')]"
                            submit_button = self.driver.find_element(By.XPATH, xpath)
                        else:
                            submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if submit_button.is_displayed():
                            submit_button.click()
                            logger.info("✅ Formulaire soumis")
                            break
                    except (NoSuchElementException, TimeoutException):
                        continue
                
                time.sleep(5)  # Attendre la réponse du serveur
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la soumission: {str(e)}")
                return False, f"Impossible de soumettre: {str(e)}"
            
            # Étape 6: Vérifier le résultat
            try:
                page_source = self.driver.page_source.lower()
                page_title = self.driver.title.lower()
                
                # Mots-clés de succès
                success_keywords = [
                    'success', 'réussi', 'succès', 'successful',
                    'claimed', 'added', 'ajouté', 'redeemed',
                    'congratulations', 'félicitations'
                ]
                
                # Mots-clés d'erreur
                error_keywords = [
                    'error', 'erreur', 'failed', 'échoué',
                    'invalid', 'invalide', 'expired', 'expiré',
                    'already used', 'déjà utilisé', 'incorrect'
                ]
                
                # Vérifier les messages de succès
                if any(keyword in page_source or keyword in page_title for keyword in success_keywords):
                    logger.info("✅ Recharge réussie détectée!")
                    return True, "✅ Diamants ajoutés avec succès à votre compte Free Fire!"
                
                # Vérifier les messages d'erreur
                if any(keyword in page_source or keyword in page_title for keyword in error_keywords):
                    logger.warning("❌ Erreur détectée dans la réponse")
                    
                    # Essayer de capturer le message d'erreur exact
                    error_message = "Code invalide ou déjà utilisé"
                    try:
                        error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, [class*='error']")
                        if error_elements:
                            error_message = error_elements[0].text
                    except:
                        pass
                    
                    return False, f"❌ Erreur lors de l'activation: {error_message}"
                
                # Résultat indéterminé
                logger.warning("⚠️ Impossible de déterminer le résultat avec certitude")
                return False, "⚠️ Recharge en cours de traitement. Vérifiez votre compte Free Fire dans quelques minutes."
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la vérification du résultat: {str(e)}")
                return False, f"Impossible de vérifier le résultat: {str(e)}"
                
        except Exception as e:
            logger.critical(f"💥 ERREUR CRITIQUE dans le processus: {str(e)}", exc_info=True)
            return False, f"❌ Erreur système: {str(e)}"
            
        finally:
            # Toujours fermer le driver
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("✅ Driver fermé proprement")
                except:
                    pass
    
    def manual_redeem_fallback(self, free_fire_id, redeem_code):
        """
        Instructions manuelles si l'automatisation échoue
        """
        message = f"""
╔════════════════════════════════════════════════╗
║     🔧 PROCESSUS MANUEL REQUIS 🔧             ║
╚════════════════════════════════════════════════╝

📱 VOTRE ID FREE FIRE: {free_fire_id}
🎁 VOTRE CODE REDEEM: {redeem_code}

📋 ÉTAPES À SUIVRE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Allez sur: https://shop2game.com/?channel=299999

2️⃣  Connectez-vous avec votre compte Garena
    (le même que pour Free Fire)

3️⃣  Entrez votre ID Free Fire: {free_fire_id}

4️⃣  Cliquez sur "Redeem" ou "Échanger"

5️⃣  Collez votre code: {redeem_code}

6️⃣  Validez - Vos diamants seront ajoutés instantanément!

⚠️  IMPORTANT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Ce code est à usage UNIQUE
• Conservez-le précieusement
• Valable pendant 7 jours

❓ Besoin d'aide ?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email: support@koitastore.com
📱 WhatsApp: +221 78 785 27 11

        """
        return False, message