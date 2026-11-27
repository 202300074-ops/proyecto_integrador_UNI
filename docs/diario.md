# Diario de trabajo

Registro breve de lo que se hizo, lo que falló y lo que sigue. Las fechas
corresponden a las sesiones de trabajo; si alguna se movió, se corrige aquí.

## 2026-10-28. Sesión de arranque

Objetivo: dejar listo el esqueleto del proyecto y la base de datos.

Hecho:

- Se creó el repositorio local y se clonó el remoto vacío de GitHub.
- Se configuró la identidad local de Git y la rama `main`.
- Se creó la estructura de carpetas: `db`, `server`, `apps/store`, `docs`,
  `scripts` y `assets`.
- Se escribieron `package.json`, `.gitignore`, `.env.example`,
  `docker-compose.yml`, `db/schema.sql` y `db/seed.sql`.
- Se escribió la API Express con salud, catálogo y detalle por slug.
- Se escribió el catálogo React con Tailwind, filtros y ficha de producto.
- `npm install` terminó con 242 paquetes.
- Se inició la descarga de la imagen `mysql:8.4` en Docker.

Problemas:

- XAMPP tiene MariaDB 10.4, no MySQL 8. Se decidió usar Docker para cumplir con
  el requisito de MySQL 8.
- La descarga de la imagen dejó el contenedor en estado `starting` durante más
  de dos minutos. Se revisaron los logs y la inicialización seguía en curso.

Decisión:

- No usar MariaDB. La base de datos del proyecto es MySQL 8.4 en Docker.

Siguiente:

- Verificar que el contenedor quede `healthy`.
- Probar la API y compilar la tienda.

## 2026-11-04. Verificación del Bloque 1

Objetivo: comprobar que la base, la API y el catálogo funcionan de punta a punta
y dejar evidencia.

Hecho:

- El contenedor `melipona-db` quedó `healthy`.
- Se verificaron las 8 tablas y los datos: 4 productos y 6 variantes.
- Se probó `GET /api/health`: `200` con `db: "up"`.
- Se probó `GET /api/products`: `200` con 4 productos y sus variantes.
- Se probó `GET /api/products/jabon-sak-po`: `200`.
- Se probó `GET /api/products/no-existe`: `404`.
- `npm run build` compiló 29 módulos sin errores.
- Se corrigieron los acentos del catálogo y de los datos de demostración.
- Se corrigió el desbordamiento horizontal en móvil con `grid-cols-1`,
  `min-w-0` y `overflow-x-hidden`.
- Se tomaron capturas de escritorio, móvil y de la ficha de producto.
- Se probó el catálogo a 390 px: `innerWidth = 390`, `scrollWidth = 390`.
- Se probó el filtro "Jabones": solo mostró el producto de jabón.

Problemas:

- Docker Desktop se detuvo después de reiniciar la base. La API respondió `503`
  con `ECONNREFUSED` al puerto 3306. Se volvió a iniciar Docker Desktop y el
  contenedor; la API se recuperó sin reiniciar el proceso de Node.
- Al lanzar procesos en segundo plano desde PowerShell, la herramienta devolvió
  un error de `ChildProcess.kill`. Los procesos sí quedaron activos; se
  verificaron con `Get-Process` y con peticiones HTTP.
- La primera captura móvil parecía cortada. Se comprobó con Puppeteer que el
  problema era el ancho mínimo del navegador headless, no el CSS. La prueba real
  a 390 px no tiene desbordamiento.

Decisión:

- La evidencia se guarda en `docs/evidencias/2026-10-28/`.
- El catálogo se considera cerrado para el Bloque 1; las fotos reales de producto
  se sustituirán en el Sprint 2 si hay tiempo.

Siguiente:

- Instalar Blender y FFmpeg.
- Modelar la abeja y el jobón.
- Implementar la etiqueta AR y el video.
- Completar el carrito y los cupones.

## 2026-11-04. Instalación de Blender/FFmpeg y blockout 3D

Objetivo: dejar listas las herramientas de modelado y video y generar una base
3D para la abeja y el jobón.

Hecho:

- Se instalaron Blender 5.2.3 LTS y FFmpeg 9.0.2 con `winget`.
- Se verificó que Blender abre en modo headless y que FFmpeg responde con la
  ruta completa; el PATH del usuario quedó actualizado.
