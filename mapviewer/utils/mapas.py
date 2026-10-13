"""
Mapas Folium de DIFUSCO₂ (design_handoff/design-system/Mapas.md).

Los mapas se incrustan directamente en la página (sin iframe): Folium arma el
mapa y aquí se separa en tres piezas que la plantilla coloca en su sitio:

- header: <script>/<link> de Leaflet y plugins + map.css (va en <head>)
- html:   el <div> del mapa
- script: el JS que crea el mapa y sus capas (va después del <div>)

Los controles (LayerSwitcher, MapControls, FluxLegend) son partials de Django;
static/mapviewer/js/map_controls.js los convierte en controles de Leaflet y
cambia la capa base sin recargar la página.
"""
import csv
import json
import logging
import re
import statistics
from pathlib import Path

import folium
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from folium.plugins import Fullscreen, MarkerCluster, MeasureControl

from .. import design
from .tablas import tabla_resumen_info

logger = logging.getLogger(__name__)

DATA_DIR = Path(settings.BASE_DIR) / "data" / "processed"
ZONAS_JSON = DATA_DIR / "grafico_nacional.json"

# Zona → archivo CSV con sus mediciones (columnas Lat, Lon, CO2_value).
ARCHIVOS_ZONA = {
    "Acoculco": "P_AcoculcoLatLon.csv",
    "Alcaparrosa": "P_AlcaparrosaLatLon.csv",
    "Azufres": "P_AzufresLatLon.csv",
    "Chichinautzin": "P_ChichinautzinLatLon.csv",
    "Escalera": "P_EscaleraLatLon.csv",
    "Michoa": "P_MichoaLatLon.csv",
    "Puruandiro": "P_PuruandiroLatLon.csv",
}
ZONA_POR_DEFECTO = "Alcaparrosa"

# Capas base (LayerSwitcher). «Mapa» es un fondo neutro gris: claro u oscuro según el tema.
# Mapas.md recomienda CARTO Positron/Dark Matter, pero CARTO ya exige API key (sus
# teselas salen con la marca «API KEY REQUIRED"); se usan los Gray Canvas de Esri,
# sin clave y del mismo proveedor que Satélite y Relieve.
CAPAS = {"mapa": "Mapa", "satelite": "Satélite", "relieve": "Relieve"}
ESRI_CANVAS = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/{}/MapServer/tile/{{z}}/{{y}}/{{x}}"
ESRI_CANVAS_ATTR = "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ"
CAPA_POR_DEFECTO = "mapa"
# Valores de ?tipo_mapa= anteriores al rediseño, para no romper enlaces guardados.
CAPAS_LEGADO = {"División Política": "mapa", "Satelital": "satelite", "Relieve": "relieve",
                "Mapa": "mapa", "Satélite": "satelite"}
TESELAS = {
    "mapa_light": {"tiles": ESRI_CANVAS.format("World_Light_Gray_Base"), "attr": ESRI_CANVAS_ATTR,
                   "max_native_zoom": 16},
    "mapa_dark": {"tiles": ESRI_CANVAS.format("World_Dark_Gray_Base"), "attr": ESRI_CANVAS_ATTR,
                  "max_native_zoom": 16},
    "satelite": {"tiles": "Esri.WorldImagery", "max_native_zoom": 18},
    "relieve": {"tiles": "Esri.WorldShadedRelief", "max_native_zoom": 13},
}
MAX_ZOOM = 21
PADDING_ENCUADRE = 40  # px, fit_bounds

LEAFLET_JS = ("leaflet", "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js")
LEAFLET_CSS = ("leaflet_css", "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css")
JQUERY_JS = ("jquery", "https://code.jquery.com/jquery-3.7.1.min.js")  # lo usa folium.Popup

