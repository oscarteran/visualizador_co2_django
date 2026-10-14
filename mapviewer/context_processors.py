"""
Datos comunes a todas las páginas:

- site_info: datos institucionales del pie de página (cita sugerida, licencia y
  fecha). Se editan aquí; los textos marcados «por completar» esperan
  confirmación (autoría, tutoría y licencia definitiva del catálogo).
- zonas_nav: zonas del menú «Zonas» de la barra superior y del paginador de la ficha.
"""
import datetime

from django.core.cache import cache

from . import design
from .utils import mapas

SITE_NAME = "DIFUSCO₂: Catálogo de emisiones naturales difusas de CO₂"
SITE_INSTITUTION = "Instituto de Geofísica, Departamento de Recursos Naturales, UNAM"
SITE_AUTHORSHIP = "Autoría y tutoría por completar"
SITE_LICENSE = "Todos los derechos reservados"

# Fecha de la última modificación de los archivos de data/processed/.
DATA_UPDATED = datetime.date(2024, 11, 26)

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")

# leer_zonas() abre los 7 CSV de data/processed/: el resultado se guarda 10 minutos.
ZONAS_NAV_CACHE = "difusco2:zonas_nav"
ZONAS_NAV_SEGUNDOS = 10 * 60


def fecha_larga(fecha):
    """Fecha en prosa: «26 de noviembre de 2024»."""
    return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}"


def site_info(request):
    return {
        "site": {
            "name": SITE_NAME,
            "institution": SITE_INSTITUTION,
            "authorship": SITE_AUTHORSHIP,
            "license": SITE_LICENSE,
            "data_updated": fecha_larga(DATA_UPDATED),
            "data_updated_iso": DATA_UPDATED.isoformat(),
            "cita": design.CITA_SUGERIDA,
        }
    }


def zonas_menu():
    """Zonas en el orden del catálogo (el de leer_zonas): clave (el valor que espera
    ?ubicacion=), nombre y entidad legibles, nº de puntos y URL de su ficha."""
    zonas = cache.get(ZONAS_NAV_CACHE)
    if zonas is None:
        zonas = [
            {"clave": z["clave"], "nombre": z["name"], "entidad": design.entidad(z["state"]),
             "n_puntos": z["n"], "url": z["href"]}
            for z in mapas.leer_zonas()
        ]
        cache.set(ZONAS_NAV_CACHE, zonas, ZONAS_NAV_SEGUNDOS)
    return zonas


def total_puntos():
    return sum(z["n_puntos"] for z in zonas_menu())


def zonas_nav(request):
    # Se pasan las funciones, no sus resultados: la plantilla las llama solo si las
    # usa, así las páginas de error (que no llevan la barra) no leen los CSV.
    return {"nav_zonas": zonas_menu, "nav_total_puntos": total_puntos}
