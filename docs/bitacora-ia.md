# Bitácora de uso de IA

Borrador basado en las interacciones reales de las sesiones de trabajo. Antes de
entregar, Joshua debe revisarlo, corregir lo que no coincida con su memoria y
agregar su reflexión personal en cada entrada.

Herramienta usada: asistente de código en la terminal (opencode).
Modelo: DeepSeek V4.1 Flash Free.
Fecha de las sesiones: 2026-10-28, 2026-11-04, 2026-11-05, 2026-11-08 y
2026-11-10.

## Reglas que se acordaron

- La IA puede proponer código, comandos, textos y estructura.
- Todo dato de mercado, entrevista o métrica debe ser real y citado; no se
  inventa.
- La base actual de abeja y jobón se generó con scripts asistidos por IA. Joshua
  debe hacer y documentar modificaciones manuales sustanciales en Blender antes
  de atribuirse la autoría final, y debe poder explicar la geometría y las
  decisiones tomadas.
- No se usa el modelo de terceros "Tetragonisca angustula Bee".
- El video se declara como recreación didáctica.
- El alumno debe poder explicar todo lo que se entregue.

## 1. Arranque del repositorio y del entorno

**Pregunta o instrucción:** dejar listo el repositorio y verificar las
herramientas disponibles.

**Respuesta de la IA:** propuso una estructura de monorepo con workspaces,
comandos de Git y una lista de verificación del entorno.

**Verificación:** se comprobó Node v22.17.1, npm 10.9.2, Docker 28.3.0, Docker
Compose v2.38.1, PHP, Composer, Python 3.12.10 y Git. Se confirmó que `gh` no
estaba instalado y que Blender y FFmpeg faltaban.

**Error o aprendizaje:** no se asumió que todas las herramientas existían; se
verificaron una por una antes de escribir comandos que dependieran de ellas.

## 2. Investigación del nombre y de la lengua maya

**Pregunta o instrucción:** confirmar el significado de `kaab`, `sak p'o'` y
`xunáan kaab` antes de usarlos en la marca.

**Respuesta de la IA:** propuso la arquitectura Kaab (miel), Sak P'o' (jabón),
Xunán (cosméticos) y Jobón (velas), con la tagline "Miel y jabón de la abeja
melipona".

**Verificación:** se revisaron fuentes como Arqueología Mexicana, el diccionario
de Bastarrachea (AULEX) y materiales de la UQROO. Se confirmó que `kaab` se
asocia a miel y abeja, y que `sak p'o'` significa jabón.

**Error o aprendizaje:** una marca en maya no se inventa; se documenta la fuente
y se evita usar una palabra solo porque "suena bien".

## 3. Diseño de la base de datos

**Pregunta o instrucción:** crear el esquema para productos, variantes, pedidos y
cupones.

**Respuesta de la IA:** propuso 8 tablas: `users`, `products`,
`product_variants`, `coupons`, `orders`, `order_items`,
`coupon_redemptions` y `order_status_history`, con llaves foráneas y estados.

**Verificación:** el contenedor ejecutó `schema.sql` y `seed.sql`; se consultaron
las tablas y los conteos: 4 productos y 6 variantes.

**Error o aprendizaje:** el esquema se probó desde cero con `db:reset`, no solo
se leyó el SQL. Un esquema que no se ejecuta no es evidencia.

## 4. MySQL 8 en Docker frente a XAMPP

**Pregunta o instrucción:** decidir cómo cumplir el requisito de MySQL 8.

**Respuesta de la IA:** explicó que XAMPP trae MariaDB 10.4 y que no es
equivalente a MySQL 8; propuso un contenedor `mysql:8.4` con volumen y
healthcheck.

**Verificación:** se levantó el contenedor, se esperó el estado `healthy` y se
probó la conexión con el usuario de la aplicación.

**Error o aprendizaje:** el contenedor tardó en quedar `healthy` y la primera
consulta falló por `ECONNREFUSED` cuando Docker Desktop se detuvo. Se aprendió a
revisar `docker compose ps` y los logs antes de culpar al código.

## 5. API de catálogo

**Pregunta o instrucción:** exponer productos y variantes para la tienda.

