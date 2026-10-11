# 1. Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto (solo requirements.txt primero para aprovechar el cache)
COPY requirements.txt .

# Instala las dependencias de Python (Asegúrate que Gunicorn esté aquí)
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Recolecta los archivos estáticos (importante para Django)
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Django
EXPOSE 8080

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PORT 8080

# COMANDO CORREGIDO: Usar Gunicorn con workers para producción en Cloud Run
# Gunicorn utiliza la variable de entorno $PORT (8080) para escuchar.
# Se recomienda usar 2 * CPU_cores + 1. Aquí usamos 2 workers como ejemplo.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "9000"]
