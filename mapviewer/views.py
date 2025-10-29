# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .utils.mapas import generar_mapa_html, generar_mapas_individuales
from .utils.tablas import tabla_resumen_info
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
    ubicacion = request.GET.get('ubicacion', 'Alcaparrosa')
    
    # Generar el mapa con el tipo seleccionado
    mapa_html = generar_mapas_individuales(ubicacion, tipo_mapa)
    
    if not mapa_html:
        return render(request, 'mapviewer/error.html', {'error': 'No se pudo generar el mapa.'})
    
    # Obtener las opciones de mapa para el dropdown
    opciones_mapa = ["División Política", "Satelital", "Relieve"]
    opciones_ubicacion = ["Acoculco", "Alcaparrosa", "Azufres", "Chichinautzin", "Escalera", "Michoa", "Puruandiro"]
    
    context = {
        'mapa': mapa_html,
        'tipo_mapa_seleccionado': tipo_mapa,
        'ubicacion_seleccionada': ubicacion,
        'opciones_mapa': opciones_mapa,
        'opciones_ubicacion': opciones_ubicacion,
    }
    
    return render(request, 'mapviewer/ficha_tecnica.html', context)

def fuentes_info(request):
    tabla_info = tabla_resumen_info()
    context = {
        'tabla_info': tabla_info,
    }
    return render(request, 'mapviewer/fuentes_info.html', context)

def acerca_de(request):
    return render(request, 'mapviewer/acerca_de.html')

def ayuda_y_contacto(request):
    return render(request, 'mapviewer/ayuda_y_contacto.html')

def error_404_view(request, exception):
    return render(request, 'mapviewer/error.html', {
        'codigo_error': 404,
        'mensaje_error': 'Página no encontrada.'
    }, status=404)

def error_500_view(request):
    return render(request, 'mapviewer/error.html', {
        'codigo_error': 500,
        'mensaje_error': 'Error interno del servidor.'
    }, status=500)


