# Memoria del proyecto Sak P'o' Kaab

- **Institución:** Universidad Politécnica de Quintana Roo (UPQRoo)
- **Alumno:** Joshua Israel Cabrera Camacho
- **Matrícula:** 202300074
- **Materia:** Multimedia y Diseño Digital
- **Entrega:** 26 y 27 de noviembre de 2026
- **Defensa:** 30 de noviembre al 4 de diciembre de 2026
- **Repositorio:** <https://github.com/202300074-ops/proyecto_integrador_UNI>

## Aviso académico

Este proyecto documenta un **caso de estudio simulado**. La cooperativa, la marca
y el meliponario no existen como empresa real. No se realizaron entrevistas ni se
inventaron testimonios, métricas o productos reales. Los datos de contexto
provienen de fuentes públicas citadas en este documento y en los archivos de
referencias del repositorio.

El video de la cosecha es una **recreación didáctica original** y se declara así
en la interfaz y en esta memoria: **“Recreación didáctica · no es metraje
documental”**. La voz es sintética y no se atribuye a ninguna persona o
comunidad.

Los modelos 3D de la abeja y el jobón se construyeron con scripts asistidos por
IA. La autoría manual final corresponde a Joshua y debe sustentarse con el pase
manual en Blender descrito en `docs/pase-manual-3d.md`. Mientras ese pase no esté
completado y documentado, los modelos no se presentan como totalmente manuales.
No se utilizó el modelo de terceros “Tetragonica angustula Bee” de
Nyilonelycompany.

## 1. Resumen ejecutivo

Sak P'o' Kaab es una tienda en línea y una experiencia multimedia alrededor de la
miel y el jabón de la abeja melipona. El proyecto integra una base de datos
MySQL, una API REST, una tienda React, realidad aumentada sobre una etiqueta,
un meliponario navegable en realidad virtual y un video de cosecha generado con
Python y FFmpeg.

La tienda permite consultar cuatro productos, elegir variantes, agregar al
carrito, aplicar el cupón `BIENVENIDA10`, simular un pedido y descontar stock
dentro de una transacción. La experiencia AR reconoce una etiqueta impresa y
muestra una abeja animada y un video. La experiencia VR permite recorrer en 360°
una granja estilizada con colisiones, vegetación circundante, un lago con peces,
cinco hotspots (uno escondido), cinco teletransportes y narración. El video
explica el proceso de cosecha como recreación didáctica.

El proyecto se verificó con pruebas de API, una prueba automatizada de comercio,
build de producción, smoke test del visor AR/VR y capturas en escritorio y
teléfono. La prueba general de AR y video pasó en
<https://proyecto-integrador-uni-ten.vercel.app>. El checkout móvil quedó
archivado. El diagnóstico del visor WebXR y la escucha de la cama sonora quedan
para después de la entrega.

## 2. Planteamiento

### 2.1 Contexto

La abeja melipona, conocida en maya como `xunáan kaab`, es una abeja sin
aguijón asociada a la meliponicultura yucateca. Su manejo tradicional emplea
jobones: troncos huecos que protegen la colonia y sus reservas. La miel y la cera
tienen valor cultural y productivo, pero las prácticas varían entre comunidades
y no deben generalizarse [1], [2].

El proyecto toma ese contexto como inspiración para un caso simulado de una
cooperativa llamada **Sak P'o' Kaab**. El nombre combina `sak p'o'` (jabón) y
`kaab` (miel/abeja). La arquitectura de marca es:

- **Kaab**: miel.
- **Sak P'o'**: jabón.
- **Xunán**: cosméticos.
- **Jobón**: velas.

### 2.2 Problema

Una marca pequeña necesita presentar sus productos y su historia sin depender de
una plataforma comercial compleja. Al mismo tiempo, el proyecto académico debe
demostrar competencias de desarrollo web, bases de datos, diseño multimedia,
modelado 3D, realidad aumentada, realidad virtual y producción de video.

