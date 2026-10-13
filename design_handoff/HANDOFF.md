# HANDOFF — Rediseño DIFUSCO₂ (Django)

> Documento para Claude Code. Léelo completo antes de tocar código. La **fuente de verdad del diseño** está en `design_handoff/design-system/`. Este archivo dice **qué** cambiar, **en qué orden** y **cómo verificarlo**.

## 0. Contexto

- El proyecto es un sitio Django (`mapviewer`) que visualiza emisiones naturales difusas de CO₂ medidas en zonas geotérmicas y volcánicas de México. Es para el Instituto de Geofísica de la UNAM y es el proyecto de titulación de Oscar, así que debe verse **institucional y académico**.
- Hoy usa Bootstrap 5.3, Montserrat/Roboto, el acento turquesa `#38B2AC`, Font Awesome y mapas Folium con `AwesomeMarkers`, además de MathJax para escribir "CO₂".
- Páginas y rutas: `/` (Inicio), `/inventario_nacional/`, `/ficha_tecnica/`, `/fuentes_info/`, `/acerca_de/` y `/ayuda_y_contacto/`.
- Estáticos actuales: `static/mapviewer/css/style.css` y `static/mapviewer/js/{theme_toggle,sidebar_toggle,map_controls,ficha_tecnica_controls}.js`.
- El tema oscuro se activa con `[data-theme="dark"]` (en `theme_toggle.js`). **Hay que conservar ese mecanismo.**

## 1. Archivos de referencia (léelos en este orden)

| Archivo | Qué contiene |
|---|---|
| `design-system/README.md` | Guía de marca: principios, voz, color, tipografía, composición, accesibilidad |
| `design-system/Mapas.md` | Diagnóstico de los mapas, distribución por página, controles, marcadores y **código Folium** |
| `design-system/tokens.json` | Todos los tokens (fuente de verdad) |
| `design-system/tokens.css` | Los tokens como variables CSS, claro y oscuro (**se copia tal cual**) |
| `design-system/components.css` | CSS de todos los componentes (clases `dx-*`) |
| `design-system/components/*.md` | Guía de uso de cada componente |
| `reference/interactive/components-reference.js` | Implementación de referencia en React: **es la especificación del HTML de cada componente**. Tradúcela a templates de Django; no uses React. |
| `reference/interactive/*.html` | Maquetas abribles en el navegador: Inventario (claro) y Ficha (claro/oscuro) |
| `reference/screens/*.png` | Capturas de cada componente y página en claro/oscuro: **el objetivo visual** |

## 2. Reglas no negociables

1. **Cero valores sueltos.** Todo color, espacio, radio y sombra sale de `var(--token)`. Nada de hex en templates ni en CSS nuevo, salvo dentro de `tokens.css`. La única excepción es Python/Folium, que necesita hex: ahí se definen **una sola vez** en `mapviewer/design.py`, copiados de `tokens.json`.
2. **Tipografía:** Source Serif 4 (títulos y KPIs), IBM Plex Sans (texto) e IBM Plex Mono (coordenadas, unidades y números de tabla). Hay que eliminar Montserrat y Roboto.
3. **CO₂ con subíndice Unicode (₂) en todos lados.** Se **elimina MathJax** y cualquier `$\text{CO}_2$`.
4. **Escala de flujo** `flux-1…5` con clases por décadas: `<1`, `1–10`, `10–100`, `100–1000` y `≥1000` g m⁻² d⁻¹. El **color se reserva para los datos**: la interfaz usa `unam-blue`, `gold`, `ink` y `paper`.
5. **El texto nunca va sobre un relleno `flux-n`.** La clase se muestra como punto de color (`.dx-dot`) junto a texto `ink`.
6. **Accesibilidad:** foco visible (`--focus`), `aria-label` en los botones de icono, `aria-current` en la navegación, contraste AA en ambos temas.
7. **No cambies modelos ni datos** sin preguntar. Si encuentras datos inconsistentes (ver §7), repórtalos y no los "corrijas" por tu cuenta.
8. **Conserva el comportamiento existente:** rutas, vistas, filtros por GET, el toggle de tema y el colapso del sidebar.

## 3. Plan por fases

Trabaja **una fase a la vez**. Al terminar cada fase, corre `python manage.py check`, levanta el servidor, revisa las páginas afectadas en claro y oscuro, haz commit y resume lo hecho antes de seguir.

