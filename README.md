# Sak P'o' Kaab

Tienda en línea y experiencia multimedia de miel y jabón de la abeja melipona.
Proyecto integrador de la materia **Multimedia y Diseño Digital** de la
Ingeniería en Software.

- Alumno: Joshua Israel Cabrera Camacho
- Matrícula: 202300074
- Entrega: 26 y 27 de noviembre de 2026
- Defensa: 30 de noviembre al 4 de diciembre de 2026

## Aviso académico

Este repositorio documenta un **caso de estudio simulado**. La cooperativa, la
marca y el meliponario no existen como empresa real. Los datos de mercado que se
citen en la documentación provienen de fuentes reales y se referencian. El video
de la cosecha será una **recreación didáctica** y así se declarará en la interfaz
y en la memoria del proyecto.

## Estado actual

Bloque 1 completado:

- Base de datos MySQL 8.4 en Docker con 8 tablas y datos de demostración.
- API REST en Express con catálogo, variantes, stock y estado de salud.
- Catálogo web en React + Vite + Tailwind, con filtros, ficha de producto y
  diseño adaptable a teléfono.
- Evidencias de ejecución y pruebas en `docs/evidencias/2026-10-28/` y
  `docs/evidencias/2026-11-10/`.

Sprint 2:

- Blender 5.2.3 y FFmpeg 9.0.2 instalados y verificados.
- Escena estilizada generada por `scripts/blender_model.py` en
  `assets/models/modelo.blend`, con exportaciones `abeja.glb` y `jobon.glb`.
- El GLB de la abeja contiene el clip `SakPoKaab`; el jobón incluye panales y
  cavidad interior.
- Renders EEVEE generados por `scripts/blender_render_eevee.py` en
  `docs/evidencias/2026-11-04/`.
- La escena generada por scripts aún requiere el pase manual y documentado de
  Joshua para sustentar la autoría.
- Guía del pase manual: `docs/pase-manual-3d.md`; skills de apoyo:
  `docs/skills-3d.md`.
- Visor A-Frame con meliponario estilizado, seis abejas, dos mariposas, una
  libélula, un colibrí, una lagartija, jobón, árboles, flores, pasto, colinas y
  un lago con peces: `npm --prefix apps/ar-preview run dev` (puerto 5174).
- Recorrido inmersivo en `/vr.html`: A-Frame 1.8, granja explorable en 360° con
  colisiones, cinco hotspots informativos, un detalle escondido y teletransporte
  por mirada entre inicio, jardín, jobón, palapa y lago. Incluye narración
  sintética con control de reproducción y joystick táctil. Una captura compartida
  en modo inmersivo muestra la escena casi negra y fragmentada; el modo abre, pero
  la calidad visual de WebXR no está aprobada y la causa sigue pendiente.
- WebXR exige contexto seguro: en el teléfono conviene `adb reverse tcp:5174
  tcp:5174` y abrir `http://localhost:5174/vr.html`; por IP LAN Chrome bloquea la
  entrada a VR.
- Experiencia MindAR en `http://localhost:5174/ar.html`; target e instrucciones de
  impresión en `assets/targets/`. La etiqueta y el video se validaron en el Galaxy
  A22.
- Recreación didáctica original de la cosecha, 720p con narración sintética:
  `assets/video/cosecha-melipona-recreacion.mp4`. Ya está disponible desde el
  botón **Ver cosecha** cuando MindAR detecta la etiqueta.
- Referencias visuales y criterios de estilo en `docs/referencias-3d.md`.
- Guion y fuentes del video: `docs/referencias-video.md`; storyboard en
  `docs/evidencias/2026-11-08/storyboard-cosecha.png`.
- Guion y fuentes de la narración VR: `docs/referencias-vr.md`; audio en
  `assets/audio/narracion-recorrido-vr.mp3`.
- Carrito adaptable con variantes, cantidades, subtotal, cupón `BIENVENIDA10` y
  checkout simulado. El pedido se guarda en `orders` y `order_items`, descuenta
  stock y registra la redención del cupón y el historial de estado.
- Panel **Pedidos de prueba** en modo desarrollo: solo lectura, máximo 25 pedidos
  `mock`, identificador parcial y sin datos personales. La ruta no está habilitada
  en producción.
- API de compra: `POST /api/coupons/validate` y `POST /api/orders`, con
  validaciones Zod, transacción y bloqueo de inventario.
- Cuatro renders de producto en `docs/evidencias/2026-11-10/producto-*-final.png`
  (1600 × 2000), integrados como WebP en las tarjetas y la ficha de la tienda. La
  vela se re-renderizó con foco frontal para mejorar la lectura de la etiqueta.