- Se escribió `scripts/blender_blockout.py`.
- El script generó `assets/models/blockout.blend`, `abeja.glb` y `jobon.glb`.
- Se renderizaron tres previews: escena general, abeja y jobón.
- Se importaron los GLB en Blender para verificar que abren y que tienen el
  tamaño esperado.

Problemas:

- La primera versión del jobón tenía una tapa que tapaba la entrada y no dejaba
  ver los panales. Se movió y luego se quitó del blockout.
- Las alas de la abeja eran demasiado grandes y tapaban la cabeza. Se redujeron
  y se movieron hacia atrás.
- La cámara del primer acercamiento a la abeja estaba demasiado cerca; se
  corrigió la distancia y la lente.

Decisión:

- El blockout es solo una base. Joshua debe refinarlo manualmente en Blender y
  documentar el proceso para cumplir con la autoría.
- No se usa ningún modelo de terceros para la abeja ni para el jobón.

Siguiente en esa etapa:

- Abrir `blockout.blend` y refinar la abeja y el jobón.
- Agregar texturas y materiales definitivos.
- Crear el rig y la animación de alas.
- Preparar el video de cosecha con FFmpeg.

## 2026-11-04. Modelo estilizado, GLB y renders EEVEE

Objetivo: desarrollar una versión estilizada de la abeja y el jobón, exportar los
modelos para WebAR y preparar evidencia visual.

Hecho:

- Se escribió `scripts/blender_model.py`, que genera `assets/models/modelo.blend`,
  `abeja.glb` y `jobon.glb`, además de previews Workbench.
- La abeja incluye abdomen segmentado, cabeza, ojos, antenas, seis patas, alas
  con venas y animación. El GLB registra un clip `SakPoKaab` y 9,908 triángulos.
- El jobón incluye tronco hueco, piquera, soportes, tapa y panales con miel; su
  GLB tiene 14,852 triángulos.
- Ambos GLB se importaron en una escena limpia de Blender: la abeja cargó 21
  mallas y el jobón una malla; se encontró el clip `SakPoKaab`.
- Se corrigió la exportación de animación con
  `export_anim_scene_split_object=False`; sin esa opción se exportaban clips
  separados por ala.
- Se escribió `scripts/blender_render_eevee.py` y se generaron los cuatro renders
  `final-*.png` en `docs/evidencias/2026-11-04/`.
- Se configuró explícitamente el nodo de mundo en el script de render, ya que
  `modelo.blend` no tenía `scene.world`; también se ajustaron exposición,
  iluminación, piso y posición de las flores.

Problemas y pendientes:

- La primera versión de los renders tenía el fondo oscuro. El fondo crema ya se
  genera correctamente; los acercamientos todavía muestran una transición entre
  el piso y el mundo que puede pulirse si se requiere un fondo totalmente limpio.
- Los GLB todavía no se han integrado ni probado en A-Frame/MindAR o en teléfono.
- La escena base fue generada mediante scripts asistidos por IA. Joshua debe
  hacer y registrar un pase manual significativo en Blender antes de presentarla
  como trabajo propio y debe poder explicar las decisiones del modelo.

Siguiente:

- Abrir `assets/models/modelo.blend`, hacer cambios propios y guardar capturas
  del proceso de edición.
- Probar `abeja.glb` y su clip en una escena A-Frame y luego en el teléfono.
- Revisar el encuadre final de los acercamientos y documentar la versión aprobada.

## 2026-11-05. Visor A-Frame para validar GLB

Objetivo: comprobar que los GLB pueden servirse desde el proyecto y dejar un
visor A-Frame local para revisar su carga y la animación.

Hecho:

- Se creó `apps/ar-preview`, visor A-Frame con la abeja y el jobón desde
  `assets/models/`; la abeja usa `animation-mixer` con el clip `SakPoKaab`.
- Se configuró Vite para servir los GLB en desarrollo y copiarlos al build sin
  duplicar los archivos fuente dentro del repositorio.
- `npm --prefix apps/ar-preview run test:smoke` confirmó respuesta HTTP del HTML
  y de los dos GLB, incluyendo firma GLB válida.
- `npm --prefix apps/ar-preview run build` compiló el visor y empaquetó ambos
  modelos.

Pendiente:

- Revisar el visor visualmente en navegador; las dependencias de A-Frame y
  aframe-extras se cargan por CDN.
- El visor no activa cámara ni tracking MindAR. Falta una imagen de etiqueta,
  generar su archivo `.mind` e integrar el seguimiento.