### Fase 1 — Fundaciones
- Crea `static/mapviewer/css/tokens.css` (copia de `design-system/tokens.css`) y `static/mapviewer/css/components.css` (desde `components.css`, **sin** las reglas `body {…}`, `.dx-row` ni `.dx-grid` de preview).
- En `base.html`, carga en este orden: Google Fonts → `tokens.css` → `components.css` → `style.css`. Quita Montserrat/Roboto y MathJax. Decide si Bootstrap sigue: puede quedarse solo para el grid/utilidades, pero ningún estilo visual de Bootstrap (botones, form-select, colores) puede verse.
- Reescribe `style.css`: borra el sistema de variables viejo (`--accent`, `--bg-*`, etc.) y usa los tokens nuevos. Fondo `--paper`, sidebar `--surface` y texto `--ink`.
- Crea `mapviewer/design.py` con `FLUX_COLORS`, `FLUX_RADII`, `FLUX_THRESHOLDS`, `FLUX_LABELS`, `FLUX_NAMES`, `MAP_STROKE` y la función `flux_class(v)`, todos copiados de tokens.json o Mapas.md.
- **Verificación:** no queda ningún `#38B2AC`, `Montserrat`, `Roboto` ni `mathjax` en el repo (`grep -ri`).

### Fase 2 — Layout y navegación
- Sidebar (`--sidebar-width` 264px): wordmark **DIFUSCO₂** en Source Serif 4 600, color `--unam-blue`, con el ₂ en `--gold-ink`. Debajo va la navegación con el patrón **NavItem** (`.dx-nav`, `.is-active` + `aria-current="page"`). Corrige el texto «Catalogo» → «Catálogo».
- Encabezado de cada página con el patrón **PageHeader** (`.dx-eyebrow`, `.dx-h1`, `.dx-lead`, `.dx-rule`).
- Pie de página ligero: `--surface-sunken`, texto `caption`, logos UNAM e IGEF a 40px, cita sugerida, licencia y fecha de actualización.
- Crea template partials en `templates/mapviewer/components/`: `page_header.html`, `nav_item.html`, `stat_tile.html`, `badge.html`, `flux_legend.html`, `zone_list.html`, `map_popup.html`, `histogram.html` y `data_table.html`. Cada uno traduce exactamente el HTML que genera `components-reference.js`, con sus clases `dx-*`.
- Si la lógica de clase/formato se repite, agrega template tags en `mapviewer/templatetags/difusco.py` (`flux_class`, `format_flux`, `flux_name`). `format_flux` usa espacio duro como separador de miles: `5 190`.

### Fase 3 — Mapas (lo más importante; sigue `Mapas.md` al pie de la letra)
- **Generación Folium:**
  - Pasa a `tiles=None` + capas `TileLayer` para Mapa (CartoDB Positron), Satélite (Esri World Imagery) y Relieve (Esri World Shaded Relief). En tema oscuro, Mapa = CartoDB Dark Matter.
  - Usa `zoom_control=False` y `control_scale=True`.
  - Renderiza con `m.get_root().render()` para que desaparezca "Make this Notebook Trusted…".
  - Inyecta `tokens.css` + `map.css` en el HTML del mapa (`folium.CssLink` o `get_root().header.add_child`).
- **Puntos de medición (Ficha):** `folium.CircleMarker` con relleno `FLUX_COLORS[c]`, radio `FLUX_RADII[c]`, `weight=1`, `color=MAP_STROKE` y `fill_opacity=1`, **ordenados de menor a mayor flujo**. El tooltip lleva el valor con unidad y el popup reproduce el componente **MapPopup**.
- **Zonas (Inventario):** `folium.Marker` con `folium.DivIcon` y el HTML de **ZoneMarker** (`.dx-zm`). Cuando haya superposición, usa `MarkerCluster` con un `icon_create_function` que genere **ClusterMarker** (`.dx-cm`).
- **Encuadre:** en la Ficha, `fit_bounds` a los puntos de la zona con padding de 40px; en el Inventario, encuadre a todas las zonas.
- **Controles:**
  - **LayerSwitcher** segmentado (`.dx-seg`) arriba a la derecha; cambia la capa **sin recargar la página** (JS + `postMessage` al iframe, o se mueve el control dentro del HTML de Folium).
  - **MapControls** (`.dx-mapctl`) debajo: zoom ±, encuadrar, pantalla completa (`folium.plugins.Fullscreen`) y, solo en Ficha, medir (`MeasureControl`). Restiliza `.leaflet-bar`, `.leaflet-control-*` y `.leaflet-popup-*` con las reglas `dx-` en `static/mapviewer/css/map.css`.
- **Leyenda:** **FluxLegend** (`.dx-legend`) flotante; en la Ficha va abajo a la izquierda y en el Inventario abajo a la derecha.
- Sustituye los `<select>` de capa por el LayerSwitcher. El selector de zona puede seguir siendo un `<select>`, pero con el estilo del sistema.

