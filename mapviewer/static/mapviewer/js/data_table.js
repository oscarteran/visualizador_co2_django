// mapviewer/static/mapviewer/js/data_table.js
// Paginación de DataTable (.dx-table-wrap[data-page-size] + el paginador que le
// sigue). Sin JS se ven todas las filas. Cuando el mapa selecciona un punto
// (map_controls.js marca su fila con .is-selected) y la fila está en otra
// página, la tabla salta a esa página.

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.dx-table-wrap[data-page-size]').forEach(initPagination);
});

function initPagination(wrap) {
    const pager = wrap.nextElementSibling;
    if (!pager || !pager.hasAttribute('data-table-pager')) return;

    const tbody = wrap.querySelector('tbody');
    const rows = Array.from(tbody.rows);
    const status = pager.querySelector('[data-pager-status]');
    const prev = pager.querySelector('[data-pager-prev]');
    const next = pager.querySelector('[data-pager-next]');
    const sizeSelect = pager.querySelector('[data-pager-size]');
    let size = parseInt(wrap.getAttribute('data-page-size'), 10);   // 0 = todas
    let page = 0;

    function pageCount() {
        return size > 0 ? Math.ceil(rows.length / size) : 1;
    }

    function render() {
        const total = pageCount();
        page = Math.min(Math.max(page, 0), total - 1);
        const first = size > 0 ? page * size : 0;
        const last = size > 0 ? Math.min(first + size, rows.length) : rows.length;
        rows.forEach(function (row, i) {
            row.hidden = i < first || i >= last;
            // sin borde inferior en la última fila visible (la sigue el caption)
            row.classList.toggle('is-last-visible', i === last - 1);
        });
        prev.disabled = page === 0;
        next.disabled = page >= total - 1;
        status.textContent = 'Filas ' + (first + 1) + '–' + last + ' de ' + rows.length
            + (total > 1 ? ' · Página ' + (page + 1) + ' de ' + total : '');
    }

    // Si el inicio de la tabla quedó oculto (arriba de la pantalla o bajo la barra
    // superior fija), se sube para leer la página nueva desde la primera fila.
    function revealTop() {
        const appbar = document.querySelector('.dx-appbar');
        if (wrap.getBoundingClientRect().top < (appbar ? appbar.offsetHeight : 0)) {
            wrap.scrollIntoView({ block: 'start' });
        }
    }

    // Si el botón pulsado queda deshabilitado (primera o última página), el foco
    // pasa al otro para no perderse.
    function go(step, button, other) {
        page += step;
        render();
        revealTop();
        if (button.disabled && !other.disabled) other.focus();
    }
    prev.addEventListener('click', function () { go(-1, prev, next); });
    next.addEventListener('click', function () { go(1, next, prev); });

    sizeSelect.addEventListener('change', function () {
        const firstShown = size > 0 ? page * size : 0;   // se mantiene a la vista
        size = parseInt(sizeSelect.value, 10);
        page = size > 0 ? Math.floor(firstShown / size) : 0;
        render();
        revealTop();
    });

    // Punto elegido en el mapa → página de su fila. Solo reacciona cuando cambia
    // la selección, para poder hojear la tabla con un popup abierto.
    let selected = null;
    new MutationObserver(function () {
        const row = rows.find(function (r) { return r.classList.contains('is-selected'); }) || null;
        if (row === selected) return;
        selected = row;
        if (row && row.hidden && size > 0) {
            page = Math.floor(rows.indexOf(row) / size);
            render();
        }
    }).observe(tbody, { subtree: true, attributes: true, attributeFilter: ['class'] });

    pager.hidden = false;
    render();
}