- Probar bajo HTTPS en un teléfono cuando exista el target.

## 2026-11-05. Meliponario estilizado y vuelo de abejas

Objetivo: convertir el visor en una escena más viva, con el jobón integrado en un
entorno y varias abejas en movimiento.

Hecho:

- Se agregó un árbol low-poly, un arbusto, flores, pasto, rocas y colinas de fondo
  construidos con primitivas de A-Frame.
- El jobón se colocó al pie del árbol y se giró para mostrar su boca y los paneles
  interiores hacia la cámara.
- Se agregaron cuatro abejas con el mismo GLB, cada una con una trayectoria
  distinta mediante el componente `bee-wander`; el componente también orienta la
  abeja hacia su dirección de avance y añade un balanceo suave.
- Se añadieron componentes para el viento en las flores (`flower`), el pasto
  (`grass-clump`) y el follaje (`foliage-sway`), además de pequeñas motas de polen
  animadas.
- Se documentaron referencias visuales en `docs/referencias-3d.md`.

Verificación:

- `npm --prefix apps/ar-preview run build` compiló la escena.
- `npm --prefix apps/ar-preview run test:smoke` confirmó el HTML y los dos GLB.

## 2026-11-08. Verificación visual del visor

- Se revisó la escena con Chrome headless y WebGL por SwiftShader. La captura
  completa está en `docs/evidencias/2026-11-08/visor-escena.png` y el acercamiento
  del jobón en `docs/evidencias/2026-11-08/visor-jobon.png`.
- La verificación por DevTools confirmó que `scene.time` avanzó, que las cuatro
  abejas cambiaron de posición y que el `mixer` de animación avanzó; no hubo
  errores de consola.
- Se ajustaron la cámara (FOV 66), la escala del jobón (0.82) y la densidad de
  flores y pasto para que la escena se leyera mejor.
- Se añadieron cuatro flores y cuatro matas de pasto en primer plano y se
  corrigió el favicon que provocaba un 404.

## 2026-11-08. Etiqueta objetivo y primera prueba MindAR

- Se diseñó `assets/targets/etiqueta-sakpokaab.svg`, se rasterizó a
  `etiqueta-sakpokaab.png` (1200 × 1600) y se compiló con MindAR Image Targets
  Compiler 1.2.5 a `etiqueta-sakpokaab.mind` (índice de target 0).
- Se creó `/ar.html` con MindAR, cámara, estado de escaneo, vista de la etiqueta y
  un diorama a escala con jobón, árbol, cinco flores y tres abejas animadas.
- La prueba usó una cámara de Chrome que reprodujo el PNG como video. DevTools
  confirmó `targetFound: true`, tracking activo y carga del clip `SakPoKaab`.
  Evidencia: `docs/evidencias/2026-11-08/ar-target-detectado.png`.
- `npm --prefix apps/ar-preview run build` y `npm --prefix apps/ar-preview run
  test:smoke` pasaron con la página AR y el target compilado.

## 2026-11-08. Recreación didáctica de la cosecha

- Se investigaron descripciones del manejo tradicional del jobón en fuentes de
  The Nature Conservancy México y SEMARNAT. El guion aclara que las prácticas
  cambian entre comunidades y que el video no es metraje documental.
- Se generó una locución sintética es-MX con Microsoft Sabina y una animación
  original de seis escenas usando Python/Pillow + FFmpeg.
- Salida: `assets/video/cosecha-melipona-recreacion.mp4`, 53.4 s, 1280 × 720,
  24 fps, H.264 Baseline/AAC, 3.5 MB. La pista se normalizó; FFmpeg midió -16.7 dB
  de volumen medio y -1.5 dB de pico máximo.
- Para la AR se generó `assets/video/cosecha-melipona-recreacion-mobile.mp4`,
  640 × 360 y 1.34 MB, con el mismo audio/duración.
- Se corrigió la codificación de tildes en el script PowerShell para que la voz
  sintética reciba `Yucatán` y el resto del guion en UTF-8 correcto.
- El botón **Ver cosecha** abre el reproductor modal en `/ar.html` cuando se
  detecta la etiqueta. Vite sirve el MP4 con solicitudes HTTP por rango.
- Tras feedback de fluidez, se ajustó el MP4 a H.264 Baseline con keyframes cada
  2 s. La AR descarga la variante móvil completa antes de habilitar el botón; al
  reproducir, MindAR pausa el tracking y lo reanuda al cerrar el modal. Una pérdida
  simulada del target ya no interrumpe el video.
