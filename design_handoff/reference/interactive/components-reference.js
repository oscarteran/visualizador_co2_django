/* @ds-bundle: {"format":4,"namespace":"Difusco","components":[{"name":"PageHeader"},{"name":"NavItem"},{"name":"Button"},{"name":"Badge"},{"name":"StatTile"},{"name":"LayerSwitcher"},{"name":"MapControls"},{"name":"FluxMarker"},{"name":"ZoneMarker"},{"name":"ClusterMarker"},{"name":"MapPopup"},{"name":"FluxLegend"},{"name":"ZoneList"},{"name":"Histogram"},{"name":"MapCanvas"},{"name":"DataTable"}]} */
(function () {
  var R = window.React, h = R.createElement;
  function cx() { return Array.prototype.filter.call(arguments, Boolean).join(" "); }

  /* ---------- helpers ---------- */
  var THRESHOLDS = [1, 10, 100, 1000];               // g m⁻² d⁻¹, clases logarítmicas (décadas)
  var CLASS_LABELS = ["< 1", "1–10", "10–100", "100–1000", "≥ 1000"];
  var CLASS_NAMES = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"];
  var RADII = [5, 6, 7, 9, 11];                       // radio del marcador por clase (px)
  function fluxClass(v) { if (v == null || isNaN(v)) return 0; var c = 1; for (var i = 0; i < THRESHOLDS.length; i++) if (v >= THRESHOLDS[i]) c = i + 2; return c; }
  function fmt(v) { if (v == null) return "—"; if (v >= 100) return Math.round(v).toLocaleString("en-US").replace(/,/g, "\u00a0"); if (v >= 10) return v.toFixed(1); return v.toFixed(2); }

  var ICONS = {
    plus: "M12 5v14M5 12h14", minus: "M5 12h14",
    fit: "M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5",
    expand: "M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7",
    target: "M12 2v4M12 18v4M2 12h4M18 12h4M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8",
    layers: "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5",
    download: "M12 4v11M7 10l5 5 5-5M5 20h14",
    ruler: "M3 17l14-14 4 4-14 14zM7 13l2 2M10 10l2 2M13 7l2 2",
    arrow: "M5 12h14M13 6l6 6-6 6"
  };
  function Icon(p) {
    return h("svg", { className: cx("dx-icon", p.className), width: p.size || 18, height: p.size || 18, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": "true" },
      h("path", { d: ICONS[p.name] || "" }));
  }

  /* ---------- base ---------- */
  function PageHeader(p) {
    return h("header", { className: cx("dx-header", p.className) },
      p.eyebrow ? h("div", { className: "dx-eyebrow" }, p.eyebrow) : null,
      h("h1", { className: "dx-h1" }, p.title),
      p.lead ? h("p", { className: "dx-lead" }, p.lead) : null,
      p.rule === false ? null : h("div", { className: "dx-rule", "aria-hidden": "true" }));
  }
  function NavItem(p) {
    return h("a", { href: p.href || "#", className: cx("dx-nav", p.active && "is-active", p.className), "aria-current": p.active ? "page" : undefined }, p.children);
  }
  function Button(p) {
    var v = p.variant || "secondary";
    var rest = Object.assign({}, p); delete rest.variant; delete rest.className; delete rest.icon;
    return h("button", Object.assign({ type: "button" }, rest, { className: cx("dx-btn", "dx-btn-" + v, p.className) }),
      p.icon ? h(Icon, { name: p.icon, size: 16 }) : null, p.children);
  }
  function Badge(p) {
    var t = p.tone || "neutral", flux = { low: 1, mid: 3, high: 5 }[t] || p.flux;
    return h("span", { className: cx("dx-badge", "dx-badge-" + (flux ? "flux" : t), p.className) },
      flux ? h("span", { className: "dx-dot dx-flux-" + flux, "aria-hidden": "true" }) : null, p.children);
  }
  function StatTile(p) {
    return h("div", { className: cx("dx-stat", p.compact && "is-compact", p.className) },
      h("div", { className: "dx-eyebrow dx-muted" }, p.label),
      h("div", { className: "dx-stat-value" }, p.value, p.unit ? h("span", { className: "dx-stat-unit" }, p.unit) : null),
      p.note ? h("div", { className: "dx-caption" }, p.note) : null);
  }

  /* ---------- map chrome ---------- */
  function LayerSwitcher(p) {
    var opts = p.options || ["Mapa", "Satélite", "Relieve"], val = p.value || opts[0];
    return h("div", { className: cx("dx-seg", p.className), role: "radiogroup", "aria-label": p.label || "Mapa base" },
      opts.map(function (o) {
        var on = o === val;
        return h("button", { key: o, type: "button", role: "radio", "aria-checked": on, className: cx("dx-seg-item", on && "is-on"), onClick: p.onChange ? function () { p.onChange(o); } : undefined }, o);
      }));
  }
  function IconButton(p) {
    return h("button", { type: "button", className: cx("dx-mapbtn", p.active && "is-on"), "aria-label": p.label, title: p.label, onClick: p.onClick }, h(Icon, { name: p.icon }));
  }
  function MapControls(p) {
    return h("div", { className: cx("dx-mapctl", p.className) },
      h("div", { className: "dx-mapctl-group" }, h(IconButton, { icon: "plus", label: "Acercar" }), h(IconButton, { icon: "minus", label: "Alejar" })),
      h("div", { className: "dx-mapctl-group" },
        h(IconButton, { icon: "fit", label: p.fitLabel || "Encuadrar zona" }),
        h(IconButton, { icon: "expand", label: "Pantalla completa" })),
      p.extra === false ? null : h("div", { className: "dx-mapctl-group" }, h(IconButton, { icon: "ruler", label: "Medir distancia" })));
  }

  /* ---------- markers ---------- */
  function FluxMarker(p) {
    var c = p.cls || fluxClass(p.value), r = c ? RADII[c - 1] : 5, pad = 6, s = (r + pad) * 2;
    var state = p.state || "default";
    return h("svg", { className: cx("dx-fm", "is-" + state, p.imagery && "on-imagery", p.className), width: s, height: s, viewBox: "0 0 " + s + " " + s, role: "img", "aria-label": c ? fmt(p.value) + " g m⁻² d⁻¹ (" + CLASS_NAMES[c - 1] + ")" : "Sin dato", style: p.style },
      state === "selected" ? h("circle", { className: "dx-fm-ring", cx: s / 2, cy: s / 2, r: r + 4 }) : null,
      c ? h("circle", { className: "dx-fm-dot dx-fill-" + c, cx: s / 2, cy: s / 2, r: state === "hover" ? r + 1.5 : r })
        : h("circle", { className: "dx-fm-nodata", cx: s / 2, cy: s / 2, r: r }));
  }
  function ZoneMarker(p) {
    return h("div", { className: cx("dx-zm", p.selected && "is-selected", p.className), style: p.style },
      h("span", { className: "dx-zm-chip" },
        h("span", { className: "dx-dot dx-flux-" + (p.cls || 3), "aria-hidden": "true" }),
        h("span", { className: "dx-zm-name" }, p.label),
        p.n != null ? h("span", { className: "dx-zm-n" }, p.n) : null),
      h("span", { className: "dx-zm-stem", "aria-hidden": "true" }),
      h("span", { className: "dx-zm-anchor", "aria-hidden": "true" }));
  }
  function ClusterMarker(p) {
    var n = p.n || 0, d = n >= 100 ? 44 : n >= 10 ? 36 : 30;
    return h("div", { className: "dx-cm", style: Object.assign({ width: d, height: d }, p.style), role: "img", "aria-label": n + " puntos" },
      h("span", { className: "dx-cm-ring dx-flux-" + (p.cls || 3) }), h("span", { className: "dx-cm-n" }, n));
  }

  /* ---------- popup & panels ---------- */
  function MapPopup(p) {
    var c = fluxClass(p.value);
    return h("div", { className: cx("dx-pop", p.className), style: p.style },
      h("div", { className: "dx-pop-head" }, h("span", { className: "dx-eyebrow dx-muted" }, p.zone || "Zona"), p.id ? h("span", { className: "dx-pop-id" }, p.id) : null),
      h("div", { className: "dx-pop-value" }, fmt(p.value), h("span", { className: "dx-stat-unit" }, p.unit || "g m⁻² d⁻¹")),
      c ? h(Badge, { flux: c }, CLASS_NAMES[c - 1]) : null,
      h("dl", { className: "dx-pop-meta" },
        p.coords ? [h("dt", { key: "a" }, "Coordenadas"), h("dd", { key: "b" }, p.coords)] : null,
        p.date ? [h("dt", { key: "c" }, "Fecha"), h("dd", { key: "d" }, p.date)] : null,
        p.method ? [h("dt", { key: "e" }, "Método"), h("dd", { key: "f", className: "is-text" }, p.method)] : null),
      p.href ? h("a", { className: "dx-pop-link", href: p.href }, p.linkLabel || "Ver ficha técnica", h(Icon, { name: "arrow", size: 14 })) : null,
      h("span", { className: "dx-pop-tip", "aria-hidden": "true" }));
  }
  function FluxLegend(p) {
    var labels = p.labels || CLASS_LABELS;
    return h("div", { className: cx("dx-legend", p.className), style: p.style, role: "group", "aria-label": (p.title || "Flujo de CO₂") + " en " + (p.unit || "g m⁻² d⁻¹") },
      h("div", { className: "dx-legend-head" },
        h("span", { className: "dx-legend-title" }, p.title || "Flujo de CO₂"),
        h("span", { className: "dx-legend-unit" }, p.unit || "g m⁻² d⁻¹")),
      h("div", { className: "dx-legend-scale" }, labels.map(function (l, i) {
        return h("div", { key: i, className: "dx-legend-step" },
          h("span", { className: "dx-legend-mk" }, h(FluxMarker, { cls: i + 1 })),
          h("span", { className: "dx-swatch dx-flux-" + (i + 1) }),
          h("span", { className: "dx-legend-label" }, l));
      })),
      p.nodata === false ? null : h("div", { className: "dx-legend-foot" }, h(FluxMarker, { cls: 0 }), h("span", null, "Sin dato / bajo límite de detección")));
  }
  function ZoneList(p) {
    return h("ul", { className: cx("dx-zl", p.className), role: "list" }, (p.zones || []).map(function (z) {
      var on = z.name === p.active;
      return h("li", { key: z.name },
        h("a", { href: z.href || "#", className: cx("dx-zl-row", on && "is-on"), "aria-current": on ? "true" : undefined },
          h("span", { className: "dx-dot dx-flux-" + (z.cls || 3), "aria-hidden": "true" }),
          h("span", { className: "dx-zl-main" }, h("span", { className: "dx-zl-name" }, z.name), h("span", { className: "dx-zl-sub" }, z.state)),
          h("span", { className: "dx-zl-n" }, z.n != null ? z.n + " pts" : "")));
    }));
  }
  function Histogram(p) {
    var vals = p.values || [], counts = [0, 0, 0, 0, 0];
    vals.forEach(function (v) { var c = fluxClass(v); if (c) counts[c - 1]++; });
    var max = Math.max.apply(null, counts.concat([1])), W = p.width || 320, H = p.height || 160, top = 18, base = H - 30, bw = (W - 8) / 5;
    return h("figure", { className: cx("dx-hist", p.className) },
      h("svg", { width: "100%", viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Histograma de flujo por clase: " + counts.join(", ") },
        h("line", { className: "dx-hist-base", x1: 0, x2: W, y1: base + 0.5, y2: base + 0.5 }),
        counts.map(function (n, i) {
          var bh = n ? Math.max(3, (base - top) * n / max) : 0, x = 4 + i * bw + 1, w = bw - 2;
          return h("g", { key: i },
            h("title", null, CLASS_LABELS[i] + " g m⁻² d⁻¹: " + n + " puntos"),
            h("rect", { className: "dx-hist-hit", x: x, y: top, width: w, height: base - top }),
            n ? h("path", { className: "dx-fill-" + (i + 1), d: "M" + x + "," + base + "V" + (base - bh + 4) + "q0,-4 4,-4H" + (x + w - 4) + "q4,0 4,4V" + base + "Z" }) : null,
            h("text", { className: "dx-hist-n", x: x + w / 2, y: base - bh - 6, textAnchor: "middle" }, n),
            h("text", { className: "dx-hist-x", x: x + w / 2, y: base + 18, textAnchor: "middle" }, CLASS_LABELS[i]));
        })),
      p.caption ? h("figcaption", { className: "dx-caption" }, p.caption) : null);
  }

  /* ---------- illustrative basemap (previews only) ---------- */
  function MapCanvas(p) {
    var kind = p.kind || "Mapa";
    return h("div", { className: cx("dx-canvas", "is-" + (kind === "Satélite" ? "imagery" : kind === "Relieve" ? "relief" : "plain"), p.className), style: p.style },
      h("svg", { className: "dx-canvas-bg", width: "100%", height: "100%", preserveAspectRatio: "none", viewBox: "0 0 100 100", "aria-hidden": "true" },
        [10, 22, 35, 49, 64, 80].map(function (r, i) { return h("ellipse", { key: "c" + i, className: "dx-iso", cx: 62, cy: 58, rx: r * 1.3, ry: r, vectorEffect: "non-scaling-stroke" }); }),
        [25, 50, 75].map(function (v) { return [h("line", { key: "x" + v, className: "dx-grat", x1: v, x2: v, y1: 0, y2: 100, vectorEffect: "non-scaling-stroke" }), h("line", { key: "y" + v, className: "dx-grat", y1: v, y2: v, x1: 0, x2: 100, vectorEffect: "non-scaling-stroke" })]; })),
      p.children,
      h("div", { className: "dx-attrib" }, p.attribution || "Mapa base ilustrativo · Leaflet"));
  }

  function DataTable(p) {
    var cols = p.columns || [];
    return h("div", { className: cx("dx-table-wrap", p.className) },
      h("table", { className: "dx-table" },
        p.caption ? h("caption", null, p.caption) : null,
        h("thead", null, h("tr", null, cols.map(function (c) { return h("th", { key: c.key, className: c.numeric ? "is-num" : undefined, scope: "col" }, c.label); }))),
        h("tbody", null, (p.rows || []).map(function (r, i) {
          return h("tr", { key: i }, cols.map(function (c) { var v = r[c.key]; return h("td", { key: c.key, className: c.numeric ? "is-num" : undefined }, c.render ? c.render(v, r) : v); }));
        }))));
  }

  window.Difusco = Object.assign(window.Difusco || {}, {
    PageHeader: PageHeader, NavItem: NavItem, Button: Button, Badge: Badge, StatTile: StatTile,
    LayerSwitcher: LayerSwitcher, MapControls: MapControls, IconButton: IconButton, Icon: Icon,
    FluxMarker: FluxMarker, ZoneMarker: ZoneMarker, ClusterMarker: ClusterMarker, MapPopup: MapPopup,
    FluxLegend: FluxLegend, ZoneList: ZoneList, Histogram: Histogram, MapCanvas: MapCanvas, DataTable: DataTable,
    fluxClass: fluxClass, formatFlux: fmt, FLUX_THRESHOLDS: THRESHOLDS, FLUX_LABELS: CLASS_LABELS, FLUX_NAMES: CLASS_NAMES, FLUX_RADII: RADII
  });
})();
