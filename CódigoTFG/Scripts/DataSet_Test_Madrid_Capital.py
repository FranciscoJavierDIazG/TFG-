import pandas as pd
import random
import os
import re
import uuid

#   Accedo a los datos de las calles del dataset de CP de los distritos
cp = pd.read_excel('C:/Users/Fran/Desktop/Distritos_CP.xlsx')
dic_DIST_CP = {}
for i in range(len(cp)-1):
    dic_DIST_CP[cp['Distrito'][i]]=[cp['CP'][i],cp['CP2'][i],cp['CP3'][i],cp['CP4'][i]]

#   Accedo a los datos de las calles del dataset CALLE_CP.xlsx
calle_cp = pd.read_excel('C:/Users/Fran/Desktop/CALLE_CP.xlsx')


#   Abro el achivo donde tengo los datos de los municipios de Madrid
df = pd.read_excel('C:/Users/Fran/Desktop/MADRID_CAPITAL.xlsx')

n=0
cont=0
KL = []
#   Creo un bucle que por cada vuelta genera un número aleatorio entre 0 y 1
#   El valor que devuelve lo comparo con la frecuencia acumulada de viviendas vacías
#   Cojo el nombre del municipio con el que coincide o es menor que él
while cont<500:
    data = open('C:/Users/Fran/Desktop/Test.txt', 'a')
    if ((os.stat('C:/Users/Fran/Desktop/Test.txt').st_size == 0) == True):
        data.write(
            'ID;Calle;Localización;Habitantes;Paro_registrado;N_detenciones;Detenciones/Habitantes;Viviendas vacías;Renta media por persona;N_extranjeros;Construcción viviendas pública;Propietario;Alarma\n')

    rnd = random.uniform(0,1)
    chosen = ''
    for i in range(len(df['Frec_Ac_viv_Vacias'])-1):
        if rnd<=df['Frec_Ac_viv_Vacias'][i]:
            h = df['Distrito'][i]

            #   Le asigno una calle
            for k in dic_DIST_CP:
                if k == df['Distrito'][i]:
                    c = random.randint(0, 3)
                    postal = dic_DIST_CP[k][c]
                    if postal!=0:
                        aux =[]
                        for j in range(len(calle_cp)-1):
                            if postal == calle_cp['CP'][j]:
                                aux.append(calle_cp['Calle'][j])
                        street = 'C/ '
                        calle = random.randint(0, len(aux)-1)
                        street+=aux[calle]
                    else:
                        postal = dic_DIST_CP[k][0]
                        aux =[]
                        for j in range(len(calle_cp)-1):
                            if postal == calle_cp['CP'][j]:
                                aux.append(calle_cp['Calle'][j])
                        street = 'C/ '
                        calle = random.randint(0, len(aux)-1)
                        xd = aux[calle]
                        street+=xd

            #   En este caso a cada vivienda le voy a asignar un ID único
            a = uuid.uuid4()
            chosen+=str(a)+';'+street+';'+df['Distrito'][i]+';'+str(df['Habitantes'][i]).replace('.',',')+';'+str(df['Paro_registrado'][i]).replace('.',',')+';'+str(df['N_detenciones'][i]).replace('.',',')+';'+str(df['Detenciones/Habitantes'][i]).replace('.',',')+';'+str(df['Viviendas vacías'][i]).replace('.',',')+';'+str(df['Renta media por persona'][i]).replace('.',',')+';'+str(df['N_extranjeros'][i]).replace('.',',')+';'+str(df['Construcción viviendas pública'][i]).replace('.',',')
            
            #   Generar la alarma
            rnd4 = random.uniform(0,1)
            alarma = ''
            if rnd4<= 0.65:
                alarma = '0'
            else:
                alarma = '1'
            
            #   Generar el propietario
            rnd3 = random.uniform(0,1)
            if rnd3<=0.4:
                propietario = 'Banco'
            elif rnd3>0.4 and rnd3<=0.8:
                propietario = 'Ayuntamiento'
            else:
                propietario = 'Particular'

            #   Monto el dato
            chosen+=';'+propietario+';'+alarma

            data.write(chosen)
            data.write('\n')
            break
    cont+=1