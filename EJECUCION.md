# 🚀 Guía de Ejecución - Visualizador CO2 Django

La aplicación **no usa base de datos**: los mapas y tablas se generan a partir de los archivos CSV/JSON en `data/processed/`. Solo necesitas Python (o Docker).

## 🛠️ Ejecución local (recomendada)

### 1. Crear y activar el entorno virtual
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. (Opcional) Archivo `.env`
```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### 4. Levantar el servidor
```bash
python manage.py runserver
```
Aplicación: http://localhost:8000

## 🐳 Ejecución con Docker

```bash
docker-compose up --build -d   # construir y levantar
docker-compose logs -f web     # ver logs
docker-compose down            # detener
```
Aplicación: http://localhost:8000

## ☁️ Despliegue en Google Cloud Run (desde la consola)

La imagen se construye con el `Dockerfile` del repositorio (Python 3.13 + gunicorn en `$PORT`).
El archivo `.env` **no** entra en la imagen: las variables se definen en el servicio.

### 1. Crear la clave secreta (una sola vez)
1. Generar un valor aleatorio, por ejemplo:
   `python -c "import secrets; print(secrets.token_urlsafe(50))"`
2. Consola → **Security → Secret Manager → Create secret**: nombre `difusco-secret-key`, valor = la clave generada.

### 2. Crear el servicio
Consola → **Cloud Run → Deploy container → Service** → *Continuously deploy from a repository*
(conectar el repositorio de GitHub, rama `main`, **Build type: Dockerfile**, ruta `/Dockerfile`).

- **Authentication:** *Allow unauthenticated invocations* (así la URL es pública).
- **Container(s) → Settings:** puerto `8080`, memoria **1 GiB**, CPU 1.
- **Request timeout:** 300 s (gunicorn usa 120 s; debe ser mayor o igual).
- **Variables & Secrets:**
  | Nombre | Valor |
  |---|---|
  | `DEBUG` | `False` |
  | `SECRET_KEY` | *Reference a secret* → `difusco-secret-key`, versión `latest` |

  `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` ya aceptan `*.run.app` por defecto; solo hay que
  definirlos si se usa un **dominio propio** (p. ej. `ALLOWED_HOSTS=difusco.igeofisica.unam.mx`
  y `CSRF_TRUSTED_ORIGINS=https://difusco.igeofisica.unam.mx`).
- La cuenta de servicio de Cloud Run necesita el rol **Secret Manager Secret Accessor** sobre el secreto.

Al terminar, Cloud Run muestra la URL pública (`https://difusco2-…-uc.a.run.app`).

### Alternativa desde la terminal
```bash
gcloud run deploy difusco2 --source . --region us-central1 \
  --allow-unauthenticated --memory 1Gi --timeout 300 \
  --set-env-vars DEBUG=False \
  --set-secrets SECRET_KEY=difusco-secret-key:latest
```
(`.gcloudignore` evita subir `venv/`, `.env` y el material de desarrollo.)

## 📊 Datos

| Página | Archivo que lee |
|---|---|
| `/inventario_nacional/` | `data/processed/grafico_nacional.json` |
| `/ficha_tecnica/` | `data/processed/P_<Ubicacion>LatLon.csv` |
| `/fuentes_info/` | `grafico_nacional.json`, los CSV y `data/raw/Catalogo_de_datos_CO2_Jacome_Paz_2020.xlsx` |

Para actualizar los mapas basta con reemplazar estos archivos; no hay migraciones ni carga de datos.

## 📝 Notas

- El puerto 8000 debe estar libre.
- Con `DEBUG=False` la variable `SECRET_KEY` es obligatoria: sin ella el servicio no arranca
  (mensaje «Falta la variable de entorno SECRET_KEY»).
