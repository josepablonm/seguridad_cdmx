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

        # clasificacion
        crimen = "Asalto"
        return render_template("crimen.html",respuesta = {"crimen":crimen,"mapa":"mapas/mapa01.html"})
    
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