# Cómo aplicar la nueva navegación con Claude Code (VS Code)

## Antes de empezar

- Trabaja en una rama nueva: `git checkout -b feat/navegacion-superior`.
- Ten el servidor local listo (`python manage.py runserver`) para revisar cada paso.

## Paso 1 — Copiar el paquete al repositorio

1. Descomprime `design_handoff_navegacion.zip`.
2. Copia **el contenido** de la carpeta `design_handoff/` dentro de la carpeta `design_handoff/` que ya existe en la raíz del repo y acepta reemplazar archivos. Se agregan `HANDOFF_NAVEGACION.md`, `PROMPT_NAVEGACION.md`, `design-system/Navegacion.md`, las guías nuevas y `reference/screens/navegacion/`. Se actualizan `components.css` y `components-reference.js`.
3. Haz commit: `git add design_handoff && git commit -m "docs(diseño): handoff fase 6 navegación"`.

## Paso 2 — Actualizar CLAUDE.md

Reemplaza la sección «Diseño (DIFUSCO₂)» de tu `CLAUDE.md` por el contenido de `design_handoff/CLAUDE.md.snippet`. La línea clave es «No hay barra lateral»: evita que Claude Code la reconstruya en sesiones futuras.

## Paso 3 — Abrir Claude Code en modo plan

1. En VS Code, abre el panel de Claude Code.
2. Empieza una **conversación nueva**, sin el contexto de las fases anteriores.
3. Selecciona el modelo más fuerte que tengas y activa el **modo plan**.
4. Pega el **prompt 1** de `PROMPT_NAVEGACION.md`.

## Paso 4 — Revisar el plan

Antes de aprobar, verifica que el plan incluya:

- Crear `context_processors.py` y registrarlo en `settings.py`.
- Crear tres partials: `app_header.html`, `zone_menu.html` y `context_bar.html`.
- Modificar `base.html`, `style.css` y el template y la vista de la ficha.
- Crear `nav.js` y eliminar `sidebar_toggle.js`.
- **No** tocar la generación de mapas ni el contenido de las fichas.

Si propone cambiar algo de los mapas o de los datos, corrígelo antes de aprobar.

## Paso 5 — Implementar por subtareas

Pega el **prompt 2**. Después de cada subtarea (6.1 … 6.5):

- Recarga el sitio y revisa la página afectada.
- Si algo no coincide con las capturas, díselo con la imagen: arrástrala desde `reference/screens/navegacion/` al chat.
- Si la conversación se alarga mucho, abre una nueva y escribe: «Continúa con la subtarea 6.x de design_handoff/HANDOFF_NAVEGACION.md».

## Paso 6 — Verificación final

Pega el **prompt 3**. Luego revisa tú mismo:

- [ ] Las 6 páginas en claro y oscuro.
- [ ] El menú «Zonas» funciona con mouse y con teclado (Tab, flechas, Esc).
- [ ] Los botones anterior/siguiente de la ficha recorren las 7 zonas.
- [ ] En el celular, o con DevTools a 390px, funciona el botón ☰.

## Paso 7 — Publicar

Haz merge a tu rama principal y despliega en Cloud Run como siempre. Antes de considerarlo terminado, revisa el sitio publicado.

## Pendientes que debes completar tú

- El texto de **«Cómo citar»** (autores, año, DOI si existe) en `CITA_SUGERIDA` de `mapviewer/design.py`.
- Confirmar con tu tutor la unidad g m⁻² d⁻¹ y el método de medición.
- Las coordenadas de Michoa, Alcaparrosa y Azufres (ver `HANDOFF.md §7`).