### Fase 4 — Páginas
- **Inventario Nacional** (`reference/screens/InventarioLayout_*.png`): PageHeader compacto (sin filete) y mapa a todo el ancho del contenido, con altura `calc(100vh - header)` y mínimo de 520px. Encima del mapa, panel flotante ZoneList (264px) arriba a la izquierda. Al hacer clic en una zona se hace `flyTo` y se abre el MapPopup con el enlace a `/ficha_tecnica/?ubicacion=<zona>`.
- **Ficha técnica** (`reference/screens/FichaLayout_*.png`):
  - Encabezado con eyebrow «Ficha técnica · <Estado>», `h1` con el nombre de la zona, selector de zona y botón «Descargar CSV» con el icono `download`. Si el CSV no existe, crea la vista y pregunta antes de agregar la URL.
  - Grid de dos columnas: mapa `1fr` + panel de 380px. El panel lleva 3 StatTile compactos (Puntos, Mediana, Máximo), el Histograma por clase y la Nota metodológica (`--gold-tint`).
  - Debajo va la DataTable de mediciones (Punto, Latitud, Longitud, Flujo, Clase). Las coordenadas van con 5 decimales y signo menos tipográfico «−».
  - Calcula las estadísticas en la vista (Python), no en JS.
- **Inicio:** PageHeader `display`, fila de StatTiles (zonas, puntos totales, rango de flujo), mapa testigo estático y botón primario «Explorar el mapa».
- **Fuentes de información:** DataTable del catálogo + bibliografía. Corrige el LaTeX sin renderizar.
- **Acerca de / Ayuda y contacto:** PageHeader + texto a `--measure`; el formulario usa `.dx-btn-primary` y campos con borde `--line-strong`.

### Fase 5 — Responsivo y pulido
- En < 768px: el sidebar se vuelve menú colapsable; el orden es encabezado → mapa (60vh) → panel → tabla; ZoneList pasa a `<select>`; MapControls muestra solo zoom y encuadrar; la leyenda queda compacta.
- Revisa todas las páginas en claro y oscuro y compáralas con las capturas de `reference/screens/`.

## 4. Mapeo de componentes → Django

| Componente | Dónde vive | Implementación |
|---|---|---|
| PageHeader, NavItem, Button, Badge, StatTile, DataTable | `templates/mapviewer/components/*.html` | `{% include %}` con `with` |
| FluxLegend, ZoneList, Histogram | `components/*.html` | Histograma en SVG generado en el template, con datos de la vista |
| LayerSwitcher, MapControls | Dentro del HTML de Folium o superpuestos al iframe | JS mínimo en `map_controls.js` |
| FluxMarker | `folium.CircleMarker` | Estilos de `design.py` |
| ZoneMarker, ClusterMarker | `folium.DivIcon` / `MarkerCluster` | HTML con clases `dx-zm` / `dx-cm` |
| MapPopup | `templates/mapviewer/components/map_popup.html` | `render_to_string` → `folium.Popup` |
| MapCanvas | — | **Solo para previews; no se implementa** |

## 5. Criterios de aceptación

- [ ] Todas las páginas cargan sin errores de consola, en claro y en oscuro.
- [ ] No queda Montserrat/Roboto/MathJax/turquesa/AwesomeMarkers/icono de fuego.
- [ ] En la Ficha de Alcaparrosa se distinguen los **23 puntos** al cargar, con su clase correcta (distribución 1 · 11 · 6 · 3 · 2).
- [ ] Los tooltips y popups muestran la unidad g m⁻² d⁻¹.
- [ ] Cambiar entre Mapa/Satélite/Relieve no recarga la página.
- [ ] No aparece el texto "Make this Notebook Trusted…".
- [ ] La navegación por teclado muestra el foco en sidebar, botones, controles de mapa y LayerSwitcher.
- [ ] El resultado se parece a `reference/screens/*` (layout, jerarquía, colores y tipografía).

## 6. Forma de trabajo

- Antes de la Fase 1, explora el repo y presenta un **plan con los archivos que vas a tocar**. Espera aprobación.
- Haz un commit por fase, con mensajes en español: `feat(diseño): fase 1 — tokens y tipografía`.
- Si algo del diseño no se puede hacer igual en Folium/Django, propón la alternativa más cercana y pregunta. **No improvises estilos nuevos.**

## 7. Pendientes de datos (no corregir sin confirmar con Oscar)

- **Michoa:** su longitud es −96.30 (Veracruz), pero el estado dice "Michoacán".
- **Alcaparrosa y Azufres:** tienen coordenadas en la zona de Acoculco, Puebla, pero el estado registrado es "Alcaparrosa" y "Los Azufres".
- La unidad de flujo (g m⁻² d⁻¹) y el método (cámara de acumulación) están **por confirmar**. Déjalos configurables en `design.py`.
- El teléfono y el email de contacto son de relleno.