- `npm --prefix apps/ar-preview run build` y `npm --prefix apps/ar-preview run
  test:smoke` pasaron. Chrome headless confirmó target detectado, modal abierto y
  reproducción avanzando después de simular `targetLost`; storyboard en
  `docs/evidencias/2026-11-08/storyboard-cosecha.png`.

Límite actual: la narración es sintética y no se usó testimonio ni material de una
comunidad.

## 2026-11-08. Validación en teléfono y fauna adicional en el visor

- Joshua confirmó que la etiqueta y el video funcionan en el Galaxy A22 y que la
  reproducción ya no se traba. Falta archivar una captura o grabación como
  evidencia formal de esa prueba.
- Se agregaron cinco animales low-poly al visor A-Frame: dos mariposas, una
  libélula, un colibrí y una lagartija. Las mariposas, la libélula y el colibrí
  usan `bee-wander` para sus trayectorias y un nuevo componente `wing-flap` para
  batir las alas; la lagartija mueve la cola con `foliage-sway`.
- La escena actualizada se verificó con Chrome headless y WebGL por SwiftShader.
  El estado reportó “Escena lista: 4 abejas, mariposas, libélula, colibrí y
  lagartija”; las cinco entidades de fauna estaban visibles y no hubo errores de
  consola. Evidencia: `docs/evidencias/2026-11-08/visor-fauna.png` y
  `visor-fauna-escena.png`.
- `npm --prefix apps/ar-preview run build` y `test:smoke` pasaron.
- Joshua usó lmik3 para mejorar los renders con un acabado estilizado. Ese apoyo
  debe registrarse como asistencia visual; no sustituye las modificaciones
  manuales en Blender ni la evidencia del proceso de autoría.
- Se creó `/vr.html` con A-Frame 1.8, botón de entrada a WebXR, cuatro hotspots
  informativos, panel anclado a la cámara y tres puntos de teletransporte. Reutiliza
  el jobón y la fauna de la escena estilizada.
- Se generó una narración sintética es-MX de ~43 s con control reproducir/pausar
  en la barra y dentro de la escena. El MP3 es de 96 kbit/s mono; guion y fuentes
  están en `docs/referencias-vr.md`.
- Chrome headless confirmó A-Frame 1.8, cuatro hotspots, tres zonas de movimiento,
  apertura/cierre del panel y teletransporte hasta el punto jardín, sin errores de
  consola. Evidencia: `docs/evidencias/2026-11-08/vr-meliponario.png` y
  `vr-hotspot-info.png`.
- Chrome headless también reprodujo la narración hasta 2.98 s y la pausó con el
  control; el MP3 llegó a `readyState: 4` y no hubo errores.
- El build ahora incluye `vr.html`; el smoke test comprueba rutas, hotspots,
  teletransporte, fauna y archivo de audio.

## 2026-11-10. Carrito, cupón y pedido simulado

Objetivo: cerrar el flujo básico de compra y dejar evidencia verificable.

Hecho:

- Se implementó `CartPanel.jsx` con variantes, cantidades, subtotal, cupón,
  formulario de entrega y confirmación de pedido.
- La API expone `POST /api/coupons/validate` y `POST /api/orders`. El pedido usa
  transacción, bloquea el stock, descuenta inventario y registra
  `coupon_redemptions` y `order_status_history`.
- Pruebas de API: `BIENVENIDA10` aplica 10 % desde $200; un subtotal de $150
  responde `coupon_minimum_not_met`; una cantidad mayor al stock responde `409`;
  un pedido válido responde `201` y devuelve número, subtotal, descuento y total.
- `npm run test:commerce` automatiza esos casos, elimina el pedido sintético al
  terminar y restaura inventario y contador del cupón.
- Una prueba de UI en Chrome headless agregó una variante, abrió el carrito,
  aplicó el cupón y confirmó un pedido de $320 con descuento de $32 y total de
  $288, sin errores de consola ni solicitudes fallidas.
- La misma prueba a 390 px reportó `innerWidth = 390`, `scrollWidth = 390` y panel
  de 390; no hubo desbordamiento horizontal.
- Evidencias: `docs/evidencias/2026-11-10/carrito-cupon.png`,
  `pedido-simulado.png`, `carrito-cupon-movil.png` y
  `pedido-simulado-movil.png`.
