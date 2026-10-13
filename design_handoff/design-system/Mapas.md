# Mapas

Esta sección define cómo se distribuyen los mapas del sitio, qué controles llevan y cómo se dibujan los puntos. Parte de una revisión del sitio actual, hecha el 11 de octubre de 2026.

## Diagnóstico del sitio actual

| Página | Qué hay | Problema |
|---|---|---|
| Inventario Nacional | Mapa Folium (OSM) con 7 marcadores `AwesomeMarkers` negros con icono de fuego | El color no codifica nada aunque la leyenda dice Bajo/Medio/Alto. Los marcadores no tienen nombre, conteo ni enlace a su ficha. |
| Ficha técnica | Mismo mapa nacional (zoom 5, centro 18.5, −100) con 23 marcadores de la zona elegida | Los 23 puntos de Alcaparrosa caben en ~100 × 40 m y a zoom 5 se ven como **un solo pin**. El tooltip dice "Valor medido: 11.4", sin unidad. No hay estadísticas. |
| Ambas | Capas en un `<select>` que recarga la página; aparece el texto "Make this Notebook Trusted…" | Recargar para cambiar el mapa base es lento, y el texto residual de Folium se ve poco profesional. |

**Dato clave para el diseño:** en Alcaparrosa el flujo va de **0.37 a 5 190**, casi cuatro órdenes de magnitud. Una escala lineal Bajo/Medio/Alto pintaría 20 de 23 puntos de "Bajo". Por eso las clases son **logarítmicas, por décadas**: `< 1`, `1–10`, `10–100`, `100–1000` y `≥ 1000` g m⁻² d⁻¹. Con los datos reales de Alcaparrosa la distribución por clase queda 1 · 11 · 6 · 3 · 2. (La unidad g m⁻² d⁻¹ es una suposición: confírmala con tu tutor.)

## Jerarquía: tres escalas, tres mapas

1. **Portada: mapa testigo.** Un mapa estático, sin interacción, con las 7 zonas. Funciona como invitación a explorar y lleva el botón primario "Explorar el mapa".
2. **Inventario Nacional: escala país.** Mapa a pantalla completa del área de contenido. Cada zona es un **ZoneMarker**: una etiqueta con el nombre, el número de puntos y un punto del color de su clase mediana. A la izquierda va un panel flotante con **ZoneList**. Al hacer clic en una zona, el mapa hace `flyTo` y aparece un MapPopup con resumen y enlace a la ficha.
3. **Ficha técnica: escala sitio (decenas de metros).** El mapa se encuadra solo con `fit_bounds` en los puntos de la zona. Cada medición es un **FluxMarker**. El mapa comparte la pantalla con un panel de datos.

## Distribución por página

### Inventario Nacional (escritorio ≥ 1024px)

```
┌ sidebar ┬──────────────────────────────────────────────────────┐
│         │ PageHeader compacto (eyebrow + h1 + 1 línea)         │
│         ├──────────────────────────────────────────────────────┤
│         │ ┌ZoneList──┐                   [Mapa|Satélite|Rel.] │
│         │ │ 7 zonas  │      ZoneMarkers                 [+ −] │
│         │ │ …        │                                  [⤢ ⛶] │
│         │ └──────────┘                                         │
│         │ escala                        [FluxLegend] atribución│
└─────────┴──────────────────────────────────────────────────────┘
```

- El mapa ocupa `calc(100vh − encabezado)` con un mínimo de 520px y va dentro de una tarjeta `radius-lg`.
- Los controles flotan a `map-inset` (16px) del borde: LayerSwitcher arriba a la derecha y MapControls debajo. La FluxLegend va abajo a la derecha en el inventario, porque la izquierda la ocupa ZoneList, y abajo a la izquierda en la ficha. La escala gráfica va en la esquina libre y la atribución abajo a la derecha.
- ZoneList va en un panel de 280px arriba a la izquierda y es colapsable.

### Ficha técnica (escritorio)

```
┌ sidebar ┬───────────────────────────────┬──────────────────────┐
│         │ PageHeader: "Alcaparrosa" + selector de zona + CSV   │
│         ├───────────────────────────────┼──────────────────────┤
│         │ MAPA (fit_bounds a la zona)    │ 3 StatTiles          │
│         │ FluxMarkers por clase          │ (n · mediana · máx.) │
│         │ [Mapa|Sat.|Rel.]        [+ −]  │ Histograma por clase │
│         │ FluxLegend                     │ Nota metodológica    │
│         ├───────────────────────────────┴──────────────────────┤
│         │ DataTable de mediciones (id, lat, lon, flujo, clase) │
└─────────┴──────────────────────────────────────────────────────┘
```

