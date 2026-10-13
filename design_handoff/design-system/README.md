# DIFUSCO₂

Sistema de diseño del **Catálogo de Emisiones Naturales Difusas de CO₂**, del Instituto de Geofísica de la UNAM (Departamento de Recursos Naturales). Es una plataforma científica de consulta: debe leerse como una publicación académica y no como un producto comercial. Hay una regla que manda sobre las demás: **el color es para los datos**. La interfaz usa papel, tinta y el azul UNAM. La escala de flujo amarillo→vino se reserva para representar mediciones de CO₂.

> Versión 1 (octubre 2026). Se construyó a partir del sitio Django existente (`static/mapviewer/css/style.css`) y se reorientó a la identidad UNAM: azul y oro.

## Principios

1. **Rigor visible.** Cada cifra lleva unidad, fuente y fecha. Un mapa sin leyenda con unidades no se publica.
2. **Institucional, sin solemnidad.** Títulos en serif y datos en mono. Los filetes y el espacio en blanco hacen el trabajo que haría la decoración.
3. **El dato primero.** El mapa, la tabla y las estadísticas ocupan el centro. El texto explicativo acompaña y no compite con ellos.
4. **Accesible.** Todo texto cumple 4.5:1 en ambos temas, y la escala de flujo varía en luminosidad, no solo en tono.

## Contenido y voz

- Español formal y en impersonal o primera del plural: *"Se midió…"*, *"Este catálogo reúne…"*. Nada de tuteo de marketing.
- **CO₂ siempre con el subíndice Unicode (₂).** No se usa MathJax ni LaTeX para fórmulas en texto corrido.
- Unidades en notación SI con exponentes Unicode: `g m⁻² d⁻¹`, `t d⁻¹`. Se separan del número con un espacio: `412 g m⁻² d⁻¹`.
- Las coordenadas van en grados decimales con 5 decimales y signo menos tipográfico: `19.94552, −98.13421`.
- Fechas en ISO (`2026-10-11`) dentro de tablas y "11 de octubre de 2026" en prosa.
- Los nombres de sitio van con acentos y entidad federativa: *Los Azufres, Michoacán*; *Acoculco, Puebla*.
- Cada página lleva su crédito: autoría, tutor, Instituto, cómo citar y fecha de última actualización.

## Fundamentos visuales

### Color

| Rol | Token | Uso |
|---|---|---|
| Fondo | `paper` | Página. Tono papel, no blanco. |
| Superficie | `surface`, `surface-sunken` | Tarjetas y barra lateral; encabezados de tabla y filtros. |
| Texto | `ink`, `ink-muted` | Texto y metadatos. |
| Institucional | `unam-blue` (+ `-hover`, `-tint`, `on-unam-blue`) | Navegación activa, botón primario, enlaces y wordmark. |
| Acento | `gold`, `gold-ink`, `gold-tint` | Filete de 2px bajo el título de página, eyebrows y notas metodológicas. Se usa con moderación: un acento por pantalla. |
| Datos | `flux-1` … `flux-5` | Solo para flujo de CO₂ en mapas, leyendas, histogramas y badges de clase. |
| Estados | `success`, `danger`, `focus` | Validación de formularios y foco de teclado. |

**Escala de flujo.** Es secuencial, de cinco clases **logarítmicas por décadas** (`< 1`, `1–10`, `10–100`, `100–1000`, `≥ 1000` g m⁻² d⁻¹) y monótona en luminosidad: `flux-1` (claro) → `flux-5` (vino). Se eligió logarítmica porque el flujo medido abarca cuatro órdenes de magnitud. En el mapa, la clase se codifica dos veces: con color y con el radio del marcador (`marker-r-1…5`). El texto nunca va sobre un relleno `flux-n`: en badges y listas la clase se muestra como un punto de color junto a texto `ink`. La distribución de mapas, los controles y los marcadores se detallan en la sección **Mapas**.

### Tipografía

- **Source Serif 4**: títulos (`display`, `h1`, `h2`) y cifras KPI (`kpi`). Le da el registro académico.
- **IBM Plex Sans**: texto, navegación y controles (`h3`, `lead`, `body`, `body-sm`, `eyebrow`, `caption`).
- **IBM Plex Mono**: coordenadas, valores de tabla y unidades (`data`), con `font-variant-numeric: tabular-nums`.
- Las tres familias se cargan desde Google Fonts:
  `https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`

### Composición

- Barra lateral fija de `sidebar-width` (264px) con el wordmark y la navegación. Contenido con un máximo de `content-max` y párrafos de hasta `measure`.
- Ritmo vertical en múltiplos de 8: `space-6` dentro de tarjetas, `space-8` entre bloques y `space-12` entre secciones.
- Encabezado de página: eyebrow `gold-ink` + `h1` + `lead` + filete `gold` de 48×2px.
- Tarjetas: `surface`, borde 1px `line`, `radius-lg` y `shadow-card`. Sin bordes laterales de color.
- El mapa va dentro de una tarjeta, a todo el ancho del contenido, con leyenda propia (componente FluxLegend) y crédito del mapa base visible.
- Pie de página ligero: `surface-sunken`, `caption`, con los logotipos UNAM e IGEF, la cita sugerida y la licencia.

### Mapas

- Mapa base neutro, sin saturación (CartoDB Positron en claro, Dark Matter en oscuro), para que la escala de flujo destaque.
- Los marcadores son círculos clasificados por `flux-n`. Nada de iconos negros genéricos.
- Las capas (División política / Satelital / Relieve) van en un control segmentado arriba del mapa, no en un select.
- Hay que eliminar el texto residual de Folium "Make this Notebook Trusted…" (aparece cuando se incrusta con `_repr_html_`; conviene usar `get_root().render()`).

## Iconografía

Se usan iconos de trazo lineal (Lucide o Phosphor Regular) de 20px, en color `ink-muted` y `unam-blue` cuando están activos, siempre acompañados de texto en la navegación.

## Logotipos

Los escudos de la UNAM y del Instituto de Geofísica están en el repositorio (`static/mapviewer/img/UNAM.png`, `geofisica.png`), pero **todavía no se han subido** a este sistema. Mientras tanto, el wordmark es tipográfico: **DIFUSCO₂** en Source Serif 4 600, color `unam-blue`, con el ₂ en `gold-ink`. Los escudos institucionales van juntos, a la misma altura (40px), en el encabezado de portada y en el pie, y nunca se recolorean.

## Accesibilidad

- Contraste mínimo de 4.5:1 en texto y de 3:1 en bordes de controles (`line-strong`), iconos y anillo de foco, en ambos temas.
- Foco visible: 2px `focus` con 2px de separación.
- La información de flujo nunca depende solo del color: el popup y la tabla siempre muestran el valor numérico.
