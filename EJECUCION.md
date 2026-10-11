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

## 📊 Datos

| Página | Archivo que lee |
|---|---|
| `/inventario_nacional/` | `data/processed/grafico_nacional.json` |
| `/ficha_tecnica/` | `data/processed/P_<Ubicacion>LatLon.csv` |
| `/fuentes_info/` | tabla definida en `mapviewer/utils/tablas.py` |

Para actualizar los mapas basta con reemplazar estos archivos; no hay migraciones ni carga de datos.

## 📝 Notas

- El puerto 8000 debe estar libre.
- Para producción, define `SECRET_KEY` y `DEBUG=False`.
