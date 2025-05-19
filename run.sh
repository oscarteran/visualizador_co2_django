#!/bin/bash

# Aplica las migraciones de la base de datos
python manage.py migrate --noinput

# Inicia el servidor Gunicorn
gunicorn --bind 0.0.0.0:8000 core.wsgi