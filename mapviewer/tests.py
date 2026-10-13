import csv
import json
from collections import Counter
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from . import design

TOKENS_PATH = Path(settings.BASE_DIR) / "design_handoff" / "design-system" / "tokens.json"
ALCAPARROSA_CSV = Path(settings.BASE_DIR) / "data" / "processed" / "P_AlcaparrosaLatLon.csv"


class DesignTokensTests(SimpleTestCase):
    """design.py debe ser una copia fiel de tokens.json."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
        cls.colors = {t["name"]: t["value"] for t in data["color"]["tokens"]}
        cls.map_tokens = {t["name"]: t["value"] for t in data["map"]["tokens"]}

    def test_flux_colors(self):
        for cls_, hex_value in design.FLUX_COLORS.items():
            self.assertEqual(hex_value, self.colors[f"flux-{cls_}"])

    def test_flux_radii(self):
        for cls_, radius in design.FLUX_RADII.items():
            self.assertEqual(f"{radius}px", self.map_tokens[f"marker-r-{cls_}"])

    def test_map_colors(self):
        self.assertEqual(design.MAP_STROKE, self.colors["map-stroke"])
        self.assertEqual(design.MAP_STROKE_IMAGERY, self.colors["map-stroke-imagery"])
        self.assertEqual(design.MARKER_SELECTED, self.colors["marker-selected"])


class FluxClassTests(SimpleTestCase):

    def test_thresholds(self):
        cases = [(0.367, 1), (0.99, 1), (1, 2), (9.9, 2), (10, 3), (99, 3),
                 (100, 4), (999, 4), (1000, 5), (5190, 5)]
        for value, expected in cases:
            self.assertEqual(design.flux_class(value), expected, value)

    def test_missing_values(self):
        for value in (None, float("nan"), "", "n/a"):
            self.assertEqual(design.flux_class(value), 0)

    def test_alcaparrosa_distribution(self):
        """Criterio de aceptación del handoff: 23 puntos, distribución 1 · 11 · 6 · 3 · 2."""
        with ALCAPARROSA_CSV.open(encoding="utf-8") as f:
            values = [float(row["CO2_value"]) for row in csv.DictReader(f)]
        counts = Counter(design.flux_class(v) for v in values)
        self.assertEqual(len(values), 23)
        self.assertEqual([counts[c] for c in range(1, 6)], [1, 11, 6, 3, 2])


class FormatTests(SimpleTestCase):

    def test_format_flux(self):
        nbsp = " "
        cases = [(5190, f"5{nbsp}190"), (2150, f"2{nbsp}150"), (644, "644"), (90.7, "90.7"),
                 (11.4, "11.4"), (8.54, "8.54"), (0.367, "0.37"), (None, "—")]
        for value, expected in cases:
            self.assertEqual(design.format_flux(value), expected, value)

    def test_format_coord(self):
        self.assertEqual(design.format_coord(-98.140431), "−98.14043")
        self.assertEqual(design.format_coord(19.937928), "19.93793")


class ComponentTests(SimpleTestCase):
    """Los partials reproducen el HTML de components-reference.js."""

    def render(self, source, **context):
        from django.template import Context, Template
        return Template("{% load difusco %}" + source).render(Context(context))

    def test_page_header(self):
        inc = '{% include "mapviewer/components/page_header.html" with eyebrow="E" title="T" lead="L" %}'
        html = self.render(inc)
        for css in ("dx-header", "dx-eyebrow", "dx-h1", "dx-lead", "dx-rule"):
            self.assertIn(css, html)
        compact = self.render(inc.replace('lead="L"', 'lead="L" rule=False'))
        self.assertNotIn("dx-rule", compact)

    def test_badge_flux_and_tone(self):
        flux = self.render('{% include "mapviewer/components/badge.html" with text="Alto" flux=4 %}')
        self.assertIn('class="dx-badge dx-badge-flux"', flux)
        self.assertIn('dx-dot dx-flux-4', flux)
        high = self.render('{% include "mapviewer/components/badge.html" with text="x" tone="high" %}')
        self.assertIn('dx-flux-5', high)
        gold = self.render('{% include "mapviewer/components/badge.html" with text="Aviso" tone="gold" %}')
        self.assertIn('dx-badge-gold', gold)
        self.assertNotIn('dx-dot', gold)

    def test_histogram_counts(self):
        html = self.render("{% histogram values 'cap' %}", values=[0.5, 2, 3, 50, 5000])
        self.assertIn("Histograma de flujo por clase: 1, 2, 1, 0, 1", html)
        self.assertEqual(html.count('class="dx-fill-'), 4)  # sin barra para la clase vacía

    def test_flux_legend(self):
        html = self.render("{% flux_legend nodata=False %}")
        self.assertEqual(html.count("dx-legend-step"), 5)
        self.assertIn(design.FLUX_UNIT, html)
        self.assertNotIn("dx-legend-foot", html)

    def test_map_popup(self):
        html = self.render('{% include "mapviewer/components/map_popup.html" with zone="Alcaparrosa" value=2150 href="/x/" %}')
        self.assertIn("2 150", html)
        self.assertIn("Muy alto", html)
        self.assertIn("dx-pop-link", html)

    def test_data_table_kinds(self):
        cols = [{"key": "lat", "label": "Latitud", "numeric": True, "kind": "coord"},
                {"key": "v", "label": "Flujo", "numeric": True, "kind": "flux"},
                {"key": "v", "label": "Clase", "kind": "flux_class"}]
        html = self.render('{% include "mapviewer/components/data_table.html" with columns=cols rows=rows %}',
                           cols=cols, rows=[{"lat": -98.14043, "v": 701}])
        self.assertIn("−98.14043", html)
        self.assertIn('class="is-num">701<', html)
        self.assertIn("dx-flux-4", html)


class PageTests(SimpleTestCase):
    PAGES = {
        "inicio": "/", "inventario_nacional": "/inventario_nacional/", "ficha_tecnica": "/ficha_tecnica/",
        "fuentes_info": "/fuentes_info/", "acerca_de": "/acerca_de/", "ayuda_y_contacto": "/ayuda_y_contacto/",
    }

    def test_pages_render_with_layout(self):
        for name, url in self.PAGES.items():
            with self.subTest(page=name):
                html = self.client.get(url).content.decode()
                self.assertIn('class="dx-header', html)
                self.assertEqual(html.count('aria-current="page"'), 1)
                self.assertIn(f'href="{url}" class="dx-nav is-active" aria-current="page"', html)
                self.assertIn('class="dx-footer"', html)
                self.assertNotIn("Catalogo", html)
                self.assertNotIn("var(--accent)", html)
