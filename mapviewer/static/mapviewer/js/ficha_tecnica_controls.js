// mapviewer/static/mapviewer/js/ficha_tecnica_controls.js
// Al elegir otra zona recarga la ficha con ?ubicacion= y la capa base actual
// (el campo oculto tipo_mapa lo mantiene al día map_controls.js).

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('map-filter-form-ficha');
    const ubicacionSelect = document.getElementById('ubicacion_ficha');

    if (form && ubicacionSelect) {
        ubicacionSelect.addEventListener('change', function () {
            form.submit();
        });
    }
});
