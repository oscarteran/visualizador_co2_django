from django.urls import path
from . import views

urlpatterns = [
    # URLs de Navegación Principal
    path('', views.inicio, name='inicio'),
    path('inventario_nacional/', views.inventario_nacional, name='inventario_nacional'),
    path('ficha_tecnica/', views.ficha_tecnica, name='ficha_tecnica'),
    path('fuentes_info/', views.fuentes_info, name='fuentes_info'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('ayuda_y_contacto/', views.ayuda_y_contacto, name='ayuda_y_contacto'),
    
    # URLs de Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]