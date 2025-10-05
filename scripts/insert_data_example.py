#!/usr/bin/env python3
"""
Ejemplo de cómo insertar datos en la base de datos
"""

import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.parent
sys.path.append(str(project_dir))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mapviewer.models import CO2Measurement
from django.contrib.gis.geos import Point

def insert_sample_data():
    """Insertar datos de ejemplo"""
    print("📊 Insertando datos de ejemplo...")
    
    # Datos de ejemplo
    sample_data = [
        {
            'utm_x': 589539.0,
            'utm_y': 2203190.0,
            'co2_value': 3.9133692,
            'zone_name': 'Acoculco',
            'latitude': 19.9230151004979,
            'longitude': -98.14446913035876
        },
        {
            'utm_x': 589509.0,
            'utm_y': 2203200.0,
            'co2_value': 9.558972,
            'zone_name': 'Acoculco',
            'latitude': 19.923106837170263,
            'longitude': -98.14475526570116
        },
        {
            'utm_x': 589511.0,
            'utm_y': 2203197.0,
            'co2_value': 81.11043,
            'zone_name': 'Acoculco',
            'latitude': 19.923079637978695,
            'longitude': -98.14473630340296
        }
    ]
    
    # Insertar datos
    measurements = []
    for data in sample_data:
        measurement = CO2Measurement(**data)
        measurements.append(measurement)
    
    # Usar bulk_create para inserción eficiente
    CO2Measurement.objects.bulk_create(measurements, ignore_conflicts=True)
    
    print(f"✅ {len(measurements)} registros insertados")

def query_data():
    """Consultar datos de ejemplo"""
    print("\n🔍 Consultando datos...")
    
    # Consulta básica
    total = CO2Measurement.objects.count()
    print(f"Total de mediciones: {total}")
    
    # Consulta por zona
    acoculco_data = CO2Measurement.objects.filter(zone_name='Acoculco')
    print(f"Mediciones en Acoculco: {acoculco_data.count()}")
    
    # Consulta con filtros
    high_co2 = CO2Measurement.objects.filter(co2_value__gt=50)
    print(f"Mediciones con CO2 > 50: {high_co2.count()}")
    
    # Consulta geográfica (requiere PostGIS)
    try:
        from django.contrib.gis.geos import Point
        from django.contrib.gis.db.models import Q
        
        # Buscar mediciones cerca de un punto
        center_point = Point(-98.144, 19.923)  # Longitud, Latitud
        nearby = CO2Measurement.objects.filter(
            location__distance_lte=(center_point, 0.01)  # 0.01 grados ≈ 1km
        )
        print(f"Mediciones cerca del centro: {nearby.count()}")
        
    except Exception as e:
        print(f"⚠️ Consulta geográfica no disponible: {e}")

def update_data():
    """Actualizar datos de ejemplo"""
    print("\n🔄 Actualizando datos...")
    
    # Actualizar todas las mediciones de una zona
    updated = CO2Measurement.objects.filter(
        zone_name='Acoculco'
    ).update(co2_value=models.F('co2_value') * 1.1)  # Aumentar 10%
    
    print(f"✅ {updated} registros actualizados")

def delete_data():
    """Eliminar datos de ejemplo"""
    print("\n🗑️ Eliminando datos...")
    
    # Eliminar mediciones con CO2 muy bajo
    deleted = CO2Measurement.objects.filter(co2_value__lt=5).delete()
    print(f"✅ {deleted[0]} registros eliminados")

if __name__ == '__main__':
    print("🚀 Ejemplo de operaciones con la base de datos")
    print("=" * 50)
    
    # Insertar datos
    insert_sample_data()
    
    # Consultar datos
    query_data()
    
    # Actualizar datos
    update_data()
    
    # Consultar después de actualizar
    query_data()
    
    # Eliminar algunos datos
    delete_data()
    
    # Consulta final
    query_data()
    
    print("\n🎉 Ejemplo completado!")
