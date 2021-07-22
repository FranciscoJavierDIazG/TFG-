from bs4 import BeautifulSoup
import requests
import os
import re
# from django.utils.encoding import smart_str, smart_text

# Abro el txt que contiene todos los links a los que voy a realizar el web scraping
f = open ('C:/Users/Fran/Desktop/tfg/links.txt','r')
tx = f.readlines()
f.close()

# Recorro el archivo, cogiendo cada link y realizando el scraping de cada uno de ellos
cont = 0
while cont<len(tx):

    # Creo una variable del tipo String, basada en el contador, la cual utilizaré para poner nombre al txt con los datos resultantes
    cont_str = str(cont+1)

    # Cojo el link
    link = tx[cont]
    # Le borro el salto de línea del final para evitar errores
    link = link.rstrip('\n')
    session = requests.Session()
    
    # Me conecto
    page = session.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')

    # Realizo un scraping especial en el primer link porque daba errores
    if cont==0:
        html1 = soup.find('div', class_= 'ue-l-article__header-content')
        html2 = soup.find('div', class_= 'ue-l-article__body ue-c-article__body')
        
        file = open('C:/Users/Fran/Desktop/tfg/Textos_bruto/texto'+cont_str+'.txt', "w")
        file.write(html1.text+html2.text)
        file.close()
        cont +=1
    
    # Del resto del links cojo todo el 'body' para posteriormente procesarlo
    else:   
        html = soup.find('body')

        file = open('C:/Users/Fran/Desktop/tfg/Textos_bruto/texto'+cont_str+'.txt', "w",encoding='utf-8')
        file.write(html.text)
        file.close()
        cont +=1
        