**Respuesta de la IA:** creó una API Express con `/api/health`,
`/api/products` y `/api/products/:slug`, usando un pool de mysql2 y respuestas
JSON normalizadas.

**Verificación:** `GET /api/health` respondió `200` con `db: "up"`;
`GET /api/products` respondió `200` con 4 productos; el detalle por slug
respondió `200`; un slug inexistente respondió `404`.

**Error o aprendizaje:** la API no debe devolver `200` si la base está caída. El
endpoint de salud se probó apagando Docker y confirmando el `503`.

## 6. Catálogo React y diseño

**Pregunta o instrucción:** construir una tienda que se viera como una marca de
miel artesanal, no como una plantilla genérica.

**Respuesta de la IA:** propuso una paleta crema, verde bosque y miel, tipografía
Fraunces + Inter, tarjetas con glifos SVG y una ficha de producto accesible.

**Verificación:** `npm run build` compiló 29 módulos; se tomaron capturas de
escritorio y móvil; el diálogo se abrió y cerró con Escape.

**Error o aprendizaje:** la primera versión tenía textos sin acentos y un
desbordamiento horizontal en móvil. Se corrigieron ambos y se volvió a probar.

## 7. Corrección de acentos y codificación

**Pregunta o instrucción:** revisar por qué el catálogo mostraba "Jabon",
"Balsamo" y "Yucatan" sin acentos.

**Respuesta de la IA:** encontró que los textos estaban escritos en ASCII para
evitar problemas de codificación; propuso usar UTF-8 en el SQL y en JSX, y
agregó `SET NAMES utf8mb4`.

**Verificación:** se reinició la base con `db:reset`, se consultó la API y se
comprobó que los nombres devueltos incluyen "Jabón", "Bálsamo" y "Yucatán".

**Error o aprendizaje:** evitar acentos por miedo a la codificación produce una
interfaz peor. La solución correcta es declarar UTF-8 y probar la salida real.

## 8. Desbordamiento horizontal en móvil

**Pregunta o instrucción:** revisar por qué la vista móvil se veía cortada.

**Respuesta de la IA:** primero sospechó del tamaño del texto y del `max-w-md`;
luego identificó que las cuadrículas sin `grid-cols-1` se dimensionaban por el
contenido máximo. Agregó `grid-cols-1`, `min-w-0` y `overflow-x-hidden`.

**Verificación:** con Puppeteer a 390 px, `innerWidth = 390` y
`scrollWidth = 390`; el diálogo también se mantuvo dentro del ancho.

**Error o aprendizaje:** la primera captura con Edge headless parecía cortada,
pero el navegador imponía un ancho mínimo de 492 px. La captura no era una prueba
válida. Se cambió a una prueba con emulación de dispositivo.

## 9. Prueba automatizada de la tienda

**Pregunta o instrucción:** comprobar que el catálogo carga, que el filtro
funciona y que la ficha de producto se abre en móvil.

**Respuesta de la IA:** escribió un script temporal con Puppeteer que abre la
tienda, espera a que aparezca "Miel de melipona", mide el ancho, hace clic en
"Ver variantes", verifica el diálogo y prueba el filtro "Jabones".

**Verificación:** el script reportó 4 productos, diálogo abierto, sin
desbordamiento y el filtro mostró solo el jabón. El script se guardó fuera del
repositorio para no agregar dependencias de prueba al proyecto.

**Error o aprendizaje:** una captura de pantalla no basta como prueba. Medir
`scrollWidth`, contar tarjetas y abrir el diálogo da evidencia más sólida.

## 10. Documentación y cierre del Bloque 1

**Pregunta o instrucción:** dejar documentado lo hecho y preparar el primer
commit.

**Respuesta de la IA:** redactó README, contexto, diario, esta bitácora,
aprendizaje y los archivos de Scrum; propuso el mensaje
`feat: base del proyecto, MySQL 8, API y catálogo`.

**Verificación:** se revisó `git status`, se ejecutó el build y se confirmó que
las capturas y el JSON de la API están en `docs/evidencias/2026-10-28/`.

**Error o aprendizaje:** no se hace commit hasta que el usuario lo pida. La
documentación debe describir lo que realmente se probó, no lo que se planea.

## 11. Blender headless para el blockout 3D

**Pregunta o instrucción:** ¿hay forma de conectar la IA con Blender y FFmpeg
para ayudar a crear los modelos?