- Proporción mapa/panel de 3:2. El panel tiene 400px fijos y el mapa ocupa el resto.
- Pasar el cursor por una fila de la tabla resalta su marcador (`is-hover`), y hacer clic en un marcador resalta su fila. Así el dato nunca depende solo del color.

### Móvil (< 768px)

El contenido se apila: encabezado → mapa (60vh) → panel → tabla. La ZoneList pasa a un `<select>` nativo encima del mapa. MapControls conserva solo zoom y encuadre, y la leyenda se vuelve compacta (solo la barra y las etiquetas de los extremos).

## Controles del mapa

| Control | Componente | Posición | Comportamiento |
|---|---|---|---|
| Mapa base | LayerSwitcher (Mapa · Satélite · Relieve) | arriba-derecha | Cambia la capa **sin recargar** (`L.control.layers` con estilo propio, o JS que llama `setUrl`). |
| Zoom | MapControls: + / − | derecha, debajo | Mismo comportamiento que Leaflet. |
| Encuadrar | MapControls: encuadrar | derecha | `fitBounds` a la zona (ficha) o al país (inventario). |
| Pantalla completa | MapControls: expandir | derecha | Plugin `Fullscreen` de Folium. |
| Medir | MapControls: regla | derecha (solo ficha) | Plugin `MeasureControl`, útil para distancias entre puntos. |
| Descarga | Button `secondary` con icono | encabezado de ficha | CSV de la zona. |

**Mapas base recomendados:** CartoDB Positron (Mapa, claro), CartoDB Dark Matter (tema oscuro), Esri World Imagery (Satélite) y Esri World Shaded Relief u OpenTopoMap (Relieve). Son neutros y no compiten con la escala de flujo.

## Marcadores

| Marcador | Dónde | Forma | Estados |
|---|---|---|---|
| **FluxMarker** | Ficha técnica, 1 por medición | Círculo con relleno `flux-n` y radio por clase (`marker-r-1` … `-5`: 5 → 11px) y contorno de 1px `map-stroke` (1.5px blanco sobre Satélite) | default · hover (+1.5px, contorno de 2px) · seleccionado (anillo `marker-selected`) · atenuado (35%, cuando hay filtro) · sin dato (blanco con contorno punteado) |
| **ZoneMarker** | Inventario Nacional, 1 por zona | Etiqueta tipo píldora (punto de color + nombre + nº de puntos) con tallo y ancla en la coordenada | default · seleccionado (fondo `unam-blue`) |
| **ClusterMarker** | Cuando hay > 50 puntos visibles a zoom bajo | Disco blanco con anillo del color de la clase mediana y el conteo en mono | — |

Reglas:

- **Color + tamaño:** la clase se codifica dos veces, para que se lea en impresión y con daltonismo.
- Los puntos se dibujan en orden ascendente de flujo, así los valores altos quedan encima.
- No se usan iconos de fuego, gotas ni pins genéricos. El punto *es* el dato.
- El **tooltip** (hover) muestra valor + unidad. El **popup** (clic) es un MapPopup con valor, clase, coordenadas, fecha, método y enlace.

## Implementación en Folium

```python
import folium
from folium.plugins import Fullscreen, MeasureControl

FLUX = ["#F4E08A", "#E9A23F", "#D2662A", "#A8321F", "#6E1A25"]
RADII = [5, 6, 7, 9, 11]
def clase(v):  # décadas: <1, 1–10, 10–100, 100–1000, ≥1000
    return 0 if v < 1 else 1 if v < 10 else 2 if v < 100 else 3 if v < 1000 else 4

m = folium.Map(tiles="CartoDB positron", control_scale=True, zoom_control=False)
for p in sorted(puntos, key=lambda p: p.flujo):
    c = clase(p.flujo)
    folium.CircleMarker(
        [p.lat, p.lon], radius=RADII[c], weight=1, color="#14213D",
        fill=True, fill_color=FLUX[c], fill_opacity=1,
        tooltip=f"{p.flujo:,.2f} g m⁻² d⁻¹",
        popup=folium.Popup(render_to_string("mapviewer/_popup.html", {"p": p}), max_width=260),
    ).add_to(m)
m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]], padding=(40, 40))
Fullscreen(position="topright").add_to(m)
MeasureControl(position="topright", primary_length_unit="meters").add_to(m)
html = m.get_root().render()   # evita "Make this Notebook Trusted…" de _repr_html_
```

Los estilos de los controles (`.leaflet-bar`, `.leaflet-control-layers`, `.leaflet-popup-content-wrapper`) se reemplazan con las clases `dx-` de este sistema en `static/mapviewer/css/map.css`, que se inyecta en el HTML del mapa con `m.get_root().header.add_child(folium.CssLink(...))`.
