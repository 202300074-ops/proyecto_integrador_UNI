# Product backlog

Estimaciones preliminares en puntos de historia. Se ajustan al final de cada
sprint. El orden prioriza lo que se necesita para la entrega y la defensa.

## Épicas

| ID | Épica | Resultado esperado |
| --- | --- | --- |
| E1 | Fundación técnica | Repositorio, MySQL 8, API y catálogo funcionando. |
| E2 | Compra simulada | Carrito, cupones, pedido y pago simulado. |
| E3 | Realidad aumentada | Etiqueta con abeja animada y video. |
| E4 | Video y audio | Recreación didáctica de la cosecha. |
| E5 | Realidad virtual | Meliponario navegable con hotspots. |
| E6 | Documentación y defensa | Memoria, evidencias, bitácora y presentación. |

## Historias

| ID | Historia | Criterio de aceptación | Puntos | Sprint | Estado |
| --- | --- | --- | --- | --- | --- |
| S1-01 | Como equipo quiero un repositorio con workspaces para separar API y tienda. | `npm install` funciona; API y tienda arrancan por separado. | 2 | 1 | Hecho |
| S1-02 | Como equipo quiero MySQL 8 en Docker con esquema y datos de prueba. | Contenedor `healthy`; 8 tablas; 4 productos y 6 variantes. | 3 | 1 | Hecho |
| S1-03 | Como visitante quiero ver el catálogo desde la API. | `/api/products` devuelve productos activos con variantes; `/api/health` responde. | 5 | 1 | Hecho |
| S1-04 | Como visitante quiero filtrar y abrir la ficha de un producto. | Filtros por categoría; ficha con variantes, precio y stock. | 5 | 1 | Hecho |
| S1-05 | Como visitante quiero usar el catálogo en mi teléfono. | A 390 px no hay desbordamiento; el diálogo se lee y se cierra. | 2 | 1 | Hecho |
| S1-06 | Como equipo queremos documentar el Bloque 1. | README, diario, bitácora y evidencias actualizadas. | 3 | 1 | Hecho |
| S2-01 | Como visitante quiero agregar productos al carrito. | Se agregan variantes, se cambia cantidad y se calcula el subtotal. | 5 | 2 | Hecho (UI y evidencia en `docs/evidencias/2026-11-10/`) |
| S2-02 | Como visitante quiero aplicar un cupón. | `BIENVENIDA10` aplica 10 % desde $200 y muestra el descuento. | 3 | 2 | Hecho (validado en API y UI) |
| S2-03 | Como visitante quiero simular un pedido. | Se guarda `orders` + `order_items` y se muestra confirmación. | 5 | 2 | Hecho (transacción, stock, cupón e historial) |
| S2-04 | Como visitante quiero escanear la etiqueta y ver la abeja. | MindAR reconoce el target y muestra el GLB animado. | 8 | 2 | En curso (Joshua validó el target y la abeja en teléfono; falta archivar evidencia) |
| S2-05 | Como visitante quiero ver el video de la cosecha en AR. | El video se reproduce dentro de la experiencia AR. | 5 | 2 | En curso (video validado en Galaxy A22 sin trabas; falta archivar evidencia) |
| S2-06 | Como equipo queremos el video editado con Python + FFmpeg. | MP4 reproducible, audio nivelado y rótulo de recreación didáctica. | 8 | 2 | Hecho (720p, narración sintética y fuentes documentadas) |
| S3-01 | Como visitante quiero recorrer el meliponario en VR. | Escena A-Frame con jobón, abeja y hotspots navegables. | 8 | 3 | En curso (A-Frame 1.8, cuatro hotspots, tres teletransportes y fauna; falta prueba física) |
| S3-02 | Como visitante quiero escuchar la narración del recorrido. | Audio integrado con control de reproducción. | 3 | 3 | En curso (narración sintética y controles integrados; falta validar en WebXR físico) |
| S3-03 | Como equipo queremos la memoria y las evidencias finales. | Documento con arquitectura, pruebas, conclusiones y referencias. | 8 | 3 | Hecho (`docs/memoria.md` y `docs/evidencias/2026-11-25/`) |
| S3-04 | Como equipo queremos preparar la defensa. | Presentación de 10-15 min, demo ensayada y respaldo del video/GLB. | 5 | 3 | En curso (guion y PDF listos; falta ensayo y respaldo físico) |

## Definición de terminado

Una historia está terminada cuando:

1. Cumple sus criterios de aceptación.
2. Se probó al menos una vez con datos reales de la base.
3. No rompe el build (`npm run build`).
4. Tiene evidencia en `docs/evidencias/`.
5. Se puede explicar en la defensa sin leer el código.
6. La documentación relacionada está actualizada.

## Prioridad si falta tiempo

1. Catálogo, ficha y base de datos.
2. Etiqueta AR con video.
3. Video de cosecha.
4. Meliponario VR.
5. Carrito y pago simulado.
6. Extras de diseño.

La entrega y la defensa valen más que una función extra a medio terminar.
