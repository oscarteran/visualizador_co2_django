# HANDOFF — Fase 6: Navegación con barra superior

> Para Claude Code. Este documento **complementa** `HANDOFF.md` (fases 1–5, ya implementadas). Las reglas no negociables de `HANDOFF.md §2` siguen vigentes. Lee también `design-system/Navegacion.md`.

## 0. Objetivo

- Reemplazar la barra lateral (`aside.sidebar`) por una **barra superior institucional** (AppHeader) con un **menú de zonas** (ZoneMenu).
- Agregar una **barra de contexto** (ContextBar) en la Ficha técnica.
- Dar al contenido **todo el ancho** de la pantalla.

**Fuera de alcance:** el contenido de los mapas, las fichas, las tablas, las estadísticas y los estilos de componentes existentes. Solo cambian el contenedor y la navegación.

## 1. Referencias

| Archivo | Uso |
|---|---|
| `design-system/Navegacion.md` | Diagnóstico, decisión (Propuesta A) y notas de implementación |
| `design-system/components/AppHeader.md`, `ZoneMenu.md`, `ContextBar.md` | Guía de cada componente |
| `design-system/components.css` | Sección `/* NAVEGACIÓN v3 */`: estilos `dx-appbar`, `dx-tab`, `dx-zmenu`, `dx-ctxbar`, `dx-crumbs`, `dx-pager`, `dx-wordmark`, `dx-toolbtn`, `dx-btn-sm` |
| `reference/interactive/components-reference.js` | Funciones `AppHeader`, `ZoneMenu`, `ContextBar`: especificación del HTML |
| `reference/screens/navegacion/*.png` | **Objetivo visual**, en claro y oscuro |
| `reference/interactive/NavA_*.html` | Maquetas que se abren en el navegador |

## 2. Etiquetas y rutas (no cambian las URLs)

| Pestaña | URL | Antes |
|---|---|---|
| Inicio | `/` | Catálogo |
| Mapa nacional | `/inventario_nacional/` | Inventario Nacional |
| Zonas ▾ | abre el menú; sin JS → `/inventario_nacional/` | Ficha técnica |
| Datos y fuentes | `/fuentes_info/` | Fuentes de información |
| Acerca de | `/acerca_de/` | Acerca de |

- «Ayuda y contacto» sale de la navegación principal y pasa al **pie de página**.
- La pestaña activa se decide por `request.resolver_match.url_name`. En `/ficha_tecnica/` la activa es «Zonas».

## 3. Tareas

### 6.1 Datos de navegación (context processor)
- Crea `mapviewer/context_processors.py` con `zonas_nav(request)`. Devuelve `{"nav_zonas": [...], "nav_total_puntos": int}`.
- Cada zona lleva: `nombre`, `entidad`, `n_puntos` y `url` (`/ficha_tecnica/?ubicacion=<valor>`). Usa los mismos valores que espera hoy el filtro de la ficha.
- Ordénalas como en el catálogo actual.
- Para el menú, agrúpalas por entidad con `{% regroup %}` en el template, o devuelve directamente la lista agrupada.
- Regístralo en `settings.TEMPLATES[0]["OPTIONS"]["context_processors"]`. Si los conteos implican consultas costosas, usa `django.core.cache` con 10 minutos de caché.
- Las entidades que se muestran en el menú deben ir con acento y formato legible (Michoacán, CDMX–Morelos) usando un diccionario de **presentación** en `design.py`. **No modifiques los datos.**

### 6.2 Partials nuevos (`templates/mapviewer/components/`)
- **`app_header.html`** — HTML exacto (traducido de `AppHeader()`):
  ```html
  <header class="dx-appbar">
    <div class="dx-appbar-inner">
      <a class="dx-appbar-brand" href="/">
        <span class="dx-wordmark">DIFUSCO<span class="dx-wordmark-sub">₂</span></span>
        <span class="dx-appbar-inst">Instituto de Geofísica<br>UNAM</span>
      </a>
      <nav class="dx-tabs" aria-label="Principal">
        <a class="dx-tab is-on" aria-current="page" href="…">Inicio</a>
        …
        <button type="button" class="dx-tab" id="zonas-trigger" aria-haspopup="true" aria-expanded="false" aria-controls="zonas-menu">
          Zonas <svg class="dx-icon" …><path d="M6 9l6 6 6-6"/></svg>
        </button>
        …
      </nav>
      <div class="dx-appbar-tools">
        <button type="button" class="dx-btn dx-btn-quiet dx-btn-sm" id="citar-btn">[icono quote] Cómo citar</button>
        <button type="button" class="dx-mapbtn dx-toolbtn" id="theme-toggle-btn" aria-label="Cambiar a tema oscuro">[icono luna/sol]</button>
        <button type="button" class="dx-mapbtn dx-toolbtn dx-appbar-burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu-movil">[icono menú]</button>
      </div>
    </div>
    {% include "mapviewer/components/zone_menu.html" %}
  </header>
  ```
  Los `path` SVG de cada icono (`quote`, `moon`, `menu`, `chevDown`, `chevLeft`, `chevRight`, `arrow`) están en el objeto `ICONS` de `components-reference.js`. Úsalos con `viewBox="0 0 24 24"`, `stroke="currentColor"`, `stroke-width="1.75"` y `fill="none"`.
