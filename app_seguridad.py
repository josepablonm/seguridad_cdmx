from flask import Flask, request, render_template, url_for, redirect, session, jsonify
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from mapea_delitos import mapa_delito
import tensorflow as tf
from tensorflow.keras.models import save_model, load_model
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
import pickle, json
from joblib import load
from scipy.spatial import distance_matrix

app = Flask(__name__)

CLASIFICADOR = load_model('modelos/modelo.h5')

ENCODER = OneHotEncoder(sparse=False)
with open('modelos/day_encoder.pkl','rb') as r:
    ENCODER = pickle.load(r)

SCALER = StandardScaler()
SCALER = load('modelos/std_scaler.bin')

LABELS = LabelEncoder()
LABELS.classes_ = np.load('modelos/classes.npy', allow_pickle = True)

COORDENADAS = np.load('modelos/coordenadas.npy',allow_pickle=True)

def get_features(Xcoords,Xtime,Xday,scaler,train=False):
    """
    Funcion para sacar features de X

    args:
        Xcoords :  array - shape=(n,2) floats
        Xtime :  array - shape=(n,1) int
        Xday :  array - shape=(n,1) str
    outs :
        X_features : array - shape=(n,188) floats
    """
    X_features = np.zeros(shape=(Xcoords.shape[0],188))
    distances = distance_matrix(Xcoords,COORDENADAS)
    if train:
        scaler.fit(distances)
    distances = scaler.transform(distances)
    X_features[:,0:180] = distances
    X_features[:,180] = np.reshape(Xtime.astype('float64')/24,(Xcoords.shape[0]))
    X_features[:,181:] = ENCODER.transform(Xday)
    return X_features, scaler

@app.route('/')
def landing():
    """Funcion para redirigir al endpoint correcto"""

    return redirect(url_for("show_map"))

@app.route('/crimen',methods=['POST','GET'])
def prediccion_delito():
    """Funcion para decir que crimen es mas probable en un lugar"""
    if request.method == 'POST':
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        dia = request.form['dia']
        hora = request.form['hora']
        print("Latitud",latitud)
        print("Longitud",longitud)
        print("Dia",dia)
        print("Hora",hora)

        # preparamos datos
        geo_point = {'location':[float(latitud),float(longitud)],'tiempo':'{}-{}'.format(dia,hora)}
        Xtime = np.array([int(hora[:2])])
        X, _ = get_features(np.array([geo_point['location']]), Xtime, np.array([dia]).reshape(-1,1), SCALER)
        # clasificamos
        pred = CLASIFICADOR.predict({'in_vector': X})
        pnum = tf.argmax(pred, axis=1)
        crimen = LABELS.inverse_transform(pnum)[0]
        geo_point['delito'] = crimen
        mapa = mapa_delito(geo_point,'mapax')
        return render_template("crimen.html",respuesta = {"crimen":crimen,"mapa":mapa})
    
    return render_template("crimen.html",respuesta = {})


@app.route('/datos')
def show_map():
    """Funcion para mostrar un mapa con datos"""
    return render_template("datos.html",respuesta={"mapa_base":"mapas/mapa01.html"})


@app.route('/revisa_estado')
def api_status():
    # hacer cosas
    return "Aplicacion en linea"
        
if __name__ == '__main__':
    app.run(host= '0.0.0.0')