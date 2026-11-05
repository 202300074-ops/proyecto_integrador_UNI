# Sak P'o' Kaab

Tienda en línea y experiencia multimedia de miel y jabón de la abeja melipona.
Proyecto integrador de la materia **Multimedia y Diseño Digital** de la
Ingeniería en Software.

- Alumno: Joshua Israel Cabrera Camacho
- Matrícula: 202300074
- Entrega: 26 y 27 de noviembre de 2026
- Defensa: 30 de noviembre al 4 de diciembre de 2026

## Aviso académico

Este repositorio documenta un **caso de estudio simulado**. La cooperativa, la
marca y el meliponario no existen como empresa real. Los datos de mercado que se
citen en la documentación provienen de fuentes reales y se referencian. El video
de la cosecha será una **recreación didáctica** y así se declarará en la interfaz
y en la memoria del proyecto.

## Estado actual

Bloque 1 completado:

- Base de datos MySQL 8.4 en Docker con 8 tablas y datos de demostración.
- API REST en Express con catálogo, variantes, stock y estado de salud.
- Catálogo web en React + Vite + Tailwind, con filtros, ficha de producto y
  diseño adaptable a teléfono.
- Evidencias de ejecución y pruebas en `docs/evidencias/2026-10-28/`.

Pendiente para los siguientes sprints:

- Etiqueta de realidad aumentada con A-Frame + MindAR.
- Meliponario virtual con A-Frame/WebXR.
- Carrito, cupones y pago simulado.
- Video de cosecha con Python + FFmpeg y modelo 3D de la abeja y el jobón.
- Documentación final, bitácora de IA y presentación de defensa.

## Tecnologías

| Capa | Tecnología |
| --- | --- |
| Base de datos | MySQL 8.4 en Docker |
| API | Node.js 22, Express 4, mysql2, Zod |
| Tienda | React 18, Vite 6, Tailwind CSS 3.4 |
| AR | A-Frame 1.6 + MindAR 1.2 |
| VR | A-Frame 1.8 / WebXR |
| 3D | Blender LTS, exportación GLB |
| Video y audio | Python 3.12 + FFmpeg |
| Control de versiones | Git + GitHub |

## Requisitos

- Node.js 20 o superior (probado con 22.17.1).
- npm 10 o superior.
- Docker Desktop con Docker Compose v2.
- Puerto 3000 libre para la API.
- Puerto 3306 libre para MySQL.
- Puerto 5173 libre para Vite.

## Puesta en marcha

1. Instalar dependencias:

   ```powershell
   npm install
   ```

2. Crear el archivo de entorno local:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Levantar MySQL:

   ```powershell
   npm run db:up
   ```

   La primera vez descarga la imagen, crea la base `melipona` y ejecuta
   `db/schema.sql` y `db/seed.sql`. Espera a que el contenedor esté `healthy`.

4. Levantar API y tienda en dos terminales, o ambas con un solo comando:

   ```powershell
   npm run dev
   ```

   También se pueden iniciar por separado:

   ```powershell
   npm run dev:api
   npm run dev:store
   ```

5. Abrir:

   - Tienda: <http://localhost:5173>
   - Salud de la API: <http://localhost:3000/api/health>
   - Catálogo: <http://localhost:3000/api/products>

## Scripts

| Comando | Qué hace |
| --- | --- |
| `npm run dev` | API y tienda en modo desarrollo. |
| `npm run dev:api` | API con `node --watch`. |
| `npm run dev:store` | Vite en el puerto 5173. |
| `npm run build` | Compila la tienda en `apps/store/dist`. |
| `npm start` | API en modo producción. |
| `npm run db:up` | Levanta MySQL en segundo plano. |
| `npm run db:down` | Detiene MySQL sin borrar datos. |
| `npm run db:reset` | Borra el volumen y vuelve a ejecutar esquema y seed. |

## Endpoints

| Método | Ruta | Respuesta |
| --- | --- | --- |
| GET | `/api/health` | Estado de la API y de MySQL. |
| GET | `/api/products` | Productos activos con sus variantes. |
| GET | `/api/products/:slug` | Un producto por slug o `404`. |

Ejemplo de respuesta de salud:

```json
{
  "ok": true,
  "service": "sak-po-kaab-api",
  "db": "up",
  "timestamp": "2026-10-29T04:49:47.392Z"
}
```

## Estructura

```text
.
├─ apps/store/          Tienda React + Vite + Tailwind
├─ server/              API Express
├─ db/                  Esquema y datos de demostración
├─ docs/                Scrum, bitácora, diario y evidencias
├─ assets/              Modelos, texturas, video y audio
├─ scripts/             Utilidades de video, audio y respaldo
├─ docker-compose.yml   MySQL 8.4
└─ package.json         Workspaces y scripts raíz
```

## Base de datos

Tablas creadas por `db/schema.sql`:

1. `users`
2. `products`
3. `product_variants`
4. `coupons`
5. `orders`
6. `order_items`
7. `coupon_redemptions`
8. `order_status_history`

Datos iniciales de `db/seed.sql`:

- 4 productos: miel, jabón, bálsamo labial y vela.
- 6 variantes con precio, stock, peso y atributos en JSON.
- 1 cupón: `BIENVENIDA10` (10 % en compras desde $200).

Para reiniciar la base desde cero:

```powershell
npm run db:reset
```

## Verificación realizada

- `GET /api/health` respondió `200` con `db: "up"`.
- `GET /api/products` respondió `200` con 4 productos y 6 variantes.
- `GET /api/products/jabon-sak-po` respondió `200` con sus 2 variantes.
- `GET /api/products/no-existe` respondió `404`.
- `npm run build` compiló 29 módulos sin errores.
- Prueba de diseño móvil a 390 px: `scrollWidth = 390`, sin desbordamiento
  horizontal; el diálogo de producto también se mantiene dentro del ancho.
- Filtro "Jabones": muestra únicamente el producto de jabón.

Las capturas y el JSON de la API están en
`docs/evidencias/2026-10-28/`.

## Fuentes de la lengua maya

- `kaab`: miel y abeja. Arqueología Mexicana; diccionario de Bastarrachea
  (AULEX); diccionario de la UQROO.
- `sak p'o'`: jabón. Diccionario de Bastarrachea (AULEX).
- `xunáan kaab`: abeja melipona (Melipona beecheii). Fuentes de la UQROO y
  Arqueología Mexicana.

## Uso

Proyecto académico sin fines comerciales. Las imágenes, modelos y videos se
crean para la entrega y se declaran como simulados o recreaciones didácticas.
