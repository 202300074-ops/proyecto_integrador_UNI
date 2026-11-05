# Diario de trabajo

Registro breve de lo que se hizo, lo que falló y lo que sigue. Las fechas
corresponden a las sesiones de trabajo; si alguna se movió, se corrige aquí.

## 2026-10-28. Sesión de arranque

Objetivo: dejar listo el esqueleto del proyecto y la base de datos.

Hecho:

- Se creó el repositorio local y se clonó el remoto vacío de GitHub.
- Se configuró la identidad local de Git y la rama `main`.
- Se creó la estructura de carpetas: `db`, `server`, `apps/store`, `docs`,
  `scripts` y `assets`.
- Se escribieron `package.json`, `.gitignore`, `.env.example`,
  `docker-compose.yml`, `db/schema.sql` y `db/seed.sql`.
- Se escribió la API Express con salud, catálogo y detalle por slug.
- Se escribió el catálogo React con Tailwind, filtros y ficha de producto.
- `npm install` terminó con 242 paquetes.
- Se inició la descarga de la imagen `mysql:8.4` en Docker.

Problemas:

- XAMPP tiene MariaDB 10.4, no MySQL 8. Se decidió usar Docker para cumplir con
  el requisito de MySQL 8.
- La descarga de la imagen dejó el contenedor en estado `starting` durante más
  de dos minutos. Se revisaron los logs y la inicialización seguía en curso.

Decisión:

- No usar MariaDB. La base de datos del proyecto es MySQL 8.4 en Docker.

Siguiente:

- Verificar que el contenedor quede `healthy`.
- Probar la API y compilar la tienda.

## 2026-11-04. Verificación del Bloque 1

Objetivo: comprobar que la base, la API y el catálogo funcionan de punta a punta
y dejar evidencia.

Hecho:

- El contenedor `melipona-db` quedó `healthy`.
- Se verificaron las 8 tablas y los datos: 4 productos y 6 variantes.
- Se probó `GET /api/health`: `200` con `db: "up"`.
- Se probó `GET /api/products`: `200` con 4 productos y sus variantes.
- Se probó `GET /api/products/jabon-sak-po`: `200`.
- Se probó `GET /api/products/no-existe`: `404`.
- `npm run build` compiló 29 módulos sin errores.
- Se corrigieron los acentos del catálogo y de los datos de demostración.
- Se corrigió el desbordamiento horizontal en móvil con `grid-cols-1`,
  `min-w-0` y `overflow-x-hidden`.
- Se tomaron capturas de escritorio, móvil y de la ficha de producto.
- Se probó el catálogo a 390 px: `innerWidth = 390`, `scrollWidth = 390`.
- Se probó el filtro "Jabones": solo mostró el producto de jabón.

Problemas:

- Docker Desktop se detuvo después de reiniciar la base. La API respondió `503`
  con `ECONNREFUSED` al puerto 3306. Se volvió a iniciar Docker Desktop y el
  contenedor; la API se recuperó sin reiniciar el proceso de Node.
- Al lanzar procesos en segundo plano desde PowerShell, la herramienta devolvió
  un error de `ChildProcess.kill`. Los procesos sí quedaron activos; se
  verificaron con `Get-Process` y con peticiones HTTP.
- La primera captura móvil parecía cortada. Se comprobó con Puppeteer que el
  problema era el ancho mínimo del navegador headless, no el CSS. La prueba real
  a 390 px no tiene desbordamiento.

Decisión:

- La evidencia se guarda en `docs/evidencias/2026-10-28/`.
- El catálogo se considera cerrado para el Bloque 1; las fotos reales de producto
  se sustituirán en el Sprint 2 si hay tiempo.

Siguiente:

- Instalar Blender y FFmpeg.
- Modelar la abeja y el jobón.
- Implementar la etiqueta AR y el video.
- Completar el carrito y los cupones.

## Pendientes inmediatos

- Confirmar el horario de fin de semana.
- Instalar Blender y FFmpeg.
- Hacer el primer commit del Bloque 1 cuando el asistente lo indique.
