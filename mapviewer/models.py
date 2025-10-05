from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

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