El reto es integrar esas piezas en una experiencia coherente, explicable y
verificable, sin inventar un caso real ni prometer funciones que no puedan
demostrarse.

### 2.3 Objetivos

**Objetivo general:** construir una tienda y experiencia multimedia funcional
para el caso simulado Sak P'o' Kaab, con catálogo, compra simulada, AR, VR y
video.

**Objetivos específicos:**

1. Modelar una base de datos relacional para productos, variantes, pedidos,
   cupones y stock.
2. Implementar una API REST con validaciones y transacciones.
3. Construir una tienda adaptable con catálogo, ficha, carrito, cupón, checkout
   simulado y vista local de pedidos de prueba.
4. Crear una etiqueta con AR que muestre una abeja animada y un video.
5. Construir un meliponario navegable en VR con hotspots y narración.
6. Producir un video de cosecha con Python y FFmpeg, declarado como recreación.
7. Documentar pruebas, evidencias, decisiones y límites del proyecto.
8. Diseñar una animación 2D breve del símbolo de la marca.
9. Preparar mapas conceptuales y un plan de mercadotecnia digital como propuesta
   académica, distinguiéndolos de resultados de campaña.

### 2.4 Alcance

Incluido:

- Catálogo de cuatro productos y seis variantes.
- Carrito, cupón, checkout simulado, pedido e historial.
- Panel local de pedidos `mock`, de solo lectura y sin datos personales.
- AR con MindAR y A-Frame.
- VR con A-Frame 1.8.
- Símbolo 2D animado en SVG.
- Video y audio sintético.
- Mapas de mercadotecnia y comercio electrónico, más un plan hipotético en
  `docs/mercadotecnia/`.
- Documentación, evidencias y defensa.

Excluido:

- Pagos reales y pasarela financiera.
- Login de usuarios y administración de pedidos reales. La vista local de pedidos
  solo muestra información resumida de registros `mock`.
- Reseñas inventadas o testimonios falsos.
- Producción comercial real.
- Metraje documental del meliponario.

## 3. Decisiones de diseño

- **Caso simulado transparente:** la marca y la cooperativa son ficticias; se
  declara en README, interfaz, video y memoria.
- **MySQL 8 en Docker:** se eligió MySQL 8.4 porque el proyecto usa funciones y
  comportamiento de MySQL 8; XAMPP/MariaDB 10.4 no era equivalente.
- **Monorepo con workspaces:** API y tienda comparten scripts y dependencias sin
  mezclar responsabilidades.
- **React + Vite + Tailwind:** permiten una interfaz rápida, adaptable y fácil de
  explicar.
- **A-Frame + MindAR:** ambas tecnologías funcionan en web y permiten demostrar
  AR/VR sin una aplicación nativa [3], [4]. El meliponario implementado usa
  A-Frame/WebXR y no Unity; esta diferencia debe explicarse y confirmarse con el
  docente frente al alcance literal de la guía.
- **GLB para web:** los modelos exportados son más ligeros y portables que un
  `.blend`.
- **Video generado por código:** Python, Pillow y FFmpeg permiten reproducir el
  proceso y documentar la autoría de la animación.
- **Voz sintética:** se declara como recurso generado, no como testimonio real.
- **Estilo low-poly:** reduce costo de render, facilita la lectura en teléfono y
  mantiene una identidad visual coherente.

## 4. Arquitectura

```text
Navegador
├─ Tienda React/Vite (5173)
│  └─ proxy /api
├─ Visor AR/VR A-Frame (5174)
│  ├─ MindAR + etiqueta
│  ├─ meliponario VR
│  └─ video/audio
└─ API Express (3000)
   └─ MySQL 8.4 en Docker (3306)
```

Componentes:

- `apps/store`: tienda React, catálogo, ficha, carrito, checkout y panel local de
  pedidos de prueba.
- `server`: API Express, rutas de catálogo, cupones y pedidos simulados.
- `db`: esquema y datos iniciales.
- `apps/ar-preview`: visor 3D, AR y VR.
- `assets`: modelos GLB, escenas Blender, target, video y audio.
- `scripts`: generación de modelos, renders, video y audio.
- `docs`: Scrum, bitácora, diario, evidencias, memoria y defensa.

