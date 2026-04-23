# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**With Docker (recommended):**
```bash
docker-compose up --build -d
docker-compose exec web python manage.py migrate
# App: http://localhost:8000 | Admin: http://localhost:8000/admin
```

**Locally (requires PostgreSQL + PostGIS):**
```bash
# Create .env with DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DEBUG, SECRET_KEY, ALLOWED_HOSTS
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py migrate
python manage.py runserver
```

**Common Django commands (Docker):**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test mapviewer
```

## Architecture

Single Django app (`mapviewer`) with `config/` holding project settings.

**Data flow:**
- Raw geospatial CO2 data lives in `data/raw/` and `data/processed/` (CSVs and JSON)
- `mapviewer/utils/mapas.py` reads these files directly from disk (relative paths) and renders interactive Folium maps as HTML strings returned to templates
- `mapviewer/utils/tablas.py` generates HTML tables for the data sources view
- Views inject the rendered HTML into templates — maps are never saved to disk

**Key models (`mapviewer/models.py`):**
- `CO2Measurement` — stores CO2 readings with UTM coordinates + a PostGIS `PointField` (SRID 4326); the `location` field is auto-populated from `latitude`/`longitude` on `save()`
- `UserProfile` — extends Django's `User` 1:1 (auto-created via `post_save` signal)

**Database:** PostGIS (PostgreSQL + spatial extension). The engine is `django.contrib.gis.db.backends.postgis`, so GDAL must be available. In Docker, the `postgis/postgis:15-3.4` image is used.

**Map tile options** (used in `generar_mapa_html` and `generar_mapas_individuales`): OpenStreetMap, Esri.WorldImagery (satellite), OpenTopoMap (relief). CO2 marker color in `ficha_tecnica` is determined by `asignar_color_emision()` thresholds in `mapas.py`.

**Static files:** Served via WhiteNoise middleware. During development, static files are sourced from `mapviewer/static/mapviewer/`. Run `collectstatic` before deploying.

**URL structure:**
- `/` — landing page
- `/inventario_nacional/` — national map (reads `data/processed/grafico_nacional.json`)
- `/ficha_tecnica/` — per-location CO2 map (reads `data/processed/P_<Ubicacion>LatLon.csv`)
- `/fuentes_info/` — data sources table
- `/login/`, `/register/`, `/logout/`, `/profile/` — auth views

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `DEBUG` | `False` | Django debug mode |
| `SECRET_KEY` | hardcoded insecure key | Override in production |
| `DB_NAME/USER/PASSWORD/HOST/PORT` | `co2_visualizador`/`postgres`/`postgres123`/`localhost`/`5432` | PostgreSQL connection |
| `ALLOWED_HOSTS` | `*` | Comma-separated hosts |
| `PORT` | `8080` | Internal app port (Docker maps 8080→8000) |
