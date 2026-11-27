# Video didáctico de cosecha

`cosecha-melipona-recreacion.mp4` es el máster de 53.3 segundos, 1280 × 720,
24 fps, H.264 Baseline/AAC, con subtítulos `mov_text`. `cosecha-melipona-recreacion-mobile.mp4`
es el derivado de 640 × 360 usado por la experiencia AR para reducir decodificación
y buffering en teléfonos. `cosecha-melipona-recreacion-social-vertical.mp4` es el
corte de 1080 × 1920 para redes. Los tres comparten narración, cama sonora y
duración.

El renderizador genera subtítulos SRT en español, una cama sonora original
mediante síntesis PCM y el derivado vertical. La mezcla se normalizó a -16 LUFS
aproximadamente; la medición local del máster fue -16.05 LUFS, -1.49 dBTP y LRA
3.40. La cama sonora sigue pendiente de escucha y aprobación de Joshua antes de
usarla en la defensa.

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
