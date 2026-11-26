# Evidencia del carrito, pedido y renders de producto

## Compra simulada

- `carrito-cupon.png`: carrito con variante agregada, cantidad, subtotal y cupón
  `BIENVENIDA10` aplicado.
- `pedido-simulado.png`: confirmación de pedido registrado con descuento y estado
  pendiente; no se realizó cobro.
- `carrito-cupon-movil.png`: el mismo carrito a 390 px, sin desbordamiento
  horizontal y con el cupón aplicado.
- `pedido-simulado-movil.png`: confirmación del pedido a 390 px.

La compra se probó contra la API y MySQL local. El pedido sintético de prueba se
eliminó al terminar y se restauraron el inventario y el contador del cupón. La
prueba móvil reportó `innerWidth = 390`, `scrollWidth = 390` y un panel de ancho
390, sin desbordamiento.

## Renders de producto

- `producto-miel-final.png`: 1600 × 2000, 40 muestras, 554.2 s.
- `producto-jabon-final.png`: 1600 × 2000, 32 muestras, 329.3 s.
- `producto-balsamo-final.png`: 1600 × 2000, 32 muestras, 343.2 s.
- `producto-vela-final.png`: 1600 × 2000, 32 muestras, 560.5 s.
- `producto-*-prueba.png`: previews de encuadre a 640 × 800 y 16 muestras.

Los cuatro renders usan el mismo estudio crema, cámara con DOF y Cycles CPU en
Blender 5.2.3 LTS. Las escenas quedaron en `assets/models/producto-*.blend` y los
scripts en `scripts/blender_render_producto_miel.py` y
`scripts/blender_render_productos_restantes.py`.

El re-render de la vela con foco frontal se documenta en
`docs/evidencias/2026-11-25/producto-vela-final-foco.png`.

Las versiones publicadas en la tienda son WebP de 800 × 1000 en
`apps/store/public/productos/`. Se usan en las tarjetas del catálogo y en la ficha
de producto. El build de la tienda pasó después de integrarlas.

- `tienda-productos.png`: catálogo completo a 1440 px con las cuatro imágenes,
  precios y stock cargados desde la API.
- `tienda-productos-movil.png`: catálogo a 390 px. La medición por DevTools
  confirmó `innerWidth = 390`, `scrollWidth = 390`, cuatro imágenes cargadas
  (`naturalWidth = 800`) y ninguna solicitud fallida.