**Respuesta de la IA:** explicó que ya existe acceso a la terminal y que se puede
usar Blender en modo headless con scripts de Python, además de ejecutar FFmpeg
por línea de comandos. Se descartó el MCP de Blender por requerir más instalación
y ser más frágil para este caso.

**Verificación:** se ejecutó un script de prueba con un cubo; Blender 5.2.3
renderizó un PNG y exportó un GLB. Después se escribió
`scripts/blender_blockout.py`, que generó `blockout.blend`, `abeja.glb` y
`jobon.glb`. Los GLB se importaron en una escena limpia: la abeja tiene 22 mallas
y el jobón 48.

**Error o aprendizaje:** la primera tapa del jobón tapaba la entrada y las alas
de la abeja eran demasiado grandes; se corrigieron las proporciones y las
cámaras. El script genera una base, no el modelo final: el refinado manual y las
texturas son responsabilidad de Joshua y deben documentarse para la autoría.

## 12. Modelo estilizado y renders para WebAR

**Pregunta o instrucción:** instalar skills de Blender para el proyecto y avanzar
de la base a modelos estilizados de abeja y jobón, con una animación exportable.

**Respuesta de la IA:** se instalaron nueve skills 3D del paquete de Ari y se
escribió `scripts/blender_model.py` para generar la escena editable y los GLB. La
abeja tiene alas animadas y el jobón muestra su interior, panales y miel. También
se escribió `scripts/blender_render_eevee.py` para generar cuatro imágenes finales
con EEVEE.

**Verificación:** Blender 5.2.3 LTS generó `modelo.blend`, `abeja.glb` y
`jobon.glb`. La abeja se exporta con el clip `SakPoKaab` (9,908 triángulos); el
jobón tiene 14,852 triángulos. Ambos GLB se importaron en una escena limpia de
Blender: la abeja cargó 21 mallas y el jobón una malla; se encontró el clip
`SakPoKaab`. EEVEE completó los cuatro renders en
`docs/evidencias/2026-11-04/`. Se corrigió el fondo configurando un nodo Background
enlazado a Output World, porque `modelo.blend` no tenía mundo asignado. En esa
sesión todavía no existía el visor A-Frame, que se añadió en la entrada 13.

**Error o aprendizaje:** el exportador separaba la animación en clips por ala; se
unificó con `export_anim_scene_split_object=False`. Los renders de detalle aún
muestran una transición piso/mundo. En ese momento, el GLB aún no se había probado
en A-Frame ni en teléfono; la entrada 13 registra el visor local posterior. Los
modelos generados por script no son evidencia suficiente de autoría manual:
Joshua debe modificarlos directamente en Blender, conservar capturas del proceso
y corregir esta bitácora con su reflexión personal.

## 13. Visor A-Frame para probar los GLB

**Pregunta o instrucción:** continuar la validación de los modelos en el
navegador y preparar el paso siguiente hacia WebAR.

**Respuesta de la IA:** como el repositorio todavía no tenía una aplicación AR ni
una imagen objetivo para MindAR, se creó `apps/ar-preview`: un visor A-Frame local
que muestra abeja y jobón y reproduce el clip `SakPoKaab`. Vite sirve los GLB
directamente desde `assets/models/` durante desarrollo y los empaqueta al compilar.

**Verificación:** `npm --prefix apps/ar-preview run test:smoke` respondió
correctamente para el HTML y los dos GLB; se comprobaron el tipo MIME y la firma
`glTF`. `npm --prefix apps/ar-preview run build` compiló la página y empaquetó los
dos modelos.

**Límite actual:** el visor no usa la cámara ni integra MindAR; A-Frame y
aframe-extras se cargan desde CDN y todavía falta revisión visual en navegador.
Para el seguimiento real se requiere una imagen de etiqueta elegida/diseñada y su
archivo `.mind`; después habrá que probar con HTTPS en el teléfono.

## 14. Escena estilizada con varias abejas

**Pregunta o instrucción:** mejorar la animación, integrar el jobón en un entorno,
agregar más abejas con vuelo aleatorio, flores, vegetación y un árbol; además,
buscar referencias visuales.

