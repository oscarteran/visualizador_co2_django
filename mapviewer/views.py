# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .utils import mapas
from .utils.tablas import tabla_resumen_info
import logging

logger = logging.getLogger(__name__)

# =============================================
# VISTAS DE NAVEGACIÓN PRINCIPAL
# =============================================

def inicio(request):
    return render(request, 'mapviewer/inicio.html')

def inventario_nacional(request):
    # Capa base inicial desde ?tipo_mapa= (el LayerSwitcher la cambia sin recargar)
    capa = mapas.capa_desde_get(request.GET.get('tipo_mapa'))

    context = {
        'mapa': mapas.mapa_nacional(capa),
        'capas': mapas.CAPAS,
        'capa_inicial': capa,
    }
    return render(request, 'mapviewer/inventario_nacional.html', context)

def ficha_tecnica(request):
    capa = mapas.capa_desde_get(request.GET.get('tipo_mapa'))
    ubicacion = request.GET.get('ubicacion', mapas.ZONA_POR_DEFECTO)
    if ubicacion not in mapas.ARCHIVOS_ZONA:
        ubicacion = mapas.ZONA_POR_DEFECTO

    context = {
        'mapa': mapas.mapa_zona(ubicacion, capa),
        'capas': mapas.CAPAS,
        'capa_inicial': capa,
        'ubicacion_seleccionada': ubicacion,
        'opciones_ubicacion': list(mapas.ARCHIVOS_ZONA),
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


