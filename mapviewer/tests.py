import csv
import json
import re
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

    # Pestaña activa de la barra superior; en Ayuda y contacto no hay ninguna
    PESTANAS = {
        "inicio": "Inicio", "inventario_nacional": "Mapa nacional", "ficha_tecnica": "Zonas",
        "fuentes_info": "Datos y fuentes", "acerca_de": "Acerca de", "ayuda_y_contacto": None,
    }

    def test_pages_render_with_layout(self):
        for name, url in self.PAGES.items():
            with self.subTest(page=name):
                html = self.client.get(url).content.decode()
                self.assertIn('class="dx-header', html)
                self.assertIn('<header class="dx-appbar">', html)
                self.assertIn('<main class="page-main', html)
                activas = re.findall(r'class="dx-tab is-on"[^>]*>\s*([^<]+?)\s*<', html)
                self.assertEqual(activas, [self.PESTANAS[name]] if self.PESTANAS[name] else [])
                self.assertIn('class="dx-footer"', html)
                self.assertIn('href="/ayuda_y_contacto/">Ayuda y contacto</a>', html)   # en el pie
                self.assertNotIn("sidebar", html)
                self.assertNotIn("Catalogo ", html)  # etiqueta sin acento; el archivo fuente es «Catalogo_…»
                self.assertNotIn("var(--accent)", html)


class MapTests(SimpleTestCase):
    """Criterios de aceptación de la Fase 3 que se pueden comprobar sin navegador."""

    def test_capa_desde_get(self):
        from .utils import mapas
        self.assertEqual(mapas.capa_desde_get("Satelital"), "satelite")      # valor antiguo
        self.assertEqual(mapas.capa_desde_get("relieve"), "relieve")
        self.assertEqual(mapas.capa_desde_get("otra"), "mapa")
        self.assertEqual(mapas.capa_desde_get(None), "mapa")

    def test_ficha_alcaparrosa(self):
        from .utils import mapas
        m = mapas.mapa_zona("Alcaparrosa")
        page = m["header"] + m["html"] + m["script"]
        self.assertEqual(page.count("L.circleMarker("), 23)
        fills = [design.FLUX_COLORS[c] for c in range(1, 6)]
        self.assertEqual([page.count(f'"fillColor": "{h}"') for h in fills], [1, 11, 6, 3, 2])
        self.assertIn(design.FLUX_UNIT, page)                       # tooltips y popups con unidad
        self.assertIn("leaflet-measure", m["header"])
        self.assertIn("fitBounds", page)
        self.assertEqual(m["config"]["kind"], "zona")

    def test_sin_residuos_de_folium(self):
        from .utils import mapas
        for m in (mapas.mapa_nacional(), mapas.mapa_zona("Escalera")):
            page = m["header"] + m["html"] + m["script"]
            for residuo in ("Make this Notebook", "awesome-markers", "AwesomeMarkers", "bootstrap",
                            "font-awesome", "fa-fire", "user-scalable", "openstreetmap.org/{z}"):
                self.assertNotIn(residuo, page)
            self.assertIn("mapviewer/css/map.css", m["header"])

    def test_inventario_zonas(self):
        from .utils import mapas
        m = mapas.mapa_nacional()
        nombres = [z["name"] for z in m["zonas"]]
        self.assertEqual(len(nombres), 7)
        alc = next(z for z in m["zonas"] if z["name"] == "Alcaparrosa")
        self.assertEqual((alc["n"], alc["cls"]), (23, 2))               # mediana 8.54 → clase 2
        self.assertEqual(m["html"].count("dx-zm"), 0)                   # las etiquetas van en el script
        self.assertEqual(m["script"].count("dx-zm-chip"), 7)
        self.assertIn("markerClusterGroup", m["script"])

    def test_paginas_de_mapa(self):
        for url in ("/inventario_nacional/?tipo_mapa=Satelital", "/ficha_tecnica/?ubicacion=Michoa&tipo_mapa=relieve"):
            with self.subTest(url=url):
                html = self.client.get(url).content.decode()
                self.assertIn('role="radiogroup"', html)
                self.assertIn('id="map-config"', html)
                self.assertIn('dx-legend', html)
                self.assertNotIn("<iframe", html)
                self.assertNotIn('name="tipo_mapa" id=', html)            # el <select> de capa ya no existe
        ficha = self.client.get("/ficha_tecnica/?ubicacion=Michoa&tipo_mapa=relieve").content.decode()
        self.assertIn('class="dx-seg-item is-on" aria-checked="true" tabindex="0" data-layer="relieve"', ficha)
        self.assertIn('data-action="measure"', ficha)
        inventario = self.client.get("/inventario_nacional/").content.decode()
        self.assertNotIn('data-action="measure"', inventario)


