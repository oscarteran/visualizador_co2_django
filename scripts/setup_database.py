#!/usr/bin/env python3
"""
Script para configurar la base de datos y cargar datos
Ejecutar después de levantar los servicios con docker-compose
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

from django.core.management import call_command
from django.db import connection
from mapviewer.models import CO2Measurement

def setup_database():
    """Configurar la base de datos completa"""
    print("🚀 Configurando base de datos...")
    
    # 1. Ejecutar migraciones
    print("📊 Ejecutando migraciones...")
    call_command('migrate')
    
    # 2. Ejecutar script SQL para crear esquemas
    print("🗄️ Creando esquemas y tablas...")
    sql_file = project_dir / 'scripts' / 'create_schemas.sql'
    
    if sql_file.exists():
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        with connection.cursor() as cursor:
            cursor.execute(sql_content)
        print("✅ Esquemas creados correctamente")
    else:
        print("⚠️ Archivo SQL no encontrado, continuando...")
    
    # 3. Cargar datos de CO2
    print("📈 Cargando datos de CO2...")
    csv_file = project_dir / 'data' / 'processed' / 'P_AcoculcoLatLon.csv'
    
    if csv_file.exists():
        call_command('load_co2_data', file=str(csv_file), clear=True)
        print("✅ Datos de CO2 cargados correctamente")
    else:
        print("⚠️ Archivo CSV no encontrado")
    
    # 4. Mostrar estadísticas
    print("\n📊 Estadísticas de la base de datos:")
    total_measurements = CO2Measurement.objects.count()
    print(f"   Total de mediciones: {total_measurements}")
    
    if total_measurements > 0:
        zones = CO2Measurement.objects.values_list('zone_name', flat=True).distinct()
        print(f"   Zonas disponibles: {', '.join(zones)}")
        
        # Estadísticas por zona
        for zone in zones:
            zone_data = CO2Measurement.objects.filter(zone_name=zone)
            count = zone_data.count()
            avg_co2 = zone_data.aggregate(avg=models.Avg('co2_value'))['avg']
            print(f"   {zone}: {count} mediciones, CO2 promedio: {avg_co2:.2f}")
    
    print("\n🎉 Configuración completada!")

if __name__ == '__main__':
    setup_database()
