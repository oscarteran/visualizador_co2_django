// mapviewer/static/mapviewer/js/nav.js
// Barra superior, sin dependencias:
// - «Zonas» abre el menú de zonas. Lo cierran Esc (el foco vuelve a «Zonas»), un
//   clic fuera o tabular fuera; ↑/↓ recorren las zonas y ←/→ cambian de columna.
//   Sin JS, «Zonas» es un enlace al mapa nacional.
// - ☰ (< 900px) abre el panel #menu-movil con las mismas secciones.
// - «Cómo citar» abre el <dialog> de la cita, con botones para copiarla.

document.addEventListener('DOMContentLoaded', function () {
    initZoneMenu();
    initMobileMenu();
    initCiteDialog();
});

function initZoneMenu() {
    const trigger = document.getElementById('zonas-trigger');
    const menu = document.getElementById('zonas-menu');
    if (!trigger || !menu) return;

    const header = trigger.closest('.dx-appbar');
    const columns = Array.from(menu.querySelectorAll('.dx-zmenu-col')).map(function (col) {
        return Array.from(col.querySelectorAll('.dx-zmenu-item'));
    });
    const items = [].concat.apply([], columns);
    const EDGE = 16;   // margen mínimo con el borde de la pantalla, en px

    function isOpen() {
        return !menu.hidden;
    }

    // Alinea el menú con la pestaña «Zonas» sin que se salga por la derecha
    function place() {
        const left = trigger.getBoundingClientRect().left - header.getBoundingClientRect().left;
        const max = header.clientWidth - menu.offsetWidth - EDGE;
        menu.style.left = Math.max(EDGE, Math.min(left, max)) + 'px';
    }

    function setOpen(open, focusFirst) {
        menu.hidden = !open;
        trigger.setAttribute('aria-expanded', String(open));
        trigger.classList.toggle('is-open', open);
        if (!open) return;
        place();
        if (focusFirst) (menu.querySelector('.dx-zmenu-item.is-on') || items[0]).focus();
    }

    trigger.addEventListener('click', function (e) {
        e.preventDefault();
        // detail === 0: el clic viene del teclado (Enter) → el foco entra al menú
        setOpen(!isOpen(), e.detail === 0);
    });

    trigger.addEventListener('keydown', function (e) {
        if (e.key === ' ' || e.key === 'ArrowDown') {
            e.preventDefault();   // la barra espaciadora no desplaza la página
            setOpen(e.key === ' ' ? !isOpen() : true, true);
        }
    });

    menu.addEventListener('keydown', function (e) {
        const current = document.activeElement;
        const i = items.indexOf(current);
        if (i < 0) return;   // el enlace del pie se recorre con Tab
        let next = null;
        if (e.key === 'ArrowDown') next = items[(i + 1) % items.length];
        else if (e.key === 'ArrowUp') next = items[(i - 1 + items.length) % items.length];
        else if (e.key === 'Home') next = items[0];
        else if (e.key === 'End') next = items[items.length - 1];
        else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
            // Misma fila en la columna vecina (o su última zona si es más corta)
            const c = columns.findIndex(function (col) { return col.indexOf(current) >= 0; });
            const row = columns[c].indexOf(current);
            const step = e.key === 'ArrowRight' ? 1 : -1;
            const target = columns[(c + step + columns.length) % columns.length];
            next = target[Math.min(row, target.length - 1)];
        }
        if (next) {
            e.preventDefault();
            next.focus();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isOpen()) {
            setOpen(false);
            trigger.focus();
        }
    });

    document.addEventListener('click', function (e) {
        if (isOpen() && !menu.contains(e.target) && !trigger.contains(e.target)) setOpen(false);
    });

    // Al tabular fuera del menú (o de «Zonas» hacia otra pestaña) se cierra
    function onFocusOut(e) {
        const to = e.relatedTarget;
        if (isOpen() && to && !menu.contains(to) && to !== trigger) setOpen(false);
    }
    menu.addEventListener('focusout', onFocusOut);
    trigger.addEventListener('focusout', onFocusOut);

    window.addEventListener('resize', function () {
        if (isOpen()) place();
    });
    // Bajo 900px las pestañas se ocultan: el menú no debe quedar abierto
    window.matchMedia('(max-width: 900px)').addEventListener('change', function (e) {
        if (e.matches) setOpen(false);
    });
}

function initMobileMenu() {
    const button = document.getElementById('menu-movil-btn');
    const panel = document.getElementById('menu-movil');
    if (!button || !panel) return;

    function setOpen(open) {
        panel.hidden = !open;
        button.setAttribute('aria-expanded', String(open));
        button.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    }

    button.addEventListener('click', function () {
        setOpen(panel.hidden);
    });

    document.addEventListener('keydown', function (e) {
        // Con el diálogo de la cita abierto, Esc solo cierra el diálogo
        if (e.key === 'Escape' && !panel.hidden && !document.querySelector('dialog[open]')) {
            setOpen(false);
            button.focus();
        }
    });

    document.addEventListener('click', function (e) {
        if (!panel.hidden && !panel.contains(e.target) && !button.contains(e.target)
            && !e.target.closest('dialog')) setOpen(false);
    });

    // Al volver a escritorio el panel no debe quedar abierto
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) {
        if (e.matches) setOpen(false);
    });
}

function initCiteDialog() {
    const dialog = document.getElementById('citar-dialog');
    if (!dialog || typeof dialog.showModal !== 'function') return;

    document.querySelectorAll('[data-citar]').forEach(function (button) {
        button.addEventListener('click', function () {
            dialog.showModal();
        });
    });

    // Clic en el fondo (fuera de la caja del diálogo) lo cierra
    dialog.addEventListener('click', function (e) {
        if (e.target !== dialog) return;
        const r = dialog.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) {
            dialog.close();
        }
    });

    function selectText(el) {
        const range = document.createRange();
        range.selectNodeContents(el);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    dialog.querySelectorAll('[data-copiar]').forEach(function (button) {
        const label = button.textContent;
        function flash(text) {
            button.textContent = text;
            setTimeout(function () { button.textContent = label; }, 2000);
        }
        button.addEventListener('click', function () {
            const source = document.getElementById(button.dataset.copiar);
            // Sin portapapeles (HTTP fuera de localhost): se selecciona el texto
            function fallback() {
                selectText(source);
                flash('Ctrl+C para copiar');
            }
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(source.textContent).then(function () { flash('Copiado'); }, fallback);
            } else {
                fallback();
            }
        });
    });
}
