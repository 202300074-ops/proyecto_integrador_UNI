# Evidencia del visor A-Frame y MindAR

Capturas del 2026-11-08 de `apps/ar-preview` con la escena estilizada.

- `visor-escena.png`: vista completa del visor con el árbol, el jobón, las flores
  y las cuatro abejas.
- `visor-jobon.png`: acercamiento al jobón al pie del árbol y a las abejas.
- `visor-fauna.png`: visor con la fauna adicional integrada.
- `visor-fauna-escena.png`: encuadre de la escena con mariposas, libélula,
  colibrí y lagartija.
- `vr-meliponario.png`: recorrido inmersivo A-Frame 1.8 con jobón, fauna y
  hotspots informativos.
- `vr-hotspot-info.png`: panel de información abierto desde el hotspot del jobón.
- `ar-target-detectado.png`: MindAR encontró el target y mostró el diorama 3D.
- `ar-target-detectado-frame.png`: cuadro de cámara virtual usado para la prueba.
- `storyboard-cosecha.png`: seis escenas de la animación de cosecha.
- `ar-video-modal.png`: reproductor del video dentro de la experiencia AR.
- El video final está en `assets/video/cosecha-melipona-recreacion.mp4` y el
  póster en `assets/video/cosecha-poster.png`.

El visor 3D se ejecutó con Chrome headless y WebGL por SwiftShader
(`--use-angle=swiftshader --enable-unsafe-swiftshader`). La comprobación por
DevTools confirmó que `scene.time` y el `mixer` de animación avanzan, que las
cuatro abejas cambian de posición y que no hay errores de consola. Esta prueba no
mide el rendimiento real en un teléfono.

Para validar MindAR se usó una cámara de prueba de Chrome que reproduce el PNG de
la etiqueta. DevTools confirmó `targetFound`, una dimensión de target de 1200 ×
1600 y el estado de tracking activo. Es una validación de escritorio, no sustituye
la prueba con etiqueta impresa y cámara del teléfono. SwiftShader emitió avisos de
`ReadPixels` por rendimiento del render headless, sin errores de JavaScript.

La prueba del modal confirmó que el reproductor cargó el MP4 móvil y comenzó la
reproducción. MindAR pausa el procesamiento durante el modal: al simular
`targetLost`, el panel siguió abierto y el video avanzó a 6.30 s. La AR descarga
completo el derivado móvil antes de habilitar el botón. La animación y la locución
son originales/sintéticas, basadas en el guion de
`docs/referencias-video.md`.

Joshua validó la etiqueta y el video en el Galaxy A22: el target se reconoce y el
video se reproduce sin trabarse. Falta archivar una captura o grabación de esa
prueba en este directorio.

La fauna adicional se verificó por DevTools: el estado reportó cuatro abejas, dos
mariposas, una libélula, un colibrí y una lagartija; las cinco entidades nuevas
estaban visibles y no hubo errores de consola.

La prueba headless de `/vr.html` confirmó A-Frame 1.8, cuatro hotspots, tres
marcas de teletransporte, panel informativo que abre/cierra y desplazamiento al
jardín. También se añadió la narración de ~43 s y controles reproducir/pausar;
Chrome headless reprodujo hasta 2.98 s y pausó el audio sin errores. No sustituye
una prueba con casco WebXR físico.
