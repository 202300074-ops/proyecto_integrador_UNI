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

## Evidencia física pendiente

- Galaxy A22: AR, video y checkout.
- Visor WebXR: entrada/salida, hotspots, teletransporte y narración.
- Blender: modificaciones manuales de abeja y jobón por Joshua.
- Video: escucha/aprobación de la cama sonora y revisión visual/audio de los MP4
  regenerados con FFmpeg.

No se registrará como realizada ninguna prueba que no tenga captura o nota del
dispositivo correspondiente.