class PaginasFase4Tests(SimpleTestCase):

    def test_fuentes_coinciden_con_csv(self):
        """La correspondencia zona → catálogo original da el mismo nº de puntos que el CSV."""
        from .utils import mapas
        from .utils.tablas import fuentes_por_zona
        fuentes = fuentes_por_zona()
        for zona in mapas.ARCHIVOS_ZONA:
            self.assertEqual(fuentes[zona]["puntos"], len(mapas.leer_puntos(zona)), zona)

    def test_descargar_csv(self):
        from .utils import mapas
        r = self.client.get("/ficha_tecnica/descargar/?ubicacion=Alcaparrosa")
        self.assertEqual(r.status_code, 200)
        self.assertIn('filename="difusco2_Alcaparrosa.csv"', r["Content-Disposition"])
        original = (mapas.DATA_DIR / "P_AlcaparrosaLatLon.csv").read_bytes()
        self.assertEqual(b"".join(r.streaming_content), original)            # sin modificar

    def test_ficha_panel_y_tabla(self):
        html = self.client.get("/ficha_tecnica/?ubicacion=Alcaparrosa").content.decode()
        self.assertIn("Flujo de CO₂ del suelo en 23 puntos de medición.", html)
        self.assertIn('class="dx-stat is-compact"', html)
        self.assertIn("8.54", html)                                         # mediana
        self.assertIn("5 190", html)                                   # máximo
        self.assertIn("Histograma de flujo por clase: 1, 11, 6, 3, 2", html)
        self.assertIn("dx-note", html)
        self.assertEqual(html.count("<tr data-point="), 23)
        self.assertIn("−98.14030", html)                               # signo menos tipográfico
        self.assertIn('href="/ficha_tecnica/descargar/?ubicacion=Alcaparrosa"', html)

    def test_inicio(self):
        html = self.client.get("/").content.decode()
        self.assertIn("is-display", html)
        self.assertEqual(html.count('class="dx-stat"'), 3)
        self.assertIn(">750<", html.replace(" ", ""))
        self.assertIn('class="dx-btn dx-btn-primary"', html)
        self.assertIn('"kind": "testigo"', html)

    def test_inventario_zonelist(self):
        html = self.client.get("/inventario_nacional/").content.decode()
        self.assertIn('class="dx-float zl-panel"', html)
        self.assertEqual(html.count("dx-zl-row"), 7)
        self.assertIn('href="/ficha_tecnica/?ubicacion=Escalera"', html)

    def test_sin_font_awesome(self):
        for url in ("/", "/acerca_de/", "/ayuda_y_contacto/", "/fuentes_info/"):
            html = self.client.get(url).content.decode()
            self.assertNotIn("font-awesome", html)
            self.assertNotIn('class="fas', html)


class ResponsivoTests(SimpleTestCase):
    """Fase 5: piezas del layout móvil presentes en el HTML."""

    def test_menu_movil(self):
        html = self.client.get("/fuentes_info/").content.decode()
        self.assertIn('dx-appbar-burger" id="menu-movil-btn" aria-label="Abrir menú" '
                      'aria-expanded="false" aria-controls="menu-movil"', html)
        panel = html[html.index('id="menu-movil"'):html.index("</header>")]
        self.assertIn("hidden", panel[:40])
        self.assertEqual(panel.count('class="dx-zmenu-item'), 7)              # zonas desplegadas
        self.assertIn('href="/fuentes_info/" class="dx-nav is-active" aria-current="page"', panel)
        self.assertIn("data-citar", panel)                                    # «Cómo citar» también en móvil

    def test_dialogo_cita(self):
        html = self.client.get("/acerca_de/").content.decode()
        self.assertIn('<dialog class="dx-card cite-dialog" id="citar-dialog"', html)
        self.assertEqual(html.count("data-citar aria-haspopup"), 2)                       # barra y panel móvil
        self.assertEqual(html.count('data-copiar="'), 2)                      # texto y BibTeX
        self.assertIn("@misc{difusco2,", html)
        self.assertIn("[Autoría por completar]", html)                       # placeholder, sin autores
        self.assertNotIn("doi.org", html.lower())                             # ni DOI inventado

    def test_inventario_select_movil(self):
        html = self.client.get("/inventario_nacional/").content.decode()
        self.assertIn("data-zone-select", html)
        self.assertEqual(html.count('<option value="') - 1, 7)   # 7 zonas + «Elegir una zona…»

    def test_controles_extra_marcados(self):
        html = self.client.get("/ficha_tecnica/").content.decode()
        self.assertIn("dx-mapctl-group dx-mapctl-extra", html)