- **`zone_menu.html`**: `<div class="dx-zmenu" id="zonas-menu" role="menu" hidden>`, con columnas por entidad (`.dx-zmenu-cols > .dx-zmenu-col`). Cada columna lleva un `.dx-eyebrow.dx-muted` con la entidad y sus enlaces `a.dx-zmenu-item[role=menuitem]`, cada uno con `.dx-zmenu-name` y `.dx-zmenu-n`. La zona actual lleva `.is-on`. El pie `.dx-zmenu-foot` dice «7 zonas · 750 puntos de medición» (con los valores reales) y enlaza «Ver todas en el mapa →».
  - **Posición:** absoluta, bajo la pestaña «Zonas» (`top: 60px`, alineada al botón). En el CSS de layout agrega `.dx-appbar { position: sticky; }` y `.dx-zmenu { position: absolute; z-index: 30; }`.
- **`context_bar.html`**: ruta `Zonas / {{ entidad }} / {{ zona }}`, «Zona n de N» y el paginador `.dx-pager` con anterior/siguiente. Cada botón muestra el nombre de la zona vecina, y el orden es cíclico. **Solo se incluye en la ficha**, mediante `{% block context_bar %}`.

### 6.3 Layout (`base.html` + `style.css`)
- **Estructura nueva:** `body` → `header.dx-appbar` → `{% block context_bar %}{% endblock %}` → `main.page-main` → `footer`.
- **Elimina:** `aside.sidebar`, `#sidebar-toggle`, `sidebar_toggle.js` y todas las reglas `.sidebar*`, `.toggle-sidebar` y `.page-wrapper`. Quita `overflow: hidden` y `height: 100vh` de `html, body`.
- `main.page-main { max-width: 1232px; margin: 0 auto; padding: var(--space-6) var(--space-6) var(--space-12); }`.
- **Mapa nacional:** el contenedor del mapa usa `height: calc(100vh - 64px - <alto del encabezado de página>)`, con mínimo de 520px. Puede ser más ancho que 1232px (`max-width: none`) si eso mejora el resultado; compáralo con la captura.
- **Pie de página:** agrega «Ayuda y contacto» junto a la cita y la licencia.

### 6.4 Comportamiento (JS mínimo: `static/mapviewer/js/nav.js`, sin dependencias)
- **Menú de zonas:**
  - Clic en `#zonas-trigger` → alterna `hidden` y `aria-expanded`; la pestaña recibe `.is-open`.
  - Se cierra con **Esc** (y el foco regresa al botón), con clic fuera o al tabular fuera del menú.
  - Las flechas ↑/↓ mueven el foco entre `.dx-zmenu-item`, y ←/→ cambian de columna.
- **Tema:** conserva la lógica de `theme_toggle.js` (`[data-theme="dark"]`), pero con el botón de icono. Actualiza `aria-label` («Cambiar a tema oscuro/claro») y el icono luna/sol.
- **Cómo citar:** abre un `<dialog>` con la cita sugerida, en texto y en BibTeX, más un botón «Copiar». El texto de la cita queda como placeholder editable en `design.py` (`CITA_SUGERIDA`). **No inventes autores ni DOI.**
- **Móvil (< 900px):** las pestañas se ocultan (ya lo hace el CSS) y ☰ abre un panel `#menu-movil` debajo del header con las mismas secciones y las zonas desplegadas por entidad.

### 6.5 Ficha técnica
- En la vista, calcula `zona_anterior`, `zona_siguiente`, `indice` y `total` según el orden de `nav_zonas`.
- Agrega `{% block context_bar %}{% include "mapviewer/components/context_bar.html" %}{% endblock %}` en el template de la ficha.
- Quita el `<select>` de zona y el botón «Cambiar zona» solo si ya quedan cubiertos por el menú y el paginador. **Pregunta antes de quitarlo.**
- El eyebrow y el contenido de la ficha **no cambian**.

## 4. Criterios de aceptación

- [ ] No queda la barra lateral, ni rastros de `.sidebar`, `sidebar_toggle.js` o `#sidebar-toggle` (`grep -ri sidebar`).
- [ ] Las 5 pestañas funcionan y la activa es la correcta en las 6 páginas (en `/ficha_tecnica/` es «Zonas»; en `/ayuda_y_contacto/` ninguna).
- [ ] El menú de zonas lista las 7 zonas con sus conteos reales y el total. Se opera solo con teclado: Tab, Enter, flechas y Esc.
- [ ] En la ficha, la ContextBar muestra la ruta correcta, y anterior/siguiente recorren las 7 zonas en ciclo.
- [ ] El mapa nacional y la ficha usan todo el ancho, sin scroll horizontal a 1024px.
- [ ] Funciona en claro y oscuro; el resultado coincide con `reference/screens/navegacion/*`.
- [ ] A 390px: el botón ☰ abre el panel móvil y el contenido no se desborda.
- [ ] `python manage.py check` pasa y la consola no muestra errores.

## 5. Forma de trabajo

1. Explora `base.html`, los templates de cada página, `style.css`, los JS y las vistas. Presenta un plan con la lista de archivos y **espera aprobación**.
2. Implementa en este orden: 6.1 → 6.2 → 6.3 → 6.4 → 6.5. Haz commit al cerrar cada subtarea: `feat(nav): 6.x — …`.
3. Al terminar, recorre las 6 páginas en claro, oscuro y a 390px. Reporta lo que no coincida con las capturas.
