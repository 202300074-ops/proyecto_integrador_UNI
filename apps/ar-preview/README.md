# Meliponario 3D y realidad aumentada

Aplicación A-Frame de validación. La página `/` muestra el meliponario low-poly
con cuatro abejas en vuelo, dos mariposas, una libélula, un colibrí y una
lagartija; `/vr.html` ofrece el recorrido inmersivo con hotspots y navegación
entre zonas; `/ar.html` inicia MindAR y superpone un diorama sobre la etiqueta de
Sak P'o' Kaab.

La abeja reproduce el clip `SakPoKaab` con `animation-mixer`. El componente
`bee-wander` crea trayectorias diferentes y orienta cada abeja en la dirección de
avance. Las mariposas y la libélula reutilizan ese movimiento; `wing-flap` anima
sus alas y `foliage-sway` mueve la cola de la lagartija. Las flores se mecen y el
follaje tiene un balanceo suave.

Al detectar la etiqueta, **Ver cosecha** abre el video ilustrado dentro de la
experiencia AR. El video es una recreación didáctica con narración sintética,
basada en fuentes citadas; no es metraje documental ni representa una práctica
única de todas las comunidades. Mientras se reproduce, MindAR pausa el cálculo de
tracking para reducir carga y que una pérdida momentánea de la etiqueta no corte
el video; al cerrar el modal, el tracking se reanuda.

## Ejecutar

Desde la raíz del repositorio:

```powershell
npm --prefix apps/ar-preview install
npm --prefix apps/ar-preview run dev
```

Abre <http://localhost:5174> para el visor 3D,
<http://localhost:5174/vr.html> para el recorrido VR o
<http://localhost:5174/ar.html> para la experiencia MindAR. La cámara funciona en
`localhost` o en un sitio servido por HTTPS; concede el permiso de cámara cuando
el navegador lo solicite.

## Publicar para probar en teléfonos

La configuración raíz de `vercel.json` publica solo el build estático de esta
aplicación. Al importarla en Vercel como proyecto individual, configura
`apps/ar-preview` como raíz del proyecto; la URL principal redirige a `/ar.html`.
La tienda y la API no forman parte de este despliegue. Las rutas directas
`/ar.html` y `/vr.html` también quedan disponibles. Vercel entrega HTTPS,
necesario para pedir permiso de cámara desde celulares que acceden por internet.

Después del primer despliegue, abre la URL HTTPS en cada teléfono, concede el
permiso de cámara y visita la página de AR. Comprueba la URL en Wi-Fi y datos
móviles antes de compartirla; la detección de MindAR necesita que el teléfono
pueda descargar el target, los modelos y el video desde la misma URL.

## Recorrido VR

- `/vr.html` usa A-Frame 1.8 y activa el botón de entrada a WebXR.
- La granja ocupa un claro de 44 unidades de radio rodeado de árboles, colinas y
  maleza. El visitante puede caminar en 360° con WASD o flechas; `vr-explore`
  aplica límites de la granja y colisiones contra troncos, palapa y lago.
- Cinco hotspots muestran información del jobón, las abejas, la fauna, el cuidado
  del meliponario y un detalle escondido. En casco se activan mirando el punto
  dorado; en escritorio se apunta con la vista.
- Cinco marcas del suelo permiten teletransportarse entre el inicio, el jardín, el
  jobón, la palapa y el lago.
- El lago tiene peces animados y el entorno suma abejas ambientales, mariposas,
  libélula, colibrí y lagartija distribuidos por toda la granja.
- El panel informativo está dentro de la escena para que también se vea en VR.
- La narración es sintética; **Escuchar recorrido** y el botón AUDIO del visor
  permiten reproducirla, pausarla y retomarla.
- Guion y fuentes: `docs/referencias-vr.md`; el servidor sirve
  `assets/audio/narracion-recorrido-vr.mp3` en `/audio/narracion-recorrido-vr.mp3`.
- La compatibilidad de WebXR depende del teléfono/casco y de que la página se
  abra por HTTPS; la validación hecha hasta ahora es headless, falta probar la
  entrada con un visor físico.

### Probar WebXR en el teléfono

WebXR exige un contexto seguro. Si abres `http://<IP-LAN>:5174/vr.html` en el
teléfono, Chrome muestra “Access this site over HTTPS to enter VR mode”. Opciones:

- **USB (recomendado):** activa la depuración USB, conecta el teléfono y ejecuta
  `adb reverse tcp:5174 tcp:5174`; después abre
  `http://localhost:5174/vr.html`. `localhost` es contexto seguro y no necesita
  certificados.
- **Sin USB:** en Chrome del teléfono abre `chrome://flags`, activa “Insecure
  origins treated as secure”, agrega `http://192.168.1.107:5174` (tu IP) y
  reinicia el navegador. Es un ajuste de prueba, no de producción.
- **Túnel HTTPS:** `cloudflared tunnel --url http://localhost:5174` o `ngrok http
  5174` si no hay USB ni acceso a flags.

En pantallas táctiles aparece un joystick para caminar; en escritorio se usa WASD
o flechas. La entrada WebXR sigue dependiendo de que el dispositivo exponga un
modo inmersivo compatible.

## Etiqueta objetivo

- Fuente editable: `assets/targets/etiqueta-sakpokaab.svg`.
- Imagen PNG usada para compilar: `assets/targets/etiqueta-sakpokaab.png` (1200 ×
  1600 px).
- Target compilado: `assets/targets/etiqueta-sakpokaab.mind`.
- El target se compiló con MindAR Image Targets Compiler 1.2.5. Vuelve a compilar
  el PNG si cambia la etiqueta; los pasos de impresión están en
  `assets/targets/README.md`.

## Video de cosecha

- MP4 maestro: `assets/video/cosecha-melipona-recreacion.mp4` (720p, H.264
  Baseline/AAC, 24 fps).
- La AR usa `assets/video/cosecha-melipona-recreacion-mobile.mp4` (640 × 360) y
lo descarga completo antes de habilitar **Ver cosecha**, para reducir cortes por
buffering en móvil. El reproductor bloquea el tracking mientras está abierto y
se cierra con **Volver a AR**, Escape o el botón Atrás del teléfono.
- Guion y fuentes: `docs/referencias-video.md`.
- Audio sintético: `assets/audio/narracion-cosecha.wav` (voz Microsoft Sabina,
  es-MX; no es testimonio de una meliponicultora).

Para regenerar la locución y el MP4 en Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/generate_harvest_narration.ps1
python -m pip install -r requirements-video.txt
python scripts/render_harvest_video.py
```

## Verificaciones

```powershell
npm --prefix apps/ar-preview run build
npm --prefix apps/ar-preview run test:smoke
```

El smoke test comprueba el visor 3D, la página AR, ambos GLB, la etiqueta, el
archivo `.mind` y el MP4, incluyendo solicitudes HTTP por rango para la
reproducción/seeking.

La revisión visual del visor 3D, la fauna adicional, la captura de MindAR y el
storyboard del video están en `docs/evidencias/2026-11-08/`. MindAR detectó el
target con una cámara de prueba; Joshua validó la etiqueta y el video en el Galaxy
A22 bajo HTTPS, sin trabas de reproducción.

## Pendiente

- Archivar captura o grabación de la prueba en el Galaxy A22.
- Completar el pase manual de autoría de la abeja y el jobón en Blender; conservar
  evidencia de los cambios propios. Registrar cualquier herramienta de IA usada
  para el acabado de renders como apoyo visual.
