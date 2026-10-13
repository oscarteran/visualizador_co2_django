# Prompt para Claude Code (copiar y pegar)

```
Vamos a rediseñar este sitio Django siguiendo un design system ya aprobado.

1. Lee completo design_handoff/HANDOFF.md y después todos los archivos que lista en la §1, en ese orden. Abre las imágenes de design_handoff/reference/screens/ para ver el objetivo visual.
2. Explora el repo (templates, static, views, la generación de mapas con Folium) y preséntame un plan de la Fase 1 con la lista exacta de archivos que vas a crear o modificar. No cambies nada todavía.
3. Cuando lo apruebe, implementa UNA fase a la vez. Al cerrar cada fase: corre `python manage.py check`, compara con las capturas de referencia, haz commit y dame un resumen.

Reglas: el diseño está en design_handoff/design-system/ y es la fuente de verdad. No inventes estilos, no uses valores hex fuera de tokens.css y design.py, y no corrijas datos: repórtalos.
```

## Comando para fases siguientes

```
Continúa con la Fase N de design_handoff/HANDOFF.md. Antes de terminar, verifica los criterios de aceptación que apliquen.
```
