##code de wilfried

import requests
from bs4 import BeautifulSoup

def get_french_writers():
    # L'URL de la page 
    url = "https://fr.wikipedia.org/wiki/Catégorie:Romancier_français_du_XXe_siècle"

    # Envoyer une requête HTTP à l'URL et stocke les réponses
    response = requests.get(url)

    # Analyse du contenu HTML de la réponse avec BeautifulSoup
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Sélectionner tous les liens d'écrivains
    writers = soup.select("div#mw-pages div.mw-category a")
    
    # Créer une liste pour stocker les noms des écrivains
    writer_names = []
    
    # Parcour tous les liens d'écrivains sélectionnés
    for writer in writers:
    
        # Extraction du nom de l'écrivain à partir du texte du lien
        writer_name = writer.text

        # Retire ce qu'il y a entre parenthèses
        i=writer_name.find('(')
        if i!=-1:
            writer_name=writer_name[:i]
    
        # Ajoute du nom de l'écrivain à la liste
        writer_names.append(writer_name)
    
    # Retourne la liste écrivains
    return writer_names

# Appele la fonction get_french_writers() pour obtenir la liste d'écrivains
writers_list = get_french_writers()

#raccourci la liste
writers_list = writers_list[:8]

# Affiche la liste des écrivains
print(writers_list)



##code de Valentine

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
from selenium.common.exceptions import NoSuchElementException


#On ouvre chrome et le site de babelio
options = Options()
options.add_experimental_option("detach", True)
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.babelio.com/")
time.sleep(2)

# Le problème c'est qu'à l'ouverture du site s'affiche une nouvelle frame pour demander notre consentement à l'utilisation de données et il faut clique sur "accepter et fermer" ou "continuer sans accepter" pour accéder au site.
# Le truc c'est que pour ça ils utilisent un iframe, donc il faut changer de frame pour accéder au bouton, et ensuite revenir au frame de départ d'où le code suivant (aussi je laisse un peu de temps
# avant de revenir à la frame de départ sinon il a pas le temps de garder l'info comme quoi j'ai cliqué)
driver.switch_to.frame("sp_message_iframe_751464")
driver.find_element(By.XPATH, "//button[@title='Continuer sans accepter X']").click()
time.sleep(4)
driver.switch_to.default_content()

driver.maximize_window() #j'agrandi la page, il y en a besoin pour plus tard sinon iltrouve pas la searchbox
pyautogui.click(x=150, y=250) #ça s'est juste pour se débarasser de la pub plus vite qu'en attendant

def hasXpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except:
        return(False)
    else:
        return(True)


#voici une fonction qui permet de se rendre sur la bibliographie d'un auteur en prenant en argument son nom, et qui rend le nombre de page de cette bibliographie (ce sera utile poour plus tard, parce que la pagination n'est pas liée à l'url pour ce site)
def go_to_list_of_books(author):
    search_field = driver.find_element(By.ID, 'searchbox') #on va dans la barre de recherche
    search_field.send_keys(f'{author}') #on rentre un auteur
    search_field.send_keys(Keys.RETURN) #on appuie sur entrée
    time.sleep(1)
    pyautogui.click(x=150, y=250) #pour se débarasser à nouveau de la pub
    try:
        driver.find_element(By.LINK_TEXT, author)
    except:
        search_field = driver.find_element(By.ID, 'searchbox')
        search_field.click()
        for i in range(len(author)+10):
            search_field.send_keys(Keys.BACK_SPACE)
        return('0')
    else:
        driver.find_element(By.LINK_TEXT, author).click() #on sélectionne l'auteur dans la liste des résultats de la recherche
    try:
        driver.find_element(By.LINK_TEXT, "Voir plus")
    except:
        return('0')
    else:
        driver.find_element(By.LINK_TEXT, "Voir plus").click() #on clique sur sa bibliographie
    if hasXpath('//*[@id="page_corps"]/div/div[3]/div[2]/div[2]/a[last()-1]'):
        number_of_pages=driver.find_element(By.XPATH, '//*[@id="page_corps"]/div/div[3]/div[2]/div[2]/a[last()-1]').text.strip() #on récupère le nombre de pages
    else:
        number_of_pages='1'
    return(number_of_pages)

#enfin on parcours la liste des auteurs pour aller chercher leur bibliohraphie à chacun, et récupérer les liens vers toutes leurs oeuvres
urls=[]
for auteur in writers_list: #on utilise la liste des auteurs récupérée sur wikipedia
    n=int(go_to_list_of_books(auteur)) #on récupère le nombre de page, et au passage on va sur la bibliographie
    if n ==1 :
        liens=driver.find_elements(By.XPATH,'//div[@class="cr_gauche"]/a') #on récupère toutes les balises avec un lien de livre comme attribut
        for url in liens:
            urls.append(url.get_attribute("href")) #on récupère le lien dans l'attribut et on l'ajoute à la liste de liens
    elif n>0:
        for i in range(n-1): #pour chaque page de la bibliographie
            liens=driver.find_elements(By.XPATH,'//div[@class="cr_gauche"]/a') #on récupère toutes les balises avec un lien de livre comme attribut
            for url in liens:
                urls.append(url.get_attribute("href")) #on récupère le lien dans l'attribut et on l'ajoute à la liste de liens
            driver.find_element(By.XPATH, '//*[@id="page_corps"]/div/div[3]/div[2]/div[2]/a[last()]').click() #on change de page

# print(urls)



## Code de Nivethan

    # Création d'une liste vide pour stocker les informations des livres
livres = []
    # Boucle pour chaque l'URL
for url in urls:
    # Envoi d'une requête GET à l'URL
    response = requests.get(url)

    # Création d'un objet BeautifulSoup à partir du contenu HTML de la réponse
    soup = BeautifulSoup(response.content, 'html.parser')
    

    # Obtenir le nom de l'auteur
    author = soup.find('span', itemprop='name').text.strip()

    # Obtenir la note moyenne
    rating = soup.find('span', {'class': 'texte_t2 rating', 'itemprop': 'ratingValue'}).text.strip()

    # Obtenir le titre
    title_element = soup.find('h1', {'itemprop': 'name'})
    title = title_element.text.strip() if title_element is not None else None
    livre = [title, author, rating]

    # Ajout des informations du livre à la liste livres
    livres.append(livre)

    # Affichage de la liste livres
# print(livres)


## Ajout dans fichier Excel (code de Valentine)
import csv
import pandas as pd


with open("donnees_livres.csv", "w", newline='') as f:
    writer =csv.writer(f, delimiter=',')
    writer.writerow(['Titre', 'Auteur', 'Note/5'])
    writer.writerows(livres)



