# LayerSwitcher

Control segmentado para cambiar el mapa base: Mapa · Satélite · Relieve.

Sustituye al `<select>` que recarga la página. Va flotando arriba a la derecha del mapa, a `map-inset`. La opción activa usa `unam-blue`. Funciona como `role="radiogroup"` y se navega con las flechas. El consumidor conecta `onChange` a `setUrl` de la capa de Leaflet.
