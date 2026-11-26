# Video didáctico de cosecha

`cosecha-melipona-recreacion.mp4` es el máster de 53.4 segundos, 1280 × 720,
24 fps, H.264 Baseline/AAC. `cosecha-melipona-recreacion-mobile.mp4` es el derivado
640 × 360 usado por la experiencia AR para reducir decodificación y buffering en
teléfonos. Ambos comparten narración y duración. Las ilustraciones se generan con
Python/Pillow y se codifican/muxean con FFmpeg; no se usó metraje real.

El renderizador ahora prepara subtítulos SRT en español, genera una cama sonora
original mediante síntesis PCM y define un derivado vertical 1080 × 1920 para redes.
Estos tres elementos **todavía no están integrados en los MP4 versionados**: en la
sesión del 26 de noviembre de 2026 no se encontró FFmpeg en `PATH`, por lo que no
se regeneraron los videos. La cama sonora sí se generó como archivo WAV, pero
Joshua debe escucharla y aprobarla antes de usarla en el corte final.

La locución está en `assets/audio/narracion-cosecha.wav`, sintetizada con la voz
Microsoft Sabina (es-MX). El guion, sus límites y las fuentes están en
`docs/referencias-video.md`. `cosecha-poster.png` es el póster del video.
La cama musical candidata está en `assets/audio/cama-sonora-original.wav`.

Para regenerarlo en Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/generate_harvest_narration.ps1
python -m pip install -r requirements-video.txt
python scripts/render_harvest_video.py
```

El rótulo “Recreación didáctica” permanece visible en el video y en el reproductor
AR. El proceso ilustrado es un ejemplo; las prácticas varían entre comunidades.
