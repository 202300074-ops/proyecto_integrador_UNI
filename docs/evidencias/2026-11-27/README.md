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

## Despliegue HTTPS

URL pública: <https://proyecto-integrador-uni-ten.vercel.app>

Comprobado el 27 de noviembre de 2026 desde escritorio, con Edge headless:

| Ruta | HTTP |
| --- | --- |
| `/` y `/ar.html` | 200 |
| `/vr.html` | 200 |
| `/index.html` | 200 |
| `/video/cosecha-melipona-recreacion.mp4` | 200 |
| `/video/cosecha-melipona-recreacion-mobile.mp4` | 200 |
| `/models/abeja.glb` y `/models/jobon.glb` | 200 |
| `/targets/etiqueta-sakpokaab.png` | 200 |
| `/audio/narracion-recorrido-vr.mp3` | 200 |

Capturas:

- `vercel-ar.png`: `/ar.html` en la URL pública. La prueba general de etiqueta y
  video en Vercel pasó.
- `vercel-vr.png`: `/vr.html` carga jobón, abejas y fauna. No es modo WebXR
  inmersivo; la escena casi negra del visor sigue sin diagnosticar.
- `vercel-visor.png`: visor 3D con la escena lista.
- `vercel-video.png`: el MP4 móvil se reproduce en el navegador y muestra el
  rótulo de recreación didáctica.

Esta publicación no incluye la tienda ni el checkout. Esas pruebas siguen
requiriendo la API local.

## Vista móvil del visor

`vercel-movil-visor.png` es `/index.html` a 390 × 844. Cargan el jobón, las abejas,
el árbol y las flores. Los botones de AR y VR caben. El texto superior se cortaba
a la derecha; se ajustó en `apps/ar-preview/src/style.css` para el siguiente
despliegue.

## Checkout móvil

La tienda no está en Vercel. La evidencia visible del teléfono ya estaba en:

- `carrito-cupon-movil.png`: carrito, cupón `BIENVENIDA10` y total simulado de $288.00.
- `pedido-simulado-movil.png`: pedido `SKP-MWBIEJG0-4EFF8D`, sin cobro real.

## Pase manual

Joshua confirmó el pase manual de la abeja y el jobón. El resultado se ve en el
visor móvil.

El diagnóstico WebXR del visor y la aprobación auditiva de la cama sonora quedan
para después de la entrega.
