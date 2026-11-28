# AGENTS.md — Compacto del proyecto

## Contexto

- Proyecto integrador de Multimedia y Diseño Digital: tienda y experiencia
  multimedia de **Sak P'o' Kaab**, caso de estudio simulado de una cooperativa
  melipona de Yucatán.
- Entrega: **26–27 de noviembre de 2026**. Defensa: **30 de noviembre al 4 de
  diciembre de 2026**.
- Repositorio: `https://github.com/202300074-ops/proyecto_integrador_UNI.git`,
  rama `main`.
- Trabajar y documentar en español.
- No hacer commit ni push sin que Joshua lo pida explícitamente.
- No borrar los pedidos manuales de prueba `SKP-MWBJ2NP1-D34916` y
  `SKP-MWBJ7X6T-490348`; el stock actual los refleja.

## Stack y arranque

- Node 22, React 18, Vite 6, Tailwind 3, Express, MySQL 8.4 en Docker.
- Blender 5.2.3 LTS y FFmpeg 9.0.2.
- Base de datos: `npm run db:up`; API y tienda: `npm run dev`.
- Tienda: `http://localhost:5173`; API: `http://localhost:3000/api`.
- AR/VR: `npm --prefix apps/ar-preview run dev` en `http://localhost:5174`.
- WebXR exige contexto seguro: en el teléfono usa `adb reverse tcp:5174 tcp:5174`
  y abre `http://localhost:5174/vr.html`; por IP LAN (`http://192.168.1.107:5174`)
  Chrome bloquea la entrada a VR.
- Build: `npm run build`.
- Prueba de compra: `npm run test:commerce`.
- Si la prueba de comercio falla con `ECONNREFUSED` o `ECONNRESET`, el watcher
  de la API pudo reiniciarse durante la prueba. Levantar una instancia estable
  con `node server/src/index.js` en el puerto 3001 y ejecutar:
  `$env:API_BASE='http://localhost:3001/api'; npm run test:commerce`.

## Estado actual (2026-11-27)

- Compra simulada terminada: carrito, variantes, cantidades, cupón
  `BIENVENIDA10` (10 % desde $200), checkout, pedido transaccional, descuento de
  stock, redención e historial.
- `server/scripts/commerce-smoke-test.mjs` limpia sus propios pedidos y restaura
  stock/cupón.
- Tienda con cuatro renders de producto integrados como WebP de 800 × 1000 en
  `apps/store/public/productos/`, visibles en tarjetas y ficha.
- Panel local **Pedidos de prueba** de solo lectura; muestra hasta 25 pedidos
  `mock` sin datos personales y no se compila ni habilita en producción.
- Mapas conceptuales y plan de mercadotecnia en `docs/mercadotecnia/`; son una
  propuesta académica, no una campaña ni métricas observadas.
- Símbolo 2D animado en `assets/animation/logo-sak-po-kaab.svg` y movimiento
  reducido respetado en la tienda.
- Manual técnico, manual de usuario, declaración de IA y anexo de bitácora en
  `docs/`.
- Memoria Markdown/HTML y PDF generada; portada: Universidad Politécnica de
  Quintana Roo (UPQRoo).
- Renders finales de miel, jabón, bálsamo y vela en
  `docs/evidencias/2026-11-10/producto-*-final.png`; escenas en
  `assets/models/producto-*.blend`.
- La vela se re-renderizó con foco frontal en la etiqueta; PNG/WebP actualizados
  y verificados en la captura final del catálogo.
- AR/video validados funcionalmente por Joshua en Galaxy A22; falta archivar
  evidencia formal.
- VR con A-Frame 1.8: granja explorable en 360° con colisiones, trece árboles,
  cinco hotspots (incluye detalle escondido), cinco teletransportes, lago con
  peces, abejas ambientales y narración sintética; validación headless y de
  navegación pasó. La captura compartida el 2026-11-27 en modo inmersivo muestra
  la vista estereoscópica casi negra y geometría muy fragmentada; es un defecto
  visual observado, causa aún no diagnosticada y no se considera aprobado.
