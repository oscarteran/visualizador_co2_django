# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Django (8000 por defecto)
EXPOSE 8080

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=mapviewer.settings

# Comando para correr el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:${PORT}"]

# Comando para correr en productivo GCP Cloud Run
# CMD ["gunicorn", "mapviewer.wsgi:application", "--bind", "0.0.0.0:${PORT}"]