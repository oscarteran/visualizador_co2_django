// mapviewer/static/mapviewer/js/map_controls.js

document.addEventListener('DOMContentLoaded', function() {
    const mapTypeSelect = document.getElementById('tipo_mapa');
    const filterForm = document.getElementById('map-filter-form');
    
    // Función que se dispara al cambiar la selección del tipo de mapa
    if (mapTypeSelect && filterForm) {
        mapTypeSelect.addEventListener('change', function() {
            // El formulario se envía directamente para recargar la página con el nuevo parámetro GET
            filterForm.submit();
        });
    }
    
    // NOTA: Si añades más filtros (como ubicaciones), puedes añadir lógica aquí 
    // para manejar los cambios o enviar el formulario dinámicamente.

    // Opcional: Ajustar el tamaño del iframe del mapa después de la carga si Folium lo requiere
    const mapWrapper = document.querySelector('.map-content-area');
    if (mapWrapper && mapWrapper.querySelector('iframe')) {
        const iframe = mapWrapper.querySelector('iframe');
        iframe.onload = () => {
             // Asegura que el iframe se ajuste al 100% de su contenedor después de cargar el mapa
             iframe.style.width = '100%';
             iframe.style.height = '100%';
        };
    }
});