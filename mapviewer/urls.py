from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inventario_nacional/', views.inventario_nacional, name='inventario_nacional'),
    path('ficha_tecnica/', views.ficha_tecnica, name='ficha_tecnica'),
    path('fuentes_info/', views.fuentes_info, name='fuentes_info')
]