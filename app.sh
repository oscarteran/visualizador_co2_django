# # Construir y levantar los servicios
# docker-compose up --build

# # En otra terminal, ejecutar migraciones
# docker-compose exec web python manage.py migrate

# # Crear superusuario (opcional)
# docker-compose exec web python manage.py createsuperuser

# Levantar servicios
docker-compose up --build -d

# Crear migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Ejecutar script SQL
docker-compose exec db psql -U postgres -d co2_visualizador -f /app/scripts/create_schemas.sql

# Cargar datos CSV
docker-compose exec web python manage.py load_co2_data --file data/processed/P_AcoculcoLatLon.csv --clear