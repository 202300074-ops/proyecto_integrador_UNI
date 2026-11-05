# Bitácora de uso de IA

Borrador basado en las interacciones reales de las sesiones de trabajo. Antes de
entregar, Joshua debe revisarlo, corregir lo que no coincida con su memoria y
agregar su reflexión personal en cada entrada.

Herramienta usada: asistente de código en la terminal (opencode).
Modelo: DeepSeek V4.1 Flash Free.
Fecha de las sesiones: 2026-10-28 y 2026-11-04.

## Reglas que se acordaron

- La IA puede proponer código, comandos, textos y estructura.
- Todo dato de mercado, entrevista o métrica debe ser real y citado; no se
  inventa.
- La abeja y el jobón se modelan a mano; la IA solo apoya concepto, texturas y
  props secundarios.
- No se usa el modelo de terceros "Tetragonisca angustula Bee".
- El video se declara como recreación didáctica.
- El alumno debe poder explicar todo lo que se entregue.

## 1. Arranque del repositorio y del entorno

**Pregunta o instrucción:** dejar listo el repositorio y verificar las
herramientas disponibles.

**Respuesta de la IA:** propuso una estructura de monorepo con workspaces,
comandos de Git y una lista de verificación del entorno.

**Verificación:** se comprobó Node v22.17.1, npm 10.9.2, Docker 28.3.0, Docker
Compose v2.38.1, PHP, Composer, Python 3.12.10 y Git. Se confirmó que `gh` no
estaba instalado y que Blender y FFmpeg faltaban.

**Error o aprendizaje:** no se asumió que todas las herramientas existían; se
verificaron una por una antes de escribir comandos que dependieran de ellas.

## 2. Investigación del nombre y de la lengua maya

**Pregunta o instrucción:** confirmar el significado de `kaab`, `sak p'o'` y
`xunáan kaab` antes de usarlos en la marca.

**Respuesta de la IA:** propuso la arquitectura Kaab (miel), Sak P'o' (jabón),
Xunán (cosméticos) y Jobón (velas), con la tagline "Miel y jabón de la abeja
melipona".

**Verificación:** se revisaron fuentes como Arqueología Mexicana, el diccionario
de Bastarrachea (AULEX) y materiales de la UQROO. Se confirmó que `kaab` se
asocia a miel y abeja, y que `sak p'o'` significa jabón.

**Error o aprendizaje:** una marca en maya no se inventa; se documenta la fuente
y se evita usar una palabra solo porque "suena bien".

## 3. Diseño de la base de datos

**Pregunta o instrucción:** crear el esquema para productos, variantes, pedidos y
cupones.

**Respuesta de la IA:** propuso 8 tablas: `users`, `products`,
`product_variants`, `coupons`, `orders`, `order_items`,
`coupon_redemptions` y `order_status_history`, con llaves foráneas y estados.

**Verificación:** el contenedor ejecutó `schema.sql` y `seed.sql`; se consultaron
las tablas y los conteos: 4 productos y 6 variantes.

**Error o aprendizaje:** el esquema se probó desde cero con `db:reset`, no solo
se leyó el SQL. Un esquema que no se ejecuta no es evidencia.

## 4. MySQL 8 en Docker frente a XAMPP

**Pregunta o instrucción:** decidir cómo cumplir el requisito de MySQL 8.

**Respuesta de la IA:** explicó que XAMPP trae MariaDB 10.4 y que no es
equivalente a MySQL 8; propuso un contenedor `mysql:8.4` con volumen y
healthcheck.

**Verificación:** se levantó el contenedor, se esperó el estado `healthy` y se
probó la conexión con el usuario de la aplicación.

**Error o aprendizaje:** el contenedor tardó en quedar `healthy` y la primera
consulta falló por `ECONNREFUSED` cuando Docker Desktop se detuvo. Se aprendió a
revisar `docker compose ps` y los logs antes de culpar al código.

## 5. API de catálogo

**Pregunta o instrucción:** exponer productos y variantes para la tienda.

**Respuesta de la IA:** creó una API Express con `/api/health`,
`/api/products` y `/api/products/:slug`, usando un pool de mysql2 y respuestas
JSON normalizadas.

