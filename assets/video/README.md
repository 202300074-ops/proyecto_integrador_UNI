# Video didáctico de cosecha

`cosecha-melipona-recreacion.mp4` es el máster de 53.4 segundos, 1280 × 720,
24 fps, H.264 Baseline/AAC. `cosecha-melipona-recreacion-mobile.mp4` es el derivado
640 × 360 usado por la experiencia AR para reducir decodificación y buffering en
teléfonos. Ambos comparten narración y duración. Las ilustraciones se generan con
Python/Pillow y se codifican/muxean con FFmpeg; no se usó metraje real.

La locución está en `assets/audio/narracion-cosecha.wav`, sintetizada con la voz
Microsoft Sabina (es-MX). El guion, sus límites y las fuentes están en
`docs/referencias-video.md`. `cosecha-poster.png` es el póster del video.

Para regenerarlo en Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/generate_harvest_narration.ps1
python -m pip install -r requirements-video.txt
python scripts/render_harvest_video.py
```

El rótulo “Recreación didáctica” permanece visible en el video y en el reproductor
AR. El proceso ilustrado es un ejemplo; las prácticas varían entre comunidades.
