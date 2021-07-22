import pandas as pd
import random
import os
import re

#   Accedo a los datos de las calles del dataset de CP de los distritos
cp = pd.read_excel('C:/Users/Fran/Desktop/tfg/DATASETS/Distritos_CP.xlsx')
dic_DIST_CP = {}
for i in range(len(cp)-1):
    dic_DIST_CP[cp['Distrito'][i]]=[cp['CP'][i],cp['CP2'][i],cp['CP3'][i],cp['CP4'][i]]

#   Accedo a los datos de las calles del dataset CALLE_CP.xlsx
calle_cp = pd.read_excel('C:/Users/Fran/Desktop/tfg/DATASETS/CALLE_CP.xlsx')


#   Abro el achivo donde tengo los datos de los municipios de Madrid
df = pd.read_excel('C:/Users/Fran/Desktop/tfg/MADRID_CAPITAL.xlsx')

n=0
cont=0
KL = []
#   Creo un bucle que por cada vuelta genera un número aleatorio entre 0 y 1
#   El valor que devuelve lo comparo con la frecuencia acumulada de viviendas vacías
#   Cojo el nombre del municipio con el que coincide o es menor que él
while cont<100000:
    data = open('C:/Users/Fran/Desktop/tfg/Datos/Data_Madrid_Capital_LAST_TRY.txt', 'a')
    if ((os.stat('C:/Users/Fran/Desktop/tfg/Datos/Data_Madrid_Capital_LAST_TRY.txt').st_size == 0) == True):
        data.write(
            'Calle;Localización;Habitantes;Paro_registrado;N_detenciones;Detenciones/Habitantes;Viviendas vacías;Renta media por persona;N_extranjeros;Construcción viviendas pública;Propietario;Alarma;Ocupada\n')

    rnd = random.uniform(0,1)
    chosen = ''
    for i in range(len(df['Frec_Ac_viv_Vacias'])-1):
        if rnd<=df['Frec_Ac_viv_Vacias'][i]:
            h = df['Distrito'][i]
            #   Le asigno una calle en función al distrito elegido
            #   En función a los CP de cada distrito se elige de forma aleatoria una calle con CP del distrito
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
            chosen+=street+';'+df['Distrito'][i]+';'+str(df['Habitantes'][i]).replace('.',',')+';'+str(df['Paro_registrado'][i]).replace('.',',')+';'+str(df['N_detenciones'][i]).replace('.',',')+';'+str(df['Detenciones/Habitantes'][i]).replace('.',',')+';'+str(df['Viviendas vacías'][i]).replace('.',',')+';'+str(df['Renta media por persona'][i]).replace('.',',')+';'+str(df['N_extranjeros'][i]).replace('.',',')+';'+str(df['Construcción viviendas pública'][i]).replace('.',',')
        
            #   Calcular si está ocupada
            #   El número aleatorio se compara con el promedio de viviendas ocupadas del distrito
            rnd2 = random.uniform(0,1)

            #   OCUPADA
            if rnd2<= df['OKUPA/VACÍAS'][i]:
                ocup = '1'
                n +=1

                #   En función de si es aleatoria, se le asigna la alarma y el propietario porque variará si el inmueble está o no ocupado
                #   Alarma
                rnd4 = random.uniform(0,1)
                alarma = ''
                if rnd4<= 0.05:
                    alarma = '1'
                else:
                    alarma = '0'
                
                #   Propietario
                rnd3 = random.uniform(0,1)
                if rnd3<=0.65:
                    propietario = 'Banco'
                elif rnd3<=0.95:
                    propietario = 'Ayuntamiento'
                else:
                    propietario = 'Particular'
                
                #   Las viviendas que salgan ocupadas se guardan en una lista, para tener en cuenta si en la calle hay más viviendas ocupadas y en función de ello variará la probabilidad
                KL.append(xd)

            #   NO OCUPADA
            else:
                ocup = '0'

                #   Alarma
                rnd4 = random.uniform(0,1)
                alarma = ''
                if rnd4<= 0.1:
                    alarma = '0'
                else:
                    alarma = '1'

                #   Propietario
                rnd3 = random.uniform(0,1)
                if rnd3<=0.8:
                    propietario = 'Banco'
                else:
                    propietario = 'Particular'

                #   Si la calle está en la lista de calles con al menos una vivienda ocupada, se recalcula
                for i in KL:
                    if xd == i:
                        if rnd2< 0.05:
                            ocup = '1'
                            n +=1

                            rnd4 = random.uniform(0,1)
                            alarma = ''
                            if rnd4<= 0.05:
                                alarma = '1'
                            else:
                                alarma = '0'
                            
                            rnd3 = random.uniform(0,1)
                            if rnd3<=0.65:
                                propietario = 'Banco'
                            elif rnd3<=0.95:
                                propietario = 'Ayuntamiento'
                            else:
                                propietario = 'Particular'
                        break
            
            #   Se monta el dato
            chosen+=';'+propietario+';'+alarma+';'+ocup

            #   Se guarda
            data.write(chosen)
            data.write('\n')
            break
    cont+=1
# print(n)
# print(KL)
