# Cierre y verificación final — 2026-11-25

Evidencias de la revisión final antes de la entrega del 26–27 de noviembre de
2026. La sesión se ejecutó en Windows con Node 22.17.1, Docker 28.3.0 y Chrome
158.

## Resultados

- MySQL 8.4 en Docker: contenedor `melipona-db` en estado `healthy`.
- `GET /api/health`: `200`, `db: "up"`.
- `GET /api/products`: cuatro productos y seis variantes.
- `npm run build`: tienda compilada sin errores.
- `npm run test:commerce`: `COMMERCE_SMOKE_OK`; cupón, mínimo, bloqueo de stock y
  pedido validados; el pedido de prueba se elimina al terminar.
- Tras la prueba quedaron los dos pedidos manuales originales en `pending`,
  `BIENVENIDA10 used_count = 0` y el inventario intacto.
- `npm --prefix apps/ar-preview run build`: visor compilado sin errores.
- `npm --prefix apps/ar-preview run test:smoke`: `AR_PREVIEW_SMOKE_OK`; visor,
  VR, hotspots, fauna, MindAR, target, modelos, audio y videos verificados.
- Revisión móvil por CDP a 390 × 844: `innerWidth = 390`,
  `scrollWidth = 390`, `clientWidth = 390`, sin desbordamiento horizontal.
- La portada y el catálogo identifican el caso y los productos como simulados o
  conceptuales; el seed y la base activa usan la misma redacción.

## Capturas

- `tienda-final-escritorio.png`: portada de la tienda a 1440 × 1200.
- `tienda-final-movil.png`: portada a 390 × 844 con emulación móvil.
- `tienda-final-catalogo.png`: catálogo a 1440 px; las cuatro imágenes WebP de
  800 × 1000 cargaron completas.
- `producto-vela-final-foco.png`: re-render 1600 × 2000 con foco frontal de la
  etiqueta; Blender terminó en 863.0 s.
- `visor-final.png`: visor 3D del meliponario.
- `vr-final.png`: recorrido VR con hotspots, panel y narración.
- `presentacion-portada.png`, `presentacion-tienda.png` y `presentacion-vr.png`:
  revisión de `docs/presentacion.html`.

El deck interactivo está en `docs/presentacion.html`; el PDF de entrega en
`docs/presentacion.pdf` tiene 12 páginas. La vela de catálogo se re-renderizó con
foco frontal; el PNG final y su WebP se actualizaron.

## Notas

- La captura móvil se tomó con emulación de dispositivo por CDP. Una captura
  directa con `--window-size=390` en Windows puede recortarse por el tamaño mínimo
  de ventana de Chrome y no debe usarse como evidencia de responsive.
- Las pruebas físicas de AR, checkout y WebXR siguen pendientes de evidencia
  formal en dispositivo.
- El pase manual de los modelos en Blender sigue pendiente.
- El video y los GLB están en `assets/`; se recomienda respaldarlos en USB o nube
  antes de la defensa.

## Comandos usados

```powershell
docker compose up -d
docker inspect --format '{{.State.Health.Status}}' melipona-db
npm run build
$env:API_BASE='http://127.0.0.1:3000/api'; npm run test:commerce
npm --prefix apps/ar-preview run build
npm --prefix apps/ar-preview run test:smoke
```
