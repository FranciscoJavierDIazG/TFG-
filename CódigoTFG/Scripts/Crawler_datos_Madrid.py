from bs4 import BeautifulSoup
import requests
import os
import re

# Cojo el link del dominio para hacer el scraping
link = 'https://datosmacro.expansion.com/paro/espana/municipios/madrid/madrid/valdemanco'
session = requests.Session()

#me conecto
page = session.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(page.content, 'html.parser')

# Cojo todas las entradas cuya etiqueta es value
municipios= [tag['value'] for tag in soup.find_all('option')]

# Creo una lista con cada uno de los dominios web de los que hay los datos que me interesan
URL=[]
for i in municipios:
    if i.startswith('http'):
        URL.append(i)
#print(len(URL))


# Cojo solamente los pertenecientes a cada municipio de la Comunidad de Madrid y cada distrito
for i in URL:
    if i.find('madrid')==-1:
        URL.remove(i)
URL=URL[11:]

# Creo la funcion que recorrerá cada dominio del que obtendré los datos que necesito
def scrp(x):
    for i in x:

        #El link será el relativo a cada municipio/distrito
        link = i
        session = requests.Session()

        #me conecto
        page = session.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')

        # Busco por la etiqueta 'tr' y me quedo el texto comprendido entre las fechas 2016 y 2017
        f = soup.find_all('tr')
        try:
            f2 = str(f)
            f1 = f2.index('2017')
            f3 = f2.index('2016')
            t=f2[f1:f3]

            # Cuento la cantidad de '>' que hay para llegar a los datos que me interesan
            cont=0
            while cont<2:
                t1 = t.index('>')
                t = t[t1+1:]
                cont+=1
            #print(t)

            # Recorro hasta el porcentaje
            pc = t.index('%')
            por = t[:pc+1]
            #print(por)

            # Vuelvo a contar la cantidad de '>' que hay para llegar a los datos que me interesan
            cont=0
            while cont<8:
                t1 = t.index('>')
                t = t[t1+1:]
                cont+=1
            #print(t)

            g = t.index('<')
            hab = t[:g]
            #print(hab)
        
        # Accedo a esta excepción si no hay datos de 2017 y realizo el mismo proceso
        except:
            f2 = str(f)
            f1 = f2.index('2018')
            f3 = f2.index('2016')
            t=f2[f1:f3]
            cont=0
            while cont<2:
                t1 = t.index('>')
                t = t[t1+1:]
                cont+=1

            #print(t)
            pc = t.index('%')
            por = t[:pc+1]
            #print(por)

            cont=0
            while cont<8:
                t1 = t.index('>')
                t = t[t1+1:]
                cont+=1
            #print(t)
            g = t.index('<')
            hab = t[:g]
            #print(hab)

        # Guardo mis datos en un txt con formato de .csv
        registro = open('registro.txt', 'a')
        if ((os.stat('registro.txt').st_size == 0) == True):
            registro.write('Municipio; %Paro; Poblacion \n')


        registro.write(link[70:])
        registro.write(';')
        registro.write(por)
        registro.write(';')
        registro.write(hab)
        registro.write('\n')
        registro.close()

scrp(URL)