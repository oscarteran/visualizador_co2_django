"""
Constantes de diseño de DIFUSCO₂ para el código Python (Folium, vistas).

Es el único lugar fuera de tokens.css donde se permiten valores hex: Folium
necesita colores literales. Todos los valores se copian de
design_handoff/design-system/tokens.json; si cambian ahí, cambian aquí
(mapviewer/tests.py comprueba que coincidan).

Las clases de flujo van de 1 a 5, igual que las clases CSS flux-1…flux-5 y que
components-reference.js; 0 significa «sin dato».
"""
import math

# Unidad y método de medición. Pendientes de confirmar con el tutor
# (design_handoff/HANDOFF.md §7); se mantienen configurables aquí.
FLUX_UNIT = "g m⁻² d⁻¹"
MEASUREMENT_METHOD = "Cámara de acumulación"

# Umbrales logarítmicos por décadas, en FLUX_UNIT.
FLUX_THRESHOLDS = (1, 10, 100, 1000)

FLUX_LABELS = {1: "< 1", 2: "1–10", 3: "10–100", 4: "100–1000", 5: "≥ 1000"}
FLUX_NAMES = {1: "Muy bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy alto"}

# Escala secuencial amarillo → vino (tokens flux-1 … flux-5).
FLUX_COLORS = {
    1: "#F4E08A",
    2: "#E9A23F",
    3: "#D2662A",
    4: "#A8321F",
    5: "#6E1A25",
}

# Radio del marcador por clase, en px (tokens marker-r-1 … marker-r-5).
FLUX_RADII = {1: 5, 2: 6, 3: 7, 4: 9, 5: 11}

# Contorno de los marcadores sobre mapa base claro/oscuro (token map-stroke)
# y sobre la capa Satélite (token map-stroke-imagery).
MAP_STROKE = {"light": "#14213D", "dark": "#ECE8DF"}
MAP_STROKE_IMAGERY = "#FFFFFF"

# Anillo del punto seleccionado (token marker-selected).
MARKER_SELECTED = {"light": "#B8892B", "dark": "#E2BC67"}


NBSP = " "
MINUS = "−"


def format_flux(value):
    """Valor de flujo como en components-reference.js: miles con espacio duro
    (5 190), 1 decimal entre 10 y 100, 2 decimales debajo de 10; «—» sin dato."""
    if value is None:
        return "—"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "—"
    if math.isnan(value):
        return "—"
    if value >= 100:
        return f"{math.floor(value + 0.5):,}".replace(",", NBSP)
    if value >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}"


def format_coord(value):
    """Coordenada en grados decimales con 5 decimales y signo menos tipográfico."""
    if value is None:
        return "—"
    value = float(value)
    text = f"{abs(value):.5f}"
    return MINUS + text if value < 0 else text


def flux_class(value):
    """Clase de flujo 1–5 por décadas; 0 si no hay dato."""
    if value is None:
        return 0
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0
    if math.isnan(value):
        return 0
    cls = 1
    for i, threshold in enumerate(FLUX_THRESHOLDS):
        if value >= threshold:
            cls = i + 2
    return cls
