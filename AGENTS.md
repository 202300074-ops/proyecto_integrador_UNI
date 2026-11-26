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
- Build: `npm run build`.
- Prueba de compra: `npm run test:commerce`.
- Si la prueba de comercio falla con `ECONNREFUSED` o `ECONNRESET`, el watcher
  de la API pudo reiniciarse durante la prueba. Levantar una instancia estable
  con `node server/src/index.js` en el puerto 3001 y ejecutar:
  `$env:API_BASE='http://localhost:3001/api'; npm run test:commerce`.

## Estado actual (2026-11-25)

- Compra simulada terminada: carrito, variantes, cantidades, cupón
  `BIENVENIDA10` (10 % desde $200), checkout, pedido transaccional, descuento de
  stock, redención e historial.
- `server/scripts/commerce-smoke-test.mjs` limpia sus propios pedidos y restaura
  stock/cupón.
- Tienda con cuatro renders de producto integrados como WebP de 800 × 1000 en
  `apps/store/public/productos/`, visibles en tarjetas y ficha.
- Renders finales de miel, jabón, bálsamo y vela en
  `docs/evidencias/2026-11-10/producto-*-final.png`; escenas en
  `assets/models/producto-*.blend`.
- La vela se re-renderizó con foco frontal en la etiqueta; PNG/WebP actualizados
  y verificados en la captura final del catálogo.
- AR/video validados funcionalmente por Joshua en Galaxy A22; falta archivar
  evidencia formal.
- VR con A-Frame 1.8, cuatro hotspots, tres teletransportes, panel y narración
  sintética; validación headless pasó, falta WebXR físico.
- Documentación actualizada en `README.md`, `PROJECT_CONTEXT.md`,
  `docs/diario.md`, `docs/bitacora-ia.md` y `docs/scrum/`.
- Evidencias de compra, renders y catálogo responsivo en
  `docs/evidencias/2026-11-10/`.
- Memoria consolidada en `docs/memoria.md`; guion y checklist de defensa en
  `docs/defensa.md`; presentación HTML y PDF en `docs/presentacion.html` y
  `docs/presentacion.pdf`.
- QA final del 2026-11-25: MySQL `healthy`, API `db: "up"`, build de tienda y
  visor, `COMMERCE_SMOKE_OK`, `AR_PREVIEW_SMOKE_OK` y móvil a 390 px sin
  desbordamiento. Evidencias en `docs/evidencias/2026-11-25/`.

## Pendientes inmediatos

1. Revisar la tienda y los renders en un teléfono físico; probar checkout y
   guardar evidencia.
2. Grabar o capturar la validación de etiqueta AR y video en el Galaxy A22.
3. Probar `/vr.html` y la narración con un visor WebXR físico.
4. Hacer el pase manual de abeja y jobón en Blender, documentar las
   modificaciones propias y registrar lmik3 solo como apoyo visual.
5. Ensayar la presentación PDF durante 12–15 minutos y respaldar físicamente el
   video/GLB.

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
- Documentación: `PROJECT_CONTEXT.md`, `docs/diario.md`,
  `docs/bitacora-ia.md`, `docs/scrum/`, `docs/evidencias/`.
- Skills locales de Blender/WebAR: `.opencode/skills/`.

## Reglas de contenido

- El video es una **recreación didáctica original**; declararlo siempre como
  “Recreación didáctica · no es metraje documental”.
- No hay metraje real, testimonios ni productos reales.
- No usar el modelo de terceros “Tetragonica angustula Bee” de
  Nyilonelycompany.
- La autoría manual de los modelos debe ser de Joshua y estar documentada.
- No agregar login, pasarela de pago real, reseñas inventadas ni panel admin.
- No commitear secretos ni archivos `.env`.
