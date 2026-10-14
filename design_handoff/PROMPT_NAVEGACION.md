# Prompts para Claude Code — Fase 6 (navegación)

## 1. Prompt inicial (modo plan)

```
Vamos a cambiar la navegación del sitio: la barra lateral se reemplaza por una barra superior institucional. El diseño ya está aprobado.

1. Lee completo design_handoff/HANDOFF_NAVEGACION.md, después design_handoff/design-system/Navegacion.md y las guías AppHeader.md, ZoneMenu.md y ContextBar.md. Revisa la sección "NAVEGACIÓN v3" de design_handoff/design-system/components.css y las funciones AppHeader, ZoneMenu y ContextBar de design_handoff/reference/interactive/components-reference.js.
2. Abre las imágenes de design_handoff/reference/screens/navegacion/: son el objetivo visual.
3. Explora base.html, los templates de las 6 páginas, style.css, los JS y las vistas. Preséntame un plan con la lista exacta de archivos que vas a crear, modificar y eliminar. No cambies nada todavía.

Reglas: no toques el contenido de los mapas ni de las fichas. No inventes estilos: usa las clases dx-* y los tokens. No modifiques datos. No inventes autores ni DOI para la cita.
```

## 2. Después de aprobar el plan

```
Aprobado. Implementa la subtarea 6.1 de HANDOFF_NAVEGACION.md, haz commit y resúmeme lo hecho. Luego sigue con 6.2, una subtarea a la vez.
```

## 3. Cierre

```
Verifica todos los criterios de aceptación de la §4 de HANDOFF_NAVEGACION.md. Recorre las 6 páginas en claro, oscuro y a 390px de ancho, compáralas con reference/screens/navegacion/ y dime qué no coincide.
```
