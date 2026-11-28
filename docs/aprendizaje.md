# Aprendizaje y preparación de la defensa

Este documento no es un resumen de la IA: es una lista de lo que Joshua debe
poder explicar. Marca cada tema cuando lo domines.

## 1. Docker y MySQL

- Qué es un contenedor y por qué MySQL 8 no es lo mismo que MariaDB 10.4.
- Qué hace `docker-compose.yml`: imagen, variables, puertos, volumen,
  healthcheck e init scripts.
- Diferencia entre `docker compose down` y `down -v`.
- Por qué el volumen conserva los datos y por qué `db:reset` los borra.
- Qué significa `utf8mb4` y por qué importa para acentos y emojis.
- Cómo se comprueba que MySQL está listo:
  `docker inspect --format '{{.State.Health.Status}}' melipona-db`.
- Qué es una llave foránea y por qué `order_items` depende de `orders`.

Preguntas posibles:

- ¿Qué pasa si borras el volumen?
- ¿Dónde viven los datos si se cae el contenedor?
- ¿Por qué el healthcheck usa `mysqladmin ping`?

## 2. API con Express

- Qué es un middleware y en qué orden se ejecutan.
- Cómo se conecta `mysql2` con un pool y por qué no se abre una conexión por
  petición.
- Qué hace `decimalNumbers: true` con los precios.
- Diferencia entre `200`, `404` y `503`.
- Por qué el endpoint de salud consulta la base y no solo responde "ok".
- Cómo se evita una inyección SQL con parámetros (`?`).
- Qué es CORS y por qué el origen es `http://localhost:5173`.

Preguntas posibles:

- ¿Qué devuelve `/api/products` si no hay productos?
- ¿Qué pasa si MySQL está apagado?
- ¿Por qué el detalle usa `slug` y no `id`?

## 3. React y Vite

- Diferencia entre componente, props y estado.
- Qué hace `useEffect` al cargar el catálogo y por qué usa una bandera `active`.
- Qué hace `useMemo` en el filtro.
- Por qué cada tarjeta necesita una `key`.
- Cómo se abre y se cierra el diálogo; qué hace `aria-modal`.
- Qué es el proxy de Vite y por qué `/api` llega al puerto 3000.
- Diferencia entre `npm run dev` y `npm run build`.
- Qué es Tailwind y cómo se aplican los breakpoints `sm`, `md`, `lg`.
- Por qué se agregó `grid-cols-1`, `min-w-0` y `overflow-x-hidden`.

Preguntas posibles:

- ¿Dónde se guarda el carrito? (En el estado de React; el pedido se confirma
  contra la API).
- ¿Qué pasa si la API tarda?
- ¿Cómo se maneja un error de red?
- ¿Cómo se evita modificar el stock si falla el pedido? (Transacción y rollback).
- ¿Por qué el cupón se valida en la API y no solo en el frontend?
- ¿Qué diferencia hay entre subtotal, descuento y total?
- ¿Qué pasa si dos personas compran la última variante al mismo tiempo?
  (Bloqueo de inventario dentro de la transacción).

## 4. Pruebas y evidencia

- Diferencia entre una captura de pantalla y una prueba automatizada.
- Cómo se prueba una API con `curl.exe` o `Invoke-RestMethod`.
- Qué mide `scrollWidth` y por qué `scrollWidth = innerWidth` indica que no hay
  desbordamiento horizontal.
- Qué es Puppeteer y por qué se usó fuera del repositorio.
- Cómo se documenta un error: qué se esperaba, qué pasó, cómo se corrigió.

## 5. AR, VR y 3D

- Qué es un image target de MindAR y por qué la cámara necesita HTTPS.
- Diferencia entre AR y VR.
- Qué es un GLB y por qué se prefiere sobre un .blend para la web.
- Qué es un low-poly y por qué ayuda al rendimiento en teléfono.
- Qué es WebXR y qué navegadores lo soportan.
- Por qué la abeja y el jobón se modelan a mano.
- Cómo se declara que el video es una recreación didáctica.

## 6. Video y audio con Python + FFmpeg

- Qué es FFmpeg y para qué sirve en el proyecto.
- Diferencia entre editar en un programa gráfico y automatizar con un script.
- Qué hace un script de Python que llama a FFmpeg.
- Cómo se recorta, se une, se ajusta el volumen y se exporta un MP4.
- Por qué se debe usar audio sin derechos o propio.

## 7. Scrum

- Qué es el product backlog y qué es un sprint backlog.
- Qué es una historia de usuario y un criterio de aceptación.
- Qué es el definition of done.
- Qué es un burndown y cómo se lee.
- Qué se revisa en la sprint review y en la retrospectiva.
- Por qué el tablero debe reflejar el trabajo real, no el ideal.

## 8. Guion de demostración (5 minutos)

1. Abrir la tienda y mostrar la portada.
2. Filtrar por "Jabones" y abrir la ficha de producto.
3. Agregar una variante al carrito y mostrar cantidades y subtotal.
4. Aplicar `BIENVENIDA10` y mostrar el descuento.
5. Confirmar el pedido simulado y mostrar el número de pedido.
6. Mostrar `GET /api/health` y `GET /api/products` en el navegador o terminal.
7. Mostrar la etiqueta AR y el video.
8. Mostrar el meliponario VR.
9. Cerrar con la arquitectura, las decisiones de autoría y lo que falta.

## 9. Checklist antes de la defensa

- [ ] Puedo explicar el flujo tienda → API → MySQL sin leer el código.
- [ ] Sé qué hace cada tabla y al menos una llave foránea.
- [ ] Sé por qué usé Docker y no XAMPP.
- [ ] Puedo mostrar el catálogo en el teléfono sin que se desborde.
- [ ] Puedo abrir una ficha de producto y explicar sus variantes.
- [ ] Sé qué es un image target y cómo se prueba en el teléfono.
- [ ] Puedo explicar el video como recreación didáctica.
- [ ] Tengo un respaldo del video y del GLB en USB o nube.
- [x] Tengo la presentación en PDF y en HTML navegable.
- [ ] Confirmo si también se requiere PPTX.
- [x] Tengo la bitácora de IA revisada y con mi reflexión.
