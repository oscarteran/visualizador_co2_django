// mapviewer/static/mapviewer/js/map_controls.js
// Controles de los mapas Folium incrustados (Inventario Nacional y Ficha técnica).
//
// - Convierte los partials LayerSwitcher, MapControls y FluxLegend en controles
//   de Leaflet (así siguen visibles en pantalla completa).
// - Cambia el mapa base sin recargar; «Mapa» usa Positron en claro y Dark Matter
//   en oscuro. La capa queda en ?tipo_mapa= para compartir o recargar.
// - Estados de FluxMarker: contorno según tema/capa, hover (+1.5px) y
//   seleccionado (anillo oro). ZoneMarker: flyTo y estado seleccionado.
// La configuración llega en <script id="map-config"> (mapviewer/utils/mapas.py).

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const configEl = document.getElementById('map-config');
        if (!configEl || !window.L) return;
        const cfg = JSON.parse(configEl.textContent);
        const map = window[cfg.map];
        if (!map) return;

        const layers = {};
        Object.keys(cfg.layers).forEach(function (key) { layers[key] = window[cfg.layers[key]]; });
        const padding = [cfg.padding, cfg.padding];
        let current = cfg.initial;
        let activeTile = null;

        function theme() {
            return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        }

        // ---------- controles (partials → L.Control) ----------
        const DomControl = L.Control.extend({
            onAdd: function () { return this.options.node; }
        });
        document.querySelectorAll('[data-map-control]').forEach(function (node) {
            L.DomEvent.disableClickPropagation(node);
            L.DomEvent.disableScrollPropagation(node);
            node.classList.add('dx-map-control');
            new DomControl({ position: node.getAttribute('data-map-control'), node: node }).addTo(map);
        });
        L.control.scale({ position: cfg.kind === 'zona' ? 'topleft' : 'bottomleft', imperial: false, maxWidth: 80 })
            .addTo(map);

        // Los botones propios de los plugins se ocultan: los maneja MapControls.
        if (map.fullscreenControl) map.fullscreenControl.getContainer().classList.add('dx-native-hidden');

        // ---------- capas base ----------
        const switcher = document.querySelector('.dx-seg[role="radiogroup"]');
        const segItems = switcher ? Array.from(switcher.querySelectorAll('[data-layer]')) : [];

        function tileFor(key) {
            return key === 'mapa' ? layers['mapa_' + theme()] : layers[key];
        }

        function setBase(key, fromUser) {
            const next = tileFor(key);
            if (!next) return;
            if (activeTile && activeTile !== next) map.removeLayer(activeTile);
            if (!map.hasLayer(next)) next.addTo(map);
            next.bringToBack();
            activeTile = next;
            current = key;
            map.getContainer().classList.toggle('is-imagery', key === 'satelite');
            segItems.forEach(function (item) {
                const on = item.getAttribute('data-layer') === key;
                item.classList.toggle('is-on', on);
                item.setAttribute('aria-checked', on ? 'true' : 'false');
                item.tabIndex = on ? 0 : -1;
            });
            restyleMarkers();
            if (fromUser) {
                const url = new URL(window.location.href);
                url.searchParams.set('tipo_mapa', key);
                window.history.replaceState(null, '', url);
                document.querySelectorAll('[data-map-layer-input]').forEach(function (input) { input.value = key; });
            }
        }

        segItems.forEach(function (item, i) {
            item.addEventListener('click', function () { setBase(item.getAttribute('data-layer'), true); });
            item.addEventListener('keydown', function (e) {
                const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
                if (!step) return;
                e.preventDefault();
                const next = segItems[(i + step + segItems.length) % segItems.length];
                next.focus();
                setBase(next.getAttribute('data-layer'), true);
            });
        });

        // ---------- FluxMarker (Ficha técnica) ----------
        const circles = [];
        map.eachLayer(function (layer) {
            if (layer instanceof L.CircleMarker) circles.push(layer);
        });
        let hovered = null;
        let ring = null;

        function strokeStyle() {
            return current === 'satelite'
                ? { color: cfg.strokeImagery, weight: 1.5 }
                : { color: cfg.stroke[theme()], weight: 1 };
        }

        function restyleMarkers() {
            const base = strokeStyle();
            circles.forEach(function (c) {
                c.setStyle({ color: base.color, weight: c === hovered ? 2 : base.weight });
            });
            if (ring) ring.setStyle({ color: cfg.selected[theme()] });
        }

        circles.forEach(function (c) {
            c._dxRadius = c.options.radius;
            c.on('mouseover', function () {
                hovered = c;
                c.setRadius(c._dxRadius + 1.5);
                c.setStyle({ weight: 2 });
            });
            c.on('mouseout', function () {
                hovered = null;
                c.setRadius(c._dxRadius);
                c.setStyle({ weight: strokeStyle().weight });
            });
            c.on('popupopen', function () {
                if (ring) map.removeLayer(ring);
                ring = L.circleMarker(c.getLatLng(), {
                    radius: c._dxRadius + 4, color: cfg.selected[theme()], weight: 2.5,
                    fill: false, interactive: false
                }).addTo(map);
            });
            c.on('popupclose', function () {
                if (ring) { map.removeLayer(ring); ring = null; }
            });
        });

        // ---------- ZoneMarker (Inventario Nacional) ----------
        const cluster = cfg.cluster ? window[cfg.cluster] : null;
        if (cluster) {
            cluster.eachLayer(function (marker) {
                marker.on('click', function () {
                    map.flyTo(marker.getLatLng(), Math.max(map.getZoom(), 9), { duration: 0.8 });
                });
                marker.on('popupopen popupclose', function (e) {
                    const el = marker.getElement() && marker.getElement().querySelector('.dx-zm');
                    if (el) el.classList.toggle('is-selected', e.type === 'popupopen');
                });
            });
        }

        // ---------- MapControls ----------
        const measure = cfg.measure ? window[cfg.measure] : null;

        function setPressed(action, on) {
            document.querySelectorAll('.dx-mapbtn[data-action="' + action + '"]').forEach(function (btn) {
                btn.classList.toggle('is-on', on);
                btn.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
        }

        const actions = {
            'zoom-in': function () { map.zoomIn(); },
            'zoom-out': function () { map.zoomOut(); },
            'fit': function () { map.fitBounds(cfg.bounds, { padding: padding }); },
            'fullscreen': function () {
                if (map.fullscreenControl) map.fullscreenControl.toggleFullScreen();
            },
            'measure': function () {
                if (!measure) return;
                if (measure._locked) {
                    measure._handleMeasureDoubleClick();
                } else {
                    // Trazo de la medición con el contorno de marcadores del tema/capa actual
                    measure.options.activeColor = measure.options.completedColor = strokeStyle().color;
                    measure._startMeasure();
                }
            }
        };
        document.querySelectorAll('.dx-mapbtn[data-action]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const run = actions[btn.getAttribute('data-action')];
                if (run) run();
            });
        });
        map.on('enterFullscreen', function () { setPressed('fullscreen', true); });
        map.on('exitFullscreen', function () { setPressed('fullscreen', false); });
        map.on('measurestart', function () { setPressed('measure', true); });
        map.on('measurefinish', function () { setPressed('measure', false); });

        // ---------- tema ----------
        new MutationObserver(function () {
            if (current === 'mapa') setBase('mapa', false);
            else restyleMarkers();
        }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

        // ---------- inicio ----------
        setBase(current, false);
        map.invalidateSize();
        map.fitBounds(cfg.bounds, { padding: padding });
    });
})();