**Respuesta de la IA:** se amplió `apps/ar-preview` con un meliponario low-poly:
árbol, arbusto, flores, pasto, rocas y colinas. El jobón se colocó al pie del
árbol y se rotó para mostrar su interior. Se añadieron cuatro abejas con el clip
`SakPoKaab` y el componente `bee-wander`, que genera trayectorias distintas,
orienta cada abeja y añade balanceo. Las flores, el pasto y el follaje tienen
movimiento suave propio.

**Verificación:** `npm --prefix apps/ar-preview run build` y
`npm --prefix apps/ar-preview run test:smoke` pasaron. El 2026-11-08 se revisó
visualmente con Chrome headless y WebGL por SwiftShader; la captura quedó en
`docs/evidencias/2026-11-08/visor-escena.png`. La verificación por DevTools
confirmó que `scene.time` y el `mixer` avanzaron, que las cuatro abejas cambiaron
de posición y que no hubo errores de consola.

**Referencias:** se documentaron en `docs/referencias-3d.md` la escena low-poly
"Bees in the garden", el diorama de abeja de Sketchfab, el proyecto de ArtStation
de una abeja entre flores y la documentación de A-Frame/aframe-extras. Se usaron
solo como orientación de composición y color; no se descargaron modelos de
terceros.

**Error o aprendizaje:** una animación de alas aislada no hace que la escena se
sienta viva. El movimiento debe distribuirse en varios elementos y con distintas
frecuencias; también hay que cuidar el rendimiento en teléfono, porque cada abeja
es un GLB con muchas mallas.

## 15. Etiqueta objetivo y primera integración MindAR

**Pregunta o instrucción:** el usuario eligió generar una etiqueta propia como
target para continuar con MindAR.

**Respuesta de la IA:** se creó una etiqueta imprimible con ilustración de abeja,
paleta verde/miel, marco y detalles de alto contraste. Se rasterizó el SVG a PNG
1200 × 1600 y se compiló el target con MindAR Image Targets Compiler 1.2.5. Se
añadió `/ar.html` con MindAR y un diorama a escala con jobón, árbol, flores y tres
abejas animadas. Se integró un panel que muestra la etiqueta y la guía para
imprimirla.

**Verificación:** build y smoke test pasaron. Una cámara virtual de Chrome que
reproducía la imagen de la etiqueta activó `targetFound`; DevTools confirmó el
tracking, el clip `SakPoKaab` y las tres abejas cargadas. Captura:
`docs/evidencias/2026-11-08/ar-target-detectado.png`.

**Límite actual:** es una validación de escritorio con cámara virtual. Falta
probar la etiqueta impresa en un teléfono bajo HTTPS y medir rendimiento real.

## 16. Recreación didáctica de la cosecha

**Pregunta o instrucción:** no existe un video fuente, así que se decidió crear
una recreación con IA.

**Respuesta de la IA:** se investigaron fuentes sobre la cosecha tradicional de
miel melipona y se preparó un guion que presenta un ejemplo, deja reservas a la
colonia y aclara que las prácticas varían. Se generó una animación original de
seis escenas con Python/Pillow y FFmpeg, más una locución sintética es-MX de
Microsoft Sabina. El video incluye de forma visible “Recreación didáctica · no es
metraje documental” y cita TNC México y SEMARNAT.

**Verificación:** `assets/video/cosecha-melipona-recreacion.mp4` es H.264
Baseline/AAC, 1280 × 720, 24 fps y 53.4 s. `ffmpeg` decodificó el archivo
completo y midió -16.7 dB de volumen medio y -1.5 dB de pico. Build y smoke test
pasaron. Chrome headless detectó el target, abrió el modal y confirmó que el video
avanza incluso después de simular `targetLost`. Storyboard y captura del modal:
`docs/evidencias/2026-11-08/storyboard-cosecha.png` y
`docs/evidencias/2026-11-08/ar-video-modal.png`.

**Corrección:** PowerShell 5.1 leyó tildes como ANSI en el guion de voz. Se cambió
la carga del texto a UTF-8 explícito y se regeneró la narración/video para corregir
la pronunciación de “Yucatán”. Tras el reporte de trabas, se cambió a H.264
Baseline con GOP de 2 s, se creó un derivado móvil 640 × 360 y se descarga completo
antes de habilitar el botón. MindAR pausa su procesamiento mientras se reproduce
el modal y lo reanuda al cerrar; el botón Atrás del teléfono también vuelve a la
AR sin salir de la página.

