import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime

# Fonction pour faire défiler la page jusqu'en bas
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Fonction pour remplir un champ en simulant une saisie lente
def type_slowly(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

# Initialisation du driver en mode navigation privée
def init_driver():
    options = uc.ChromeOptions()
    options.headless = False  # False pour voir l'exécution, True pour arrière-plan
    options.add_argument("--incognito")  # Mode navigation privée
    return uc.Chrome(options=options)

# Attendre la présence d'un élément avant de l'utiliser
def attendre_element(driver, by, valeur, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, valeur)))

# Attendre que l'élément soit cliquable avant d'agir
def attendre_et_cliquer(driver, by, valeur, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, valeur)))
    element.click()
    print(f"✅ Élément cliqué : {valeur}")

# Accepter les cookies sur Bouygues Telecom
def accepter_cookies_bouygues(driver):
    try:
        accept_cookies = driver.find_element(By.ID, "popin_tc_privacy_button_3")
        attendre_et_cliquer(driver, By.ID, "popin_tc_privacy_button_3")
        print("🍪 Cookies acceptés sur Bouygues Telecom.")
        time.sleep(2)  # Attendre avant de continuer
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur Bouygues Telecom : {e}")

# Remplir les champs du formulaire Bouygues Telecom
def remplir_champs_bouygues(driver, numero):
    try:
        # Remplir le champ téléphone
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.clear()
        type_slowly(phone_field, numero)
        print("✅ Numéro de téléphone renseigné sur Bouygues Telecom.")
        
        # Cliquer sur le bouton "Me faire rappeler"
        rappeler_button = driver.find_element(By.XPATH, "//a[@class='is-primary button']")
        attendre_et_cliquer(driver, By.XPATH, "//a[@class='is-primary button']")
        print("✅ Demande de rappel envoyée sur Bouygues Telecom.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur Bouygues Telecom : {e}")

# Processus pour remplir un site Bouygues Telecom
def process_site_bouygues(driver, url, numero):
    driver.get(url)
    time.sleep(6)  # Chargement initial

    # Accepter les cookies et remplir le formulaire spécifique
    accepter_cookies_bouygues(driver)
    remplir_champs_bouygues(driver, numero)

# Fonction principale
def main():
    url_bouygues = "https://www.bouyguestelecom.fr/rappelez-moi"
    numero = input("📞 Entrez le numéro de téléphone à utiliser : ")

    # Initialiser le driver
    driver = init_driver()

    try:
        process_site_bouygues(driver, url_bouygues, numero)
    except Exception as e:
        print(f"⚠️ Erreur sur le site Bouygues : {e}")
    
    # Attendre quelques secondes avant de fermer
    print("⏳ Attente avant de quitter...")
    time.sleep(5)  # Attente avant de fermer le navigateur
    driver.quit()

if __name__ == "__main__":
    main()
