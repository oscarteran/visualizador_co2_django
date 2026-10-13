// mapviewer/static/mapviewer/js/sidebar_toggle.js
// Colapsa/expande la barra lateral. El chevron gira por CSS (.sidebar-collapsed).

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('app-sidebar');
    const toggleButton = document.getElementById('sidebar-toggle');

    if (sidebar && toggleButton) {
        toggleButton.addEventListener('click', function () {
            // Alterna la clase 'collapsed' en la barra lateral
            const collapsed = sidebar.classList.toggle('collapsed');

            // Alterna la clase 'sidebar-collapsed' en el botón para cambiar su posición
            toggleButton.classList.toggle('sidebar-collapsed', collapsed);

            const text = collapsed ? 'Mostrar barra lateral' : 'Ocultar barra lateral';
            toggleButton.setAttribute('aria-expanded', String(!collapsed));
            toggleButton.setAttribute('aria-label', text);
            toggleButton.setAttribute('title', text);
        });
    }
});
