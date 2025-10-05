import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from mapviewer.models import CO2Measurement
from pathlib import Path

class Command(BaseCommand):
    help = 'Carga datos de CO2 desde archivos CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Ruta del archivo CSV a cargar',
            default='data/processed/P_AcoculcoLatLon.csv'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar datos existentes antes de cargar',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Tamaño del lote para inserción en lote',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        clear_data = options['clear']
        batch_size = options['batch_size']

        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            raise CommandError(f'El archivo {file_path} no existe.')

        # Limpiar datos existentes si se solicita
        if clear_data:
            self.stdout.write('Limpiando datos existentes...')
            CO2Measurement.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Datos existentes eliminados.')
            )

        # Cargar datos
        self.load_co2_data(file_path, batch_size)

    def load_co2_data(self, file_path, batch_size):
        """
        Carga datos de CO2 desde un archivo CSV
        """
        self.stdout.write(f'Cargando datos desde {file_path}...')
        
        measurements = []
        total_loaded = 0
        total_errors = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(reader, start=2):  # Empezar en 2 por el header
                    try:
                        # Validar y convertir datos
                        measurement = CO2Measurement(
                            utm_x=float(row['UTM X']),
                            utm_y=float(row['UTM Y']),
                            co2_value=float(row['CO2_value']),
                            zone_name=row['Nombre de la zona'].strip(),
                            latitude=float(row['Lat']),
                            longitude=float(row['Lon'])
                        )
                        measurements.append(measurement)
                        
                        # Insertar en lotes
                        if len(measurements) >= batch_size:
                            self.bulk_create_measurements(measurements)
                            total_loaded += len(measurements)
                            self.stdout.write(f'Cargados {total_loaded} registros...')
                            measurements = []
                            
                    except (ValueError, KeyError) as e:
                        total_errors += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'Error en fila {row_num}: {e} - Datos: {row}'
                            )
                        )
                        continue

                # Insertar registros restantes
                if measurements:
                    self.bulk_create_measurements(measurements)
                    total_loaded += len(measurements)

        except Exception as e:
            raise CommandError(f'Error al procesar el archivo: {e}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Carga completada: {total_loaded} registros cargados, '
                f'{total_errors} errores encontrados.'
            )
        )

    @transaction.atomic
    def bulk_create_measurements(self, measurements):
        """
        Inserta mediciones en lote usando transacciones
        """
        CO2Measurement.objects.bulk_create(measurements, ignore_conflicts=True)
