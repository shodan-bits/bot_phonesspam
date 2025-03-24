import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


numero_telephone = "0765524990"


url = "https://www.bouyguestelecom.fr/rappelez-moi"

options = uc.ChromeOptions()
options.headless = False  
driver = uc.Chrome(options=options)

def accepter_cookies():
    """Vérifie si une bannière de cookies est affichée et l'accepte."""
    try:
        bouton_cookies = driver.find_element(By.XPATH, '//button[contains(text(), "Accepter") or contains(text(), "Tout accepter")]')
        bouton_cookies.click()
        print("🍪 Cookies acceptés !")
    except NoSuchElementException:
        print("✅ Aucune bannière de cookies détectée.")

def detecter_et_cocher_captcha():
    """Vérifie si un CAPTCHA est affiché et coche la case si possible."""
    try:
        captcha = driver.find_element(By.XPATH, '//iframe[contains(@src, "recaptcha")]')  
        driver.switch_to.frame(captcha)  
        case_captcha = driver.find_element(By.XPATH, '//div[@class="recaptcha-checkbox-border"]')
        case_captcha.click()  
        print("✅ CAPTCHA coché automatiquement !")
        driver.switch_to.default_content()  
        time.sleep(5)  
        return True
    except NoSuchElementException:
        return False  

def remplir_numero():
    """Remplit le champ de numéro de téléphone, peu importe son ID."""
    try:
        champ_telephone = driver.find_element(By.ID, "telNumber")
    except NoSuchElementException:
        try:
            champ_telephone = driver.find_element(By.ID, "phone")
        except NoSuchElementException:
            print("❌ Aucun champ de numéro de téléphone trouvé !")
            return False

    champ_telephone.clear()
    champ_telephone.send_keys(numero_telephone)
    print("📲 Numéro de téléphone saisi :", numero_telephone)
    return True

def cliquer_sur_bouton():
    """Clique sur les boutons 'Contactez-moi' et 'Me faire rappeler'."""
    try:
        bouton_contact = driver.find_element(By.ID, "submitCallr")
        bouton_contact.click()
        time.sleep(2)
        bouton_contact.click()  
        print("📞 Bouton 'Contactez-moi' cliqué deux fois !")
        return True
    except NoSuchElementException:
        print("❌ Bouton 'Contactez-moi' non trouvé, essai sur 'Me faire rappeler'...")
    
    try:
        bouton_rappel = driver.find_element(By.XPATH, '//a[contains(@class, "is-primary button") and contains(text(), "Me faire rappeler")]')
        bouton_rappel.click()
        print("📞 Bouton 'Me faire rappeler' cliqué !")
        return True
    except NoSuchElementException:
        print("❌ Aucun bouton valide trouvé !")
        return False

try:
    while True:
       
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        time.sleep(3)  

        accepter_cookies()  

        if detecter_et_cocher_captcha():
            print("⏳ Attente validation du CAPTCHA...")
            time.sleep(5)  

        if remplir_numero():
            if cliquer_sur_bouton():
                print("✅ Demande envoyée avec succès !")
        
        print("⏳ Attente de 60 secondes avant la prochaine tentative...")

        time.sleep(5)  
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
        
        time.sleep(55)  

except Exception as e:
    print("❌ Erreur :", e)

finally:
    try:
        if driver:
            driver.quit()
    except Exception as e:
        print("⚠️ Erreur lors de la fermeture du navigateur :", e)
