# Create your views here.
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from . import design
from .utils import mapas
from .utils.tablas import fuentes_por_zona, tabla_resumen_info
import logging

logger = logging.getLogger(__name__)


def _zona_desde_get(request):
    zona = request.GET.get('ubicacion', mapas.ZONA_POR_DEFECTO)
    return zona if zona in mapas.ARCHIVOS_ZONA else mapas.ZONA_POR_DEFECTO


def _entidades():
    return {fila['Nombre']: fila['Estado'] for fila in tabla_resumen_info()}


# =============================================
# VISTAS DE NAVEGACIÓN PRINCIPAL
# =============================================

def inicio(request):
    resumen = mapas.resumen_catalogo()
    context = {
        'resumen': resumen,
        'rango_flujo': f"{design.format_flux(resumen['minimo'])} – {design.format_flux(resumen['maximo'])}",
        'unidad': design.FLUX_UNIT,
        # Mapa testigo: las 7 zonas, sin interacción
        'mapa': mapas.mapa_nacional(estatico=True),
    }
    return render(request, 'mapviewer/inicio.html', context)

def inventario_nacional(request):
    # Capa base inicial desde ?tipo_mapa= (el LayerSwitcher la cambia sin recargar)
    capa = mapas.capa_desde_get(request.GET.get('tipo_mapa'))
    mapa = mapas.mapa_nacional(capa)

    context = {
        'mapa': mapa,
        'zonas': mapa['zonas'],
        'capas': mapas.CAPAS,
        'capa_inicial': capa,
    }
    return render(request, 'mapviewer/inventario_nacional.html', context)

def ficha_tecnica(request):
    capa = mapas.capa_desde_get(request.GET.get('tipo_mapa'))
    ubicacion = _zona_desde_get(request)
    mapa = mapas.mapa_zona(ubicacion, capa)
    puntos = mapa['puntos']

    # Estadísticas calculadas aquí (no en JS)
    stats = mapas.estadisticas([p['valor'] for p in puntos])
    filas = [
        {'id': p['id'], 'lat': p['lat'], 'lon': p['lon'], 'flujo': p['valor'], 'clase': p['valor']}
        for p in sorted(puntos, key=lambda p: p['valor'], reverse=True)
    ]
    columnas = [
        {'key': 'id', 'label': 'Punto'},
        {'key': 'lat', 'label': 'Latitud', 'numeric': True, 'kind': 'coord'},
        {'key': 'lon', 'label': 'Longitud', 'numeric': True, 'kind': 'coord'},
        {'key': 'flujo', 'label': f'Flujo ({design.FLUX_UNIT})', 'numeric': True, 'kind': 'flux'},
        {'key': 'clase', 'label': 'Clase', 'kind': 'flux_class'},
    ]

    entidad = _entidades().get(ubicacion, '')
    context = {
        'mapa': mapa,
        'capas': mapas.CAPAS,
        'capa_inicial': capa,
        'ubicacion_seleccionada': ubicacion,
        'opciones_ubicacion': list(mapas.ARCHIVOS_ZONA),
        'entidad': entidad,
        'eyebrow': f'Ficha técnica · {entidad}' if entidad else 'Ficha técnica',
        'lead': f'Flujo de CO₂ del suelo en {stats["n"]} puntos de medición.',
        'hist_caption': f'{design.FLUX_UNIT}, clases por décadas.',
        'tabla_caption': f'{stats["n"]} mediciones, ordenadas por flujo. Fuente: Instituto de Geofísica, UNAM.',
        'stats': stats,
        'stats_mediana': design.format_flux(stats['mediana']),
        'stats_maximo': design.format_flux(stats['maximo']),
        'valores': [p['valor'] for p in puntos],
        'columnas': columnas,
        'filas': filas,
        'fuente': fuentes_por_zona()[ubicacion],
        'unidad': design.FLUX_UNIT,
        'metodo': design.MEASUREMENT_METHOD,
        'url_descarga': reverse('descargar_csv') + '?ubicacion=' + ubicacion,
    }
    return render(request, 'mapviewer/ficha_tecnica.html', context)

def descargar_csv(request):
    """CSV procesado de la zona, sin modificar (data/processed/P_<Zona>LatLon.csv)."""
    zona = _zona_desde_get(request)
    archivo = mapas.DATA_DIR / mapas.ARCHIVOS_ZONA[zona]
    return FileResponse(open(archivo, 'rb'), as_attachment=True,
                        filename=f'difusco2_{zona}.csv', content_type='text/csv')

def fuentes_info(request):
    zonas = mapas.leer_zonas()
    fuentes = fuentes_por_zona()
    context = {
        'catalogo_columnas': [
            {'key': 'name', 'label': 'Zona'},
            {'key': 'state', 'label': 'Entidad'},
            {'key': 'lat', 'label': 'Latitud', 'numeric': True, 'kind': 'coord'},
            {'key': 'lon', 'label': 'Longitud', 'numeric': True, 'kind': 'coord'},
            {'key': 'n', 'label': 'Puntos', 'numeric': True},
        ],
        'catalogo_filas': zonas,
        'fuentes_columnas': [
            {'key': 'zona', 'label': 'Zona'},
            {'key': 'nombre_catalogo', 'label': 'Nombre en el catálogo'},
            {'key': 'origen', 'label': 'Origen de los datos'},
            {'key': 'fecha', 'label': 'Fecha de medición'},
            {'key': 'puntos', 'label': 'Puntos', 'numeric': True},
        ],
        'fuentes_filas': [fuentes[z['name']] for z in zonas],
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
