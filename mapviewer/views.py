# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils.mapas import generar_mapa_html, generar_mapas_individuales
from .utils.tablas import tabla_resumen_info
from .forms import LoginForm, RegisterForm, UserProfileForm
import logging

logger = logging.getLogger(__name__)

# =============================================
# VISTAS DE AUTENTICACIÓN
# =============================================

def login_view(request):
    """Vista para iniciar sesión."""
    # Redirigir si ya está autenticado
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            next_url = request.GET.get('next', 'inicio')
            return redirect(next_url)
    else:
        form = LoginForm()
        
    return render(request, 'mapviewer/login.html', {'form': form})

def register_view(request):
    """Vista para registrar un nuevo usuario."""
    # Redirigir si ya está autenticado
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # El perfil se crea automáticamente por la señal post_save en models.py
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('inicio')
    else:
        form = RegisterForm()
        
    return render(request, 'mapviewer/register.html', {'form': form})

def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('inicio')

@login_required
def profile_view(request):
    """Vista del perfil de usuario, permite ver y editar datos."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        # Actualizar datos del modelo User también (nombre, apellido, email)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.email = form.cleaned_data.get('email', user.email)
            user.save()
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
    else:
        # Pre-poblar datos del modelo User
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=request.user.profile, initial=initial_data)
        
    return render(request, 'mapviewer/profile.html', {'form': form})

# =============================================
# VISTAS DE NAVEGACIÓN PRINCIPAL
# =============================================

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