- Se agregó un favicon SVG local para eliminar el `404` de `/favicon.ico`.

Verificación:

- Después de la limpieza, `orders` quedó vacío, `BIENVENIDA10` volvió a
  `used_count = 0` y el stock de las variantes se restauró.
- Build de tienda y raíz pasan; el flujo se probó contra la API y MySQL locales.

Problemas:

- La primera captura mostró un `404` de favicon. Se agregó
  `apps/store/public/favicon.svg` y una etiqueta `link` en `index.html`.
- El script temporal de limpieza necesitó ajustar la importación ESM en Windows;
  después se verificó directamente en MySQL que no quedaran pedidos de prueba.

Decisión:

- Los pedidos sintéticos de las pruebas no se conservan en la base; las capturas
  y el resultado del smoke test son la evidencia.
- El pago sigue siendo simulado y así se declara en la interfaz.

## 2026-11-10. Renders de producto e integración en la tienda

Objetivo: sustituir los glifos del catálogo por imágenes de producto coherentes
con la identidad de Sak P'o' Kaab.

Hecho:

- Se construyó un estudio crema reutilizable en Blender 5.2.3 LTS con Cycles CPU,
  cámara con DOF, ciclorama, luces de estudio y materiales procedurales.
- Se renderizó la miel a 1600 × 2000 y 40 muestras en 554.2 s; el usuario aprobó
  el resultado. La escena quedó en `assets/models/producto-miel.blend`.
- Se generaron previews de jabón, bálsamo y vela a 640 × 800 y 16 muestras. Tras
  ajustar el encuadre del bálsamo para que la tapa acostada no quedara cortada, se
  renderizaron los finales a 1600 × 2000 y 32 muestras: jabón 329.3 s, bálsamo
  343.2 s y vela 560.5 s.
- Los cuatro PNG están en `docs/evidencias/2026-11-10/producto-*-final.png`; las
  escenas, en `assets/models/producto-*.blend`.
- Se generaron versiones WebP de 800 × 1000 en `apps/store/public/productos/` y se
  integraron en `ProductCard.jsx` y en la ficha de `App.jsx`.

Verificación:

- `npm --prefix apps/store run build` pasó después de integrar las imágenes.
- La captura de Chrome headless mostró las cuatro tarjetas con sus imágenes,
  precios y stock, sin errores de carga; quedó en
  `docs/evidencias/2026-11-10/tienda-productos.png`.
- La emulación móvil por DevTools reportó `innerWidth = 390`, `scrollWidth = 390`,
  las cuatro imágenes con `naturalWidth = 800` y ninguna solicitud fallida.
  Evidencia: `docs/evidencias/2026-11-10/tienda-productos-movil.png`.
- Las cuatro URLs WebP respondieron `200 image/webp`.
- `npm run test:commerce` pasó contra una instancia estable de la API en el puerto
  3001 y limpió su pedido sintético.
- Los archivos WebP pesan entre 8.7 KB y 13.6 KB; los PNG originales se conservan
  como evidencia.

Problemas:

- La primera versión de la miel estaba sobreexpuesta; se corrigió exposición y
  balance de luces.
- La etiqueta de la vela se ve algo suave por la profundidad de campo y el vidrio;
  se aceptó para la tarjeta, pero puede repetirse con foco frontal si se necesita
  una lectura más nítida.
- La imagen horizontal del jabón deja aire arriba en formato 4:5; en la tarjeta se
  ve completa y el encuadre se puede recortar por CSS si hace falta.
- `npm run test:commerce` falló dos veces con `ECONNREFUSED`/`ECONNRESET` porque
  el watcher de desarrollo reinició la API durante la prueba. Se repitió con
  `node server/src/index.js` en el puerto 3001 y pasó.

Decisión:

- Usar las mismas imágenes en catálogo y ficha para mantener consistencia visual.
- Mantener los PNG a resolución completa como evidencia y publicar WebP ligeros.

## 2026-11-25. Cierre documental y QA final

Objetivo: retomar el proyecto después de varios días y cerrar lo que no depende
de una prueba física.

Hecho:

- Se levantó Docker Desktop, MySQL 8.4 y los servicios de tienda, API y visor.
- Se ejecutó el QA final: `/api/health` con `db: "up"`, cuatro productos y seis
  variantes, `npm run build`, `npm run test:commerce`,
  `npm --prefix apps/ar-preview run build` y el smoke test de AR/VR.
