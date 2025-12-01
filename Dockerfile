# 1. Usa una imagen base oficial de Python
FROM python:3.11-slim

# 2. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA (LA CORRECCIÓN)
# Instalamos los paquetes necesarios para compilar GDAL, psycopg2 y otros:
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    build-essential \
    libgdal-dev \
    libpq-dev \
    # Limpieza para reducir el tamaño de la imagen
    && rm -rf /var/lib/apt/lists/*

# 3. Configuración de Variables de Entorno para GDAL
# Esto es crucial para que el instalador de Python (pip) sepa dónde buscar 'gdal-config'.
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# ----------------------------------------------------
# 4. RESTO DE TU CONFIGURACIÓN (sin cambios mayores)
# ----------------------------------------------------

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto (solo requirements.txt primero para aprovechar el cache)
COPY requirements.txt .

# Instala las dependencias de Python (Asegúrate que Gunicorn esté aquí)
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Copia el script de entrada
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# Dar permisos de ejecución
RUN chmod +x /usr/local/bin/entrypoint.sh

# Recolecta los archivos estáticos (importante para Django)
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Django
EXPOSE 8080

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PORT 8080

# Establece el entrypoint por defecto
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# COMANDO CORREGIDO: Usar Gunicorn con workers para producción en Cloud Run
# Gunicorn utiliza la variable de entorno $PORT (8080) para escuchar.
# Se recomienda usar 2 * CPU_cores + 1. Aquí usamos 2 workers como ejemplo.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "9000"]
