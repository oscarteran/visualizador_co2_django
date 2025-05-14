# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .utils.mapas import generar_mapa_html

def inicio(request):
    return render(request, 'mapviewer/inicio.html')

def catalogo(request):
    return render(request, 'mapviewer/catalogo.html')

def inventario_nacional(request):
    mapa_template = generar_mapa_html('data/processed/grafico_nacional.json')
    if not mapa_template:
        return render(request, 'mapviewer/error.html', {'error': 'No se pudo generar el mapa.'})
    return render(request, mapa_template)

def ficha_tec(request):
    return render(request, 'mapviewer/ficha_tecnica.html')

def fuentes_info(request):
    return render(request, 'mapviewer/fuentes_info.html')

