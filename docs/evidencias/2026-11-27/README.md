# Evidencias del 27 de noviembre de 2026

## Alcance

Cierre de los dos ajustes reportados durante la prueba en el Galaxy A22:

1. Las fichas de los hotspots VR no se podían cerrar y permanecían en pantalla.
2. El video de cosecha se trababa al reproducirse sobre la cámara de AR.

## Cambios verificados por código y pruebas

- `apps/ar-preview/vr.html` y `apps/ar-preview/src/vr.js`: botón DOM
  «Cerrar ficha», cierre con `Escape` y al teletransportar; se retiró la X de la
  escena para no duplicar el botón DOM.
- `apps/ar-preview/ar.html`: las ventanas conservan sus controles de texto
  «Cerrar» y «Volver a AR»; no existía una X gráfica en el código.
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
  comprobaciones correctas de apertura/cierre y visibilidad del botón, antes de
  retirar la X redundante. El smoke actualizado comprueba que la X no vuelva a
  aparecer y que los controles de cierre AR y VR sigan presentes. Esto no sustituye
  la prueba WebXR en el visor físico.

## Límite

Después de estas verificaciones, Joshua compartió una captura de `/vr.html` en
modo inmersivo. La separación en dos vistas es consistente con el modo
estereoscópico esperado, pero la escena aparece casi negra y con geometría muy
fragmentada. Se registra como defecto visual observado, no como una causa
diagnosticada ni como validación aprobada. La captura aún no está guardada como
archivo dentro del repositorio y no identifica teléfono, navegador, visor ni URL.

Antes de la defensa quedan pendientes: repetir la prueba y diagnosticar el
renderizado; validar AR/video y checkout en teléfono usando una URL HTTPS de
Vercel (GitHub reporta `success` para el deployment del commit `b735403`, pero el
dominio público aún no está anotado ni probado en teléfono); escuchar y aprobar la
cama sonora; y hacer el pase manual de los modelos en Blender. La prueba headless
y el build no sustituyen estas comprobaciones físicas.
