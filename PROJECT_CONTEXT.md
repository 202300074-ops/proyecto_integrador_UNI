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
- La abeja y el jobón se modelan manualmente en Blender para cumplir con la
  autoría. La IA solo apoya concepto, texturas y props secundarios.
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
- Blender y FFmpeg aún no están instalados.
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

Pendiente:

- Sprint 2: carrito, cupones, pago simulado, etiqueta AR y video.
- Sprint 3: meliponario VR, modelo 3D final, audio, documentación y defensa.

## Siguientes pasos concretos

1. Instalar Blender y FFmpeg (winget) y verificar versiones.
2. Modelar la abeja y el jobón en Blender; exportar GLB optimizado.
3. Crear el video de cosecha con Python + FFmpeg y declararlo como recreación.
4. Implementar la etiqueta AR con MindAR y el video integrado.
5. Implementar el meliponario VR con A-Frame.
6. Completar carrito, cupones y pago simulado.
7. Cerrar documentación, evidencias, bitácora y presentación.

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
- Confirmar si se instalan Blender y FFmpeg con winget o manualmente.
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
