# Contexto del proyecto

Documento de trabajo para mantener el hilo entre sesiones. No sustituye a la
memoria académica ni a la bitácora de IA.

## Objetivo

Entregar el proyecto integrador de **Multimedia y Diseño Digital**:

- Tienda en línea de miel y jabón de la abeja melipona.
- Etiqueta con realidad aumentada que muestra una abeja animada y un video.
- Meliponario virtual navegable en realidad virtual.
- Video del proceso de cosecha editado con Python + FFmpeg.
- Documentación, evidencias, bitácora de IA y defensa oral.

Fecha de entrega: **26 y 27 de noviembre de 2026**.
Defensa: **30 de noviembre al 4 de diciembre de 2026**.

## Reglas del caso de estudio

- La cooperativa, la marca y el meliponario son **simulados**.
- No se tuvo acceso a un meliponario real; el video será una **recreación
  didáctica** y se declarará así en la interfaz y en la memoria.
- Los datos de mercado deben venir de fuentes reales y citarse. No se inventan
  entrevistas, métricas ni testimonios.
- La autoría final de la abeja y el jobón corresponde a Joshua. La base actual se
  generó mediante scripts asistidos por IA; Joshua debe hacer modificaciones
  manuales sustanciales en Blender, documentarlas y explicar sus decisiones antes
  de presentar los modelos como propios.
- No usar el modelo de terceros "Tetragonisca angustula Bee" de
  Nyilonelycompany.
- Todo lo que se entregue debe poder explicarse en la defensa.

## Marca

- Nombre: **Sak P'o' Kaab**.
- Tagline: "Miel y jabón de la abeja melipona".
- `sak p'o'` = jabón; `kaab` = miel/abeja; `xunáan kaab` = Melipona beecheii.
- Arquitectura:
  - **Kaab**: miel.
  - **Sak P'o'**: jabón.
  - **Xunán**: cosméticos.
  - **Jobón**: velas.
- Slug del proyecto: `sak-po-kaab`.

## Stack confirmado

- Node.js 22 + Express 4 + React 18 + Vite 6 + Tailwind 3.4.
- MySQL 8.4 en Docker (XAMPP/MariaDB 10.4 no cumple con MySQL 8).
- AR: A-Frame 1.6 + MindAR 1.2.
- VR: A-Frame 1.8 en una aplicación separada.
- 3D: Blender LTS, exportación GLB.
- Video/audio: Python 3.12 + FFmpeg.

## Entorno verificado

- Node v22.17.1, npm 10.9.2.
- Docker 28.3.0, Docker Compose v2.38.1.
- MySQL 8.4.13 en el contenedor `melipona-db`.
- Puertos usados: 3000 (API), 3306 (MySQL), 5173 (tienda).
- `gh` no está instalado; el repositorio se creó manualmente en GitHub.
- Blender 5.2.3 LTS y FFmpeg 9.0.2 están instalados y verificados.
- Windows PowerShell 5.1; usar `cmd1; if ($?) { cmd2 }` en lugar de `&&`.

## Repositorio

- Remoto: <https://github.com/202300074-ops/proyecto_integrador_UNI.git>
- Ruta local: `C:\Users\tiojo\dev\proyecto_integrador_UNI` (fuera de OneDrive).
- Rama: `main`.
- Identidad local: Joshua Israel Cabrera Camacho,
  `202300074-ops@users.noreply.github.com`.
- `.env` está ignorado. Las credenciales de ejemplo están en `.env.example`.

## Estado actual

Completado (Bloque 1):

- Estructura del monorepo con workspaces.
- MySQL 8.4 con 8 tablas y seed de 4 productos / 6 variantes.
- API Express con `/api/health`, `/api/products` y `/api/products/:slug`.
- Catálogo React con filtros, ficha de producto y diseño móvil.
- Pruebas de API, build y capturas en `docs/evidencias/2026-10-28/`.
- Documentación base: README, contexto, diario, bitácora de IA, aprendizaje y
  Scrum.

Completado (Sprint 2):

- Blender 5.2.3 y FFmpeg 9.0.2 instalados y verificados.
- `scripts/blender_model.py` genera `assets/models/modelo.blend`, `abeja.glb` y
  `jobon.glb`, además de previews Workbench.
- La abeja exporta un clip `SakPoKaab` y tiene 9,908 triángulos; el jobón tiene
  14,852 triángulos.
- Ambos GLB se importaron en una escena limpia de Blender; la abeja cargó 21
  mallas y el jobón una malla. La animación se verificó en el visor, en MindAR de
  escritorio y en el Galaxy A22.
- `scripts/blender_render_eevee.py` genera los cuatro renders EEVEE `final-*.png`
  en `docs/evidencias/2026-11-04/`.
- `apps/ar-preview` contiene un meliponario estilizado en A-Frame con jobón,
  árboles, flores, pasto, colinas, un lago con peces, seis abejas en vuelo y fauna
  adicional: dos mariposas, una libélula, un colibrí y una lagartija. La prueba HTTP
  sirve ambos GLB y el build compila el visor. `/ar.html` integra cámara y MindAR
  con `assets/targets/etiqueta-sakpokaab.mind`; el target se validó con cámara
  virtual y en el Galaxy A22. `/vr.html` usa A-Frame 1.8 con una granja explorable
  en 360° (colisiones de `vr-explore`), cinco hotspots, cinco zonas de
  teletransporte, panel de información y narración sintética con control
  reproducir/pausar.