## 5. Base de datos

La base `melipona` usa `utf8mb4` y contiene ocho tablas:

| Tabla | Función |
| --- | --- |
| `users` | Datos mínimos del comprador simulado. |
| `products` | Producto, slug, categoría, descripción y estado. |
| `product_variants` | Presentación, precio, stock, peso y atributos. |
| `coupons` | Código, porcentaje, mínimo y contador de usos. |
| `orders` | Pedido, estado, subtotal, descuento y total. |
| `order_items` | Líneas del pedido con precio y cantidad. |
| `coupon_redemptions` | Relación entre pedido y cupón utilizado. |
| `order_status_history` | Historial de cambios de estado. |

Relaciones principales:

- Un producto tiene varias variantes.
- Un pedido tiene varias líneas `order_items`.
- Cada línea referencia una variante.
- Un pedido puede tener una redención de cupón.
- El historial de estado depende del pedido.

El flujo de compra usa una transacción:

1. Validar datos y cupón.
2. Bloquear inventario de las variantes solicitadas.
3. Verificar stock suficiente.
4. Crear `orders` y `order_items`.
5. Descontar stock.
6. Registrar la redención del cupón.
7. Registrar el estado inicial.
8. Confirmar o revertir la transacción.

Los pedidos manuales de prueba se conservan para evidenciar el estado real de la
base. La prueba automatizada crea y elimina sus propios pedidos, y restaura stock
y contador del cupón.

## 6. API

La API Express expone:

| Método | Ruta | Función |
| --- | --- | --- |
| `GET` | `/api/health` | Estado de la API y de MySQL. |
| `GET` | `/api/products` | Productos activos con variantes. |
| `GET` | `/api/products/:slug` | Detalle de un producto. |
| `POST` | `/api/coupons/validate` | Valida código y subtotal. |
| `POST` | `/api/orders` | Crea pedido simulado y descuenta stock. |
| `GET` | `/api/orders/demo` | Lista pedidos `mock`, fuera de producción y sin datos personales. |

Decisiones técnicas:

- `mysql2` con pool de conexiones.
- Consultas parametrizadas para evitar inyección SQL.
- Validación de cuerpos con Zod.
- `decimalNumbers: true` para precios numéricos.
- CORS limitado al origen de la tienda.
- Respuestas de error claras para cupón mínimo, stock insuficiente y datos
  inválidos.
- El endpoint de salud consulta la base, no solo responde “ok”.
- `npm start` inicia la API con `NODE_ENV=production`; la ruta del panel de
  demostración responde `404` en ese modo. El smoke test `test:production-panel`
  verifica la desactivación.

## 7. Tienda

La tienda incluye:

- Portada con identidad visual, resumen y acceso al catálogo.
- Catálogo de cuatro productos con filtros por categoría.
- Ficha de producto con variantes, precio y stock.
- Tarjetas con renders de producto en WebP.
- Carrito adaptable con cantidades y subtotal.
- Cupón `BIENVENIDA10` con 10 % de descuento desde $200.
- Checkout simulado con datos mínimos.
- Confirmación con número de pedido.
- Panel **Pedidos de prueba**, visible solo en desarrollo; lista un máximo de 25
  pedidos simulados con número parcial, estado, total, cantidad de artículos y
  fecha. No permite mutaciones ni expone datos de contacto; la API deshabilita
  esta ruta cuando `NODE_ENV=production`.
- Símbolo con animación 2D ligera en SVG y alternativa de movimiento reducido;
  fuente en `assets/animation/logo-sak-po-kaab.svg`.
- Diseño adaptable a escritorio y teléfono.

La interfaz evita prometer pagos reales: el checkout se identifica como
simulación académica. El carrito se maneja en el cliente y el pedido se confirma
contra la API.

## 8. Modelado 3D y autoría

Los modelos principales son:

