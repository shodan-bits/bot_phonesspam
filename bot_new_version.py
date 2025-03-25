import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime

# Initialisation du driver en mode navigation privée
def init_driver():
    options = uc.ChromeOptions()
    options.headless = False  # False pour voir l'exécution, True pour arrière-plan
    options.add_argument("--incognito")  # Mode navigation privée
    return uc.Chrome(options=options)

# Attendre la présence d'un élément avant de l'utiliser
def attendre_element(driver, by, valeur, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, valeur)))

# Accepter les cookies
def accepter_cookies(driver):
    try:
        bouton_cookies = attendre_element(driver, By.XPATH, '//a[contains(@class, "ei_btn_typ_validate") and @data-type="accept"]')
        bouton_cookies.click()
        print("🍪 Cookies acceptés !")
    except:
        print("✅ Aucune bannière de cookies détectée.")

# Faire défiler jusqu'à un élément
def scroll_jusqu_a_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

# Imiter l'écriture humaine lettre par lettre
def taper_texte(element, texte):
    for char in texte:
        element.send_keys(char)
        time.sleep(0.1)  # Pause entre chaque lettre

# Sélectionner une option (ex: téléphonie)
def cocher_telephonie(driver):
    try:
        label_telephonie = attendre_element(driver, By.ID, "mainBlock.R_2.R3:lbl")
        scroll_jusqu_a_element(driver, label_telephonie)
        label_telephonie.click()
        print("✅ Option 'LA TELEPHONIE' cochée")
    except:
        print("❌ Option 'LA TELEPHONIE' non trouvée")

# Sélectionner l'heure de rappel
def choisir_heure_proche(driver):
    try:
        heure_actuelle = datetime.now().hour
        select_heure = attendre_element(driver, By.ID, "mainBlock.dpdownHeure:DataEntry")
        scroll_jusqu_a_element(driver, select_heure)
        options = select_heure.find_elements(By.TAG_NAME, "option")
        for option in options:
            heure_range = option.get_attribute("value").split('|')
            if int(heure_range[0]) >= heure_actuelle:
                option.click()
                print(f"⏰ Heure sélectionnée : {option.text}")
                return
    except:
        print("❌ Impossible de sélectionner l'heure")

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
        for _ in range(3):  # Essayer 3 fois si erreur stale element
            try:
                input_field = attendre_element(driver, By.ID, id)
                scroll_jusqu_a_element(driver, input_field)
                input_field.clear()
                
                if champ == "telephone":
                    taper_texte(input_field, valeurs[champ])
                else:
                    input_field.send_keys(valeurs[champ])
                
                print(f"✅ Champ {champ} rempli : {valeurs[champ]}")
                break  # Sortir de la boucle si succès
            except StaleElementReferenceException:
                print(f"🔄 Retenter remplissage du champ {champ}...")

# Sélectionner si le client est existant
def selectionner_client(driver):
    try:
        client_non = attendre_element(driver, By.ID, "mainBlock.clientnon:DataEntry")
        scroll_jusqu_a_element(driver, client_non)
        client_non.click()
        print("✅ Sélectionné comme nouveau client")
    except:
        print("❌ Option client non trouvée")

# Cliquer sur le bouton d'envoi
def cliquer_bouton(driver):
    try:
        bouton = attendre_element(driver, By.XPATH, '//input[@type="image" and contains(@alt, "Valider")]')
        scroll_jusqu_a_element(driver, bouton)
        bouton.click()
        time.sleep(8)
        print("📞 Demande envoyée avec succès !")
    except:
        print("❌ Bouton non trouvé !")

# Processus principal pour chaque site
def process_site(driver, url, numero, nom, prenom, email, code_postal):
    driver.get(url)
    time.sleep(6)  # Chargement initial
    accepter_cookies(driver)
    cocher_telephonie(driver)
    remplir_champs(driver, numero, nom, prenom, email, code_postal)
    choisir_heure_proche(driver)
    selectionner_client(driver)
    cliquer_bouton(driver)

# Fonction principale
def main():
    sites = [
        #"https://www.garagebernard.fr/fr/rappel-gratuit#",
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
