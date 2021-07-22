from flask import Flask, request, render_template, redirect
#import sklearn.external.joblib as extjoblib
import forms

from tensorflow import keras
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import io
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import os
import re
from difflib import SequenceMatcher


def cargarModelo():
    model = tf.keras.models.load_model('app/MODELO_FINAL')
    return(model)
app = Flask(__name__)

@app.route("/", methods= ['GET', 'POST'])
def index():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST':
        calle = comment_form.calle.data

        distrito= comment_form.distrito.data

        alarma = comment_form.alarma.data
        if alarma== 'Si' or alarma== 'si' or alarma== 'Sí' or alarma== 'SI' or alarma== 'SÍ':
            alarma = '1'
        else:
            alarma = '0'

        propietario = comment_form.propietario.data
        
        chosen = 'C/ '+calle

        df = pd.read_excel('app\datasets\MADRID_CAPITAL.xlsx')

        data = open('test_modelo.txt', 'a', encoding='latin-1')
        if ((os.stat('test_modelo.txt').st_size == 0) == True):
                data.write(
                    'Calle;Localización;Habitantes;Paro_registrado;N_detenciones;Detenciones/Habitantes;Viviendas vacías;Renta media por persona;N_extranjeros;Construcción viviendas pública;Propietario;Alarma\n')

        Ratio=[]
        for i in range(len(df['Distrito'])-1):
            fail = False
            if df['Distrito'][i] == distrito:
                chosen+=';'+df['Distrito'][i]+';'+str(df['Habitantes'][i]).replace('.',',')+';'+str(df['Paro_registrado'][i]).replace('.',',')+';'+str(df['N_detenciones'][i]).replace('.',',')+';'+str(df['Detenciones/Habitantes'][i]).replace('.',',')+';'+str(df['Viviendas vacías'][i]).replace('.',',')+';'+str(df['Renta media por persona'][i]).replace('.',',')+';'+str(df['N_extranjeros'][i]).replace('.',',')+';'+propietario+';'+alarma
                data.write(chosen)
                data.write('\n')
                fail = True
                break
            else:
                Ratio.append(SequenceMatcher(None, df['Distrito'][i], distrito).ratio())


        if fail == False:
            max_value = max(Ratio)
            for i in range(len(Ratio)-1):
                if max_value == Ratio[i]:
                    pos = i
                    break
            chosen+=';'+df['Distrito'][pos]+';'+str(df['Habitantes'][pos]).replace('.',',')+';'+str(df['Paro_registrado'][pos]).replace('.',',')+';'+str(df['N_detenciones'][pos]).replace('.',',')+';'+str(df['Detenciones/Habitantes'][pos]).replace('.',',')+';'+str(df['Viviendas vacías'][pos]).replace('.',',')+';'+str(df['Renta media por persona'][pos]).replace('.',',')+';'+str(df['N_extranjeros'][pos]).replace('.',',')+';'+propietario+';'+alarma
            data.write(chosen)
            data.write('\n')


        model = tf.keras.models.load_model('app/MODELO_FINAL')

        data_test = pd.read_csv('test_modelo.txt',sep=';', decimal=",", error_bad_lines=False)

        columns_to_extract2 = ['Calle','Localización',	'Habitantes','Paro_registrado','N_detenciones',
                            'Detenciones/Habitantes','Viviendas vacías','Renta media por persona',
                            'N_extranjeros', 'Propietario',
                            'Alarma']

        #Creo un dataframe con las variables con las que voy a predecir
        test_features = data_test[columns_to_extract2]

        # Voy a coger por separado las variables numéricas y las categóricas para tratarlas más fácilmente
        # Creo el dataframe de las variables numéricas -->  var_num
        var_t = ['Habitantes','Paro_registrado','N_detenciones',
            'Detenciones/Habitantes','Viviendas vacías','Renta media por persona',
            'N_extranjeros']
        var_num_t=test_features[var_t]

        # Creo el dataframe de las variables categóricas -->  var_cat
        var2_t = ['Calle','Localización','Propietario','Alarma']
        var_cat_t=test_features[var2_t]

        #Creo una función para normalizar mis valores de las variables numéricas --> norm(df)
        def norm(df):
            return (df - df.min()) / ( df.max() - df.min())


        #Normalizo los valores de las variables numéricas
        var_num_t = norm(var_num_t)


        var_cat_t = pd.get_dummies(var_cat_t, columns=['Alarma'] ,drop_first=True)

        # Hago lo mismo con la variable -- Localización -- pero a parte porque al tener 21 entradas, no se podía dejar en una sola columna
        var_cat_t = pd.get_dummies(var_cat_t, columns=['Calle','Localización','Propietario'])

        #Uno los 2 dataframes de variables (categóricas y numéricas)
        test_features = pd.concat([var_num_t,var_cat_t],axis=1,sort=False)

        tam = 8204-len(test_features.columns)
        cont=0
        while cont<tam:
            name = 'Calle_'+ str(cont)
            test_features.insert(0,name,'0', allow_duplicates=False)
            cont+=1


        test_features = np.asarray(test_features).astype('float32')


        predictions = model.predict(test_features)

        # print(predictions)
        # Lista donde almacenaré mis predicciones
        out = []
        for i in predictions:
            # Como los resultados son tan próximos a uno, establezco mi umbral en 0.7
            if i>=0.7:
                out.append(1)
            else:
                out.append(0)
        print('')
        if out[-1]==0:
            return redirect('/no')
            # print('No se va a ocupar')
        else:
            return redirect('/si')
            # print('Corre a comprar una alarma')


    title = 'Ocupation prediction'

    return render_template('index.html', title = title, form = comment_form)

@app.route('/si')
def si():
    return render_template('si.html')

@app.route('/no')
def no():
    return render_template('no.html')

if __name__ == '__main__':
    app.run(debug=True)


