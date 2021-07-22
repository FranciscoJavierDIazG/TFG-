from bs4 import BeautifulSoup
import requests
import os
import re

#   Función para obtener la calle
def street(x, L):
    for i in x:
        t = str(i)
        t = t[:-9]
        a = t.index('postales')
        t = t[a+10:]
        L.append(t)
    return(L)

#   Función para obtener el CP de la calle
def code(x, L):
    for i in x:
        t = str(i)
        t = t[:-5]
        a = t.index('code')
        t = t[a+6:]
        L.append(t)
    return(L)

n_page = 1
#   Lista donde almacenaré la calle y el CP
C = []
CP = []

#   315 vueltas porque son el número de páginas de la web
while n_page<315:

    #   Scraping a la siguiente dirección, que almacena todas las calles de Madrid con su CP
    link = 'https://www.codigo-postal.info/madrid/madrid/'+str(n_page)
    session = requests.Session()

    page = session.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')

    calle = soup.find_all('td', class_ = 'street')
    cp = soup.find_all('td', class_ = 'postal_code')

    street(calle, C)
    code(cp, CP)

    n_page+=1

dic = {}

#   Monto los datos
cont = 0
while cont<len(C):
    dic[C[cont]]=CP[cont]
    cont+=1

#   Lo guardo
file = open("C:/Users/Fran/Desktop/tfg/Calle_CP_dic_FINAL.txt", "w")
for i in dic:
    file.write(i+':'+dic[i]+'\n')
file.close()
