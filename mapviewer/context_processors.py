"""
Datos institucionales del pie de página (cita sugerida, licencia y fecha).

Se editan aquí; los textos marcados «por completar» esperan confirmación
(autoría, tutoría y licencia definitiva del catálogo).
"""
import datetime

SITE_NAME = "DIFUSCO₂: Catálogo de emisiones naturales difusas de CO₂"
SITE_INSTITUTION = "Instituto de Geofísica, Departamento de Recursos Naturales, UNAM"
SITE_AUTHORSHIP = "Autoría y tutoría por completar"
SITE_LICENSE = "Todos los derechos reservados"

# Fecha de la última modificación de los archivos de data/processed/.
DATA_UPDATED = datetime.date(2024, 11, 26)

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


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
        }
    }
