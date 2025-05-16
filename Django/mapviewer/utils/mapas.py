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

def generar_mapa_html(file_path: str, tipo_mapa: str = "División Política"):
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
    
    # Opciones de mapas con sus atribuciones correspondientes
    opciones_mapa = {
        "División Política": {
            "tiles": "OpenStreetMap",
            "attr": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        },
        "Satelital": {
            "tiles": "Esri.WorldImagery",
            "attr": '&copy; <a href="https://www.esri.com/">Esri</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        },
        "Relieve": {
            "tiles": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",  # URL de OpenTopoMap
            "attr": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://opentopomap.org/">OpenTopoMap</a>'
        }
    }
    
    # Usar los valores predeterminados si el tipo de mapa no está en las opciones
    opcion = opciones_mapa.get(tipo_mapa, opciones_mapa["División Política"])

    mapa = folium.Map(location=[18.5, -100], tiles=opcion["tiles"], zoom_start=5, attr=opcion["attr"])

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=row['ubi'],
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    # En lugar de guardar el mapa, devolvemos el HTML del mapa directamente
    mapa_html = mapa._repr_html_()
    return mapa_html


def generar_mapas_individuales(ubicacion: str, tipo_mapa: str):
    opciones_localizaciones = {"Acoculco": "data/processed/P_AcoculcoLatLon.csv", "Alcaparrosa": "data/processed/P_AlcaparrosaLatLon.csv", "Azufres": "data/processed/P_AzufresLatLon.csv", "Chichinautzin": "data/processed/P_ChichinautzinLatLon.csv", "Escalera": "data/processed/P_EscaleraLatLon.csv", "Michoa": "data/processed/P_MichoaLatLon.csv", "Puruandiro": "data/processed/P_PuruandiroLatLon.csv"}

    # Usar los valores predeterminados si el tipo de mapa no está en las opciones
    opcion = opciones_localizaciones.get(ubicacion, opciones_localizaciones["Michoa"])

    df = pd.read_csv(opcion) 
    
        # Opciones de mapas con sus atribuciones correspondientes
    opciones_mapa = {
        "División Política": {
            "tiles": "OpenStreetMap",
            "attr": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        },
        "Satelital": {
            "tiles": "Esri.WorldImagery",
            "attr": '&copy; <a href="https://www.esri.com/">Esri</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        },
        "Relieve": {
            "tiles": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",  # URL de OpenTopoMap
            "attr": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://opentopomap.org/">OpenTopoMap</a>'
        }
    }
    
    # Usar los valores predeterminados si el tipo de mapa no está en las opciones
    opcion = opciones_mapa.get(tipo_mapa, opciones_mapa["División Política"])

    mapa = folium.Map(location=[18.5, -100], tiles=opcion["tiles"], zoom_start=5, attr=opcion["attr"])

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            #popup=row['ubi'],
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    # En lugar de guardar el mapa, devolvemos el HTML del mapa directamente
    mapa_html = mapa._repr_html_()
    return mapa_html
    