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
- `mapviewer/utils/mapas.py` reads these files from `data/processed/` and builds the Folium maps (`mapa_nacional()`, `mapa_zona()`)
- `mapviewer/utils/tablas.py` generates the data for the data sources table
- Maps are embedded inline (no iframe): `mapas.py` splits the Folium figure into `header` (goes in `{% block head_extra %}`), `html` and `script`, plus a `config` dict rendered with `json_script` — maps are never saved to disk

**Maps:** base layers are Esri World Light/Dark Gray Canvas («Mapa», follows the theme; CARTO now requires an API key), Esri.WorldImagery («Satélite») and Esri.WorldShadedRelief («Relieve»). Measurement points are `CircleMarker`s colored/sized by `design.flux_class()` (log classes 1–5); zones are `DivIcon` ZoneMarkers in a `MarkerCluster`. `static/mapviewer/js/map_controls.js` turns the LayerSwitcher/MapControls/FluxLegend partials into Leaflet controls, switches layers without reloading (keeps `?tipo_mapa=`), and handles theme, hover and selection states; `static/mapviewer/css/map.css` restyles Leaflet with tokens.

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
| `SECRET_KEY` | — (required when `DEBUG=False`; dev-only fallback when `DEBUG=True`) | Django secret key; in Cloud Run use Secret Manager |
| `ALLOWED_HOSTS` | `.run.app,localhost,127.0.0.1,0.0.0.0` | Comma-separated hosts |
| `CSRF_TRUSTED_ORIGINS` | `https://*.run.app` | Comma-separated origins (add a custom domain here) |
| `LOG_LEVEL` | `INFO` | Root logging level |
| `PORT` | `8080` | Port gunicorn binds to (set by Cloud Run; Docker Compose maps 8080→8000) |

`.env` is for local development only: `.dockerignore`/`.gcloudignore` keep it out of the image. Deployment target is Google Cloud Run (see `EJECUCION.md`); `requirements.txt` only lists what the code imports.


## Diseño (DIFUSCO₂)

- La fuente de verdad visual es `design_handoff/design-system/` (README.md, Mapas.md, tokens.json). El plan de implementación está en `design_handoff/HANDOFF.md`.
- Colores, espacios y radios siempre con `var(--token)` de `static/mapviewer/css/tokens.css`. En Python/Folium, importa `mapviewer/design.py`; nunca escribas hex sueltos.
- Fuentes: Source Serif 4 (títulos), IBM Plex Sans (texto), IBM Plex Mono (datos). CO₂ con subíndice Unicode; no usar MathJax.
- Clases de flujo por décadas (<1, 1–10, 10–100, 100–1000, ≥1000 g m⁻² d⁻¹) → `flux-1…5`. El color se reserva para los datos.
- Los componentes usan clases `dx-*` (`static/mapviewer/css/components.css`) y partials en `templates/mapviewer/components/`.