- Revisión visual en escritorio: `docs/evidencias/2026-11-08/visor-escena.png`.
  Fauna adicional: `docs/evidencias/2026-11-08/visor-fauna.png`.
  Captura de MindAR: `docs/evidencias/2026-11-08/ar-target-detectado.png`.

Cierre documental:

- Memoria del proyecto: `docs/memoria.md`.
- Manual técnico y manual de usuario: `docs/manual-tecnico.md` y
  `docs/manual-usuario.md`.
- Declaración de IA y anexo seleccionado de bitácora:
  `docs/declaracion-uso-ia.md` y `docs/anexos/bitacora-ia-entrega.md`.
- Mapas conceptuales y plan de mercadotecnia:
  `docs/mercadotecnia/` (propuesta; no presenta métricas ni colaboraciones como
  hechos).
- Memoria en PDF: `docs/memoria.pdf`; versión HTML imprimible:
  `docs/memoria.html`.
- Guion, demo, preguntas y checklist de defensa: `docs/defensa.md`.
- Presentación navegable de 13 diapositivas: `docs/presentacion.html`; versión
  PDF lista para entregar en `docs/presentacion.pdf`.
- Evidencias de la revisión final: `docs/evidencias/2026-11-25/`.
- Captura de escritorio tras las correcciones visuales: `docs/evidencias/2026-11-26/`.
- QA final: MySQL `healthy`, API `db: "up"`, cuatro productos y seis variantes.
- `npm run build`, `npm run test:commerce`, los smoke tests AR/VR y las pruebas
  unitarias de utilidades multimedia están disponibles.
- Video regenerado: máster 720p, móvil 360p y vertical 1080 × 1920, con SRT y
  cama sonora; medición del máster -16.05 LUFS y -1.49 dBTP.
- Para regenerar la memoria PDF: `python -m pip install -r requirements-docs.txt`
  y `python scripts/render_memory_pdf.py` (configura `INSTITUTION_NAME` primero).
- Revisión móvil por CDP a 390 px sin desbordamiento horizontal.

Pendiente de cierre:

- Hacer el pase manual de los modelos y documentar las modificaciones propias.
- Archivar la evidencia de la validación de AR/video y checkout en el Galaxy A22.
- Diagnosticar y validar la calidad del recorrido WebXR con un casco/teléfono
  compatible; guardar evidencia con modelo, navegador y visor identificados.
- Obtener la URL de producción de Vercel y probar `/ar.html` por HTTPS con cámara
  en un teléfono. GitHub reporta `success` para `b735403`; falta comprobar la ruta
  publicada y la cámara en dispositivo.
- Probar narración y controles de audio en el dispositivo WebXR.
- Ensayar la presentación PDF y la demostración; preparar respaldos físicos del
  video y los GLB.
- Confirmar el nombre oficial de la institución para reemplazar el marcador de
  portada del PDF.
- Escuchar y aprobar la cama sonora; los MP4 con SRT y exportación vertical ya
  están regenerados y revisados técnicamente.

## Tecnologías

| Capa | Tecnología |
| --- | --- |
| Base de datos | MySQL 8.4 en Docker |
| API | Node.js 22, Express 4, mysql2, Zod |
| Tienda | React 18, Vite 6, Tailwind CSS 3.4 |
| AR | A-Frame 1.6 + MindAR 1.2 |
| VR | A-Frame 1.8 / WebXR |
| 3D | Blender LTS, exportación GLB |
| Video y audio | Python 3.12 + FFmpeg |
| Control de versiones | Git + GitHub |

## Requisitos

- Node.js 20 o superior (probado con 22.17.1).
- npm 10 o superior.
- Docker Desktop con Docker Compose v2.
- Puerto 3000 libre para la API.
- Puerto 3306 libre para MySQL.
- Puerto 5173 libre para Vite.

## Puesta en marcha

1. Instalar dependencias:

   ```powershell
   npm install
   ```

2. Crear el archivo de entorno local:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Levantar MySQL:

   ```powershell
   npm run db:up
   ```

   La primera vez descarga la imagen, crea la base `melipona` y ejecuta
   `db/schema.sql` y `db/seed.sql`. Espera a que el contenedor esté `healthy`.

4. Levantar API y tienda en dos terminales, o ambas con un solo comando:

   ```powershell
   npm run dev
   ```

   También se pueden iniciar por separado:

   ```powershell
   npm run dev:api
   npm run dev:store
   ```

5. Abrir:

   - Tienda: <http://localhost:5173>
   - Salud de la API: <http://localhost:3000/api/health>
   - Catálogo: <http://localhost:3000/api/products>

## Scripts

