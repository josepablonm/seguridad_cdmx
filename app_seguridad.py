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

@app.route('/prueba',methods=['POST','GET'])
def funcion_prueba():

    if request.method == 'POST':
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        print(latitud)
        print(longitud)
        return render_template("menu.html",respuesta = {"latitud":latitud,"longitud":longitud})
    
    return render_template("menu.html",respuesta = {})

@app.route('/revisa_estado')
def api_status():
    # hacer cosas
    return render_template("menu.html")

@app.route('/mapa')
def show_map():
    
    return 'Aplicacion en linea'

        
if __name__ == '__main__':
    app.run(host= '0.0.0.0')