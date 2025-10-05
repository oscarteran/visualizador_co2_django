# 🚀 Guía de Ejecución - Visualizador CO2 Django

## Requisitos Previos

- Docker Desktop instalado y funcionando
- Docker Compose v2.0+
- Git (para clonar el repositorio)

## Configuración de la Base de Datos

Este proyecto utiliza **PostgreSQL** como base de datos principal, configurado con Docker Compose.

### Características de la Base de Datos:
- **Motor**: PostgreSQL 15
- **Nombre**: `co2_visualizador`
- **Usuario**: `postgres`
- **Contraseña**: `postgres123`
- **Puerto**: `5432`
- **Persistencia**: Los datos se mantienen entre reinicios

## 🐳 Ejecución con Docker (Recomendado)

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd visualizador_co2_django
```

### 2. Levantar los Servicios
```bash
# Construir y levantar todos los servicios (PostgreSQL + Django)
docker-compose up --build -d
```

### 3. Ejecutar Migraciones
```bash
# Crear las tablas en PostgreSQL
docker-compose exec web python manage.py migrate
```

### 4. Crear Superusuario (Opcional)
```bash
# Crear usuario administrador para acceder al panel de admin
docker-compose exec web python manage.py createsuperuser
```

### 5. Acceder a la Aplicación
- **Aplicación Web**: http://localhost:8000
- **Panel de Admin**: http://localhost:8000/admin
- **Base de Datos**: localhost:5432

## 🔧 Comandos Útiles

### Gestión de Servicios
```bash
# Ver estado de los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f db

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ CUIDADO: Elimina datos)
docker-compose down -v
```

### Comandos Django
```bash
# Ejecutar comandos Django dentro del contenedor
docker-compose exec web python manage.py <comando>

# Ejemplos:
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py makemigrations
```

### Acceso a la Base de Datos
```bash
# Conectar directamente a PostgreSQL
docker-compose exec db psql -U postgres -d co2_visualizador

# O desde tu máquina local (si tienes psql instalado)
psql -h localhost -p 5432 -U postgres -d co2_visualizador
```

## 🛠️ Desarrollo Local (Sin Docker)

### 1. Instalar PostgreSQL
- Instalar PostgreSQL 15+ en tu sistema
- Crear base de datos: `co2_visualizador`
- Crear usuario: `postgres` con contraseña: `postgres123`

### 2. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
DB_NAME=co2_visualizador
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### 3. Instalar Dependencias
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
```bash
# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Levantar servidor
python manage.py runserver
```

## 📊 Estructura de la Base de Datos

La aplicación utiliza las siguientes tablas principales:
- `auth_user` - Usuarios del sistema
- `auth_group` - Grupos de usuarios
- `django_session` - Sesiones de usuario
- `django_content_type` - Tipos de contenido
- `django_migrations` - Historial de migraciones

## 🔍 Solución de Problemas

### Error de Conexión a la Base de Datos
```bash
# Verificar que PostgreSQL esté funcionando
docker-compose logs db

# Reiniciar solo el servicio de base de datos
docker-compose restart db
```

### Error de Migraciones
```bash
# Verificar estado de migraciones
docker-compose exec web python manage.py showmigrations

# Aplicar migraciones específicas
docker-compose exec web python manage.py migrate <app_name>
```

### Limpiar Todo y Empezar de Nuevo
```bash
# Detener servicios
docker-compose down

# Eliminar volúmenes y contenedores
docker-compose down -v --remove-orphans

# Eliminar imágenes
docker-compose down --rmi all

# Volver a construir
docker-compose up --build -d
```

## 📝 Notas Importantes

- Los datos de PostgreSQL se almacenan en un volumen persistente
- El puerto 8000 debe estar libre para la aplicación web
- El puerto 5432 debe estar libre para PostgreSQL
- Para producción, cambiar las credenciales por defecto
- El archivo `.env` no debe subirse al repositorio (está en `.gitignore`)

## 🆘 Soporte

Si encuentras problemas:
1. Verificar que Docker esté funcionando: `docker --version`
2. Revisar logs: `docker-compose logs`
3. Verificar puertos disponibles: `netstat -an | findstr :8000`
4. Reiniciar Docker Desktop si es necesario
