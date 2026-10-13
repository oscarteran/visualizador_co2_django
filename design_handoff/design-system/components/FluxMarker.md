# FluxMarker

Punto de medición: círculo con color y radio según la clase logarítmica de flujo (`flux-1…5`, radio 5 a 11px).

Es el marcador de la Ficha técnica, uno por medición. Lleva contorno `map-stroke` de 1px, o blanco de 1.5px sobre Satélite (`imagery`). Estados: `hover`, `selected` (anillo oro `marker-selected`), `muted` (cuando hay un filtro activo) y sin dato (punteado). Los puntos se dibujan ordenados de menor a mayor flujo. En Folium equivale a `CircleMarker` (ver sección Mapas).
