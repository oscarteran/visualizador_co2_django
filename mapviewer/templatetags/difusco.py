"""
Template tags del sistema DIFUSCO₂.

Traducen la lógica de design_handoff/reference/interactive/components-reference.js
(fluxClass, formatFlux, Icon, FluxMarker, FluxLegend, Histogram) a Django. Los
partials que generan el HTML viven en templates/mapviewer/components/.
"""
from django import template
from django.utils.html import format_html

from .. import design

register = template.Library()

# Trazos de 24×24 de components-reference.js (ICONS). moon, sun y chevron-* son
# de Lucide, la familia de iconos lineales que indica el README del sistema.
ICONS = {
    "plus": "M12 5v14M5 12h14",
    "minus": "M5 12h14",
    "fit": "M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5",
    "expand": "M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7",
    "target": "M12 2v4M12 18v4M2 12h4M18 12h4M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8",
    "layers": "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5",
    "download": "M12 4v11M7 10l5 5 5-5M5 20h14",
    "ruler": "M3 17l14-14 4 4-14 14zM7 13l2 2M10 10l2 2M13 7l2 2",
    "arrow": "M5 12h14M13 6l6 6-6 6",
    "moon": "M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z",
    "sun": "M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41"
           "M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41",
    "chevron-left": "M15 18l-6-6 6-6",
    "chevron-right": "M9 18l6-6-6-6",
    # Lucide: contacto (Ayuda y contacto)
    "mail": "M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 6l-10 7L2 6",
    "phone": "M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1"
             "-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09"
             " 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z",
    "map-pin": "M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0zM12 7a3 3 0 1 0 0 6a3 3 0 1 0 0-6",
    "send": "M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z",
}

MARKER_PAD = 6  # margen alrededor del círculo en FluxMarker


# ---------- filtros de datos ----------

@register.filter
def flux_class(value):
    return design.flux_class(value)


@register.filter
def format_flux(value):
    return design.format_flux(value)


@register.filter
def flux_name(cls):
    return design.FLUX_NAMES.get(cls, "Sin dato")


@register.filter
def format_coord(value):
    return design.format_coord(value)


@register.filter
def badge_flux(flux, tone=None):
    """Clase de flujo de un Badge: tone low/mid/high = 1/3/5, o el valor de flux."""
    by_tone = {"low": 1, "mid": 3, "high": 5}.get(tone)
    if by_tone:
        return by_tone
    try:
        return int(flux)
    except (TypeError, ValueError):
        return 0


@register.filter
def get_item(mapping, key):
    """Acceso por clave variable en plantillas: {{ row|get_item:col.key }}."""
    try:
        return mapping[key]
    except (KeyError, IndexError, TypeError):
        return getattr(mapping, key, "")


@register.simple_tag
def flux_unit():
    return design.FLUX_UNIT


# ---------- iconos ----------

@register.simple_tag
def icon(name, size=18, css_class=""):
    classes = f"dx-icon {css_class}".strip()
    return format_html(
        '<svg class="{}" width="{}" height="{}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="{}"></path></svg>',
        classes, size, size, ICONS.get(name, ""),
    )


# ---------- componentes con geometría ----------

def _marker(cls=0, value=None, state="default", imagery=False):
    """Contexto de FluxMarker (mismo cálculo que components-reference.js)."""
    r = design.FLUX_RADII.get(cls, design.FLUX_RADII[1])
    s = (r + MARKER_PAD) * 2
    if cls:
        label = f"{design.format_flux(value)} {design.FLUX_UNIT} ({design.FLUX_NAMES[cls]})"
    else:
        label = "Sin dato"
    return {
        "cls": cls, "state": state, "imagery": imagery, "size": s, "center": s / 2,
        "r": r + 1.5 if state == "hover" else r, "ring_r": r + 4, "label": label,
    }


@register.inclusion_tag("mapviewer/components/flux_marker.html")
def flux_marker(value=None, cls=None, state="default", imagery=False):
    if cls is None:
        cls = design.flux_class(value)
    return {"m": _marker(cls, value, state, imagery)}


@register.inclusion_tag("mapviewer/components/flux_legend.html")
def flux_legend(title="Flujo de CO₂", unit=None, nodata=True, css_class=""):
    steps = [
        {"cls": c, "label": design.FLUX_LABELS[c], "marker": _marker(c)}
        for c in sorted(design.FLUX_LABELS)
    ]
    return {
        "title": title, "unit": unit or design.FLUX_UNIT, "steps": steps,
        "nodata": nodata, "nodata_marker": _marker(0), "css_class": css_class,
    }


def _num(v):
    """Número compacto para atributos SVG."""
    return f"{round(v, 2):g}"


@register.inclusion_tag("mapviewer/components/histogram.html")
def histogram(values, caption="", width=320, height=160, css_class=""):
    counts = [0] * 5
    for v in values or []:
        c = design.flux_class(v)
        if c:
            counts[c - 1] += 1
    peak = max(counts + [1])
    top, base = 18, height - 30
    bw = (width - 8) / 5
    bars = []
    for i, n in enumerate(counts):
        bh = max(3, (base - top) * n / peak) if n else 0
        x, w = 4 + i * bw + 1, bw - 2
        bars.append({
            "cls": i + 1, "n": n, "label": design.FLUX_LABELS[i + 1],
            "x": _num(x), "w": _num(w), "cx": _num(x + w / 2),
            "path": (f"M{_num(x)},{_num(base)}V{_num(base - bh + 4)}q0,-4 4,-4"
                     f"H{_num(x + w - 4)}q4,0 4,4V{_num(base)}Z") if n else "",
            "n_y": _num(base - bh - 6), "x_y": _num(base + 18),
        })
    return {
        "bars": bars, "counts": ", ".join(str(n) for n in counts), "caption": caption,
        "width": width, "height": height, "top": top, "hit_h": base - top,
        "base_line": _num(base + 0.5), "unit": design.FLUX_UNIT, "css_class": css_class,
    }
