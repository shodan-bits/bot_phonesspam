import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def type_slowly(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)


def init_driver():
    options = uc.ChromeOptions()
    options.headless = False  
    options.add_argument("--incognito")  
    return uc.Chrome(options=options)


def attendre_element(driver, by, valeur, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, valeur)))


def attendre_et_cliquer(driver, by, valeur, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, valeur)))
    element.click()
    print(f"✅ Élément cliqué : {valeur}")


def accepter_cookies_bouygues(driver):
    try:
        accept_cookies = driver.find_element(By.ID, "popin_tc_privacy_button_3")
        attendre_et_cliquer(driver, By.ID, "popin_tc_privacy_button_3")
        print("🍪 Cookies acceptés sur Bouygues Telecom.")
        time.sleep(2)  
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur Bouygues Telecom : {e}")


def remplir_champs_bouygues(driver, numero):
    try:
       
        phone_field = driver.find_element(By.ID, "input is-default")
        phone_field.clear()
        type_slowly(phone_field, numero)
        print("✅ Numéro de téléphone renseigné sur Bouygues Telecom.")
        
        
        rappeler_button = driver.find_element(By.XPATH, "//a[@class='button is-conversion']")
        attendre_et_cliquer(driver, By.XPATH, "//a[@class=button is-conversion']")
        print("✅ Demande de rappel envoyée sur Bouygues Telecom.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur Bouygues Telecom : {e}")


def process_site_bouygues(driver, url, numero):
    driver.get(url)
    time.sleep(6)  

    
    accepter_cookies_bouygues(driver)
    remplir_champs_bouygues(driver, numero)


def main():
    url_bouygues = "https://www.bouyguestelecom.fr/rappelez-moi"
    numero = input("📞 Entrez le numéro de téléphone à utiliser : ")

    
    driver = init_driver()

    try:
        process_site_bouygues(driver, url_bouygues, numero)
    except Exception as e:
        print(f"⚠️ Erreur sur le site Bouygues : {e}")
    
    
    print("⏳ Attente avant de quitter...")
    time.sleep(5)  
    driver.quit()

if __name__ == "__main__":
    main()
