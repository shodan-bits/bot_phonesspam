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

# Accepter les cookies sur chaque site
def accepter_cookies_credit_mutuel(driver):
    try:
        # Accepter les cookies de Crédit Mutuel en utilisant la balise fournie
        accept_cookies = driver.find_element(By.CLASS_NAME, "ei_btn.ei_btn_typ_validate")
        attendre_et_cliquer(driver, By.CLASS_NAME, "ei_btn.ei_btn_typ_validate")
        print("🍪 Cookies acceptés sur Crédit Mutuel.")
        time.sleep(2)  # Attendre avant de continuer
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur Crédit Mutuel : {e}")

def accepter_cookies_bouygues(driver):
    try:
        accept_cookies = driver.find_element(By.ID, "popin_tc_privacy_button_3")
        accept_cookies.click()
        scroll_to_bottom(driver)
        print("🍪 Cookies acceptés sur Bouygues Telecom.")
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur Bouygues Telecom : {e}")

def accepter_cookies_cic(driver):
    try:
        accept_cookies = driver.find_element(By.CLASS_NAME, "ei_btn ei_btn_typ_validate")
        accept_cookies.click()
        scroll_to_bottom(driver)
        print("🍪 Cookies acceptés sur CIC.")
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur CIC : {e}")

def accepter_cookies_independance(driver):
    try:
        accept_cookies = driver.find_element(By.ID, "didomi-notice-agree-button")
        accept_cookies.click()
        scroll_to_bottom(driver)
        print("🍪 Cookies acceptés sur Indépendance Royale.")
    except Exception as e:
        print(f"❌ Erreur en acceptant les cookies sur Indépendance Royale : {e}")

# Remplir les champs du formulaire pour chaque site
def remplir_champs_credit_mutuel(driver, numero):
    try:
        # Attente explicite pour s'assurer que l'élément est visible avant d'interagir
        phone_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "phone")))
        phone_field.clear()
        type_slowly(phone_field, numero)
        print("✅ Numéro de téléphone renseigné sur Crédit Mutuel.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le champ sur Crédit Mutuel : {e}")

def remplir_champs_bouygues(driver, numero):
    try:
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.clear()
        type_slowly(phone_field, numero)
        print("✅ Numéro de téléphone renseigné sur Bouygues Telecom.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le champ sur Bouygues Telecom : {e}")

def remplir_champs_cic(driver, nom, prenom, email, code_postal):
    try:
        name_field = driver.find_element(By.ID, "mainBlock.nom")
        name_field.clear()
        type_slowly(name_field, nom)

        prenom_field = driver.find_element(By.ID, "mainBlock.prenom")
        prenom_field.clear()
        type_slowly(prenom_field, prenom)

        email_field = driver.find_element(By.ID, "mainBlock.email")
        email_field.clear()
        type_slowly(email_field, email)

        code_postal_field = driver.find_element(By.ID, "mainBlock.codepostal")
        code_postal_field.clear()
        type_slowly(code_postal_field, code_postal)

        print("✅ Formulaire CIC rempli avec succès.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur CIC : {e}")

def remplir_champs_independance(driver, numero, nom, prenom, code_postal):
    try:
        phone_field = driver.find_element(By.ID, "edit-telephone")
        phone_field.clear()
        type_slowly(phone_field, numero)

        name_field = driver.find_element(By.ID, "edit-nom")
        name_field.clear()
        type_slowly(name_field, nom)

        prenom_field = driver.find_element(By.ID, "edit-prenom")
        prenom_field.clear()
        type_slowly(prenom_field, prenom)

        code_postal_field = driver.find_element(By.ID, "edit-code-postal")
        code_postal_field.clear()
        type_slowly(code_postal_field, code_postal)

        print("✅ Formulaire Indépendance Royale rempli avec succès.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur Indépendance Royale : {e}")

# Processus pour remplir un site
def process_site(driver, url, numero, nom, prenom, email, code_postal):
    driver.get(url)
    time.sleep(6)  # Chargement initial

    # Selon le site, on accepte les cookies et on remplit les champs spécifiques
    if "creditmutuel" in url:
        accepter_cookies_credit_mutuel(driver)
        remplir_champs_credit_mutuel(driver, numero)
    elif "bouygues" in url:
        accepter_cookies_bouygues(driver)
        remplir_champs_bouygues(driver, numero)
    elif "cic" in url:
        accepter_cookies_cic(driver)
        remplir_champs_cic(driver, nom, prenom, email, code_postal)
    elif "independance" in url:
        accepter_cookies_independance(driver)
        remplir_champs_independance(driver, numero, nom, prenom, code_postal)

# Fonction principale
def main():
    sites = [
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
            
            # Attendre quelques secondes avant de passer au prochain site
            print("⏳ Attente de 10 secondes avant de changer de site...")
            time.sleep(10)  # Attendre avant de changer de site
        
        driver.quit()
        print("🔄 Redémarrage dans 45 secondes...")
        time.sleep(45)

if __name__ == "__main__":
    main()
