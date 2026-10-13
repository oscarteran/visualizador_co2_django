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
