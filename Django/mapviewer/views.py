# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    return render(request, 'mapviewer/inicio.html')

def catalogo(request):
    return render(request, 'mapviewer/catalogo.html')

def inventario_nacional(request):
    return render(request, 'mapviewer/inventario_nacional.html')

def ficha_tec(request):
    return render(request, 'mapviewer/ficha_tecnica.html')

def fuentes_info(request):
    return render(request, 'mapviewer/fuentes_info.html')