**Verificación:** `GET /api/health` respondió `200` con `db: "up"`;
`GET /api/products` respondió `200` con 4 productos; el detalle por slug
respondió `200`; un slug inexistente respondió `404`.

**Error o aprendizaje:** la API no debe devolver `200` si la base está caída. El
endpoint de salud se probó apagando Docker y confirmando el `503`.

## 6. Catálogo React y diseño

**Pregunta o instrucción:** construir una tienda que se viera como una marca de
miel artesanal, no como una plantilla genérica.

**Respuesta de la IA:** propuso una paleta crema, verde bosque y miel, tipografía
Fraunces + Inter, tarjetas con glifos SVG y una ficha de producto accesible.

**Verificación:** `npm run build` compiló 29 módulos; se tomaron capturas de
escritorio y móvil; el diálogo se abrió y cerró con Escape.

**Error o aprendizaje:** la primera versión tenía textos sin acentos y un
desbordamiento horizontal en móvil. Se corrigieron ambos y se volvió a probar.

## 7. Corrección de acentos y codificación

**Pregunta o instrucción:** revisar por qué el catálogo mostraba "Jabon",
"Balsamo" y "Yucatan" sin acentos.

**Respuesta de la IA:** encontró que los textos estaban escritos en ASCII para
evitar problemas de codificación; propuso usar UTF-8 en el SQL y en JSX, y
agregó `SET NAMES utf8mb4`.

**Verificación:** se reinició la base con `db:reset`, se consultó la API y se
comprobó que los nombres devueltos incluyen "Jabón", "Bálsamo" y "Yucatán".

**Error o aprendizaje:** evitar acentos por miedo a la codificación produce una
interfaz peor. La solución correcta es declarar UTF-8 y probar la salida real.

## 8. Desbordamiento horizontal en móvil

**Pregunta o instrucción:** revisar por qué la vista móvil se veía cortada.

**Respuesta de la IA:** primero sospechó del tamaño del texto y del `max-w-md`;
luego identificó que las cuadrículas sin `grid-cols-1` se dimensionaban por el
contenido máximo. Agregó `grid-cols-1`, `min-w-0` y `overflow-x-hidden`.

**Verificación:** con Puppeteer a 390 px, `innerWidth = 390` y
`scrollWidth = 390`; el diálogo también se mantuvo dentro del ancho.

**Error o aprendizaje:** la primera captura con Edge headless parecía cortada,
pero el navegador imponía un ancho mínimo de 492 px. La captura no era una prueba
válida. Se cambió a una prueba con emulación de dispositivo.

## 9. Prueba automatizada de la tienda

**Pregunta o instrucción:** comprobar que el catálogo carga, que el filtro
funciona y que la ficha de producto se abre en móvil.

**Respuesta de la IA:** escribió un script temporal con Puppeteer que abre la
tienda, espera a que aparezca "Miel de melipona", mide el ancho, hace clic en
"Ver variantes", verifica el diálogo y prueba el filtro "Jabones".

**Verificación:** el script reportó 4 productos, diálogo abierto, sin
desbordamiento y el filtro mostró solo el jabón. El script se guardó fuera del
repositorio para no agregar dependencias de prueba al proyecto.

**Error o aprendizaje:** una captura de pantalla no basta como prueba. Medir
`scrollWidth`, contar tarjetas y abrir el diálogo da evidencia más sólida.

## 10. Documentación y cierre del Bloque 1

**Pregunta o instrucción:** dejar documentado lo hecho y preparar el primer
commit.

**Respuesta de la IA:** redactó README, contexto, diario, esta bitácora,
aprendizaje y los archivos de Scrum; propuso el mensaje
`feat: base del proyecto, MySQL 8, API y catálogo`.

**Verificación:** se revisó `git status`, se ejecutó el build y se confirmó que
las capturas y el JSON de la API están en `docs/evidencias/2026-10-28/`.

**Error o aprendizaje:** no se hace commit hasta que el usuario lo pida. La
documentación debe describir lo que realmente se probó, no lo que se planea.

## Reflexión personal pendiente

Escribe aquí, con tus palabras:

- ¿Qué aprendiste de la base de datos y de Docker?
- ¿Qué te costó más del catálogo?
- ¿Qué harías distinto en el siguiente sprint?
- ¿Qué parte del código puedes explicar sin ayuda y cuál necesitas repasar?