- `assets/video/cosecha-melipona-recreacion.mp4` es una animación original 720p,
  con narración sintética es-MX, generada con Python/Pillow y FFmpeg. La AR usa
  un derivado 640 × 360 predescargado en el modal **Ver cosecha** de `/ar.html`.
- Referencias visuales en `docs/referencias-3d.md`; evidencias de escritorio y de
  la fauna adicional en `docs/evidencias/2026-11-08/`. Joshua validó target y
  video en el Galaxy A22; falta archivar la evidencia formal de esa prueba.
- El render configura explícitamente el mundo crema y ajusta la iluminación y el
  piso; `modelo.blend` no tenía mundo asignado.
- Carrito adaptable con variantes, cantidades, cupón `BIENVENIDA10` y checkout
  simulado. La API `POST /api/orders` usa transacción, descuenta stock y registra
  cupón e historial. Pruebas y capturas en `docs/evidencias/2026-11-10/`.
- Cuatro renders de producto a 1600 × 2000 con Cycles CPU y estudio crema:
  miel, jabón, bálsamo y vela. Las escenas están en `assets/models/producto-*.blend`
  y las versiones WebP de 800 × 1000 se usan en las tarjetas y la ficha de la
  tienda desde `apps/store/public/productos/`.

Cierre documental (2026-11-25):

- Memoria consolidada en `docs/memoria.md`.
- Guion, demo, preguntas y checklist en `docs/defensa.md`.
- Presentación navegable en `docs/presentacion.html` y PDF de 13 diapositivas en
  `docs/presentacion.pdf`.
- Evidencias finales en `docs/evidencias/2026-11-25/`.
- QA: MySQL `healthy`, API `db: "up"`, cuatro productos y seis variantes.
- `npm run build`, `npm run test:commerce` y
  `npm --prefix apps/ar-preview run test:smoke` pasan.
- Revisión móvil por CDP a 390 px: `innerWidth = 390`, `scrollWidth = 390`.

Cierre de criterios y correcciones (2026-11-26):

- Plan y mapas conceptuales de mercadotecnia en `docs/mercadotecnia/`.
- Panel local de pedidos `mock` de solo lectura, sin datos personales y desactivado
  en producción.
- Símbolo SVG animado con movimiento reducido; manuales y declaración de IA.
- Memoria citada y exportada a PDF; deck actualizado a 13 diapositivas/PDF.
- Captura desktop de tienda actualizada en `docs/evidencias/2026-11-26/`.
- Renderer prepara SRT, cama sonora original y salida vertical. No se regeneraron
  MP4 porque FFmpeg no está en `PATH`; la cama sonora requiere escucha de Joshua.
- En esta sesión se observó Node 20.20.2, Python 3.13.15 y no se encontraron
  Blender ni FFmpeg en `PATH`; la prueba física y el pase manual 3D siguen siendo
  responsabilidad de Joshua.

Pendiente:

- Pase manual de los modelos en Blender y documentación de la autoría.
- Evidencia formal de AR/video y checkout en el Galaxy A22.
- Prueba física de WebXR, narración y comodidad.
- Escuchar y aprobar la cama sonora; regenerar los MP4 con SRT y exportación
  vertical cuando FFmpeg esté disponible.
- Ensayar la presentación PDF durante 20 minutos, al menos 15 minutos de preguntas
  y un cambio en vivo de unos 10 minutos; preparar respaldos físicos del video y
  los GLB.

## Siguientes pasos concretos

1. Abrir `assets/models/modelo.blend`, hacer modificaciones manuales propias y
   guardar capturas del proceso para sustentar la autoría.
2. Archivar la evidencia de la validación de AR/video y checkout en el Galaxy A22.
3. Validar hotspots, teletransporte y narración de `/vr.html` con un visor VR
   físico.
4. Confirmar el nombre institucional y regenerar `docs/memoria.pdf` con la portada
   completa.
5. Ensayar 20 minutos de exposición, 15 minutos de preguntas y el cambio en vivo.
6. Revisar la memoria y las evidencias antes de la entrega.

## Riesgos

- Tiempo: solo se trabaja de 7 a 11 pm y fines de semana. Priorizar el producto
  y la defensa sobre extras.
- AR en teléfono: la cámara requiere HTTPS. Usar Netlify, GitHub Pages o
  cloudflared para probar en el Galaxy A22.
- Blender/FFmpeg: si no se instalan a tiempo, el video y el GLB se retrasan.
- Autoría: no usar modelos de terceros para la abeja ni para el jobón.
- Alcance: no prometer funciones que no se puedan explicar o demostrar.

## Dudas abiertas

- Confirmar si el fin de semana se trabaja solo de 16 a 18 o también de 9 a 13.
- Confirmar el nombre final de la cooperativa simulada y si aparecerá en la
  portada de la memoria.

## Comandos de verificación

```powershell
docker compose ps
docker inspect --format '{{.State.Health.Status}}' melipona-db
curl.exe -s http://127.0.0.1:3000/api/health
curl.exe -s http://127.0.0.1:3000/api/products
npm run build
```

## Regla de commits

No hacer commit hasta que el usuario lo pida o hasta que el asistente indique
"commit". Antes de commitear, revisar `git status` y `git diff`.
