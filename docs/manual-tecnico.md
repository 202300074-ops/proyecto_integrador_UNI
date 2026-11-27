# Manual técnico

## 1. Propósito y arquitectura

Sak P'o' Kaab es un caso académico simulado. La solución integra una tienda
React/Vite, una API Express, MySQL 8.4 en Docker y un visor independiente de AR/VR
con A-Frame y MindAR.

```text
Navegador ── React/Vite :5173 ── /api proxy ── Express :3000 ── MySQL :3306
Teléfono/navegador ── A-Frame + MindAR :5174 ── GLB / video / audio
```

## 2. Requisitos

- Node.js 22 recomendado; el `package.json` raíz admite Node 20 o superior.
- npm 10 o superior.
- Docker Desktop y Docker Compose v2.
- Puertos locales 3000, 3306, 5173 y 5174 disponibles.
- Blender y FFmpeg para regenerar modelos, renders, audio o video.

En la sesión remota de cierre del 26 de noviembre de 2026 se observó Node.js
20.20.2. Blender y FFmpeg no se encontraron en `PATH` en ese entorno. En la sesión
local posterior se usó FFmpeg 9.0.2 para regenerar y validar el máster, el móvil y
el vertical; Blender sigue pendiente para el pase manual.

## 3. Instalación y arranque

Desde la raíz del repositorio:

```powershell
npm install
Copy-Item .env.example .env
npm run db:up
npm run dev
```

El contenedor MySQL inicializa `db/schema.sql` y `db/seed.sql` al crear el
volumen. Espera a que su estado sea `healthy`. No ejecutes `npm run db:reset` para
una revisión normal: borra el volumen. Conserva los pedidos manuales de prueba
documentados en `AGENTS.md`.

En otra terminal se puede arrancar el visor:

```powershell
npm --prefix apps/ar-preview run dev
```

Si se personaliza el origen del visor para Vite, define
`VITE_AR_PREVIEW_URL`; por defecto los botones de la tienda apuntan a
`http://localhost:5174`.

## 4. Servicios

| Servicio | URL local | Función |
| --- | --- | --- |
| Tienda | `http://localhost:5173` | Catálogo, fichas, carrito y checkout simulado |
| API | `http://localhost:3000/api` | Salud, catálogo, cupones y pedidos |
| Visor | `http://localhost:5174` | GLB de abeja y jobón |
| AR | `http://localhost:5174/ar.html` | Seguimiento de etiqueta y recreación didáctica |
| VR | `http://localhost:5174/vr.html` | Meliponario, hotspots, teletransporte y audio |

### Endpoints principales

| Método | Ruta | Uso |
| --- | --- | --- |
| GET | `/api/health` | Estado de API y MySQL |
| GET | `/api/products` | Catálogo con variantes |
| GET | `/api/products/:slug` | Ficha de producto |
| POST | `/api/coupons/validate` | Validación de cupón |
| POST | `/api/orders` | Pedido de prueba con transacción y descuento de stock |
| GET | `/api/orders/demo` | Lista de hasta 25 pedidos `mock`, solo fuera de producción y sin datos personales |

El panel de pedidos es de solo lectura y solo se muestra en desarrollo. `npm start`
inicia la API con `NODE_ENV=production`, y la ruta responde `404` en ese modo. La
consulta usa una lista
fija de campos: identificador parcial, estado, total, cantidad de artículos y
fecha; nunca devuelve nombre, correo, teléfono ni dirección. No es un panel para
operar pedidos reales.

## 5. Base de datos

El esquema de demostración contiene usuarios, productos, variantes, cupones,
pedidos, artículos de pedido, redenciones de cupón e historial de estados. El
checkout usa `payment_method = mock`; no existe una pasarela de pago real. Las
consultas de escritura del checkout están parametrizadas y se ejecutan dentro de
una transacción.

## 6. Pruebas y builds

```powershell
npm run build
npm run test:commerce
npm --workspace @sak-po-kaab/server run test:production-panel
npm --prefix apps/ar-preview run build
npm --prefix apps/ar-preview run test:smoke
```

La prueba de comercio crea un pedido con correo `.test`, valida cupón, subtotal y
stock y luego elimina únicamente ese pedido y restaura su stock/cupón. No elimina
los pedidos manuales de prueba. Si el watcher de API se reinicia durante la
prueba, utiliza la instancia estable descrita en `AGENTS.md`.

## 7. Assets y regeneración multimedia

- Modelos editables: `assets/models/*.blend`.
- GLB para navegador: `assets/models/abeja.glb` y `assets/models/jobon.glb`.
- Etiqueta y target: `assets/targets/`.
- Video y poster: `assets/video/`.
- Narraciones: `assets/audio/`.
- Scripts Blender y video: `scripts/`.
- Símbolo animado 2D: `assets/animation/logo-sak-po-kaab.svg`.

El video es una **recreación didáctica · no es metraje documental**. Consulta
`docs/referencias-video.md` antes de regenerarlo o editar el guion. La revisión
manual de autoría de los modelos y la prueba WebXR física requieren a Joshua y
equipo físico; no se dan por realizadas por ejecutar el build.

## 8. Generación de la memoria PDF

Instala la dependencia documental y define el nombre institucional oficial antes
de exportar la portada:

```powershell
python -m pip install -r requirements-docs.txt
$env:INSTITUTION_NAME = "Nombre oficial de la institución"
python scripts/render_memory_pdf.py
```

El script genera `docs/memoria.html` y `docs/memoria.pdf` con Microsoft Edge. Si
Edge está en una ruta no estándar, define `EDGE_PATH` antes de ejecutarlo.

## 9. Límites de despliegue

El caso y los productos son simulados. No despliegues el endpoint de pedidos de
demostración como función administrativa ni lo habilites en producción. El
proyecto no incorpora autenticación, pagos reales, gestión de pedidos reales ni
analítica de usuarios. Usa datos de prueba y documenta cualquier cambio antes de
presentarlo.
