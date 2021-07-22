import os
import re


#Divido el texto por oraciones
def div_oraciones(x):
    return x.split('.')

#Me quedo solo con las oraciones con números, que son los que tienen datos
def numeros(x):
    L =[]
    for i in x:
        if any(map(str.isdigit, i)):
            L.append(i)
    return(L)

#Uno los valores que estaban separados porque las unidades de millar estaban separadas por punto
def union(x):
    i = 0
    while i<len(x):
        try:
            if x[i][len(x[i])-1].isdigit():
                if x[i+1][0].isdigit():
                    x[i]= x[i]+x[i+1]
                    x.remove(x[i+1])
                else:
                    i+=1
            else:
                i+=1
        except IndexError:
            return(x)
    return(x)

#Muestro mi lista con las oraciones con números
def printear(x):
    for i in x:
        print(i)
    print(x)
    print(len(x))
    print('')

#Creo una lista que contiene las frases que tienen %, ya que para generar datos necesito proporciones
def porcentajes(x):
    P = []
    for i in x:
        for j in i:
            if j == '%':
                P.append(i)
                break
    return(P)

#Compruebo si hay nombres de bancos con cifras, ya que me podrían indicar promedio o valor absoluto de viviendas que tienen ocupadas
def banks(x):
    Bancos=['BBVA', 'Santander', 'Bankia', 'Caixa', 'Sabadell', 'Bankinter', 'Abanca', 'Caja Madrid']
    B=[]
    for i in x:
        for j in Bancos:
            if j in i:
                B.append(i)
                break
    return(B)

#Guardar en un txt
def guardar_txt(x, y):
    file = open("C:/Users/Fran/Desktop/tfg/Textos_procesados/"+y+".txt", "w",encoding='utf-8')
    for i in x:
        file.write(i+'\n')
    file.close()


#Guardo en una variable el número de archivos de texto que tengo guardados para procesar
num_arch = sum([len(files) for r, d, files in os.walk("C:/Users/Fran/Desktop/tfg/Textos_bruto")])

#Creo un contador en 1, con el que recorreré todos los archivos
cont = 1

#Accedo a los archivos que hay en la carpeta de Textos_bruto, los proceso y los guardo en Textos_procesados
while cont<=num_arch:
    cont_str = str(cont)
    f = open ('C:/Users/Fran/Desktop/tfg/Textos_bruto/texto'+cont_str+'.txt','r',encoding='latin-1')
    tx = f.read()
    f.close()

    aux = div_oraciones(tx)
    L = numeros(aux)
    L = union(L)

    T = banks(L)
    if len(T)!=0:
        guardar_txt(T,'bancos'+cont_str+'')

    L = porcentajes(L)
    guardar_txt(L,'porcentajes_texto'+cont_str+'')
    cont+=1