# Icono de grupo de zonas (ClusterMarker, .dx-cm): diámetro 30/36/44 px según el
# conteo y anillo del color de la clase mediana de las zonas agrupadas.
CLUSTER_ICON_JS = """
function (cluster) {
    var hijos = cluster.getAllChildMarkers();
    var n = hijos.length;
    var clases = hijos.map(function (m) { return m.options.fluxClass || 3; })
                      .sort(function (a, b) { return a - b; });
    var cls = clases[Math.floor((clases.length - 1) / 2)];
    var d = n >= 100 ? 44 : n >= 10 ? 36 : 30;
    var html = '<div class="dx-cm" style="width:' + d + 'px;height:' + d + 'px" role="img" aria-label="' +
        n + ' zonas"><span class="dx-cm-ring dx-flux-' + cls + '"></span><span class="dx-cm-n">' + n + '</span></div>';
    return L.divIcon({html: html, className: 'dx-divicon', iconSize: L.point(d, d)});
}
"""


# ---------- datos ----------

def capa_desde_get(valor):
    """Clave de capa a partir de ?tipo_mapa= (acepta los valores antiguos)."""
    if valor in CAPAS:
        return valor
    return CAPAS_LEGADO.get(valor, CAPA_POR_DEFECTO)


def leer_puntos(zona):
    """Mediciones de una zona con su id de punto (prefijo de la zona + nº de fila)."""
    prefijo = zona[:3].upper()
    with open(DATA_DIR / ARCHIVOS_ZONA[zona], encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return [
        {"id": f"{prefijo}-{i:02d}", "lat": float(r["Lat"]), "lon": float(r["Lon"]),
         "valor": float(r["CO2_value"])}
        for i, r in enumerate(filas, start=1)
    ]


def leer_zonas():
    """Zonas del inventario con coordenadas, entidad, nº de puntos y clase mediana."""
    with open(ZONAS_JSON, encoding="utf-8") as f:
        coordenadas = json.load(f)
    entidades = {fila["Nombre"]: fila["Estado"] for fila in tabla_resumen_info()}
    zonas = []
    for clave, (lat, lon) in coordenadas.items():
        nombre = clave.removeprefix("P_")
        if nombre not in ARCHIVOS_ZONA:
            continue
        valores = [p["valor"] for p in leer_puntos(nombre)]
        mediana = statistics.median(valores)
        zonas.append({
            "name": nombre, "state": entidades.get(nombre, ""), "lat": float(lat), "lon": float(lon),
            "n": len(valores), "median": mediana, "cls": design.flux_class(mediana),
            "href": reverse("ficha_tecnica") + "?ubicacion=" + nombre,
        })
    return zonas


# ---------- mapa base ----------

def _crear_mapa():
    # maxZoom va como opción de L.map: con tiles=None, max_zoom de Folium solo afecta a
    # la capa por defecto y MarkerCluster exige que el mapa lo tenga definido.
    m = folium.Map(location=[23.5, -102], zoom_start=5, tiles=None, zoom_control=False,
                   control_scale=False, maxZoom=MAX_ZOOM)
    # Solo Leaflet (+ jQuery para los popups): sin Bootstrap 3, Font Awesome ni AwesomeMarkers.
    m.default_js = [LEAFLET_JS, JQUERY_JS]
    m.default_css = [LEAFLET_CSS]
    capas = {}
    for clave, conf in TESELAS.items():
        capa = folium.TileLayer(conf["tiles"], attr=conf.get("attr"), name=clave, show=False, control=False,
                                max_zoom=MAX_ZOOM, max_native_zoom=conf.get("max_native_zoom"))
        capa.add_to(m)
        capas[clave] = capa.get_name()
    fs = Fullscreen(position="topright", title="Pantalla completa", title_cancel="Salir de pantalla completa")
    fs.add_to(m)
    return m, capas


def _partes(m):
    """Separa el mapa en header/html/script para incrustarlo en la página."""
    fig = m.get_root()
    fig.render()
    # map.css al final del header para que gane sobre leaflet.css y los plugins.
    fig.header.add_child(folium.CssLink(static("mapviewer/css/map.css")), name="dx_map_css")
    header = fig.header.render()
    # Folium repite <meta> que ya están en base.html; su viewport impide hacer zoom
    # en móvil (user-scalable=no), así que se quitan.
    header = re.sub(r"<meta[^>]*>", "", header)
    return {
        "header": header,
        "html": fig.html.render(),
        "script": "<script>" + fig.script.render() + "</script>",
    }


def _config(m, capas, capa_inicial, bounds, tipo):
    return {
        "map": m.get_name(),
        "layers": capas,
        "initial": capa_inicial,
        "bounds": bounds,
        "padding": PADDING_ENCUADRE,
        "kind": tipo,
        "stroke": design.MAP_STROKE,
        "strokeImagery": design.MAP_STROKE_IMAGERY,
        "selected": design.MARKER_SELECTED,
    }


def _popup(html):
    return folium.Popup(html, max_width=260, class_name="dx-leaflet-popup", close_button=False)


# ---------- mapas por página ----------

def mapa_nacional(capa_inicial=CAPA_POR_DEFECTO):
    """Inventario Nacional: una etiqueta ZoneMarker por zona, agrupadas si se traslapan."""
    zonas = leer_zonas()
    m, capas = _crear_mapa()
    grupo = MarkerCluster(icon_create_function=CLUSTER_ICON_JS, options={
        "showCoverageOnHover": False, "spiderfyOnMaxZoom": True, "maxClusterRadius": 60})
    grupo.add_to(m)
    for z in zonas:
        icono = folium.DivIcon(html=render_to_string("mapviewer/components/zone_marker.html", {"z": z}),
                               class_name="dx-divicon", icon_size=(0, 0), icon_anchor=(0, 0))
        popup = render_to_string("mapviewer/components/map_popup.html", {
            "zone": f"{z['name']} · mediana", "id": f"{z['n']} pts", "value": z["median"],
            "coords": f"{design.format_coord(z['lat'])}, {design.format_coord(z['lon'])}",
            "method": design.MEASUREMENT_METHOD, "href": z["href"],
        })
        folium.Marker([z["lat"], z["lon"]], icon=icono, popup=_popup(popup),
                      flux_class=z["cls"], zone_name=z["name"]).add_to(grupo)
    lats = [z["lat"] for z in zonas]
    lons = [z["lon"] for z in zonas]
    bounds = [[min(lats), min(lons)], [max(lats), max(lons)]]
    m.fit_bounds(bounds, padding=(PADDING_ENCUADRE, PADDING_ENCUADRE))
    partes = _partes(m)
    partes["config"] = _config(m, capas, capa_inicial, bounds, "nacional")
    partes["config"]["cluster"] = grupo.get_name()
    partes["zonas"] = zonas
    return partes


def mapa_zona(zona, capa_inicial=CAPA_POR_DEFECTO):
    """Ficha técnica: un FluxMarker (CircleMarker) por medición, encuadrado en la zona."""
    puntos = leer_puntos(zona)
    m, capas = _crear_mapa()
    # Medición de distancias: el botón «Medir» de MapControls maneja este plugin;
    # su control propio se oculta en map.css.
    medir = MeasureControl(position="topright", primary_length_unit="meters", secondary_length_unit=None,
                           primary_area_unit="sqmeters", secondary_area_unit=None, localization="es")
    medir.add_to(m)
    # Orden ascendente: los valores altos quedan encima.
    for p in sorted(puntos, key=lambda p: p["valor"]):
        c = design.flux_class(p["valor"])
        coords = f"{design.format_coord(p['lat'])}, {design.format_coord(p['lon'])}"
        popup = render_to_string("mapviewer/components/map_popup.html", {
            "zone": zona, "id": p["id"], "value": p["valor"], "coords": coords,
            "method": design.MEASUREMENT_METHOD,
        })
        folium.CircleMarker(
            [p["lat"], p["lon"]], radius=design.FLUX_RADII[c], weight=1,
            color=design.MAP_STROKE["light"], fill=True, fill_color=design.FLUX_COLORS[c], fill_opacity=1,
            tooltip=folium.Tooltip(f"{design.format_flux(p['valor'])} {design.FLUX_UNIT}",
                                   class_name="dx-leaflet-tooltip", sticky=False),
            popup=_popup(popup),
        ).add_to(m)
    lats = [p["lat"] for p in puntos]
    lons = [p["lon"] for p in puntos]
    bounds = [[min(lats), min(lons)], [max(lats), max(lons)]]
    m.fit_bounds(bounds, padding=(PADDING_ENCUADRE, PADDING_ENCUADRE))
    partes = _partes(m)
    partes["config"] = _config(m, capas, capa_inicial, bounds, "zona")
    partes["config"]["measure"] = medir.get_name()
    partes["puntos"] = puntos
    return partes
