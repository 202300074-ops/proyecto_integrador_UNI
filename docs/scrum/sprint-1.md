# Sprint 1. Base funcional del catálogo

Fechas propuestas: **2026-10-28 a 2026-11-08**.
Duración: 2 semanas.
Horario de trabajo: 7 a 11 pm entre semana; fin de semana por confirmar.

## Objetivo del sprint

Tener una tienda que muestre productos reales desde MySQL, con API propia,
filtros, ficha de producto y diseño móvil, además de la documentación mínima
para demostrar que funciona.

## Sprint backlog

| Historia | Puntos | Estado |
| --- | --- | --- |
| S1-01 Repositorio y workspaces | 2 | Hecho |
| S1-02 MySQL 8 con esquema y seed | 3 | Hecho |
| S1-03 API de catálogo y salud | 5 | Hecho |
| S1-04 Catálogo, filtros y ficha | 5 | Hecho |
| S1-05 Diseño móvil sin desbordamiento | 2 | Hecho |
| S1-06 Documentación del Bloque 1 | 3 | En curso |
| **Total** | **20** | **17 hechos, 3 en curso** |

## Trabajo realizado

- Monorepo con `server` y `apps/store`.
- MySQL 8.4 en Docker con volumen, healthcheck y scripts de inicio.
- 8 tablas: usuarios, productos, variantes, cupones, pedidos, detalle de pedido,
  canjes de cupón e historial de estados.
- Seed con 4 productos, 6 variantes y el cupón `BIENVENIDA10`.
- API Express con `/api/health`, `/api/products` y `/api/products/:slug`.
- Catálogo React con filtros, stock, precio desde, ficha de producto y aviso de
  que el carrito llega en el Sprint 2.
- Corrección de acentos y de la codificación UTF-8.
- Corrección del desbordamiento horizontal en móvil.
- Evidencias de API, build y capturas.

## Daily log

### 2026-10-28

- Se creó el repositorio y la estructura.
- Se escribieron el esquema, el seed, la API y el catálogo.
- `npm install` terminó con 242 paquetes.
- La imagen de MySQL seguía descargándose; el contenedor quedó en `starting`.

### 2026-11-04

- El contenedor quedó `healthy`; se verificaron 8 tablas, 4 productos y 6
  variantes.
- Se probaron los endpoints: salud `200`, catálogo `200`, detalle `200`,
  inexistente `404`.
- `npm run build` compiló 29 módulos.
- Se corrigieron acentos y desbordamiento móvil.
- Se generaron capturas de escritorio, móvil y ficha de producto.
- Se probó el catálogo a 390 px sin desbordamiento.

## Sprint review

Demo realizada:

1. Se abrió la tienda en `http://localhost:5173`.
2. Se mostraron los 4 productos y las 6 variantes.
3. Se filtró por "Jabones" y se abrió la ficha del jabón.
4. Se mostró el stock y los precios traídos desde MySQL.
5. Se mostró `GET /api/health` y `GET /api/products`.
6. Se mostró la vista móvil a 390 px.

Resultado: el objetivo del sprint se cumple. La documentación queda en curso
hasta cerrar la bitácora y el primer commit.

## Retrospectiva

Qué funcionó:

- Separar API y tienda permitió probar cada parte por separado.
- El seed con datos reales hizo visible el catálogo desde el primer día.
- Las capturas y el JSON de la API son evidencia fácil de revisar.

Qué mejorar:

- Verificar la codificación UTF-8 desde el inicio, no al final.
- Probar el diseño móvil con emulación real, no solo con una ventana pequeña.
- Revisar Docker Desktop antes de culpar a la API cuando hay `ECONNREFUSED`.

Acciones para el Sprint 2:

- Instalar Blender y FFmpeg antes de empezar el modelado y el video.
- Probar la AR en el Galaxy A22 con HTTPS desde el primer prototipo.
- No empezar el carrito hasta cerrar la etiqueta AR y el video.

## Evidencias

- `docs/evidencias/2026-10-28/catalogo.png`: vista de escritorio.
- `docs/evidencias/2026-10-28/catalogo-movil.png`: vista móvil a 390 px.
- `docs/evidencias/2026-10-28/producto-movil.png`: ficha de producto.
- `docs/evidencias/2026-10-28/products.json`: respuesta real de la API.
- `docs/bitacora-ia.md`: interacciones y verificaciones.
