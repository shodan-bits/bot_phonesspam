import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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

# Attendre que l'élément soit cliquable avant d'agir
def attendre_et_cliquer(driver, by, valeur, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, valeur)))
    element.click()
    print(f"✅ Élément cliqué : {valeur}")

# Accepter les cookies sur Indépendance Royale
def cookie_independance_royal(driver):
    try:
        attendre_et_cliquer(driver, By.ID, "didomi-notice-agree-button")
        print("Cookies acceptés")
        time.sleep(2)
    except Exception as e:
        print(f"Erreur d'acceptation des cookies: {e}")

def remplir_champs_independance(driver, numero, nom, prenom, code_postal):
    try:
        # Sélection du champ "téléphone"
        phone_field = driver.find_element(By.ID, "edit-telephone")
        phone_field.clear()
        type_slowly(phone_field, numero)

        # Sélection du champ "nom"
        name_field = driver.find_element(By.ID, "edit-nom")
        name_field.clear()
        type_slowly(name_field, nom)

        # Sélection du champ "prénom"
        prenom_field = driver.find_element(By.ID, "edit-prenom")
        prenom_field.clear()
        type_slowly(prenom_field, prenom)

        # Sélection du champ "code postal"
        code_postal_field = driver.find_element(By.ID, "edit-code-postal")
        code_postal_field.clear()
        type_slowly(code_postal_field, code_postal)

        # Sélection de la valeur "modif_rdv" dans la liste déroulante
        select_element = Select(driver.find_element(By.ID, "edit-ma-demande-concerne"))
        select_element.select_by_value("modif_rdv")
        print("🔄 Sélection de la valeur : modif_rdv")

        driver.execute_script("window.scrollBy(0, 300);")  # Défiler de 300px vers le bas
        time.sleep(2)

       # Sélection de case 1 
        checkbox = driver.find_element(By.ID, "edit-opt-in-offres") 
        if not checkbox.is_selected():
             checkbox.click()  
       # Sélection de case 2
        checkbox2 = driver.find_element(By.ID, "edit-opt-in-partenaires") 
        if not checkbox2.is_selected():
             checkbox2.click()
         
       #Sélection bouton envoyer
        btn_envoi = driver.find_element(By.CSS_SELECTOR, ".webform-button--submit.button.button--primary.js-form-submit.form-submit.relative")
        btn_envoi.click()

 
        print("✅ Formulaire Indépendance Royale rempli avec succès.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur Indépendance Royale : {e}")

        print("✅ Formulaire Indépendance Royale rempli avec succès.")
    except Exception as e:
        print(f"❌ Erreur en remplissant le formulaire sur Indépendance Royale : {e}")




# Processus pour remplir un site
def process_site(driver, url, numero, nom, prenom, code_postal):
    driver.get(url)
    time.sleep(6)  # Chargement initial
    cookie_independance_royal(driver)
    remplir_champs_independance(driver, numero, nom, prenom, code_postal)

# Fonction principale
def main():
    url_indepandance = "https://www.independanceroyale.com/je-souhaite-etre-contacte-par-telephone"
    numero = input("Entrez le numéro de téléphone cible : ")
    nom = "Jean"
    prenom = "Dupont"
    code_postal = "75000"
    
    driver = init_driver()
    process_site(driver, url_indepandance, numero, nom, prenom, code_postal)
    
    print("Attente avant de quitter...")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()