- Se capturaron evidencias nuevas en `docs/evidencias/2026-11-25/`: portada de
  escritorio, portada móvil, visor 3D y recorrido VR.
- La revisión móvil por CDP a 390 × 844 reportó `innerWidth = 390`,
  `scrollWidth = 390` y `clientWidth = 390`, sin desbordamiento horizontal.
- Se consolidó `docs/memoria.md` con contexto, arquitectura, base de datos, API,
  tienda, 3D, AR, VR, video, pruebas, límites y referencias.
- Se creó `docs/defensa.md` con estructura de diapositivas, guion oral, demo,
  plan de respaldo, preguntas probables y checklist.
- Se preparó `docs/presentacion.html` como deck navegable de 12 diapositivas y se
  exportó `docs/presentacion.pdf`; se verificó que el PDF tenga 12 páginas.
- Se actualizaron README, PROJECT_CONTEXT, backlog, sprint 3, AGENTS y la guía de
  aprendizaje.
- Se ajustó el script de renders para enfocar el frente de la etiqueta de la vela.
  El re-render terminó en 863.0 s; la etiqueta se lee nítida y se actualizaron
  `docs/evidencias/2026-11-25/producto-vela-final-foco.png` y
  `apps/store/public/productos/vela-jobon.webp`.
- Se corrigió el texto de la sección Experiencia de la tienda, que todavía decía
  “en los siguientes sprints”, y se cambiaron las etiquetas internas “Sprint 2/3”
  por “AR” y “VR”.
- Se hizo explícito en la portada, el catálogo y las fichas que la cooperativa y
  los productos son simulados/conceptuales; `db/seed.sql` y la base activa se
  actualizaron sin tocar pedidos, stock ni cupón.

Verificación:

- `COMMERCE_SMOKE_OK` y `AR_PREVIEW_SMOKE_OK`.
- Build de tienda y visor sin errores.
- Capturas finales revisadas; la portada móvil se tomó con emulación de
  dispositivo, no con una ventana de 390 px, para evitar el recorte mínimo de
  Chrome en Windows.

Problemas:

- Una captura móvil directa con `--window-size=390` se recortó por el tamaño
  mínimo de ventana de Chrome. Se corrigió usando CDP y
  `Emulation.setDeviceMetricsOverride`.
- La etiqueta de la vela se veía suave por el DOF. Se añadió un objetivo de foco
  separado del punto de mira y se re-renderizó con f/7.1; la composición se
  conservó y la etiqueta quedó nítida.

Decisión:

- Mantener la documentación y el QA automatizable cerrados; dejar para Joshua las
  pruebas que requieren teléfono, cámara, casco y edición manual en Blender.

## 2026-11-26. Ajustes frente a la guía de regularización

Objetivo: contrastar el estado del repositorio con la guía y cerrar hoy las
brechas que podían resolverse con código y documentación sin inventar pruebas ni
datos.

Hecho:

- Se prepararon dos mapas conceptuales SVG y un plan de mercadotecnia con perfiles
  hipotéticos, calendario, criterios para colaboraciones y fórmulas de medición.
  No se presentaron entrevistas, acuerdos ni resultados como reales.
- Se implementó un panel local de pedidos `mock`, de solo lectura, máximo 25
  registros, sin datos personales y no disponible en producción. La prueba de
  comercio valida el campo resumido y limpia únicamente su pedido temporal.
- Se añadió el símbolo animado 2D en SVG con respeto a `prefers-reduced-motion`.
- Se redactaron manual técnico, manual de usuario, declaración de IA y anexo de
  diez interacciones seleccionadas. La reflexión personal del alumno queda
  pendiente.
- Se numeraron referencias y citas de la memoria; se generaron `docs/memoria.html`
  y `docs/memoria.pdf`. La portada mantiene pendiente el nombre oficial de la
  institución.
- Se actualizó la presentación a 13 diapositivas y se exportó nuevamente a PDF.
- El renderizador de video ahora prepara subtítulos SRT, una cama sonora original
  y una exportación vertical. Se generaron el SRT y el WAV candidato.
- Se capturó `docs/evidencias/2026-11-26/tienda-cierre-escritorio.png` con Edge
  headless a 1440 px; la imagen incluye la portada, catálogo y tarjetas AR/VR
  actualizadas.

Verificación:

- `npm run build` pasó después de los cambios en la tienda.
- `npm run test:commerce` pasó con una API estable en el puerto 3001 como
  `COMMERCE_SMOKE_OK`; se restauraron los datos de la prueba.
