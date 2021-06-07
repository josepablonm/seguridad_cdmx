from flask import Flask, render_template, url_for, redirect, session, jsonify
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, MarkerCluster
import json
from datetime import datetime as dt

def mapa_global(df, df_alcpp, df_estaciones, geo_data, loc_ini = [19.43,-99.14], tiles='Stamen Toner'):
    """
        Funcion para graficar delitos cometidos, estaciones de policia, estaciones de metrobus y colonias

        args:
            df : pandas.DataFrame
            df_alcpp : pandas.DataFrame
            df_estaciones : pandas.DataFrame
            geo_data : poly
            loc_ini : list - opcional
            tiles : string - opcional
        
        outs:
            map_it : folium.Map
    """
    map_it = folium.Map(location = loc_ini,tiles=tiles,zoom_start=11)

    for i in range(0,len(df_estaciones)):
      folium.Circle( radius=80,location=[ df_estaciones.stop_lat.values[i], df_estaciones.stop_lon.values[i] ], tooltip=df_estaciones.stop_name[i], 
                    color='red').add_to(map_it)
    
    map_cluster = MarkerCluster().add_to(map_it)

    for indx, row in df.iterrows():

        if row.categoria_delito == 'ROBO DE VEHÍCULO CON Y SIN VIOLENCIA':
            color = 'crimson'
            icon = 'automobile'
        elif row.categoria_delito == 'ROBO A TRANSEUNTE EN VÍA PÚBLICA CON Y SIN VIOLENCIA':
            color = 'green'
            icon = 'male'
        elif row.categoria_delito == 'ROBO A NEGOCIO CON VIOLENCIA':
            color = 'purple'
            icon = 'shopping-bag'
        else:
            color = 'darkgreen'
            icon = 'motorcycle'
        
        folium.Marker(location = [row.latitud,row.longitud],
                      icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                      popup=dt.strftime(row.fecha_hechos,'%Y-%m-%d %H:%M:%S')).add_to(map_cluster)



    for indx, row in df_alcpp.iterrows():
        folium.Circle(
            radius=120,
            location=[row.Latitud, row.Longitud],
            popup=str(row['Nombre y sede']),
            color='blue',
        ).add_to(map_it)
    
    folium.GeoJson(
        geo_data).add_to(map_it)
    folium.LayerControl().add_to(map_it)
    
    return map_it


def mapa_delito(geo_point, nombre, tiles='Stamen Toner'):
    """
        Funcion para graficar delitos cometidos, estaciones de policia, estaciones de metrobus y colonias
        args:
            df : pandas.DataFrame
            loc_ini : list - opcional
            tiles : string - opcional
        outs:
            map_it : folium.Map
    """
    map_it = folium.Map(location = geo_point['location'],tiles=tiles,zoom_start=11, prefer_cavas = True)
    
    map_cluster = MarkerCluster().add_to(map_it)

    if geo_point['delito'] == 'R. Vehiculo' or geo_point['delito'] == 'R. Vehículo':
        color = 'crimson'
        icon = 'automobile'
    elif geo_point['delito'] == 'R. Transeunte':
        color = 'green'
        icon = 'male'
    elif geo_point['delito'] == 'R. Negocio':
        color = 'purple'
        icon = 'shopping-bag'
    elif geo_point['delito'] == 'R. Repartidor':
        color = 'darkgreen'
        icon = 'motorcycle'
    elif geo_point['delito'] == 'R. Metro':
        color = 'darkrblue'
        icon = 'subway'
    else:
        color = 'black'
        icon = 'exclamation-circle'
        
    folium.Marker(location = geo_point['location'],
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            popup= geo_point['tiempo']).add_to(map_cluster)
    
    htmlname = 'mapas/{}.html'.format(nombre)
    map_it.save('templates/{}'.format(htmlname))

    return htmlname