- Abeja melipona estilizada con clip de animación `SakPoKaab`.
- Jobón con panales y cavidad interior.
- Cuatro escenas de producto: miel, jabón, bálsamo y vela.
- Símbolo de marca 2D animado en SVG.

La escena base se generó con `scripts/blender_model.py`, asistido por IA. Los
renders de producto se generaron con Cycles CPU y estudio crema. La vela se
re-renderizó con un punto de foco separado del punto de mira para que la etiqueta
frontal quedara nítida sin cambiar la composición; evidencia en
`docs/evidencias/2026-11-25/producto-vela-final-foco.png`. Las escenas se guardan
en `assets/models/producto-*.blend` y las versiones WebP se integran en la tienda.

La autoría manual se documenta en `docs/pase-manual-3d.md`. El pase de la abeja
y el jobón quedó confirmado. El resultado se ve en el visor público, en
`docs/evidencias/2026-11-27/vercel-movil-visor.png`. La base inicial sigue siendo
asistida; el pase manual es el cierre de esa autoría.

## 9. Realidad aumentada

La experiencia AR usa:

- Target de imagen `assets/targets/etiqueta-sakpokaab.mind`.
- MindAR 1.2 y A-Frame 1.6 [3], [4], [8].
- Abeja animada y jobón.
- Botón **Ver cosecha** con video móvil de 640 × 360.
- Instrucciones de impresión y uso de la etiqueta.

La cámara requiere HTTPS. La prueba general de etiqueta y video se hizo en
<https://proyecto-integrador-uni-ten.vercel.app> y pasó.

## 10. Realidad virtual

El recorrido VR usa A-Frame 1.8 [3], [4] e incluye:

- Meliponario estilizado con jobón, árbol, flores, pasto y colinas.
- Seis abejas, dos mariposas, libélula, colibrí y lagartija.
- Cinco hotspots informativos (incluye un detalle escondido).
- Cinco zonas de teletransporte: inicio, jardín, jobón, palapa y lago.
- Interacción por mirada con temporizador de 900 ms.
- Panel de información anclado a la cámara.
- Narración sintética de aproximadamente 43 s con reproducir/pausar.

La validación headless comprobó carga de modelos, hotspots, panel, teletransporte,
audio y ausencia de errores. Se compartió una captura desde el modo inmersivo:
la vista estereoscópica aparece, pero la escena se ve casi negra y fragmentada.
Esto se registra como defecto visual observado, no como causa diagnosticada ni
como validación WebXR aprobada. Falta repetir la prueba en un dispositivo
identificado, diagnosticar el render, y validar comodidad y audio.

## 11. Video y audio

El video `assets/video/cosecha-melipona-recreacion.mp4` es una animación original
720p con narración sintética en español de México. Se genera con Python, Pillow y
FFmpeg. El derivado móvil se usa en AR.

El guion muestra:

1. La colonia y el jobón.
2. Preparación del espacio.
3. Revisión y apertura cuidadosa.
4. Recolección por gravedad, sin centrifugado.
5. Filtrado y cierre.
6. Reservas para la colonia.

El video incluye el rótulo de recreación didáctica y no se presenta como registro
documental. Las fuentes de contexto son The Nature Conservancy México y SEMARNAT
[1], [2]. El script genera subtítulos SRT, una cama sonora original y un derivado
vertical para redes. En la sesión local del 26 de noviembre de 2026 se regeneraron
con FFmpeg 9.0.2 el máster 720p, el derivado móvil y el vertical 1080 × 1920; los
tres incluyen la cama sonora y la pista de subtítulos. La medición del máster fue
-16.05 LUFS, -1.49 dBTP y LRA 3.40. La escucha final de esa mezcla queda para
después de la entrega; técnicamente ya está integrada.

## 12. Mercadotecnia digital y comercio electrónico

