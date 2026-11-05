# Evidencia del Bloque 1

Fecha de la sesión: 2026-10-28 (capturas regeneradas el 2026-11-04 después de
corregir acentos y diseño móvil).

Objetivo: demostrar que MySQL 8, la API y el catálogo funcionan de punta a punta.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `catalogo.png` | Portada y catálogo en escritorio, 1440 px de ancho. |
| `catalogo-movil.png` | Catálogo completo a 390 px, sin desbordamiento horizontal. |
| `producto-movil.png` | Ficha de producto abierta en móvil, con variantes y stock. |
| `products.json` | Respuesta real de `GET /api/products`. |

## Comandos y resultados

### Contenedor de MySQL

```powershell
docker inspect --format '{{.State.Health.Status}}' melipona-db
```

Resultado: `healthy`.

```powershell
docker exec melipona-db mysql -umelipona -p"<contraseña-de-.env>" -D melipona `
  -e "SHOW TABLES; SELECT COUNT(*) FROM products; SELECT COUNT(*) FROM product_variants;"
```

Resultado:

- 8 tablas: `coupon_redemptions`, `coupons`, `order_items`,
  `order_status_history`, `orders`, `product_variants`, `products`, `users`.
- 4 productos.
- 6 variantes.

### API

```powershell
curl.exe -s http://127.0.0.1:3000/api/health
```

Resultado:

```json
{"ok":true,"service":"sak-po-kaab-api","db":"up","timestamp":"2026-10-29T04:49:47.392Z"}
```

```powershell
curl.exe -s http://127.0.0.1:3000/api/products
```

Resultado: 4 productos con sus variantes; el JSON completo está en
`products.json`.

```powershell
curl.exe -s http://127.0.0.1:3000/api/products/jabon-sak-po
```

Resultado: `200` con el producto "Jabón Sak P'o'" y sus 2 variantes.

```powershell
curl.exe -s http://127.0.0.1:3000/api/products/no-existe
```

Resultado: `404` con `{"error":"product_not_found"}`.

### Build

```powershell
npm run build
```

Resultado:

- 29 módulos transformados.
- `dist/index.html`: 0.94 kB.
- CSS: 20.70 kB (4.58 kB gzip).
- JS: 160.23 kB (50.83 kB gzip).
- Compilado en 4.03 s.

### Prueba móvil

Se usó Puppeteer con Microsoft Edge para emular un viewport real de 390 x 844.

Resultado:

- `innerWidth`: 390.
- `scrollWidth`: 390.
- `bodyScrollWidth`: 390.
- Diálogo de producto: abierto y dentro del ancho.
- Filtro "Jabones": mostró el producto de jabón.

Nota: una captura anterior con `msedge --headless --window-size=390` parecía
cortada, pero el navegador imponía un ancho mínimo de 492 px. Esa captura no era
una prueba válida; se reemplazó por la emulación con Puppeteer.

## Cómo reproducir

```powershell
npm install
Copy-Item .env.example .env
npm run db:up
npm run dev
```

Luego abrir <http://localhost:5173> y <http://localhost:3000/api/health>.

## Aviso

La cooperativa y la marca son un caso de estudio simulado. Los datos de la base
son de demostración y no representan ventas reales.
