# Evidencia de Blender y FFmpeg

Fecha: 2026-11-04.

Objetivo: verificar la instalación de Blender y FFmpeg y generar el primer
blockout 3D de la abeja melipona y el jobón.

## Herramientas verificadas

- Blender 5.2.3 LTS, ruta:
  `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- FFmpeg 9.0.2 full build, ruta:
  `C:\Users\tiojo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe`.

FFmpeg quedó agregado al PATH del usuario; hay que abrir una terminal nueva para
usar `ffmpeg` sin la ruta completa.

## Script

`scripts/blender_blockout.py` genera una escena con:

- Abeja low-poly: abdomen con franjas, tórax, cabeza, ojos, antenas, seis patas
  y cuatro alas.
- Jobón: tronco hueco con pared, interior oscuro, bordes, tres panales con
  celdas hexagonales y dos soportes de madera.
- Cámara, luces y piso de estudio.
- Render de previews con Workbench y exportación GLB.

## Salidas

| Archivo | Contenido |
| --- | --- |
| `assets/models/blockout.blend` | Escena editable con ambos modelos. |
| `assets/models/abeja.glb` | GLB generado en esta primera iteración; el archivo se reemplazó después por la versión estilizada descrita abajo. |
| `assets/models/jobon.glb` | GLB generado en esta primera iteración; el archivo se reemplazó después por la versión estilizada descrita abajo. |
| `docs/evidencias/2026-11-04/blockout-escena.png` | Vista general. |
| `docs/evidencias/2026-11-04/blockout-abeja.png` | Acercamiento a la abeja. |
| `docs/evidencias/2026-11-04/blockout-jobon.png` | Acercamiento al jobón. |

## Verificación

Se importaron los dos GLB en una escena limpia de Blender y se midieron sus
cajas envolventes:

- `abeja.glb`: 22 mallas, tamaño aproximado 0.132 x 0.160 x 0.072 m.
- `jobon.glb`: 48 mallas, tamaño aproximado 1.240 x 0.450 x 0.575 m.

Los archivos pesan:

- `abeja.glb`: 245 KB.
- `jobon.glb`: 151 KB.
- `blockout.blend`: 172 KB.

## Reproducir

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" `
  --background --python scripts/blender_blockout.py
```

## Aviso de autoría

Este blockout es una **base generada con un script de apoyo**. No es el modelo
final ni sustituye el trabajo manual. Joshua debe abrir `blockout.blend`,
refinar proporciones, agregar detalles, texturas, rig y animación, y documentar
esos cambios con capturas o video. No se usó ningún modelo de terceros.

## Iteración estilizada y renders EEVEE

Después del blockout se escribieron `scripts/blender_model.py` y
`scripts/blender_render_eevee.py`. Los archivos actuales son:

| Archivo | Contenido |
| --- | --- |
| `assets/models/modelo.blend` | Escena estilizada editable generada por script. |
| `assets/models/abeja.glb` | Abeja para tiempo real; 9,908 triángulos y clip `SakPoKaab`. |
| `assets/models/jobon.glb` | Jobón para tiempo real; 14,852 triángulos. |
| `final-escena.png` | Toma general del jobón, abeja y flores. |
| `final-abeja.png` | Acercamiento a la abeja. |
| `final-jobon.png` | Acercamiento al jobón. |
| `final-interior.png` | Interior, panales y miel. |

Los dos GLB actuales se importaron en una escena limpia de Blender: la abeja
cargó 21 mallas y el jobón una malla. Se encontró el clip `SakPoKaab`. Aún falta
probarlos en A-Frame/MindAR y en un teléfono.

`modelo.blend` y los GLB de esta iteración se generaron mediante scripts asistidos
por IA. Antes de presentar la autoría final como propia, Joshua debe realizar y
documentar modificaciones manuales sustanciales. La guía de trabajo está en
`docs/pase-manual-3d.md`.
