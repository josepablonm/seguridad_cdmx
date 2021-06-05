from flask import Flask, request, render_template, url_for, redirect, session, jsonify
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
#import folium
#from folium.plugins import HeatMap, MarkerCluster
import json
from datetime import datetime as dt
#from sqlalchemy import create_engine, MetaData, Table, select, Column
#import sqlalchemy as sdb

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def prediccion_delito():

    if request.method == 'POST':
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        dia = request.form['dia']
        hora = request.form['hora']
        print("Latitud",latitud)
        print("Longitud",longitud)
        print("Dia",dia)
        print("Hora",hora)

        # clasificacion
        crimen = "Asalto"
        return render_template("crimen.html",respuesta = {"crimen":crimen,"mapa":"mapas/mapa01.html"})
    
    return render_template("crimen.html",respuesta = {})


@app.route('/revisa_estado')
def api_status():
    # hacer cosas
    return render_template("menu.html")

@app.route('/mapa')
def show_map():
    
    return 'Aplicacion en linea'

        
if __name__ == '__main__':
    app.run(host= '0.0.0.0')