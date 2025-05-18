# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto
COPY . /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Django (8000 por defecto)
EXPOSE 8000

# Comando para correr el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]