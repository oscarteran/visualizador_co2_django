import folium
import json
import pandas as pd
import logging
import os 
from django.conf import settings

logger = logging.getLogger(__name__)

def generar_mapa_html_v1(file_path):
    #file_path = os.path.join(settings.BASE_DIR, 'data', 'processed', 'nombres_unicos.json')
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    logger.info("Proceso de log")
    nombres, lat, lon = [], [], []
    for k, v in data.items():
        nombres.append(k)
        lat.append(v[0])
        lon.append(v[1])

    df = pd.DataFrame({'ubi': nombres, 'Lat': lat, 'Lon': lon})

    mapa = folium.Map(location=[23.5, -100], tiles='OpenStreetMap', zoom_start=5)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=row['ubi'],
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    return mapa._repr_html_()  # Devuelve HTML embebido



def generar_mapa_html_v2(file_path: str):
    #file_path = os.path.join(settings.BASE_DIR, 'data', 'processed', 'nombres_unicos.json')

    with open(file_path, 'r') as f:
        data = json.load(f)

    nombres, lat, lon = [], [], []

    for k, v in data.items():
        try:
            lat_val = float(v[0])
            lon_val = float(v[1])
            nombres.append(k)
            lat.append(lat_val)
            lon.append(lon_val)
        except (ValueError, TypeError):
            continue

    df = pd.DataFrame({'ubi': nombres, 'Lat': lat, 'Lon': lon})

    if df.empty:
        return None

    mapa = folium.Map(location=[23.5, -100], tiles='OpenStreetMap', zoom_start=5)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=row['ubi'],
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    #output_path = os.path.join(settings.BASE_DIR, 'Django', 'mapviewer', 'templates', 'mapviewer', 'mapa_render.html')
    #TODO: Quitar el Hardcode
    output_path = "C:/Users/Oscar/OneDrive/Escritorio/visualizador_co2_django/Django/mapviewer/templates/mapviewer/mapa_render.html"
    mapa.save(output_path)

    return mapa

def generar_mapa_html(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)

    nombres, lat, lon = [], [], []

    for k, v in data.items():
        try:
            lat_val = float(v[0])
            lon_val = float(v[1])
            nombres.append(k)
            lat.append(lat_val)
            lon.append(lon_val)
        except (ValueError, TypeError):
            continue

    df = pd.DataFrame({'ubi': nombres, 'Lat': lat, 'Lon': lon})

    if df.empty:
        return None

    mapa = folium.Map(location=[23.5, -100], tiles='OpenStreetMap', zoom_start=5)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=row['ubi'],
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    # En lugar de guardar el mapa, devolvemos el HTML del mapa directamente
    mapa_html = mapa._repr_html_()
    return mapa_html