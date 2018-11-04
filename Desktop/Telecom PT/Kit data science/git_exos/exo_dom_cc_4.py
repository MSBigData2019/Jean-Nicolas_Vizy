# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 15:31:26 2018

@author: JN
"""

#version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.


import pandas as pd
import requests
from bs4 import BeautifulSoup

#récupérons déjà la liste des liens vers des annonces en Idf:

# paramètres généraux des requêtes et regex utilisée pour extraire les liens vers les annonces
url = "https://www.leboncoin.fr/recherche/?category=2&regions=12&model=Zoe&brand=Renault"
region = "ile_de_france"
request_headers = {
       "Accept-Language": "en-US,en;q=0.5",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
       "Referer": "http://thewebsite.com",
       "Connection": "keep-alive"
   }
regex = '(?<=href=)\"\/(.+?)(?=\s)'


#%%
#le nombre de résultats affichés par page semble limité à 35, on fait donc une boucle qui va récupérer les liens à partir de chaque page de résultats
# initialisation de la boucle
r = requests.get(url, headers = request_headers)
soup = BeautifulSoup(r.content, "html.parser")
annonces = list(soup.find_all(class_="_3DFQ-"))
liste_annonces = [str(element) for element in annonces]
df_annonces = pd.DataFrame(liste_annonces)
df_annonces["lien"] = df_annonces[0].str.extract(regex)
i = 1

#corps de la boucle
while r.status_code == 200:
    i += 1
    page = "https://www.leboncoin.fr/recherche/?category=2&regions=12&model=Zoe&brand=Renault&page=" + str(i)
    r = requests.get(page, headers = request_headers)
    if r.status_code != 200:
        break
    soup = BeautifulSoup(r.content, "html.parser")
    annonces = list(soup.find_all(class_="_3DFQ-"))
    liste_annonces = [str(element) for element in annonces]
    if len(liste_annonces) == 0:
        break
    df_ad = pd.DataFrame(liste_annonces)
    df_ad["lien"] = df_ad[0].str.extract(regex)
    df_annonces = pd.concat([df_annonces, df_ad], axis = 0)

#%%   
#une fois la liste des liens obtenue, extrayons-en les informations demandées

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(options=opts)
browser.get('https://duckduckgo.com')



url2 = "https://www.leboncoin.fr/voitures/1492396226.htm/"
r2 = requests.get(url2, headers = request_headers)
s = BeautifulSoup(r.content, "html.parser")
ga = s.find_all(class_="_3Jxf3")
bu=[k for k in ga]
annee = int(bu[2].text)
km = int(bu[3][:-3])
zo = s.find(class_="_3Jxf3")