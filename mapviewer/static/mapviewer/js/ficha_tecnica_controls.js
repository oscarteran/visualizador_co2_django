// mapviewer/static/mapviewer/js/ficha_tecnica_controls.js

document.addEventListener('DOMContentLoaded', function() {
    const tipoMapaSelect = document.getElementById('tipo_mapa_ficha');
    const ubicacionSelect = document.getElementById('ubicacion_ficha');
    const form = document.getElementById('map-filter-form-ficha');

    // Función que maneja el envío
    function actualizarMapa() {
        // Obtenemos los valores de ambos selectores
        const tipoMapa = tipoMapaSelect.value;
        const ubicacion = ubicacionSelect.value;
        
        // Construimos la URL con los nuevos parámetros GET
        // Usamos la propiedad action del formulario y añadimos los query params
        form.action = form.action.split('?')[0] + 
                     '?tipo_mapa=' + encodeURIComponent(tipoMapa) + 
                     '&ubicacion=' + encodeURIComponent(ubicacion);
        
        form.submit();
    }
    
    // Asignamos la función de actualización a ambos eventos 'change'
    if (tipoMapaSelect) {
        tipoMapaSelect.addEventListener('change', actualizarMapa);
    }
    
    if (ubicacionSelect) {
        ubicacionSelect.addEventListener('change', actualizarMapa);
    }
});
