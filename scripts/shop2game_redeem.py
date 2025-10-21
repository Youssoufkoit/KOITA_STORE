import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Shop2GameRedeemer:
    """Classe pour automatiser le processus de recharge sur shop2game.com"""
    
    def __init__(self):
        self.driver = None
        self.base_url = "https://shop2game.com/?channel=299999"
        
    def setup_driver(self):
        """Configuration du driver Selenium"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Mode sans interface
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def redeem_diamonds(self, free_fire_id, redeem_code):
        """
        Automatise le processus de recharge sur Shop2Game
        
        Retourne: (success: bool, message: str)
        """
        try:
            self.setup_driver()
            
            # Étape 1: Accéder au site
            self.driver.get(self.base_url)
            logger.info(f"Navigation vers {self.base_url}")
            
            # Étape 2: Remplir l'ID Free Fire
            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "id"))
            )
            id_input.clear()
            id_input.send_keys(free_fire_id)
            logger.info(f"ID Free Fire saisi: {free_fire_id}")
            
            # Étape 3: Cliquer sur le bouton Redeem
            redeem_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Redeem')]")
            redeem_button.click()
            logger.info("Clic sur le bouton Redeem")
            
            time.sleep(2)  # Attendre le chargement
            
            # Étape 4: Remplir le code REDEEM
            code_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "code"))  # Ajuster le sélecteur si nécessaire
            )
            code_input.clear()
            code_input.send_keys(redeem_code)
            logger.info(f"Code REDEEM saisi: {redeem_code}")
            
            # Étape 5: Soumettre le formulaire
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Confirmer')]")
            submit_button.click()
            logger.info("Formulaire soumis")
            
            # Étape 6: Vérifier le résultat
            time.sleep(5)  # Attendre la réponse
            
            # Vérifier les messages de succès/erreur
            page_source = self.driver.page_source.lower()
            
            if any(keyword in page_source for keyword in ['success', 'réussi', 'succès', 'added', 'ajouté']):
                logger.info("✅ Recharge réussie!")
                return True, "✅ Vos diamants ont été ajoutés avec succès!"
            elif any(keyword in page_source for keyword in ['error', 'erreur', 'invalid', 'invalide']):
                logger.warning("❌ Erreur lors de la recharge")
                return False, "❌ Erreur lors de l'ajout des diamants. Veuillez contacter le support."
            else:
                logger.info("⚠️ Résultat indéterminé, vérification manuelle nécessaire")
                return True, "⚠️ Recharge en cours de traitement. Vous recevrez une confirmation sous peu."
                
        except Exception as e:
            logger.error(f"Erreur lors du processus automatique: {str(e)}")
            return False, f"❌ Erreur technique: {str(e)}"
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def manual_redeem_fallback(self, free_fire_id, redeem_code):
        """
        Alternative manuelle si l'automatisation échoue
        """
        message = f"""
        🔄 Processus manuel requis:
        
        📱 ID Free Fire: {free_fire_id}
        🎁 Code REDEEM: {redeem_code}
        
        Étapes à suivre manuellement:
        1. Aller sur: https://shop2game.com/?channel=299999
        2. Entrer l'ID: {free_fire_id}
        3. Cliquer sur 'Redeem'
        4. Entrer le code: {redeem_code}
        5. Valider
        """
        return False, message