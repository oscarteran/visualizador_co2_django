import pandas as pd

def tabla_resumen_info():
    data = {
        "Nombre": ["Acoculco", "Alcaparrosa", "Azufres", "Chichinautzin", "Escalera", "Michoa", "Puruandiro"],
        "Ubicacion": [(19.94551763857352, -98.1342090794785), (19.938287335451456, -98.1403903008043), (19.922608931287755, -98.1446972068743), (19.08627758098732, -99.1271971420124), (19.59937443895357, -101.03290674004415), (19.329928048541866, -96.30251214624522), (20.088816962773418, -101.49355905556486)],
        "Estado": ["Puebla", "Alcaparrosa", "Los Azufres", "CDMX-Morelos", "Michoacan", "Michoacan", "Michoacan"],
        "Descripción": ["", "", "", "", "", "", ""], 
        "Archivo": ["P_Acoculco.csv", "P_alcaparrosa.csv", "P_Azufres.csv", "P_Chichinautzin.csv", "P_Escalera.csv", "P_Michoa.csv", "P_Puruandiro.csv"]  # Nombres de archivos CSV
    }
    df = pd.DataFrame(data)
    tabla_info = df.to_dict(orient='records')
    
    return tabla_info