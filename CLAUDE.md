# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**Locally (recommended, no database needed):**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver
# App: http://localhost:8000
```

**With Docker:**
```bash
docker-compose up --build -d
# App: http://localhost:8000
```

## Architecture

Single Django app (`mapviewer`) with `config/` holding project settings. **There is no database** (`DATABASES = {}`) and no auth/admin/sessions apps — Django is used only to render templates and maps.

**Data flow:**
- Raw geospatial CO2 data lives in `data/raw/` and `data/processed/` (CSVs and JSON)
- `mapviewer/utils/mapas.py` reads these files directly from disk (relative paths) and renders interactive Folium maps as HTML strings returned to templates
- `mapviewer/utils/tablas.py` generates the data for the data sources table
- Views inject the rendered HTML into templates — maps are never saved to disk

**Map tile options** (used in `generar_mapa_html` and `generar_mapas_individuales`): OpenStreetMap, Esri.WorldImagery (satellite), OpenTopoMap (relief). CO2 marker color in `ficha_tecnica` is determined by `asignar_color_emision()` thresholds in `mapas.py`.

**Static files:** Served via WhiteNoise middleware. During development, static files are sourced from `mapviewer/static/mapviewer/`. Run `collectstatic` before deploying.

**URL structure:**
- `/` — landing page
- `/inventario_nacional/` — national map (reads `data/processed/grafico_nacional.json`)
- `/ficha_tecnica/` — per-location CO2 map (reads `data/processed/P_<Ubicacion>LatLon.csv`)
- `/fuentes_info/` — data sources table
- `/acerca_de/`, `/ayuda_y_contacto/` — static pages

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `DEBUG` | `False` | Django debug mode |
| `SECRET_KEY` | hardcoded insecure key | Override in production |
| `ALLOWED_HOSTS` | `*` | Comma-separated hosts |
| `PORT` | `8080` | Internal app port (Docker maps 8080→8000) |
