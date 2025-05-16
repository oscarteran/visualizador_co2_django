# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .utils.mapas import generar_mapa_html, generar_mapas_individuales
import logging

logger = logging.getLogger(__name__)

def inicio(request):
    return render(request, 'mapviewer/inicio.html')

def catalogo(request):
    return render(request, 'mapviewer/catalogo.html')

def inventario_nacional(request):
    # Obtener el tipo de mapa seleccionado del parámetro GET
    tipo_mapa = request.GET.get('tipo_mapa', 'División Política')
    
    # Ruta del archivo JSON (ajusta según tu estructura de proyecto)
    json_path = 'data/processed/grafico_nacional.json'
    
    # Generar el mapa con el tipo seleccionado
    mapa_html = generar_mapa_html(json_path, tipo_mapa)
    
    if not mapa_html:
        return render(request, 'mapviewer/error.html', {'error': 'No se pudo generar el mapa.'})
    
    # Obtener las opciones de mapa para el dropdown
    opciones_mapa = ["División Política", "Satelital", "Relieve"]
    
    context = {
        'mapa': mapa_html,
        'tipo_mapa_seleccionado': tipo_mapa,
        'opciones_mapa': opciones_mapa
    }
    
    return render(request, 'mapviewer/inventario_nacional.html', context)

def ficha_tecnica(request):
    # Obtener el tipo de mapa seleccionado del parámetro GET
    tipo_mapa = request.GET.get('tipo_mapa', 'División Política')
    
    # Generar el mapa con el tipo seleccionado
    mapa_html = generar_mapas_individuales('Alcaparrosa')
    
    if not mapa_html:
        return render(request, 'mapviewer/error.html', {'error': 'No se pudo generar el mapa.'})
    
    # Obtener las opciones de mapa para el dropdown
    opciones_mapa = ["División Política", "Satelital", "Relieve"]
    
    context = {
        'mapa': mapa_html,
        'tipo_mapa_seleccionado': 'tipo_mapa',
        'opciones_mapa': opciones_mapa
    }
    
    return render(request, 'mapviewer/ficha_tecnica.html', context)

def fuentes_info(request):
    return render(request, 'mapviewer/fuentes_info.html')

