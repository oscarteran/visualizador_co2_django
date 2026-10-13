# ZoneMarker

Marcador de zona para el mapa nacional: etiqueta (punto de clase mediana + nombre + nº de puntos) anclada a la coordenada con un tallo.

Sustituye a los pins negros con fuego. Al hacer clic, el mapa hace `flyTo` a la zona y abre un MapPopup de resumen. El estado `selected` se usa con la zona activa en ZoneList. En Folium se implementa con `folium.Marker(icon=folium.DivIcon(html=...))` y las clases `dx-zm`. Cuando las etiquetas se traslapan (Acoculco, Alcaparrosa y Los Azufres están a ~3 km), a zoom bajo se agrupan con ClusterMarker.
