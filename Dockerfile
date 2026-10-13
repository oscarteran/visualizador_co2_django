# DIFUSCO₂ — imagen para Google Cloud Run
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PORT=8080

WORKDIR /app

# Dependencias primero (capa en caché mientras requirements.txt no cambie)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Código y datos (.dockerignore excluye .env, entornos virtuales y archivos de desarrollo)
COPY . .

# Estáticos comprimidos para WhiteNoise. SECRET_KEY solo para este paso: la real
# se define en Cloud Run y nunca queda guardada en la imagen.
RUN SECRET_KEY=solo-para-collectstatic python manage.py collectstatic --noinput

# Usuario sin privilegios
RUN useradd --create-home --uid 1000 app && chown -R app:app /app
USER app

EXPOSE 8080

# Cloud Run define $PORT (8080 por defecto). gthread: 2 procesos × 4 hilos.
# El timeout (s) debe ser menor o igual al timeout de solicitud del servicio en Cloud Run.
CMD exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 2 --threads 4 --worker-class gthread \
    --timeout 120 \
    --access-logfile - --error-logfile -
