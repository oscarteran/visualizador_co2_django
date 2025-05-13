from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    #path('', views.catalogo, name='catalogo'),
    path('inventario_nacional/', views.inventario_nacional, name='inventario_nacional'),
    path('ficha_tec/', views.ficha_tec, name='ficha_tec'),
    path('fuentes_info/', views.fuentes_info, name='fuentes_info')
]