**Límite actual:** la voz es sintética, no un testimonio de una productora. Joshua
ya validó target y reproducción en el Galaxy A22; falta archivar la evidencia y
completar el pase manual de Blender.

## 17. Fauna adicional en el visor A-Frame

**Pregunta o instrucción:** Joshua pidió agregar más fauna al meliponario virtual
y comentó que usó lmik3 para mejorar los renders con un acabado estilizado.

**Respuesta de la IA:** se añadieron dos mariposas, una libélula, un colibrí y una
lagartija construidos con primitivas low-poly. Las especies voladoras reutilizan
`bee-wander` y un nuevo componente `wing-flap` para batir las alas; la lagartija
mueve la cola con `foliage-sway`. Se actualizaron el texto de estado y la leyenda
del visor. Después se creó `/vr.html` con A-Frame 1.8, cuatro hotspots, un panel
informativo dentro de la escena y tres zonas de teletransporte. También se generó
una narración sintética es-MX, con botones reproducir/pausar en la página y en la
escena.

**Verificación:** build y smoke test pasaron. Chrome headless confirmó cinco
entidades de fauna, A-Frame 1.8, cuatro hotspots, apertura/cierre del panel y
teletransporte al jardín, sin errores de consola. Evidencias:
`docs/evidencias/2026-11-08/visor-fauna.png`, `visor-fauna-escena.png` y
`vr-meliponario.png`. El control de audio reprodujo el MP3, avanzó a 2.98 s y lo
pausó; guion y referencias en `docs/referencias-vr.md`.

**Límite actual:** lmik3 se registra como apoyo visual para los renders, no como
sustituto de la edición manual en Blender. Falta que Joshua archive el proceso y
las imágenes antes/después. También falta probar el modo WebXR y la narración con
un casco físico.

## 18. Carrito, cupón y pedido simulado

**Pregunta o instrucción:** cerrar el flujo básico de compra y comprobar que el
pedido se guarda correctamente en MySQL.

**Respuesta de la IA:** se implementó el carrito en `CartPanel.jsx` con variantes,
cantidades, subtotal, cupón, datos de entrega y confirmación. En la API se
agregaron `POST /api/coupons/validate` y `POST /api/orders`, con validaciones Zod,
transacción, bloqueo de stock, descuento de inventario y registro de redención e
historial. También se creó `npm run test:commerce` para probar cupón, mínimo,
stock insuficiente y pedido, y limpiar los datos de prueba.

**Verificación:** las pruebas de API confirmaron 10 % de descuento desde $200,
rechazo por mínimo no alcanzado, `409` por stock insuficiente y `201` para un
pedido válido. La prueba de UI en Chrome headless agregó una variante, aplicó el
cupón y confirmó un pedido de $320 con descuento de $32 y total de $288. La misma
prueba a 390 px no presentó desbordamiento: `innerWidth = 390`,
`scrollWidth = 390` y panel de 390. Las capturas de escritorio y móvil quedaron en
`docs/evidencias/2026-11-10/`. Después de la limpieza,
`orders` quedó vacío, el cupón volvió a `used_count = 0` y el stock se restauró.

**Error o aprendizaje:** una prueba de compra no termina cuando la interfaz
muestra la confirmación; hay que revisar las tablas, el stock y el contador del
cupón, y dejar la base limpia. También se corrigió el `404` de favicon con un SVG
local.

**Límite actual:** el pago es simulado y el flujo aún debe probarse en el teléfono
y documentarse para la defensa.

## 19. Renders de producto e integración en la tienda

**Pregunta o instrucción:** generar renders realistas de los cuatro productos y
usarlos en la tienda.

**Respuesta de la IA:** se creó un estudio crema reutilizable en Blender con Cycles
CPU y se renderizaron miel, jabón, bálsamo y vela a 1600 × 2000. La miel se hizo
con 40 muestras y los otros tres con 32. Se ajustó el encuadre del bálsamo para no
cortar la tapa acostada y se exportaron WebP de 800 × 1000 para las tarjetas y la
ficha de producto.

