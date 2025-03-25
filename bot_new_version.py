import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

# Faire défiler la page jusqu'à un élément donné
def scroll_jusqu_a_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)  # Pause pour éviter tout problème de chargement

# Cocher la case "LA TELEPHONIE"
def cocher_telephonie(driver):
    try:
        label_telephonie = driver.find_element(By.ID, "mainBlock.R_2.R3:lbl")
        scroll_jusqu_a_element(driver, label_telephonie)
        label_telephonie.click()  # Cliquer sur le label pour cocher l'option
        print("✅ Option 'LA TELEPHONIE' cochée")
    except NoSuchElementException:
        print("❌ Option 'LA TELEPHONIE' non trouvée")

# Sélectionner l'heure la plus proche
def choisir_heure_proche(driver):
    try:
        heure_actuelle = datetime.now().hour
        select_heure = driver.find_element(By.ID, "mainBlock.dpdownHeure:DataEntry")
        scroll_jusqu_a_element(driver, select_heure)
        
        options = select_heure.find_elements(By.TAG_NAME, "option")
        for option in options:
            heure_range = option.get_attribute("value").split('|')
            if int(heure_range[0]) >= heure_actuelle:
                option.click()
                print(f"⏰ Heure de rappel sélectionnée : {option.text}")
                return
        print("⚠️ Aucune heure valide trouvée.")
    except NoSuchElementException:
        print("❌ Impossible de sélectionner l'heure de rappel.")

# Remplir les champs du formulaire avec un scroll + écriture lettre par lettre
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
            scroll_jusqu_a_element(driver, input_field)  # Scroll avant de taper
            
            input_field.clear()
            
            # Remplissage du champ téléphone avec délai (imite l'écriture humaine)
            if champ == "telephone":
                for char in valeurs[champ]:
                    input_field.send_keys(char)
                    time.sleep(0.1)
                print(f"✅ Champ {champ} rempli : {valeurs[champ]}")
            else:
                input_field.send_keys(valeurs[champ])
                print(f"✅ Champ {champ} rempli : {valeurs[champ]}")
        except NoSuchElementException:
            print(f"⚠️ Champ {champ} non trouvé")

# Sélectionner si le client est existant
def selectionner_client(driver):
    try:
        client_non = driver.find_element(By.ID, "mainBlock.clientnon:DataEntry")
        scroll_jusqu_a_element(driver, client_non)
        client_non.click()
        print("✅ Sélectionné comme nouveau client")
    except NoSuchElementException:
        print("❌ Option client non trouvée")

# Cliquer sur le bouton d'envoi
def cliquer_bouton(driver):
    try:
        bouton = driver.find_element(By.XPATH, '//input[@type="image" and contains(@alt, "Valider")]')
        scroll_jusqu_a_element(driver, bouton)
        bouton.click()
        time.sleep(8)  # Attente pour éviter un changement trop rapide de page
        print("📞 Demande envoyée avec succès !")
    except NoSuchElementException:
        print("❌ Bouton non trouvé !")

# Processus principal pour chaque site
def process_site(driver, url, numero, nom, prenom, email, code_postal):
    driver.get(url)
    time.sleep(6)  # Temps de chargement avant toute action
    accepter_cookies(driver)
    cocher_telephonie(driver)
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
