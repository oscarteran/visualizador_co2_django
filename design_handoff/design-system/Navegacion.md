# Navegación

Revisión de la barra lateral del sitio publicado (13 de octubre de 2026) y dos propuestas.

> **Decisión (13 de octubre de 2026): se adopta la Propuesta A, barra superior institucional.** La Propuesta B se conserva solo como referencia.

## Diagnóstico de la barra lateral actual

| Observación | Por qué importa |
|---|---|
| Ocupa 264px fijos (≈ 26% del ancho a 1024px) | Los mapas y la ficha son el producto, y la barra les quita una cuarta parte del espacio para mostrar seis enlaces. |
| Seis enlaces planos, sin jerarquía | «Catálogo», «Inventario Nacional» y «Ficha técnica» suenan a lo mismo. Quien llega por primera vez no sabe por dónde empezar. |
| Las zonas no aparecen | Un investigador piensa por sitio («quiero ver Escalera»). Hoy tiene que entrar a Ficha técnica y usar un `<select>`. |
| Un hueco vacío entre los dos grupos | Se ve sin terminar y empuja el botón de tema hasta el fondo. |
| Un botón flotante «‹» para colapsar, pegado al borde | Es poco descubrible y rompe la línea de la barra. |
| El botón de tema ocupa un lugar destacado | Es una preferencia secundaria; merece un icono, no un botón ancho. |
| Faltan la cita, la versión de datos y la fecha | Es lo que un científico busca para reutilizar el dato. |

## Principios para un público científico

1. **Lo predecible le gana a lo ingenioso.** Etiquetas literales, sin iconos sin texto en el estado normal y la misma ubicación en todas las páginas.
2. **Un clic a cualquier zona** desde cualquier página.
3. **Recorrido sistemático:** poder pasar de una zona a la siguiente sin volver al menú.
4. **Reproducibilidad visible:** «Cómo citar» y la versión de los datos siempre a la mano.
5. **El espacio horizontal es para los datos.**

## Propuesta A — Barra superior institucional *(recomendada)*

```
┌──────────────────────────────────────────────────────────────────────────┐
│ DIFUSCO₂ │ IGEF·UNAM   Inicio  Mapa nacional  Zonas ▾  Datos y fuentes  Acerca de   ❝ Cómo citar  ☾ │  AppHeader 64px
├──────────────────────────────────────────────────────────────────────────┤
│ Zonas / Puebla / Alcaparrosa                  Zona 2 de 7  [‹ Acoculco][Los Azufres ›] │  ContextBar 44px (solo fichas)
├──────────────────────────────────────────────────────────────────────────┤
│                     contenido a todo el ancho (máx. 1232px)              │
```

- **AppHeader**: wordmark + institución, cinco pestañas y las herramientas (Cómo citar, tema). Es fijo arriba.
- **Zonas ▾** abre **ZoneMenu**: las 7 zonas en columnas por entidad, con su conteo de puntos y el total.
- **ContextBar**, solo en fichas: la ruta y los botones anterior/siguiente con el nombre de la zona vecina, más la posición «Zona n de 7».
- Es el patrón de los portales de datos institucionales (USGS, NOAA, SGM). Se reconoce sin aprenderlo.
- **Móvil (< 900px):** las pestañas pasan a un botón ☰ que abre un panel con las mismas secciones y las zonas desplegadas.

**Renombres sugeridos** (solo etiquetas, mismas URLs): Catálogo → **Inicio** · Inventario Nacional → **Mapa nacional** · Ficha técnica → **Zonas** (cada ficha es una zona) · Fuentes de información → **Datos y fuentes**. «Ayuda y contacto» pasa al pie de página.

## Propuesta B — Barra lateral exploradora

- Conserva la columna, pero baja a 248px y la organiza en tres grupos: **Explorar** (Inicio, Mapa nacional), **Zonas** (árbol por entidad con conteo, cada zona un enlace directo) y **Referencia** (Datos y fuentes, Acerca de).
- Al pie lleva la versión de los datos, el total de mediciones, «Cómo citar» y el tema.
- Se **contrae** a un riel de iconos de 60px con el botón ◫ del encabezado, y el estado se recuerda con `localStorage`.
- Sirve si se espera que el catálogo crezca a decenas de zonas. A partir de ~20 zonas, el árbol escala mejor que un mega-menú.

## Comparación

| Criterio | A · Barra superior | B · Lateral exploradora |
|---|---|---|
| Ancho para mapa y ficha | **100%** | 100% − 248px (o − 60px contraída) |
| Acceso a una zona | 2 clics (Zonas ▾ → zona) | **1 clic** (siempre visible) |
| Recorrer zonas en orden | **Anterior/siguiente** | Clic en la lista |
| Familiaridad para investigadores | **Alta** (portales de datos) | Media (patrón de aplicación) |
| Escala a muchas zonas | Hasta ~20 en el menú; luego, buscador | **Alta** (árbol con scroll) |
| Esfuerzo de implementación | Medio: cambia `base.html` y el layout | Bajo: cambia solo la barra |

## Implementación (Propuesta A)

- `base.html`: el `.page-wrapper` pasa de flex horizontal a flujo vertical: `header.dx-appbar` → `{% block context_bar %}` → `main` → `footer`. Se eliminan `aside.sidebar` y el botón `#sidebar-toggle` junto con `sidebar_toggle.js`, y se quita `overflow: hidden` de `html, body`.
- Partials nuevos: `components/app_header.html`, `components/zone_menu.html` y `components/context_bar.html`.
- Las zonas del menú salen de un **context processor** (`mapviewer/context_processors.py → zonas_nav`) con nombre, entidad, conteo y slug, para que estén disponibles en todas las páginas.
- ZoneMenu: un `<button aria-haspopup="true" aria-expanded>` con JS mínimo que abre al clic, cierra con Esc o clic fuera y se navega con flechas. Sin JS, «Zonas» enlaza a `/inventario_nacional/`.
- En la vista de ficha, anterior y siguiente se calculan en Python según el orden del catálogo.
- El mapa nacional ocupa `calc(100vh − 64px − encabezado de página)`.
- No se toca el contenido de los mapas ni de las fichas: solo el contenedor gana ancho.