`docs/mercadotecnia/plan.md` contiene una propuesta académica con posicionamiento,
perfiles hipotéticos, calendario editorial, criterios para una colaboración
propuesta con creadores y un plan de medición. No hay campaña publicada, creadores
contactados ni métricas observadas; los perfiles no se presentan como resultados
de entrevistas. Las fechas sobre polinizadores se apoyan en efemérides públicas y
no se usan para generalizar prácticas de cosecha [5], [6].

Los mapas conceptuales están en `docs/mercadotecnia/mapa-mercadotecnia.svg` y
`docs/mercadotecnia/mapa-comercio-electronico.svg`. Las métricas propuestas
incluyen alcance, CTR, vistas de ficha, carrito, checkout simulado y éxito de AR;
se indican fórmula y método de medición. No se instaló analítica de usuarios. Los
eventos de comercio electrónico se describen de acuerdo con la guía de Google,
pero no están instrumentados [7].

## 13. Pruebas y evidencias

Pruebas realizadas:

- `GET /api/health` responde `200` con `db: "up"`.
- `GET /api/products` devuelve cuatro productos y seis variantes.
- `GET /api/products/:slug` responde `200` o `404` según corresponda.
- `npm run test:commerce` valida cupón, mínimo, stock y pedido; limpia sus datos.
- `npm run build` compila la tienda de producción.
- `npm --prefix apps/ar-preview run build` compila el visor.
- `npm --prefix apps/ar-preview run test:smoke` valida visor, VR, MindAR,
  etiqueta, modelos, audio y videos.
- Revisión móvil a 390 px: `innerWidth = 390`, `scrollWidth = 390`, sin
  desbordamiento horizontal.
- Capturas finales base en `docs/evidencias/2026-11-25/`; la nueva captura de
  escritorio del 26 de noviembre está en `docs/evidencias/2026-11-26/`.
- `python -m unittest scripts.test_subtitle_utils` valida el formateo temporal y
  ajuste de línea de subtítulos.
- `python -m unittest scripts.test_audio_bed scripts.test_subtitle_utils` ejecuta
  cinco pruebas de síntesis PCM y subtítulos.

Evidencias principales:

- `docs/evidencias/2026-10-28/`: API, catálogo y primeras pruebas.
- `docs/evidencias/2026-11-04/`: modelos y renders EEVEE.
- `docs/evidencias/2026-11-08/`: AR, VR, fauna y storyboard.
- `docs/evidencias/2026-11-10/`: compra simulada, renders de producto y catálogo.
- `docs/evidencias/2026-11-25/`: cierre, build, smoke test y capturas finales.
- `docs/evidencias/2026-11-26/`: cierre documental del día.
- `docs/evidencias/2026-11-27/`: visor público en Vercel, vista móvil y checkout.
- Manuales y declaración: `docs/manual-tecnico.md`, `docs/manual-usuario.md` y
  `docs/declaracion-uso-ia.md`; bitácora seleccionada en
  `docs/anexos/bitacora-ia-entrega.md`.

## 14. Limitaciones

Cerrado para la entrega:

- Portada: Universidad Politécnica de Quintana Roo (UPQRoo).
- Pase manual de abeja y jobón confirmado. El visor móvil lo muestra en
  `docs/evidencias/2026-11-27/vercel-movil-visor.png`.
- Prueba general de AR y video en
  <https://proyecto-integrador-uni-ten.vercel.app>.
- Checkout móvil archivado: cupón `BIENVENIDA10` y pedido simulado
  `SKP-MWBIEJG0-4EFF8D`.
- Video máster, móvil y vertical regenerados, con SRT y cama sonora medida en
  -16.05 LUFS y -1.49 dBTP.

Después de la entrega:

- Diagnosticar la escena WebXR que se vio casi negra y fragmentada.
- Escuchar y aprobar la cama sonora.
- Ensayar la defensa.

Límites del caso:

- No hay pagos reales, login, administración de pedidos reales ni reseñas. El
  panel local de pedidos `mock` es de solo lectura y no se incluye en producción.
- El caso es simulado y no representa una empresa o comunidad real.
- No se realizó un estudio de mercado primario; cualquier dato de mercado debe
  citarse de fuentes reales.
