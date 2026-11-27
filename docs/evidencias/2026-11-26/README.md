# Evidencias del cierre — 26 de noviembre de 2026

## Verificaciones automatizadas

- `npm run build`: build de tienda completado.
- `npm run test:commerce`: `COMMERCE_SMOKE_OK`; el script limpió solo su pedido y
  restauró stock/cupón.
- `npm --prefix apps/ar-preview run test:smoke`:
  `AR_PREVIEW_SMOKE_OK` y `VR_NAVIGATION_OK` (límites, colisiones y destinos de
  teletransporte).
- `npm --prefix apps/ar-preview run build`: build del visor completado.
- `python -m unittest scripts.test_audio_bed scripts.test_subtitle_utils`: cinco
  pruebas pasaron.
- `python -m py_compile scripts/render_harvest_video.py scripts/audio_bed.py
  scripts/subtitle_utils.py`: sin errores de sintaxis.

## Capturas de interfaz

- `tienda-cierre-escritorio.png`: página de inicio y experiencia AR/VR después de
  reemplazar los placeholders; captura de Edge headless a 1440 px de ancho.
- `vr-granja-360.png`: granja VR ampliada vista desde el inicio, con palapa,
  árboles circundantes, lago con peces, hotspots y abejas; captura de Edge
  headless a 1280 × 720. La validación es visual/headless, no WebXR físico.

No se archiva una captura móvil como prueba de viewport: la ventana headless
Windows impuso un ancho mínimo. La validación móvil física sigue pendiente.

## Video regenerado

- `assets/video/cosecha-melipona-recreacion.mp4`: 1280 × 720, 24 fps, 53.34 s,
  H.264/AAC y pista de subtítulos `mov_text`; 3,680,910 bytes.
- `assets/video/cosecha-melipona-recreacion-mobile.mp4`: 640 × 360, 53.34 s,
  1,474,716 bytes.
- `assets/video/cosecha-melipona-recreacion-social-vertical.mp4`: 1080 × 1920,
  53.29 s, 2,016,522 bytes; fondo desenfocado corregido para evitar barras negras.
- `assets/video/cosecha-melipona-recreacion.srt`: diez bloques en español,
  integrados también como pista de subtítulos.
- `assets/audio/cama-sonora-original.wav`: PCM mono 22.05 kHz, 53.34 s; mezcla al
  30 % con la narración. Loudness del máster: -16.05 LUFS, -1.49 dBTP, LRA 3.40.

La revisión visual de frames y storyboard pasó. La escucha y aprobación de la
cama sonora por Joshua sigue pendiente antes de presentarla como corte final.

## Evidencia física pendiente

- Galaxy A22: AR, video y checkout.
- Visor WebXR: entrada/salida, hotspots, teletransporte y narración.
- Blender: modificaciones manuales de abeja y jobón por Joshua.
- Video: escucha y aprobación de la cama sonora por Joshua.

No se registrará como realizada ninguna prueba que no tenga captura o nota del
dispositivo correspondiente.
