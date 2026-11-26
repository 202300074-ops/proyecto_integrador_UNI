# Memoria del proyecto Sak P'o' Kaab

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
muestra una abeja animada y un video. La experiencia VR recorre un meliponario
estilizado con hotspots, teletransportes y narración. El video explica el proceso
de cosecha como recreación didáctica.

El proyecto se verificó con pruebas de API, una prueba automatizada de comercio,
build de producción, smoke test del visor AR/VR y capturas en escritorio y
teléfono. Las pruebas físicas de AR, checkout y WebXR siguen siendo tareas de
cierre que requieren el dispositivo y la evidencia correspondiente.

## 2. Planteamiento

### 2.1 Contexto

La abeja melipona, conocida en maya como `xunáan kaab`, es una abeja sin
aguijón asociada a la meliponicultura yucateca. Su manejo tradicional emplea
jobones: troncos huecos que protegen la colonia y sus reservas. La miel y la cera
tienen valor cultural y productivo, pero las prácticas varían entre comunidades
y no deben generalizarse.

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
3. Construir una tienda adaptable con catálogo, ficha, carrito y checkout
   simulado.
4. Crear una etiqueta con AR que muestre una abeja animada y un video.
5. Construir un meliponario navegable en VR con hotspots y narración.
6. Producir un video de cosecha con Python y FFmpeg, declarado como recreación.
7. Documentar pruebas, evidencias, decisiones y límites del proyecto.

### 2.4 Alcance

Incluido:

- Catálogo de cuatro productos y seis variantes.
- Carrito, cupón, checkout simulado, pedido e historial.
- AR con MindAR y A-Frame.
- VR con A-Frame 1.8.
- Video y audio sintético.
- Documentación, evidencias y defensa.

Excluido:

- Pagos reales y pasarela financiera.
- Login de usuarios y panel administrativo.
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
  AR/VR sin una aplicación nativa.
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

- `apps/store`: tienda React, componentes de catálogo, ficha, carrito y checkout.
- `server`: API Express, rutas de catálogo, cupones y pedidos.
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

Decisiones técnicas:

- `mysql2` con pool de conexiones.
- Consultas parametrizadas para evitar inyección SQL.
- Validación de cuerpos con Zod.
- `decimalNumbers: true` para precios numéricos.
- CORS limitado al origen de la tienda.
- Respuestas de error claras para cupón mínimo, stock insuficiente y datos
  inválidos.
- El endpoint de salud consulta la base, no solo responde “ok”.

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
- Diseño adaptable a escritorio y teléfono.

La interfaz evita prometer pagos reales: el checkout se identifica como
simulación académica. El carrito se maneja en el cliente y el pedido se confirma
contra la API.

## 8. Modelado 3D y autoría

Los modelos principales son:

- Abeja melipona estilizada con clip de animación `SakPoKaab`.
- Jobón con panales y cavidad interior.
- Cuatro escenas de producto: miel, jabón, bálsamo y vela.

La escena base se generó con `scripts/blender_model.py`, asistido por IA. Los
renders de producto se generaron con Cycles CPU y estudio crema. La vela se
re-renderizó con un punto de foco separado del punto de mira para que la etiqueta
frontal quedara nítida sin cambiar la composición; evidencia en
`docs/evidencias/2026-11-25/producto-vela-final-foco.png`. Las escenas se guardan
en `assets/models/producto-*.blend` y las versiones WebP se integran en la tienda.

La autoría manual se documenta en `docs/pase-manual-3d.md`. El pase pendiente
incluye cambios visibles de geometría, materiales o detalles en Blender, capturas
del proceso y exportación de los GLB actualizados. Hasta completarlo, la memoria
distingue entre la base asistida y la edición manual.

## 9. Realidad aumentada

La experiencia AR usa:

- Target de imagen `assets/targets/etiqueta-sakpokaab.mind`.
- MindAR 1.2 y A-Frame 1.6.
- Abeja animada y jobón.
- Botón **Ver cosecha** con video móvil de 640 × 360.
- Instrucciones de impresión y uso de la etiqueta.

