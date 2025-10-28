// mapviewer/static/mapviewer/js/sidebar_toggle.js

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('app-sidebar');
    const toggleButton = document.getElementById('sidebar-toggle');

    if (sidebar && toggleButton) {
        toggleButton.addEventListener('click', function () {
            
            // Alterna la clase 'collapsed' en la barra lateral
            sidebar.classList.toggle('collapsed');
            
            // CLAVE: Alterna la clase 'sidebar-collapsed' en el botón para cambiar su posición
            toggleButton.classList.toggle('sidebar-collapsed'); 
            
            // Alterna el ícono de la flecha
            const icon = toggleButton.querySelector('.fas');
            if (sidebar.classList.contains('collapsed')) {
                icon.classList.remove('fa-chevron-left');
                icon.classList.add('fa-chevron-right');
            } else {
                icon.classList.remove('fa-chevron-right');
                icon.classList.add('fa-chevron-left');
            }
        });
    }
});