| Comando | Qué hace |
| --- | --- |
| `npm run dev` | API y tienda en modo desarrollo. |
| `npm run dev:api` | API con `node --watch`. |
| `npm run dev:store` | Vite en el puerto 5173. |
| `npm run build` | Compila la tienda en `apps/store/dist`. |
| `npm run test:commerce` | Prueba cupón, mínimo, stock y pedido; limpia sus datos. |
| `npm --workspace @sak-po-kaab/server run test:production-panel` | Verifica que el endpoint de pedidos de demostración responda `404` en producción. |
| `npm start` | API en modo producción. |
| `npm run db:up` | Levanta MySQL en segundo plano. |
| `npm run db:down` | Detiene MySQL sin borrar datos. |
| `npm run db:reset` | Borra el volumen y vuelve a ejecutar esquema y seed. |

## Endpoints

| Método | Ruta | Respuesta |
| --- | --- | --- |
| GET | `/api/health` | Estado de la API y de MySQL. |
| GET | `/api/products` | Productos activos con sus variantes. |
| GET | `/api/products/:slug` | Un producto por slug o `404`. |
| POST | `/api/coupons/validate` | Valida código y subtotal; devuelve descuento. |
| POST | `/api/orders` | Crea un pedido simulado y descuenta stock. |

Ejemplo de respuesta de salud:

```json
{
  "ok": true,
  "service": "sak-po-kaab-api",
  "db": "up",
  "timestamp": "2026-10-29T04:49:47.392Z"
}
```

## Estructura

```text
.
├─ apps/store/          Tienda React + Vite + Tailwind
├─ server/              API Express
├─ db/                  Esquema y datos de demostración
├─ docs/                Scrum, bitácora, diario y evidencias
├─ assets/              Modelos, texturas, video y audio
├─ scripts/             Utilidades de video, audio y respaldo
├─ docker-compose.yml   MySQL 8.4
└─ package.json         Workspaces y scripts raíz
```

## Base de datos

Tablas creadas por `db/schema.sql`:

1. `users`
2. `products`
3. `product_variants`
4. `coupons`
5. `orders`
6. `order_items`
7. `coupon_redemptions`
8. `order_status_history`

Datos iniciales de `db/seed.sql`:

- 4 productos: miel, jabón, bálsamo labial y vela.
- 6 variantes con precio, stock, peso y atributos en JSON.
- 1 cupón: `BIENVENIDA10` (10 % en compras desde $200).

Para reiniciar la base desde cero:

```powershell
npm run db:reset
```

## Verificación realizada

- `GET /api/health` respondió `200` con `db: "up"`.
- `GET /api/products` respondió `200` con 4 productos y 6 variantes.
- `GET /api/products/jabon-sak-po` respondió `200` con sus 2 variantes.
- `GET /api/products/no-existe` respondió `404`.
- `npm run build` compiló 29 módulos sin errores.
- Prueba de diseño móvil a 390 px: `scrollWidth = 390`, sin desbordamiento
  horizontal; el diálogo de producto también se mantiene dentro del ancho.
- Filtro "Jabones": muestra únicamente el producto de jabón.
- Cupón `BIENVENIDA10`: 10 % desde $200; un subtotal de $150 responde
  `coupon_minimum_not_met`.
- Pedido simulado: subtotal $320, descuento $32 y total $288; el stock se
  descuenta dentro de una transacción.
- `npm run test:commerce` valida cupón, mínimo, stock insuficiente y pedido; al
  terminar elimina el pedido de prueba y restaura inventario y contador del cupón.
- Flujo UI en Chrome headless: agregar variante, abrir carrito, aplicar cupón y
  confirmar pedido; capturas en `docs/evidencias/2026-11-10/`.
- Flujo móvil a 390 px: `innerWidth = 390`, `scrollWidth = 390` y panel de 390;
  capturas `carrito-cupon-movil.png` y `pedido-simulado-movil.png`.
- QA final del 2026-11-25: MySQL `healthy`, API `db: "up"`, build de tienda y
  visor, `COMMERCE_SMOKE_OK`, `AR_PREVIEW_SMOKE_OK` y revisión móvil por CDP con
  `innerWidth = 390` y `scrollWidth = 390`.

Las capturas y el JSON de la API están en
`docs/evidencias/2026-10-28/`; la compra simulada, en
`docs/evidencias/2026-11-10/`; el cierre, en `docs/evidencias/2026-11-25/`.

## Fuentes de la lengua maya

- `kaab`: miel y abeja. Arqueología Mexicana; diccionario de Bastarrachea
  (AULEX); diccionario de la UQROO.
- `sak p'o'`: jabón. Diccionario de Bastarrachea (AULEX).
- `xunáan kaab`: abeja melipona (Melipona beecheii). Fuentes de la UQROO y
  Arqueología Mexicana.

## Uso

Proyecto académico sin fines comerciales. Las imágenes, modelos y videos se
crean para la entrega y se declaran como simulados o recreaciones didácticas.
