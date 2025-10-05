#!/bin/bash
# wait-for-it.sh

# Nombre del host de la DB y puerto (según docker-compose)
DB_HOST=db
DB_PORT=5432

# Bucle de espera. Netcat (nc) intenta conectarse al host y puerto
echo "Waiting for PostgreSQL ($DB_HOST:$DB_PORT)..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5 # Espera medio segundo antes de reintentar
done

echo "PostgreSQL started!"

# Ejecutar el comando principal (el que estaba en docker-compose)
exec "$@"