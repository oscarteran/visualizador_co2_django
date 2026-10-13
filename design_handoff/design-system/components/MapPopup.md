# MapPopup

Tarjeta que se abre al hacer clic en un punto o una zona: valor grande con unidad, badge de clase, coordenadas, fecha, método y enlace.

Reemplaza el tooltip "Valor medido: 11.4". El *tooltip* (hover) muestra solo valor + unidad, y el popup (clic) muestra esta ficha. Mide 240px de ancho y lleva una flecha hacia el punto. En Folium se pasa como `folium.Popup(html, max_width=260)`, y el `.leaflet-popup-content-wrapper` se restiliza con estas reglas. (La fecha de la preview es ilustrativa.)