import re


class CacheYMapaBaseTests(SimpleTestCase):
    """Evita que un navegador use JS/CSS viejos de caché y que el mapa quede sin fondo."""

    def test_estaticos_versionados(self):
        import re
        html = self.client.get("/inventario_nacional/").content.decode()
        for archivo in ("map_controls.js", "nav.js", "theme_toggle.js", "style.css", "tokens.css", "map.css"):
            self.assertRegex(html, re.escape(archivo) + r"\?v=\d+", archivo)

    def test_capa_base_inicial_desde_el_servidor(self):
        from .utils import mapas
        for capa, servicio in (("mapa", "World_Light_Gray_Base"), ("satelite", "World_Imagery"),
                               ("relieve", "World_Shaded_Relief")):
            script = mapas.mapa_nacional(capa)["script"]
            # Solo la capa inicial se agrega al mapa en el script de Folium (show=True)
            tile_vars = re.findall(r"var (tile_layer_\w+) = L\.tileLayer\(\s*\"([^\"]+)\"", script)
            añadidas = [url for var, url in tile_vars if f"{var}.addTo(" in script]
            self.assertEqual(len(añadidas), 1, capa)
            self.assertIn(servicio, añadidas[0])


class NavegacionTests(SimpleTestCase):
    """Fase 6: datos de la barra superior (menú de zonas y paginador de la ficha)."""

    def test_zonas_menu(self):
        from .context_processors import zonas_menu, total_puntos
        zonas = zonas_menu()
        self.assertEqual([z["nombre"] for z in zonas],
                         ["Acoculco", "Alcaparrosa", "Azufres", "Chichinautzin", "Escalera", "Michoa", "Puruandiro"])
        self.assertEqual([z["n_puntos"] for z in zonas], [180, 23, 42, 98, 246, 53, 108])
        self.assertEqual(total_puntos(), 750)
        self.assertEqual([z["entidad"] for z in zonas],
                         ["Puebla"] * 3 + ["CDMX–Morelos"] + ["Michoacán"] * 3)
        self.assertEqual(zonas[0]["url"], "/ficha_tecnica/?ubicacion=Acoculco")

    def test_entidad_sin_modificar_datos(self):
        from .utils.tablas import tabla_resumen_info
        self.assertIn("Michoacan", [f["Estado"] for f in tabla_resumen_info()])   # el dato queda igual
        self.assertEqual(design.entidad("Michoacan"), "Michoacán")
        self.assertEqual(design.entidad("Otra"), "Otra")

    def test_context_processor_registrado(self):
        context = self.client.get("/acerca_de/").context
        self.assertEqual(len(context["nav_zonas"]()), 7)
        self.assertEqual(context["nav_total_puntos"](), 750)

    def _render(self, plantilla, url, **contexto):
        from django.template.loader import render_to_string
        from django.test import RequestFactory
        from django.urls import resolve
        request = RequestFactory().get(url)
        request.resolver_match = resolve(request.path)
        return render_to_string(f"mapviewer/components/{plantilla}", contexto, request=request)

    def test_app_header_pestana_activa(self):
        activas = {"/": "Inicio", "/inventario_nacional/": "Mapa nacional",
                   "/fuentes_info/": "Datos y fuentes", "/acerca_de/": "Acerca de"}
        for url, etiqueta in activas.items():
            with self.subTest(url=url):
                html = self._render("app_header.html", url)
                self.assertEqual(html.count("is-on"), 1)
                self.assertIn(f'is-on" aria-current="page" href="{url}">{etiqueta}</a>', html)
        ficha = self._render("app_header.html", "/ficha_tecnica/", ubicacion_seleccionada="Escalera")
        self.assertIn('class="dx-tab is-on" id="zonas-trigger"', ficha)          # «Zonas» activa en la ficha
        self.assertIn('class="dx-zmenu-item is-on" aria-current="page"', ficha)
        ayuda = self._render("app_header.html", "/ayuda_y_contacto/")
        self.assertNotIn("is-on", ayuda)                                           # ninguna pestaña activa

    def test_zone_menu(self):
        html = self._render("zone_menu.html", "/")
        self.assertIn('id="zonas-menu" role="menu"', html)
        self.assertEqual(html.count('class="dx-zmenu-col"'), 3)
        self.assertEqual(html.count('role="menuitem" href="/ficha_tecnica/?ubicacion='), 7)
        for entidad in ("Puebla", "CDMX–Morelos", "Michoacán"):
            self.assertIn(f">{entidad}</div>", html)
        self.assertIn("7 zonas · 750 puntos de medición", html)

    def test_context_bar(self):
        zona = lambda n, e: {"nombre": n, "entidad": e, "url": f"/ficha_tecnica/?ubicacion={n}"}
        html = self._render("context_bar.html", "/ficha_tecnica/", indice=2, total=7,
                            zona_actual=zona("Alcaparrosa", "Puebla"), zona_anterior=zona("Acoculco", "Puebla"),
                            zona_siguiente=zona("Azufres", "Puebla"))
        self.assertIn('<span class="dx-crumbs-cur" aria-current="page">Alcaparrosa</span>', html)
        self.assertIn("Zona 2 de 7", html)
        self.assertIn('href="/ficha_tecnica/?ubicacion=Acoculco" rel="prev"', html)
        self.assertIn('href="/ficha_tecnica/?ubicacion=Azufres" rel="next"', html)

    def test_ficha_context_bar(self):
        html = self.client.get("/ficha_tecnica/?ubicacion=Alcaparrosa").content.decode()
        self.assertIn('<div class="dx-ctxbar">', html)
        self.assertIn("<span>Puebla</span>", html)
        self.assertIn('<span class="dx-crumbs-cur" aria-current="page">Alcaparrosa</span>', html)
        self.assertIn("Zona 2 de 7", html)
        self.assertIn('href="/ficha_tecnica/?ubicacion=Acoculco" rel="prev"', html)
        self.assertIn('href="/ficha_tecnica/?ubicacion=Azufres" rel="next"', html)
        self.assertIn("Ficha técnica · Puebla", html)                       # eyebrow con la entidad legible
        self.assertNotIn('id="ubicacion_ficha"', html)                     # sin el <select> de zona
        self.assertIn('href="/ficha_tecnica/descargar/?ubicacion=Alcaparrosa" download', html)
        self.assertNotIn("dx-ctxbar", self.client.get("/inventario_nacional/").content.decode())

    def test_recorrido_ciclico(self):
        from .views import _recorrido
        from .context_processors import zonas_menu
        nombres = [z["nombre"] for z in zonas_menu()]
        for i, nombre in enumerate(nombres):
            with self.subTest(zona=nombre):
                r = _recorrido(nombre)
                self.assertEqual((r["indice"], r["total"]), (i + 1, 7))
                self.assertEqual(r["zona_anterior"]["nombre"], nombres[i - 1])
                self.assertEqual(r["zona_siguiente"]["nombre"], nombres[(i + 1) % 7])
        self.assertEqual(_recorrido("Acoculco")["zona_anterior"]["nombre"], "Puruandiro")
        self.assertEqual(_recorrido("Puruandiro")["zona_siguiente"]["nombre"], "Acoculco")


class TablaPaginadaTests(SimpleTestCase):
    """La tabla de mediciones de la ficha se pagina en el navegador (data_table.js)."""

    def test_ficha_paginada(self):
        html = self.client.get("/ficha_tecnica/?ubicacion=Acoculco").content.decode()
        self.assertIn('class="dx-table-wrap" data-page-size="15"', html)
        self.assertEqual(html.count("<tr data-point="), 180)          # sin JS se ven todas las filas
        self.assertIn('<div class="dx-table-pager" data-table-pager hidden>', html)
        for valor in ('value="15" selected', 'value="30"', 'value="60"', 'value="0">Todas'):
            self.assertIn(valor, html)
        self.assertRegex(html, r"data_table\.js\?v=\d+")

    def test_tabla_corta_sin_paginador(self):
        html = self.client.get("/fuentes_info/").content.decode()
        self.assertNotIn("data-page-size", html)
        self.assertNotIn("data-table-pager", html)