- Video maestro 720p, móvil 360p y vertical 1080 × 1920 regenerados con FFmpeg,
  SRT y cama sonora; falta la escucha/aprobación de Joshua.
- 2026-11-27: las fichas VR se cierran con botón DOM, `Escape` y teletransporte;
  se retiró la X de la escena para evitar duplicar controles. Las ventanas AR usan
  botones de texto «Cerrar» y «Volver a AR»; no tenían una X gráfica en el código.
  El video AR pausa MindAR y el render, y se reanuda al cerrar. Smoke y builds
  pasaron; la prueba física sigue pendiente.
- Visor público: `https://proyecto-integrador-uni-ten.vercel.app`. La prueba
  general de AR y video pasó. Capturas en `docs/evidencias/2026-11-27/`. Los
  cambios locales posteriores a `7eeb98f` todavía no están publicados.
- Documentación actualizada en `README.md`,
  `docs/diario.md`, `docs/bitacora-ia.md` y `docs/scrum/`.
- Evidencias de compra, renders y catálogo responsivo en
  `docs/evidencias/2026-11-10/`.
- Memoria consolidada en `docs/memoria.md`; guion y checklist de defensa en
  `docs/defensa.md`; presentación HTML y PDF en `docs/presentacion.html` y
  `docs/presentacion.pdf`.
- QA final del 2026-11-25: MySQL `healthy`, API `db: "up"`, build de tienda y
  visor, `COMMERCE_SMOKE_OK`, `AR_PREVIEW_SMOKE_OK` y móvil a 390 px sin
  desbordamiento. Evidencias en `docs/evidencias/2026-11-25/`.

## Después de la entrega

1. Diagnosticar la escena casi negra/fragmentada vista en la captura WebXR y
   repetir la prueba con datos del dispositivo, navegador y visor.
2. Escuchar/aprobar la cama sonora. Los MP4 ya están regenerados y revisados
   técnicamente.
3. Ensayar 20 minutos de presentación, preguntas y el cambio en vivo.

## Archivos clave

- Tienda: `apps/store/src/App.jsx`, `components/ProductCard.jsx`,
  `components/CartPanel.jsx`, `api.js`, `public/productos/`.
- API: `server/src/index.js`, `server/src/routes/commerce.js`,
  `server/src/db.js`, `server/scripts/commerce-smoke-test.mjs`.
- Base de datos: `db/schema.sql`, `db/seed.sql`, `docker-compose.yml`.
- AR/VR: `apps/ar-preview/ar.html`, `vr.html`, `src/ar.js`, `src/vr.js`,
  `src/vr.css`, `scripts/smoke-test.mjs`.
- Modelos y recursos: `assets/models/`, `assets/targets/`, `assets/video/`,
  `assets/audio/`.
- Render: `scripts/blender_render_producto_miel.py`,
  `scripts/blender_render_productos_restantes.py`.
- Documentación: `docs/diario.md`,
  `docs/bitacora-ia.md`, `docs/scrum/`, `docs/evidencias/`.
- Skills locales de Blender/WebAR: `.opencode/skills/`.

## Reglas de contenido

- El video es una **recreación didáctica original**; declararlo siempre como
  “Recreación didáctica · no es metraje documental”.
- No hay metraje real, testimonios ni productos reales.
- No usar el modelo de terceros “Tetragonica angustula Bee” de
  Nyilonelycompany.
- La autoría manual de los modelos debe ser de Joshua y estar documentada.
- No agregar login, pasarela de pago real, reseñas inventadas ni administración
  de pedidos reales. El panel de pedidos de demostración local, de solo lectura,
  está permitido por la guía; debe seguir sin exponer información personal.
- No commitear secretos ni archivos `.env`.
