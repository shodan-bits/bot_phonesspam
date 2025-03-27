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

def cookie_independance_royal(driver):
    try:
        accept_cookies = driver.find_element(By.CLASS_NAME,"didomi-notice-agree-button")
        attendre_et_cliquer(driver, By.CLASS_NAME,"didomi-notice-agree-button")
        print("Cookies acceptés")
        time.sleep(2)
    except Exception as e:
        print(f"Erreur d'acceptation des cookies: {e}")    