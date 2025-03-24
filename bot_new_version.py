import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Initialisation du driver en mode navigation privée
def init_driver():
    options = uc.ChromeOptions()
    options.headless = False  # Mettre True pour exécuter en arrière-plan
    options.add_argument("--incognito")  # Mode navigation privée
    return uc.Chrome(options=options)

# Accepter les cookies si une bannière est présente
def accepter_cookies(driver):
    try:
        bouton_cookies = driver.find_element(By.XPATH, '//button[contains(text(), "Accepter") or contains(text(), "Tout accepter")]')
        bouton_cookies.click()
        print("🍪 Cookies acceptés !")
    except NoSuchElementException:
        print("✅ Aucune bannière de cookies détectée.")

# Détection et gestion du CAPTCHA simple (case à cocher)
def detecter_captcha_simple(driver):
    try:
        captcha_checkbox = driver.find_element(By.XPATH, '//iframe[contains(@title, "reCAPTCHA") or contains(@src, "recaptcha")]')
        driver.switch_to.frame(captcha_checkbox)
        checkbox = driver.find_element(By.XPATH, '//div[@class="recaptcha-checkbox-border"]')
        checkbox.click()
        print("🔍 CAPTCHA coché avec succès !")
        driver.switch_to.default_content()
        time.sleep(5)  # Attendre la validation du CAPTCHA
        return True
    except NoSuchElementException:
        return False

# Remplir les champs du formulaire
def remplir_champs(driver, numero, nom, prenom, email, code_postal):
    champs = {
        "telephone": ["edit-telephone", "telNumber", "phone"],
        "nom": ["edit-nom", "name", "full_name"],
        "prenom": ["edit-prenom"],
        "email": ["email", "email_address"],
        "code_postal": ["edit-code-postal", "zip", "postal_code"]
    }
    
    valeurs = {"telephone": numero, "nom": nom, "prenom": prenom, "email": email, "code_postal": code_postal}
    
    for champ, ids in champs.items():
        for id in ids:
            try:
                input_field = driver.find_element(By.ID, id)
                input_field.clear()
                input_field.send_keys(valeurs[champ])
                print(f"✅ Champ {champ} rempli : {valeurs[champ]}")
                break
            except NoSuchElementException:
                continue

# Cocher les cases nécessaires
def cocher_cases(driver):
    try:
        case_offres = driver.find_element(By.ID, "edit-opt-in-offres")
        case_offres.click()
        print("✅ Case 'Offres' cochée")
    except NoSuchElementException:
        pass
    
    try:
        case_partenaires = driver.find_element(By.ID, "edit-opt-in-partenaires")
        case_partenaires.click()
        print("✅ Case 'Partenaires' cochée")
    except NoSuchElementException:
        pass

# Cliquer sur le bouton d'envoi
def cliquer_bouton(driver):
    try:
        bouton = driver.find_element(By.XPATH, '//button[contains(text(), "Envoyer") or contains(text(), "Me faire rappeler") or contains(text(), "Contactez moi")]')
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
    
    if detecter_captcha_simple(driver):
        print("⏳ Attente validation du CAPTCHA...")
        time.sleep(5)
    
    remplir_champs(driver, numero, nom, prenom, email, code_postal)
    cocher_cases(driver)
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
