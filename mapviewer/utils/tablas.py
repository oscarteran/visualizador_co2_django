import datetime
from collections import Counter
from functools import lru_cache
from pathlib import Path

import openpyxl
import pandas as pd
from django.conf import settings

# Catálogo original del que salen los CSV de data/processed/.
CATALOGO_XLSX = Path(settings.BASE_DIR) / "data" / "raw" / "Catalogo_de_datos_CO2_Jacome_Paz_2020.xlsx"

# Zona del sitio → nombre(s) de la zona en el catálogo original. La correspondencia
# se comprueba en las pruebas: el nº de filas coincide con el CSV procesado
# (p. ej. Escalera = «Escalera » + «Escalera_02» = 246; Michoa = «Michoacan » = 53).
ZONAS_CATALOGO = {
    "Acoculco": ["Acoculco"],
    "Alcaparrosa": ["Alcaparrosa"],
    "Azufres": ["Los Azufres"],
    "Chichinautzin": ["Chichinautzin"],
    "Escalera": ["Escalera ", "Escalera_02"],
    "Michoa": ["Michoacan "],
    "Puruandiro": ["Puruandiro"],
}


def _texto_fecha(valor):
    if isinstance(valor, datetime.datetime):
        return valor.date().isoformat()
    return str(valor)


@lru_cache(maxsize=1)
def fuentes_por_zona():
    """Origen, fecha de medición y nº de puntos de cada zona, tal como aparecen
    en el catálogo original (no se corrigen nombres ni fechas)."""
    wb = openpyxl.load_workbook(CATALOGO_XLSX, read_only=True, data_only=True)
    filas = list(wb.worksheets[0].iter_rows(min_row=2, values_only=True))
    wb.close()
    resumen = {}
    for zona, nombres in ZONAS_CATALOGO.items():
        origenes, fechas, n = Counter(), Counter(), 0
        for fila in filas:
            if fila[3] in nombres:
                n += 1
                if fila[5]:
                    origenes[str(fila[5]).strip()] += 1
                if fila[4]:
                    fechas[_texto_fecha(fila[4])] += 1
        resumen[zona] = {
            "zona": zona,
            "nombre_catalogo": " / ".join(nombre.strip() for nombre in nombres),
            "origen": "; ".join(origenes) or "Sin registrar",
            "fecha": ", ".join(sorted(fechas)) or "Sin registrar",
            "puntos": n,
        }
    return resumen


def tabla_resumen_info():
    data = {
        "Nombre": ["Acoculco", "Alcaparrosa", "Azufres", "Chichinautzin", "Escalera", "Michoa", "Puruandiro"],
        "Ubicacion": [(19.94551763857352, -98.1342090794785), (19.938287335451456, -98.1403903008043), (19.922608931287755, -98.1446972068743), (19.08627758098732, -99.1271971420124), (19.59937443895357, -101.03290674004415), (19.329928048541866, -102.30251214624523), (20.088816962773418, -101.49355905556486)],
        "Estado": ["Puebla", "Alcaparrosa", "Los Azufres", "CDMX-Morelos", "Michoacan", "Michoacan", "Michoacan"],
        "Descripción": ["", "", "", "", "", "", ""], 
        "Archivo": ["P_Acoculco.csv", "P_alcaparrosa.csv", "P_Azufres.csv", "P_Chichinautzin.csv", "P_Escalera.csv", "P_Michoa.csv", "P_Puruandiro.csv"]  # Nombres de archivos CSV
    }
    df = pd.DataFrame(data)
    tabla_info = df.to_dict(orient='records')
    
    return tabla_info