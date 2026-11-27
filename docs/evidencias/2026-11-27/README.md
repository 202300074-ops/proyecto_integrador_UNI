# Evidencias del 27 de noviembre de 2026

## Alcance

Cierre de los dos ajustes reportados durante la prueba en el Galaxy A22:

1. Las fichas de los hotspots VR no se podían cerrar y permanecían en pantalla.
2. El video de cosecha se trababa al reproducirse sobre la cámara de AR.

## Cambios verificados por código y pruebas

- `apps/ar-preview/vr.html` y `apps/ar-preview/src/vr.js`: botón DOM
  «Cerrar ficha», cierre con la X de la escena, con `Escape` y al teletransportar.
- `apps/ar-preview/src/vr.css`: estilos del botón de cierre, visible solo con la
  ficha abierta y adaptado a pantallas táctiles.
- `apps/ar-preview/src/ar.js` y `apps/ar-preview/src/ar.css`: pausa de MindAR y
  del render de A-Frame, ocultamiento del canvas y retiro del `backdrop-filter`
  mientras se reproduce el video; reanudación al cerrar.
- `apps/ar-preview/scripts/smoke-test.mjs`: cobertura de los nuevos controles.

## Verificación automatizada

- `npm --prefix apps/ar-preview run test:smoke`:
  `AR_PREVIEW_SMOKE_OK` y `VR_NAVIGATION_OK`.
- `npm --prefix apps/ar-preview run build`: correcto.
- `npm run build`: correcto.
- `python -m unittest scripts.test_audio_bed scripts.test_subtitle_utils`: 5
  pruebas correctas.
- Prueba funcional headless con Edge y el protocolo CDP sobre `/vr.html`: diez
  comprobaciones correctas (ficha oculta al inicio, apertura por hotspot, cierre
  por botón DOM, X de la escena, `Escape` y teletransporte, y visibilidad del
  botón). No sustituye la prueba WebXR en el visor físico.

## Límite

No se registra una prueba física nueva del 27 de noviembre: no había Galaxy A22
ni visor WebXR conectados. La fluidez del video y la comodidad de las fichas
deben confirmarse en el dispositivo antes de la defensa. La cama sonora sigue
pendiente de escucha y aprobación de Joshua.