La cámara requiere HTTPS en el teléfono. Para pruebas se puede usar un túnel
Cloudflare o un despliegue estático. El target y el video se validaron
funcionalmente en un Galaxy A22; la evidencia formal de esa prueba queda
pendiente de archivar.

## 10. Realidad virtual

El recorrido VR usa A-Frame 1.8 e incluye:

- Meliponario estilizado con jobón, árbol, flores, pasto y colinas.
- Cuatro abejas, dos mariposas, libélula, colibrí y lagartija.
- Cuatro hotspots informativos.
- Tres zonas de teletransporte: inicio, jardín y jobón.
- Interacción por mirada con temporizador de 900 ms.
- Panel de información anclado a la cámara.
- Narración sintética de aproximadamente 43 s con reproducir/pausar.

La validación headless comprobó carga de modelos, hotspots, panel, teletransporte,
audio y ausencia de errores. Falta validar la entrada WebXR, la comodidad y el
audio en un casco o teléfono compatible físico.

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
documental. Las fuentes de contexto son The Nature Conservancy México y SEMARNAT.

## 12. Pruebas y evidencias

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
- Capturas finales en `docs/evidencias/2026-11-25/`.

Evidencias principales:

- `docs/evidencias/2026-10-28/`: API, catálogo y primeras pruebas.
- `docs/evidencias/2026-11-04/`: modelos y renders EEVEE.
- `docs/evidencias/2026-11-08/`: AR, VR, fauna y storyboard.
- `docs/evidencias/2026-11-10/`: compra simulada, renders de producto y catálogo.
- `docs/evidencias/2026-11-25/`: cierre, build, smoke test y capturas finales.

## 13. Limitaciones y trabajo pendiente

- El pase manual de abeja y jobón en Blender sigue pendiente de ejecución y
  documentación.
- La evidencia formal de AR/video en el Galaxy A22 debe archivarse.
- El checkout en teléfono físico debe probarse y documentarse.
- La entrada WebXR, la comodidad y el audio deben validarse en un dispositivo
  físico.
- No hay pagos reales, login, panel administrativo ni reseñas.
- El caso es simulado y no representa una empresa o comunidad real.
- No se realizó un estudio de mercado primario; cualquier dato de mercado debe
  citarse de fuentes reales.

## 14. Conclusiones

El proyecto logra integrar en una sola experiencia una tienda funcional, una base
de datos relacional, una API transaccional, AR, VR, modelado 3D y video. La
arquitectura permite explicar el flujo completo desde la interfaz hasta MySQL y
demostrar cada componente por separado.

La decisión más importante fue mantener la transparencia: el caso es simulado, el
video es una recreación, la voz es sintética y la autoría manual de los modelos
se documenta solo cuando el pase en Blender esté completo. Esa honestidad
fortalece la defensa porque permite explicar qué se hizo, con qué herramientas y
cuáles son los límites.

El siguiente paso es cerrar las pruebas físicas, completar el pase manual y
ensayar la demostración con respaldos del video, los GLB y las capturas.

## 15. Referencias

- The Nature Conservancy México. *Manejo tradicional de la abeja de los pueblos
  mayas*.
  <https://www.nature.org/content/dam/tnc/nature/en/documents/mexico/Manejo_tradicional_de_la_abeja_de_los_pueblos_mayas.pdf>
- SEMARNAT. *La meliponicultura en México* (2023), sección 8.7.
  <https://biblioteca.semarnat.gob.mx/janium/Documentos/Ciga/libros2023/CD008608.pdf>
- A-Frame. *Models*.
  <https://aframe.io/docs/1.8.0/introduction/models.html>
- aframe-extras. *Loaders / animation-mixer*.
  <https://github.com/c-frame/aframe-extras/blob/master/src/loaders/README.md>
- A-Frame. *gltf-model*.
  <https://github.com/aframevr/aframe/blob/master/docs/components/gltf-model.md>
- Referencias visuales y criterios de estilo: `docs/referencias-3d.md`.
- Guion y fuentes del video: `docs/referencias-video.md`.
- Guion y fuentes del recorrido VR: `docs/referencias-vr.md`.

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