**Verificación:** Blender reportó los cuatro `PRODUCT_RENDER_OK`; los tiempos
fueron 554.2 s, 329.3 s, 343.2 s y 560.5 s. `npm --prefix apps/store run build`
pasó y una captura de Chrome headless mostró las cuatro imágenes cargadas con sus
precios y stock; quedó en `docs/evidencias/2026-11-10/tienda-productos.png`. La
emulación móvil reportó `innerWidth = 390`, `scrollWidth = 390`, las cuatro
imágenes con `naturalWidth = 800` y ninguna solicitud fallida; evidencia en
`tienda-productos-movil.png`. Las cuatro URLs WebP respondieron `200 image/webp`.
`npm run test:commerce` pasó contra una API estable en el puerto 3001. Los PNG
quedaron en `docs/evidencias/2026-11-10/` y los WebP en
`apps/store/public/productos/`.

**Error o aprendizaje:** la primera miel quedó sobreexpuesta y se corrigió la
exposición. Un preview a baja resolución permite detectar encuadres cortados antes
de gastar varios minutos en un final. La etiqueta de la vela queda algo suave por
el DOF y el vidrio; si se requiere máxima nitidez, conviene enfocar el frente de la
etiqueta y cerrar un poco el diafragma.

**Límite actual:** los renders son una representación digital del caso simulado, no
fotografías de productos reales. La autoría manual en Blender sigue pendiente.

## 20. Cierre documental y QA final

**Pregunta o instrucción:** retomar el proyecto después de varios días y avanzar
con lo que falta antes de la entrega del 26–27 de noviembre.

**Respuesta de la IA:** se levantó el entorno, se ejecutó el QA final y se
consolidó la documentación. Se creó `docs/memoria.md` con el contexto, la
arquitectura, el modelo de datos, la API, la tienda, 3D, AR, VR, video, pruebas,
límites y referencias. Se creó `docs/defensa.md` con estructura de diapositivas,
guion oral, secuencia de demo, plan de respaldo, preguntas probables y checklist.
Se generó `docs/presentacion.html` como deck navegable de 12 diapositivas y
`docs/presentacion.pdf` como PDF final de 12 páginas.
También se actualizaron README, PROJECT_CONTEXT, backlog, sprint 3, AGENTS y la
guía de aprendizaje. Se ajustó el script de render de la vela para separar el
punto de foco del punto de mira y se re-renderizó con foco frontal; terminó en
863.0 s y la etiqueta quedó nítida. Se corrigió el texto de la sección Experiencia
de la tienda y se cambiaron las etiquetas internas “Sprint 2/3” por “AR” y “VR”.
La portada, el catálogo, el seed y la base activa ahora aclaran que la cooperativa
y los productos son simulados/conceptuales; los pedidos, stock y cupón no se
modificaron.

**Verificación:** MySQL `healthy`; `/api/health` con `db: "up"`; cuatro productos
y seis variantes; `npm run build`; `npm run test:commerce` con
`COMMERCE_SMOKE_OK`; `npm --prefix apps/ar-preview run build`; smoke test con
`AR_PREVIEW_SMOKE_OK`; revisión móvil por CDP con `innerWidth = 390`,
`scrollWidth = 390` y `clientWidth = 390`. Las capturas nuevas están en
`docs/evidencias/2026-11-25/`.

**Error o aprendizaje:** una captura directa de Chrome con `--window-size=390` en
Windows se recortó porque la ventana tiene un ancho mínimo; no debe usarse como
evidencia de responsive. La captura correcta se hizo con CDP y
`Emulation.setDeviceMetricsOverride`, que sí cambia el viewport de layout. También
se comprobó que el watcher de desarrollo puede interferir con la prueba de
comercio; una instancia estable de la API evita ese problema.

**Límite actual:** el QA automatizable está cerrado, pero siguen pendientes las
pruebas físicas de AR, checkout y WebXR, la evidencia formal en teléfono y el pase
manual de los modelos en Blender.

## Reflexión personal pendiente

Escribe aquí, con tus palabras:

- ¿Qué aprendiste de la base de datos y de Docker?
- ¿Qué te costó más del catálogo?
- ¿Qué harías distinto en el siguiente sprint?
- ¿Qué parte del código puedes explicar sin ayuda y cuál necesitas repasar?
