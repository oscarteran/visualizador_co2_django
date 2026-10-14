/* @ds-bundle: {"format":4,"namespace":"Difusco","components":[{"name":"PageHeader"},{"name":"NavItem"},{"name":"Button"},{"name":"Badge"},{"name":"StatTile"},{"name":"LayerSwitcher"},{"name":"MapControls"},{"name":"FluxMarker"},{"name":"ZoneMarker"},{"name":"ClusterMarker"},{"name":"MapPopup"},{"name":"FluxLegend"},{"name":"ZoneList"},{"name":"Histogram"},{"name":"MapCanvas"},{"name":"DataTable"},{"name":"AppHeader"},{"name":"ZoneMenu"},{"name":"ContextBar"},{"name":"ExplorerSidebar"}]} */
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
    arrow: "M5 12h14M13 6l6 6-6 6",
    chevDown: "M6 9l6 6 6-6", chevLeft: "M15 6l-6 6 6 6", chevRight: "M9 6l6 6-6 6",
    moon: "M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z", quote: "M7 7h4v4c0 3-2 5-4 5M14 7h4v4c0 3-2 5-4 5",
    menu: "M4 6h16M4 12h16M4 18h16", panel: "M3 4h18v16H3zM9 4v16", search: "M11 4a7 7 0 1 0 0 14a7 7 0 1 0 0-14M20 20l-4-4",
    home: "M3 11l9-7 9 7M5 10v10h14V10", map: "M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14", pin: "M12 21s-7-6-7-11a7 7 0 1 1 14 0c0 5-7 11-7 11zM12 8a2 2 0 1 0 0 4a2 2 0 1 0 0-4", book: "M4 5a2 2 0 0 1 2-2h14v16H6a2 2 0 0 0-2 2zM4 5v16", info: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 11v5M12 8h.01"
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


  /* ---------- navegación v3 ---------- */
  var ZONES_DEFAULT = [
    { name: "Acoculco", state: "Puebla", n: 180 }, { name: "Alcaparrosa", state: "Puebla", n: 23 }, { name: "Los Azufres", state: "Puebla", n: 42 },
    { name: "Chichinautzin", state: "CDMX–Morelos", n: 98 },
    { name: "Escalera", state: "Michoacán", n: 246 }, { name: "Michoa", state: "Michoacán", n: 53 }, { name: "Puruándiro", state: "Michoacán", n: 108 }];
  function groupByState(zs) { var g = [], idx = {}; zs.forEach(function (z) { if (!(z.state in idx)) { idx[z.state] = g.length; g.push({ state: z.state, zones: [] }); } g[idx[z.state]].zones.push(z); }); return g; }

  function AppHeader(p) {
    var items = p.items || [["Inicio", "/"], ["Mapa nacional", "/inventario_nacional/"], ["Zonas", "#zonas", true], ["Datos y fuentes", "/fuentes_info/"], ["Acerca de", "/acerca_de/"]];
    return h("header", { className: cx("dx-appbar", p.className) },
      h("div", { className: "dx-appbar-inner" },
        h("a", { className: "dx-appbar-brand", href: "/" },
          h("span", { className: "dx-wordmark" }, "DIFUSCO", h("span", { className: "dx-wordmark-sub" }, "₂")),
          h("span", { className: "dx-appbar-inst" }, "Instituto de Geofísica", h("br"), "UNAM")),
        h("nav", { className: "dx-tabs", "aria-label": "Principal" }, items.map(function (it) {
          var on = it[0] === p.active, menu = it[2];
          return h("a", { key: it[0], href: it[1], className: cx("dx-tab", on && "is-on", menu && p.menuOpen && "is-open"), "aria-current": on ? "page" : undefined, "aria-haspopup": menu ? "true" : undefined, "aria-expanded": menu ? !!p.menuOpen : undefined },
            it[0], menu ? h(Icon, { name: "chevDown", size: 14 }) : null);
        })),
        h("div", { className: "dx-appbar-tools" },
          h("button", { type: "button", className: "dx-btn dx-btn-quiet dx-btn-sm" }, h(Icon, { name: "quote", size: 16 }), "Cómo citar"),
          h("button", { type: "button", className: "dx-mapbtn dx-toolbtn", "aria-label": "Cambiar a tema oscuro", title: "Tema oscuro" }, h(Icon, { name: "moon" })),
          h("button", { type: "button", className: "dx-mapbtn dx-toolbtn dx-appbar-burger", "aria-label": "Abrir menú" }, h(Icon, { name: "menu" })))),
      p.children);
  }

  function ZoneMenu(p) {
    var zs = p.zones || ZONES_DEFAULT, total = zs.reduce(function (a, z) { return a + (z.n || 0); }, 0);
    return h("div", { className: cx("dx-zmenu", p.className), style: p.style, role: "menu" },
      h("div", { className: "dx-zmenu-cols" }, groupByState(zs).map(function (g) {
        return h("div", { key: g.state, className: "dx-zmenu-col" },
          h("div", { className: "dx-eyebrow dx-muted" }, g.state),
          g.zones.map(function (z) {
            return h("a", { key: z.name, href: "#", role: "menuitem", className: cx("dx-zmenu-item", z.name === p.active && "is-on") },
              h("span", { className: "dx-zmenu-name" }, z.name), h("span", { className: "dx-zmenu-n" }, z.n));
          }));
      })),
      h("div", { className: "dx-zmenu-foot" },
        h("span", { className: "dx-caption" }, zs.length + " zonas · " + total.toLocaleString("en-US").replace(/,/g, "\u00a0") + " puntos de medición"),
        h("a", { href: "/inventario_nacional/", className: "dx-pop-link" }, "Ver todas en el mapa", h(Icon, { name: "arrow", size: 14 }))));
  }

  function ContextBar(p) {
    var zs = p.zones || ZONES_DEFAULT, i = 0;
    zs.forEach(function (z, k) { if (z.name === p.zone) i = k; });
    var prev = zs[(i - 1 + zs.length) % zs.length], next = zs[(i + 1) % zs.length], cur = zs[i];
    return h("div", { className: cx("dx-ctxbar", p.className) },
      h("nav", { className: "dx-crumbs", "aria-label": "Ruta" },
        h("a", { href: "#" }, "Zonas"), h("span", { "aria-hidden": "true" }, "/"),
        h("span", null, cur.state), h("span", { "aria-hidden": "true" }, "/"),
        h("span", { "aria-current": "page", className: "dx-crumbs-cur" }, cur.name)),
      h("div", { className: "dx-ctxbar-tools" },
        h("span", { className: "dx-caption" }, "Zona " + (i + 1) + " de " + zs.length),
        h("div", { className: "dx-pager" },
          h("a", { href: "#", className: "dx-pager-btn", title: "Anterior: " + prev.name }, h(Icon, { name: "chevLeft", size: 16 }), h("span", null, prev.name)),
          h("a", { href: "#", className: "dx-pager-btn", title: "Siguiente: " + next.name }, h("span", null, next.name), h(Icon, { name: "chevRight", size: 16 })))));
  }

  function ExplorerSidebar(p) {
    var zs = p.zones || ZONES_DEFAULT, collapsed = !!p.collapsed;
    function item(icon, label, active, extra) {
      return h("a", { href: "#", className: cx("dx-xnav", active && "is-on"), "aria-current": active ? "page" : undefined, title: collapsed ? label : undefined },
        h(Icon, { name: icon, size: 18 }), collapsed ? null : h("span", { className: "dx-xnav-label" }, label), collapsed ? null : extra);
    }
    return h("aside", { className: cx("dx-xside", collapsed && "is-collapsed", p.className), style: p.style },
      h("div", { className: "dx-xside-top" },
        collapsed ? h("span", { className: "dx-wordmark dx-wordmark-sm" }, "D", h("span", { className: "dx-wordmark-sub" }, "₂"))
          : h("a", { href: "/", className: "dx-wordmark" }, "DIFUSCO", h("span", { className: "dx-wordmark-sub" }, "₂")),
        h("button", { type: "button", className: "dx-mapbtn dx-toolbtn", "aria-label": collapsed ? "Expandir barra" : "Contraer barra" }, h(Icon, { name: "panel", size: 16 }))),
      h("nav", { className: "dx-xside-nav", "aria-label": "Principal" },
        collapsed ? null : h("div", { className: "dx-xhead" }, "Explorar"),
        item("home", "Inicio", p.active === "Inicio"),
        item("map", "Mapa nacional", p.active === "Mapa nacional"),
        collapsed ? null : h("div", { className: "dx-xhead" }, "Zonas", h("span", { className: "dx-xhead-n" }, zs.length)),
        collapsed ? item("pin", "Zonas", !!p.zone) : groupByState(zs).map(function (g) {
          return h("div", { key: g.state, className: "dx-xgroup" },
            h("div", { className: "dx-xgroup-state" }, g.state),
            g.zones.map(function (z) {
              var on = z.name === p.zone;
              return h("a", { key: z.name, href: "#", className: cx("dx-xzone", on && "is-on"), "aria-current": on ? "page" : undefined },
                h("span", { className: "dx-xzone-name" }, z.name), h("span", { className: "dx-xzone-n" }, z.n));
            }));
        }),
        collapsed ? null : h("div", { className: "dx-xhead" }, "Referencia"),
        item("book", "Datos y fuentes", p.active === "Datos y fuentes"),
        item("info", "Acerca de", p.active === "Acerca de")),
      collapsed ? h("div", { className: "dx-xside-foot" }, h("button", { type: "button", className: "dx-mapbtn dx-toolbtn", "aria-label": "Tema oscuro" }, h(Icon, { name: "moon" })))
        : h("div", { className: "dx-xside-foot" },
          h("dl", { className: "dx-xmeta" }, h("dt", null, "Versión de datos"), h("dd", null, "v1.0 · 2026-10"), h("dt", null, "Mediciones"), h("dd", null, "750")),
          h("div", { className: "dx-row", style: { gap: 8 } },
            h("button", { type: "button", className: "dx-btn dx-btn-secondary dx-btn-sm", style: { flex: 1 } }, h(Icon, { name: "quote", size: 16 }), "Cómo citar"),
            h("button", { type: "button", className: "dx-mapbtn dx-toolbtn", "aria-label": "Tema oscuro", title: "Tema oscuro" }, h(Icon, { name: "moon" })))));
  }

  window.Difusco = Object.assign(window.Difusco || {}, {
    PageHeader: PageHeader, NavItem: NavItem, Button: Button, Badge: Badge, StatTile: StatTile,
    LayerSwitcher: LayerSwitcher, MapControls: MapControls, IconButton: IconButton, Icon: Icon,
    FluxMarker: FluxMarker, ZoneMarker: ZoneMarker, ClusterMarker: ClusterMarker, MapPopup: MapPopup,
    FluxLegend: FluxLegend, ZoneList: ZoneList, Histogram: Histogram, MapCanvas: MapCanvas, DataTable: DataTable,
    fluxClass: fluxClass, formatFlux: fmt, FLUX_THRESHOLDS: THRESHOLDS, FLUX_LABELS: CLASS_LABELS, FLUX_NAMES: CLASS_NAMES, FLUX_RADII: RADII,
    AppHeader: AppHeader, ZoneMenu: ZoneMenu, ContextBar: ContextBar, ExplorerSidebar: ExplorerSidebar, ZONES: ZONES_DEFAULT
  });
})();
