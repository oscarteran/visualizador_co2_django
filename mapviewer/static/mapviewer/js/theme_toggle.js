// mapviewer/static/mapviewer/js/theme_toggle.js

(function() {
    'use strict';

    const THEME_KEY = 'difusco2-theme';
    const DARK = 'dark';
    const LIGHT = 'light';

    // Aplicar tema guardado INMEDIATAMENTE (antes de DOMContentLoaded para evitar flash)
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme === DARK) {
        document.documentElement.setAttribute('data-theme', DARK);
    }

    document.addEventListener('DOMContentLoaded', function() {
        const btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        const icon = btn.querySelector('i');
        const label = btn.querySelector('.theme-label');

        function updateButton(theme) {
            if (icon) {
                icon.classList.remove('fa-moon', 'fa-sun');
                icon.classList.add(theme === DARK ? 'fa-sun' : 'fa-moon');
            }
            if (label) {
                label.textContent = theme === DARK ? 'Tema Claro' : 'Tema Oscuro';
            }
        }

        // Establecer estado inicial del botón
        const currentTheme = document.documentElement.getAttribute('data-theme') || LIGHT;
        updateButton(currentTheme);

        // Evento click
        btn.addEventListener('click', function() {
            const isCurrentlyDark = document.documentElement.getAttribute('data-theme') === DARK;
            const newTheme = isCurrentlyDark ? LIGHT : DARK;

            if (newTheme === DARK) {
                document.documentElement.setAttribute('data-theme', DARK);
            } else {
                document.documentElement.removeAttribute('data-theme');
            }

            localStorage.setItem(THEME_KEY, newTheme);
            updateButton(newTheme);
        });
    });
})();
