---
name: blender-3d
description: Use when modeling, refining, texturing, animating, rendering, or exporting the Sak P'o' Kaab bee or jobón in Blender, including scripts/blender_*.py, assets/models/*.blend, GLB/GLTF files, and WebAR/A-Frame assets. Covers the stylized low-poly workflow, headless commands, export checks, and authorship evidence.
---

# Blender 3D para Sak P'o' Kaab

## Cuándo usarla

Usa esta skill para cualquier tarea de modelado, materiales, animación,
renderizado o exportación 3D del proyecto: la abeja melipona, el jobón, la
etiqueta AR, el meliponario VR o los videos con Blender/FFmpeg.

## Estilo y presupuesto

- Estilo: **estilizado cinematográfico**, low-poly con materiales PBR simples.
- La abeja se modela a escala de exhibición de ~14 cm; la melipona real mide
  ~1.4 cm. Documenta esta decisión y escala en A-Frame si hace falta.
- El jobón se modela a escala real: ~1.2 m de largo.
- Presupuesto objetivo: abeja < 8,000 triángulos; jobón < 15,000.
- GLB final: < 2 MB por modelo, sin cámaras, luces ni piso.
- No usar modelos de terceros. La IA es copiloto; Joshua debe refinar y
  documentar su intervención manual.

## Flujo de trabajo

1. Edita o crea el script en `scripts/blender_*.py`.
2. Ejecuta Blender en headless y genera `.blend`, `.glb` y previews.
3. Abre los previews y corrige proporciones, cámara, materiales y encuadre.
4. Repite hasta que el modelo se lea bien en teléfono y en escritorio.
5. Exporta los GLB y verifica que abren en una escena limpia.
6. Pide a Joshua un pase manual corto en la GUI y guarda evidencia.
7. Actualiza `docs/evidencias/2026-11-04/README.md`, el diario y la bitácora.

## Comandos

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" `
  --background --python "C:\Users\tiojo\dev\proyecto_integrador_UNI\scripts\blender_model.py"
```

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" `
  --background "C:\Users\tiojo\dev\proyecto_integrador_UNI\assets\models\modelo.blend" `
  --python-expr "import bpy; print('OBJETOS', len(bpy.data.objects))"
```

## Exportación GLB

- `export_format="GLB"`, `use_selection=True`, `export_apply=True`.
- Exporta solo la jerarquía del modelo; no incluyas piso, luces ni cámaras.
- Mantén `+Y up` (valor predeterminado de glTF).
- Incluye animaciones si existen; comprueba el nombre de la acción.
- Para las alas, el origen del objeto debe estar en la raíz del ala para que el
  aleteo rote alrededor del cuerpo, no del centro de la malla.

## Verificación obligatoria

- Importa cada GLB en una escena limpia y reporta:
  - número de mallas y triángulos,
  - dimensiones en metros,
  - materiales,
  - animaciones.
- Abre el GLB en A-Frame o en un visor glTF y confirma que se ve y anima.
- Revisa que el peso del archivo sea razonable para móvil.

## Evidencia y autoría

- Guarda previews en `docs/evidencias/2026-11-04/`.
- Documenta el comando exacto, la versión de Blender y los cambios.
- Joshua debe hacer al menos un ajuste manual y capturar la pantalla de Blender
  con la jerarquía y el modelo. Sin esa evidencia, el modelo no se considera
  propio para la defensa.
- En la bitácora explica qué generó la IA y qué modificó Joshua.

## Errores comunes

- En PowerShell 5.1 no uses `&&`; usa `cmd1; if ($?) { cmd2 }`.
- Workbench solo muestra el color si `material.diffuse_color` está definido.
- Las alas transparentes necesitan `Alpha` en el Principled BSDF y un método de
  mezcla; verifica el GLB, no solo el viewport.
- Si un objeto animado se exporta con el origen en el centro de la malla, el
  aleteo se ve como una hélice; corrige el origen antes de animar.
- El blockout no es el modelo final: no lo presentes como entrega terminada.

## Archivos clave

- `scripts/blender_model.py`: modelo estilizado principal.
- `scripts/blender_blockout.py`: base histórica.
- `assets/models/modelo.blend`: escena editable final.
- `assets/models/abeja.glb`, `assets/models/jobon.glb`: GLB para WebAR/VR.
- `docs/evidencias/2026-11-04/`: previews y verificación.
