from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Hola, esta es mi primera vista Django. \n"
                        "Este valor se esta presentando en el apartado de Maps")