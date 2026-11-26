# Manual de usuario

## Aviso antes de comenzar

Sak P'o' Kaab es un proyecto académico y un caso de estudio simulado. Los
productos, precios, existencias y pedidos son datos de demostración; no se
realizan ventas ni cobros reales.

## Ver el catálogo

1. Abre `http://localhost:5173` con la tienda iniciada.
2. Usa los filtros para cambiar entre miel, jabones, cosméticos y velas.
3. Selecciona un producto para ver sus variantes, precio y existencias de prueba.
4. Cierra la ficha con **Cerrar** o la tecla **Esc**.

## Probar el carrito y cupón

1. En la ficha, pulsa **Agregar** junto a una variante disponible.
2. Abre **Carrito** y ajusta cantidades o elimina artículos.
3. Escribe `BIENVENIDA10`; aplica un descuento de demostración del 10 % a partir
   de $200 MXN de subtotal.
4. Completa el formulario de entrega de prueba y confirma el pedido.
5. La confirmación muestra el número y total del pedido. El pago es simulado.

Los datos de prueba no deben ser datos personales reales. La prueba automatizada
del repositorio limpia su propio pedido al finalizar.

## Consultar pedidos de demostración

En el modo de desarrollo local, usa el enlace **Pedidos de prueba** del pie de
página. El panel muestra hasta 25 pedidos simulados con identificador parcial,
estado, total, número de artículos y fecha. Es de solo lectura: no permite
cambiar el estado y no enseña datos de contacto. No aparece en el build de
producción.

## Probar realidad aumentada

1. Inicia `npm --prefix apps/ar-preview run dev`.
2. Abre `http://localhost:5174/ar.html` desde un teléfono.
3. Permite el acceso a la cámara. Si el navegador requiere un contexto seguro,
   usa HTTPS.
4. Pulsa **Ver etiqueta** y abre la etiqueta en papel tamaño A5/A4 o en otra
   pantalla.
5. Apunta la cámara a la etiqueta completa, con luz pareja y sin reflejos.
6. Cuando el target se detecte, explora la abeja y pulsa **Ver cosecha** para
   reproducir el video. Pulsa **Volver a AR** para volver a la cámara.

El video es una **recreación didáctica · no es metraje documental** y su voz es
sintética.

## Recorrer el meliponario virtual

1. Abre `http://localhost:5174/vr.html`.
2. En pantalla, arrastra para mirar y usa WASD o las marcas del suelo para
   desplazarte.
3. Mantén el cursor sobre un punto dorado para abrir su información.
4. Usa **Escuchar recorrido** para iniciar o pausar la narración.
5. Si tienes un visor WebXR, entra al modo VR desde el control del escenario.

El recorrido también puede usarse sin visor con mouse o pantalla táctil. La
compatibilidad y comodidad deben comprobarse en el dispositivo físico disponible.

## Ayuda rápida

| Síntoma | Revisión |
| --- | --- |
| La tienda no muestra productos | Comprueba Docker, MySQL y la API; revisa `/api/health` |
| No funciona AR | Revisa permiso de cámara, HTTPS, luz, target completo y que el visor esté en `:5174` |
| El video no inicia | Espera a que el botón se habilite y toca reproducir si el navegador bloquea autoplay |
| No aparece el botón de pedidos | El panel solo existe en desarrollo; no aparece en producción |
| VR no entra a modo casco | Comprueba compatibilidad WebXR y el origen HTTPS; también puedes usar mouse/táctil |
