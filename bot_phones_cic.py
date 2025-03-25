import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random

# Demander le numéro de téléphone avant d'ouvrir le navigateur
numero_telephone = input("Entrez le numéro de téléphone : ")

# Configuration du navigateur en mode incognito
options = uc.ChromeOptions()
options.add_argument("--incognito")  # Mode incognito

# Démarrer le navigateur
driver = uc.Chrome(options=options)

# Fonction pour remplir le formulaire
def remplir_formulaire():
    # Ouvrir le site
    driver.get("https://www.cic.fr/fr/contacts/etre-rappele-par-telephone.html")  # URL du site CIC

    # Attendre que la page se charge
    time.sleep(2)

    # Accepter les cookies
    try:
        accept_cookies_btn = driver.find_element(By.XPATH, '//a[@class="ei_btn ei_btn_typ_validate"]')
        accept_cookies_btn.click()
        print("Cookies acceptés.")
    except NoSuchElementException:
        print("Bouton des cookies non trouvé.")
    time.sleep(2)  # Attendre un peu avant la prochaine action

    # Cocher la case "La Téléphonie" (élément radio)
    try:
        radio_telephonie = driver.find_element(By.ID, "mainBlock.R_2.R3:DataEntry")
        if not radio_telephonie.is_selected():  # Vérifier si ce n'est pas déjà sélectionné
            radio_telephonie.click()  # Cocher la case
        print("Option 'La Téléphonie' sélectionnée.")
        time.sleep(2)
    except NoSuchElementException:
        print("La case 'La Téléphonie' n'a pas été trouvée.")
        return

    # Remplir le numéro de téléphone
    try:
        champ_telephone = driver.find_element(By.ID, "mainBlock.telephone")
        champ_telephone.send_keys(numero_telephone)
        print(f"Numéro de téléphone {numero_telephone} rempli.")
        time.sleep(2)
    except NoSuchElementException:
        print("Champ du numéro de téléphone non trouvé.")
        return

    # Remplir le nom et prénom avec des valeurs aléatoires
    nom = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
    prenom = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
    email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10)) + "@gmail.com"
    code_postal = random.randint(10000, 99999)

    try:
        champ_nom = driver.find_element(By.ID, "mainBlock.nom")
        champ_nom.send_keys(nom)
        print(f"Nom {nom} rempli.")
    except NoSuchElementException:
        print("Champ du nom non trouvé.")

    try:
        champ_prenom = driver.find_element(By.ID, "mainBlock.prenom")
        champ_prenom.send_keys(prenom)
        print(f"Prénom {prenom} rempli.")
    except NoSuchElementException:
        print("Champ du prénom non trouvé.")

    try:
        champ_email = driver.find_element(By.ID, "mainBlock.email")
        champ_email.send_keys(email)
        print(f"Email {email} rempli.")
    except NoSuchElementException:
        print("Champ de l'email non trouvé.")

    try:
        champ_code_postal = driver.find_element(By.ID, "mainBlock.codepostal")
        champ_code_postal.send_keys(str(code_postal))
        print(f"Code postal {code_postal} rempli.")
    except NoSuchElementException:
        print("Champ du code postal non trouvé.")
    
    # Soumettre le formulaire
    try:
        valider_btn = driver.find_element(By.XPATH, '//input[@type="image"]')
        valider_btn.click()
        print("Formulaire soumis.")
    except NoSuchElementException:
        print("Bouton de validation non trouvé.")
    
    time.sleep(3)

# Appeler la fonction pour remplir le formulaire
remplir_formulaire()

# Fermer le navigateur après 5 secondes
time.sleep(5)
driver.quit()
