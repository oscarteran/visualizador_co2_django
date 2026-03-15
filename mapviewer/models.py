from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =============================================
# PERFIL DE USUARIO
# =============================================

class UserProfile(models.Model):
    """
    Perfil extendido del usuario, enlazado 1:1 con el modelo User de Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    institution = models.CharField(max_length=200, blank=True, default='', verbose_name='Institución')
    role = models.CharField(max_length=100, blank=True, default='', verbose_name='Rol / Cargo')
    bio = models.TextField(blank=True, default='', verbose_name='Biografía')

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f'Perfil de {self.user.username}'

    @property
    def avatar_initial(self):
        """Retorna la inicial del nombre o del username para el avatar."""
        if self.user.first_name:
            return self.user.first_name[0].upper()
        return self.user.username[0].upper()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente al registrar un usuario nuevo."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil al guardar el usuario."""
    if hasattr(instance, 'profile'):
        instance.profile.save()


# =============================================
# MODELOS DE DATOS GEO
# =============================================

# Create your models here.

class CO2Measurement(models.Model):
    """
    Modelo para almacenar mediciones de CO2 con coordenadas geográficas
    """
    utm_x = models.FloatField(verbose_name="UTM X")
    utm_y = models.FloatField(verbose_name="UTM Y")
    co2_value = models.FloatField(verbose_name="Valor CO2")
    zone_name = models.CharField(max_length=100, verbose_name="Nombre de la zona")
    latitude = models.FloatField(verbose_name="Latitud")
    longitude = models.FloatField(verbose_name="Longitud")
    
    # Campo geográfico para consultas espaciales
    location = gis_models.PointField(
        geography=True,
        srid=4326,
        verbose_name="Ubicación",
        help_text="Punto geográfico (lat, lon)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        db_table = 'co2_measurements'
        verbose_name = 'Medición de CO2'
        verbose_name_plural = 'Mediciones de CO2'
        indexes = [
            models.Index(fields=['zone_name']),
            models.Index(fields=['co2_value']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        # Crear el punto geográfico automáticamente
        if self.latitude and self.longitude:
            self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.zone_name} - CO2: {self.co2_value:.2f} ({self.latitude:.4f}, {self.longitude:.4f})"