- `npm --prefix apps/ar-preview run test:smoke` pasó como `AR_PREVIEW_SMOKE_OK`.
- `python -m unittest scripts.test_audio_bed scripts.test_subtitle_utils` pasó
  cinco pruebas; `py_compile` de los scripts multimedia pasó.
- El PDF de memoria se generó en 11 páginas y el de presentación en 13 páginas.

Problemas y pendientes:

- Blender y FFmpeg no se encontraron en `PATH`. No se pudo realizar el pase
  manual de autoría de Joshua ni regenerar los MP4; los subtítulos y la cama
  musical aún no están integrados en el video final.
- La cama sonora se generó, pero Joshua debe escucharla y aprobarla.
- No se hicieron pruebas físicas de Galaxy A22 ni WebXR durante esta sesión. No
  se registran como evidencia realizada.
- La captura móvil directa de Edge no se conservó como evidencia porque el ancho
  mínimo de ventana en Windows no garantiza un viewport de 390 px.
- La bitácora y la portada del PDF requieren la revisión personal del alumno y el
  nombre institucional oficial, respectivamente.

Decisión:

- Registrar las estimaciones de Sprint 4 como propuestas y no reconstruir valores
  históricos de burndown que no estén documentados.
- Mantener el panel como demostración local y sin datos personales; no convertirlo
  en administración de pedidos reales.

## 2026-11-26. Granja VR explorable en 360°

Objetivo: ampliar `/vr.html` para que el recorrido no se limite al frente de la
escena y se sienta como una granja melipona acogedora y explorable; la AR se
mantiene acotada a la etiqueta.

Cambios:

- Terreno circular de 44 unidades de radio (`vr-farm-ground`), niebla más abierta
  y nueve colinas alrededor del claro.
- Trece árboles con el componente `farm-tree` distribuidos en todas las
  direcciones, además de arbustos, flores, pasto y rocas.
- Componente `vr-explore` sobre el rig de cámara: caminata con WASD/flechas,
  límite de la granja y colisiones contra troncos, palapa y lago mediante
  `src/vr-navigation.js`.
- Lago con banco de tierra, agua translúcida y tres peces animados
  (`pond-fish`); nueva zona de teletransporte **LAGO**.
- Cuatro abejas ambientales ligeras (`ambient-bee`), seis abejas GLB y fauna
  repartida por toda la granja (mariposas, libélula, colibrí y lagartija).
- Palapa con jobones adicionales y un detalle escondido (`vr-easter-egg`) que
  añade el quinto hotspot.
- Cinco teletransportes: inicio, jardín, jobón, palapa y lago.
- Joystick táctil para caminar en teléfono; en escritorio se conserva WASD o
  flechas. Se corrigió la velocidad del movimiento diagonal.
- Al abrir `/vr.html` desde el Galaxy A22 por `http://192.168.1.107:5174`, Chrome
  bloqueó la entrada a VR por contexto inseguro. Se documentó el uso de
  `adb reverse tcp:5174 tcp:5174` con `http://localhost:5174` y la alternativa de
  un túnel HTTPS; la entrada WebXR física sigue sin validarse.

Verificación:

- `npm --prefix apps/ar-preview run test:smoke` pasó con `AR_PREVIEW_SMOKE_OK` y
  `VR_NAVIGATION_OK`; la prueba de navegación valida límites, colisiones y que
  los cinco destinos de teletransporte caen en suelo libre.
- `npm --prefix apps/ar-preview run build` y `npm run build` pasaron.

Límite: la validación es headless y de navegación; la comodidad, escala y entrada
WebXR siguen pendientes de un visor físico.

## 2026-11-26. Regeneración del video con FFmpeg

Objetivo: integrar en los MP4 los subtítulos, la cama sonora y la exportación
vertical que ya estaban preparados en el renderizador.

Hecho:

- Se regeneró el máster de 53.34 s, 1280 × 720, 24 fps, H.264/AAC, con pista de
  subtítulos `mov_text` y 3,680,910 bytes.
- Se regeneró el derivado móvil de 640 × 360 y 1,474,716 bytes para la AR.
- Se generó el corte vertical 1080 × 1920 y se corrigió el fondo desenfocado para
  que no quedara en negro.
- Se actualizaron el SRT de diez bloques, la cama sonora PCM, el póster y el
  storyboard. La mezcla del máster midió -16.05 LUFS, -1.49 dBTP y LRA 3.40.
