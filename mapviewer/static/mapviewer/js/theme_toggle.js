// mapviewer/static/mapviewer/js/theme_toggle.js
// Se carga en <head>: aplica el tema guardado antes de pintar la página.
// El botón de la barra superior es solo un icono: luna en claro y sol en oscuro
// (por CSS según [data-theme]); aria-label y title dicen a qué tema cambia.

(function() {
    'use strict';

    const THEME_KEY = 'difusco2-theme';
    const DARK = 'dark';
    const LIGHT = 'light';

    function readTheme() {
        try {
            return localStorage.getItem(THEME_KEY);
        } catch (e) {
            return null;
        }
    }

    function saveTheme(theme) {
        try {
            localStorage.setItem(THEME_KEY, theme);
        } catch (e) {
            // Sin almacenamiento (modo privado): el tema dura solo esta visita.
        }
    }

    // Aplicar tema guardado INMEDIATAMENTE (antes de DOMContentLoaded para evitar flash)
    if (readTheme() === DARK) {
        document.documentElement.setAttribute('data-theme', DARK);
    }

    document.addEventListener('DOMContentLoaded', function() {
        const btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        function updateButton(theme) {
            const next = theme === DARK ? 'claro' : 'oscuro';
            btn.setAttribute('aria-label', 'Cambiar a tema ' + next);
            btn.setAttribute('title', 'Tema ' + next);
        }

        updateButton(document.documentElement.getAttribute('data-theme') || LIGHT);

        btn.addEventListener('click', function() {
            const isCurrentlyDark = document.documentElement.getAttribute('data-theme') === DARK;
            const newTheme = isCurrentlyDark ? LIGHT : DARK;

            if (newTheme === DARK) {
                document.documentElement.setAttribute('data-theme', DARK);
            } else {
                document.documentElement.removeAttribute('data-theme');
            }

            saveTheme(newTheme);
            updateButton(newTheme);
        });
    });
})();
