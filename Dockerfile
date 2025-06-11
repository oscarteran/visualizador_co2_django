# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recolecta los archivos estáticos (importante para Django)
# Si no usas archivos estáticos, puedes omitir esta línea
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Django (8000 por defecto)
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=mapviewer.settings
ENV PORT 8000

# Comando para correr el servidor
#CMD ["python", "manage.py", "runserver", "0.0.0.0:${PORT}"]

# Comando para correr en productivo GCP Cloud Run
#CMD ["gunicorn", "mapviewer.wsgi:application", "--bind", "0.0.0.0:8080"]
CMD ["gunicorn",  "--bind", "0.0.0.0:${PORT}", "mapviewer.wsgi:application",]