- Vercel publica el visor, no la tienda. El catálogo y el checkout se demuestran
  en local, con la API y MySQL.

## 15. Conclusiones

El proyecto logra integrar en una sola experiencia una tienda funcional, una base
de datos relacional, una API transaccional, AR, VR, modelado 3D y video. La
arquitectura permite explicar el flujo completo desde la interfaz hasta MySQL y
demostrar cada componente por separado.

La decisión más importante fue mantener la transparencia: el caso es simulado, el
video es una recreación, la voz es sintética y el pase manual de los modelos ya
quedó confirmado. Esa honestidad fortalece la defensa porque permite explicar qué
se hizo, con qué herramientas y cuáles son los límites.

Después de la entrega quedan el diagnóstico WebXR del visor, la escucha de la
cama sonora y el ensayo de la demostración.

## 16. Referencias

[1] Secretaría de Medio Ambiente y Recursos Naturales, *La meliponicultura en
México: un acercamiento a las prácticas tradicionales y a las perspectivas de su
manejo contemporáneo*. México: SEMARNAT, 2023. [En línea]. Disponible:
<https://biblioteca.semarnat.gob.mx/janium/Documentos/Ciga/libros2023/CD008608.pdf>.
[Consultado: 26-nov-2026].

[2] The Nature Conservancy México, *Manejo tradicional de la abeja de los pueblos
mayas*. [En línea]. Disponible:
<https://www.tncmx.org/content/dam/tnc/nature/en/documents/mexico/Manejo_tradicional_de_la_abeja_de_los_pueblos_mayas.pdf>.
[Consultado: 26-nov-2026].

[3] A-Frame, “Models,” *A-Frame Documentation*, versión 1.8.0. [En línea].
Disponible: <https://aframe.io/docs/1.8.0/introduction/models.html>.
[Consultado: 26-nov-2026].

[4] A-Frame, “gltf-model,” *A-Frame Documentation*. [En línea]. Disponible:
<https://aframe.io/docs/1.8.0/components/gltf-model.html>.
[Consultado: 26-nov-2026].

[5] Food and Agriculture Organization of the United Nations, “World Bee Day | 20
May.” [En línea]. Disponible: <https://www.un.org/observances/bee-day>.
[Consultado: 26-nov-2026].

[6] United Nations, “International Mother Earth Day.” [En línea]. Disponible:
<https://www.un.org/en/observances/earth-day>.
[Consultado: 26-nov-2026].

[7] Google, “Measure ecommerce,” *Google Analytics for Developers*. [En línea].
Disponible:
<https://developers.google.com/analytics/devguides/collection/ga4/ecommerce>.
[Consultado: 26-nov-2026].

[8] H. Kim, “Image Tracking Quick Start: Overview,” *MindAR Documentation*. [En
línea]. Disponible: <https://hiukim.github.io/mind-ar-js-doc/quick-start/overview>.
[Consultado: 26-nov-2026].

Las referencias visuales y técnicas adicionales se detallan en
`docs/referencias-3d.md`, `docs/referencias-video.md` y
`docs/referencias-vr.md`.

## Anexo A. Comandos de verificación

```powershell
npm run db:up
npm run dev
npm run build
npm run test:commerce
npm --prefix apps/ar-preview run build
npm --prefix apps/ar-preview run test:smoke
docker inspect --format '{{.State.Health.Status}}' melipona-db
curl.exe -s http://127.0.0.1:3000/api/health
```

## Anexo B. Estructura del repositorio

```text
.
├─ apps/store/          Tienda React + Vite + Tailwind
├─ apps/ar-preview/     Visor A-Frame, MindAR y VR
├─ server/              API Express
├─ db/                  Esquema y datos de demostración
├─ docs/                Scrum, bitácora, diario, memoria y evidencias
├─ assets/              Modelos, target, video y audio
├─ scripts/             Utilidades de Blender, video y audio
├─ docker-compose.yml   MySQL 8.4
└─ package.json         Workspaces y scripts raíz
```
