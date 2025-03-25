import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytesseract
from PIL import Image
import io
import base64
from datetime import datetime

# Initialisation du driver en mode navigation privée
def init_driver():
    options = uc.ChromeOptions()
    options.headless = False  # Mettre True pour exécuter en arrière-plan
    options.add_argument("--incognito")  # Mode navigation privée
    return uc.Chrome(options=options)

# Accepter les cookies si une bannière est présente
def accepter_cookies(driver):
    try:
        bouton_cookies = driver.find_element(By.XPATH, '//a[contains(@class, "ei_btn_typ_validate") and @data-type="accept"]')
        bouton_cookies.click()
        print("🍪 Cookies acceptés !")
    except NoSuchElementException:
        print("✅ Aucune bannière de cookies détectée.")

# Détection et tentative de résolution de CAPTCHA basé sur des images
def detecter_captcha(driver):
    try:
        captcha_frame = driver.find_element(By.XPATH, '//iframe[contains(@src, "recaptcha")]')
        driver.switch_to.frame(captcha_frame)
        captcha_image = driver.find_element(By.XPATH, '//img')
        src = captcha_image.get_attribute("src")
        
        # Décoder l'image
        image_data = base64.b64decode(src.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        print(f"🔍 CAPTCHA détecté : {text}")
        
        driver.switch_to.default_content()
        time.sleep(5)
        return True
    except NoSuchElementException:
        return False

# Sélectionner l'heure de rappel la plus proche
def choisir_heure_proche(driver):
    try:
        heure_actuelle = datetime.now().hour
        options = driver.find_elements(By.XPATH, '//select[@id="mainBlock.dpdownHeure:DataEntry"]/option')
        for option in options:
            heure_range = option.get_attribute("value").split('|')
            if int(heure_range[0]) >= heure_actuelle:
                option.click()
                print(f"⏰ Heure de rappel sélectionnée : {option.text}")
                return
    except NoSuchElementException:
        print("❌ Impossible de sélectionner l'heure de rappel.")

# Remplir les champs du formulaire
def remplir_champs(driver, numero, nom, prenom, email, code_postal):
    champs = {
        "telephone": "mainBlock.telephone",
        "nom": "mainBlock.nom",
        "prenom": "mainBlock.prenom",
        "email": "mainBlock.email",
        "code_postal": "mainBlock.codepostal"
    }
    
    valeurs = {"telephone": numero, "nom": nom, "prenom": prenom, "email": email, "code_postal": code_postal}
    
    for champ, id in champs.items():
        try:
            input_field = driver.find_element(By.ID, id)
            input_field.clear()
            input_field.send_keys(valeurs[champ])
            print(f"✅ Champ {champ} rempli : {valeurs[champ]}")
        except NoSuchElementException:
            print(f"⚠️ Champ {champ} non trouvé")

# Sélectionner si le client est existant
def selectionner_client(driver):
    try:
        client_non = driver.find_element(By.ID, "mainBlock.clientnon:DataEntry")
        client_non.click()
        print("✅ Sélectionné comme nouveau client")
    except NoSuchElementException:
        print("❌ Option client non trouvée")

# Cliquer sur le bouton d'envoi
def cliquer_bouton(driver):
    try:
        bouton = driver.find_element(By.XPATH, '//input[@type="image" and contains(@alt, "Valider")]')
        bouton.click()
        time.sleep(2)
        print("📞 Demande envoyée avec succès !")
    except NoSuchElementException:
        print("❌ Bouton non trouvé !")

# Processus principal pour chaque site
def process_site(driver, url, numero, nom, prenom, email, code_postal):
    driver.get(url)
    time.sleep(3)
    accepter_cookies(driver)
    
    if detecter_captcha(driver):
        print("⏳ Attente validation du CAPTCHA...")
        time.sleep(5)
    
    remplir_champs(driver, numero, nom, prenom, email, code_postal)
    choisir_heure_proche(driver)
    selectionner_client(driver)
    cliquer_bouton(driver)

# Fonction principale
def main():
    sites = [
        "https://www.garagebernard.fr/fr/rappel-gratuit#",
        "https://www.creditmutuel.fr/fr/contacts/etre-rappele-par-telephone.html",
        "https://www.bouyguestelecom.fr/rappelez-moi",
        "https://www.cic.fr/fr/contacts/etre-rappele-par-telephone.html",
        "https://www.independanceroyale.com/je-souhaite-etre-contacte-par-telephone"
    ]
    
    numero = input("📞 Entrez le numéro de téléphone à utiliser : ")
    nom = "Jean"
    prenom = "Dupont"
    email = "jean.dupont@example.com"
    code_postal = "75000"
    
    while True:
        driver = init_driver()
        for site in sites:
            try:
                process_site(driver, site, numero, nom, prenom, email, code_postal)
            except Exception as e:
                print(f"⚠️ Erreur sur {site} : {e}")
        
        driver.quit()
        print("🔄 Redémarrage dans 45 secondes...")
        time.sleep(45)

if __name__ == "__main__":
    main()
