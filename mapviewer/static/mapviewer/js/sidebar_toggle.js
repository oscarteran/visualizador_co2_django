// mapviewer/static/mapviewer/js/sidebar_toggle.js
// Escritorio: colapsa/expande la barra lateral (el chevron gira por CSS).
// Móvil (< 768px): la barra lateral es un menú que se abre desde la barra
// superior; se cierra con Esc, con el fondo o con el mismo botón.

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('app-sidebar');
    const toggleButton = document.getElementById('sidebar-toggle');
    const menuButton = document.getElementById('mobile-menu-btn');
    const backdrop = document.getElementById('sidebar-backdrop');
    if (!sidebar) return;

    // ---------- escritorio ----------
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            const collapsed = sidebar.classList.toggle('collapsed');
            toggleButton.classList.toggle('sidebar-collapsed', collapsed);

            const text = collapsed ? 'Mostrar barra lateral' : 'Ocultar barra lateral';
            toggleButton.setAttribute('aria-expanded', String(!collapsed));
            toggleButton.setAttribute('aria-label', text);
            toggleButton.setAttribute('title', text);
        });
    }

    // ---------- móvil ----------
    if (!menuButton) return;

    function setMenu(open) {
        sidebar.classList.toggle('is-open', open);
        document.body.classList.toggle('menu-open', open);
        menuButton.setAttribute('aria-expanded', String(open));
        if (backdrop) backdrop.hidden = !open;
        if (open) {
            // Forzar el recálculo de estilos: sin esto el enlace aún tiene
            // visibility: hidden y focus() no surte efecto.
            void sidebar.offsetWidth;
            const first = sidebar.querySelector('.dx-nav');
            if (first) first.focus();
        }
    }

    menuButton.addEventListener('click', function () {
        setMenu(!sidebar.classList.contains('is-open'));
    });
    if (backdrop) backdrop.addEventListener('click', function () { setMenu(false); });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebar.classList.contains('is-open')) {
            setMenu(false);
            menuButton.focus();
        }
    });
    // Al volver a escritorio, el menú móvil no debe quedar abierto
    window.matchMedia('(min-width: 769px)').addEventListener('change', function (e) {
        if (e.matches) setMenu(false);
    });
});