- Se revisaron visualmente frames del máster y del vertical, además del storyboard.

Límite: la cama sonora sigue pendiente de escucha y aprobación de Joshua; no se
presenta como corte final aprobado.

## 2026-11-27. Cierre de fichas VR y fluidez del video AR

Objetivo: terminar los dos ajustes reportados en la prueba del Galaxy A22: las
fichas de los hotspots VR no se cerraban y el video de cosecha se trababa al
reproducirse sobre la cámara de realidad aumentada.

Hecho:

- VR: se añadió un botón DOM «Cerrar ficha» con estilos propios y se centralizó
  el cierre en `closeInfoPanel`. Para evitar dos controles de cierre, después se
  retiró la X dibujada dentro de la escena. La ficha se cierra con el botón,
  `Escape` o al usar un teletransporte.
- AR: los paneles ya tienen botones de texto «Cerrar» y «Volver a AR»; se comprobó
  el código y no había una X gráfica separada que retirar.
- AR: al abrir «Ver cosecha» se pausa MindAR y el render de A-Frame, se oculta el
  canvas AR y se retira el `backdrop-filter`; al cerrar se reanuda la cámara y el
  render.
- El smoke test ahora verifica el botón de cierre, el componente de escena, los
  estilos del botón y las funciones de pausa/reanudación del video.

Verificación:

- `npm --prefix apps/ar-preview run test:smoke`: `AR_PREVIEW_SMOKE_OK` y
  `VR_NAVIGATION_OK`.
- `npm --prefix apps/ar-preview run build` y `npm run build` pasaron.
- `python -m unittest scripts.test_audio_bed scripts.test_subtitle_utils`: 5
  pruebas correctas.
- Prueba funcional headless con Edge y CDP sobre `/vr.html`: comprobó apertura y
  cierre de ficha con botón DOM, `Escape` y teletransporte. El smoke actual comprueba
  que no reaparezca el control X redundante y que los botones AR de cierre sigan
  presentes.

Límite: la fluidez del video y el cierre de fichas siguen pendientes de prueba
física en el Galaxy A22 y en un visor WebXR; la validación de esta sesión es de
código, build, smoke y navegador headless.

## 2026-11-27. Incidencia visual reportada en modo WebXR

Observación reportada por Joshua mediante una captura de `/vr.html` en modo
inmersivo:

- Se ven dos vistas lado a lado, consistente con la presentación estereoscópica
  esperada en VR.
- La escena aparece casi negra y algunas formas del entorno tienen artefactos de
  alto contraste y fragmentación. Esa calidad no es aceptable para dar la prueba
  WebXR por aprobada; sí es un defecto visual observable en la captura.
- La captura no identifica teléfono, versión de Chrome, visor, URL ni condiciones
  de la prueba, y no se ha archivado como archivo dentro del repositorio. Por eso
  no se atribuye todavía a las luces, al código, a la GPU ni al visor.

Siguiente diagnóstico: comparar `/vr.html` fuera y dentro del modo inmersivo en el
mismo teléfono; anotar modelo, navegador/versión, visor y URL/commit; repetir en
otro dispositivo compatible si está disponible. Solo después ajustar iluminación,
renderer o calidad gráfica según el resultado.

## Pendientes inmediatos

- Hacer el pase manual de la abeja y el jobón en Blender y guardar evidencia de
  las modificaciones propias. Registrar lmik3 como apoyo de render, si se usa.
- Archivar la evidencia de la prueba de etiqueta, video y checkout en el Galaxy
  A22.
- Diagnosticar y volver a probar `/vr.html` en modo WebXR: la captura compartida
  muestra una imagen casi negra y fragmentada; comprobar también comodidad/escala.
- Validar narración y controles de audio en un dispositivo WebXR real.
- GitHub reporta estado Vercel `success` para `b735403`; obtener el dominio de
  producción y probar `/ar.html` por HTTPS antes de compartir la URL.
- Guardar la captura WebXR como evidencia e identificar dispositivo, navegador,
  visor y URL usados.
- Completar la reflexión personal pendiente en `docs/bitacora-ia.md`.
- Ensayar `docs/defensa.md` y la presentación durante 20 minutos; reservar al
  menos 15 minutos de preguntas y practicar el cambio en vivo de unos 10 minutos.
- Hacer el commit solo cuando Joshua lo solicite.
