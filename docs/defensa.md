# Guion y preparación de la defensa

**Proyecto:** Sak P'o' Kaab

**Alumno:** Joshua Israel Cabrera Camacho

**Duración objetivo:** 12–15 minutos de exposición + preguntas

**Demo:** tienda, API, AR, VR y video

**Presentación:** PDF listo en `docs/presentacion.pdf`; para la versión navegable,
abrir `docs/presentacion.html` en Chrome y usar las flechas.

## 1. Idea central

> Sak P'o' Kaab es una tienda y experiencia multimedia de caso simulado. Integra
> catálogo, compra simulada, AR, VR y video, y distingue con claridad qué es real,
> qué es recreación y qué fue asistido por IA.

La defensa debe demostrar tres cosas:

1. El flujo técnico funciona: tienda → API → MySQL.
2. La experiencia multimedia está integrada: 3D, AR, VR y video.
3. El proyecto es honesto: caso simulado, video de recreación, voz sintética y
   autoría manual documentada.

## 2. Estructura sugerida de diapositivas

| # | Diapositiva | Tiempo |
| --- | --- | --- |
| 1 | Portada: Sak P'o' Kaab, nombre, materia y fecha | 20 s |
| 2 | Problema y contexto: melipona, jobón y caso simulado | 1 min |
| 3 | Objetivos y alcance: qué sí y qué no incluye | 1 min |
| 4 | Arquitectura: React, Express, MySQL, AR/VR | 1.5 min |
| 5 | Base de datos y flujo de compra | 1.5 min |
| 6 | Demo de tienda: catálogo, ficha, carrito y cupón | 2.5 min |
| 7 | Demo de API y MySQL | 1 min |
| 8 | AR: etiqueta, abeja y video | 2 min |
| 9 | VR: meliponario, hotspots y narración | 2 min |
| 10 | Video de cosecha y declaración de recreación | 1.5 min |
| 11 | Pruebas, evidencias y límites | 1.5 min |
| 12 | Conclusiones y aprendizaje | 1 min |

## 3. Guion oral

### Diapositiva 1. Portada

> Buen día. Presento Sak P'o' Kaab, un proyecto integrador de Multimedia y Diseño
> Digital. Es una tienda y experiencia multimedia de miel y jabón de la abeja
> melipona, planteada como caso de estudio simulado.

### Diapositiva 2. Problema y contexto

> La melipona, o xunáan kaab, es una abeja sin aguijón asociada a la
> meliponicultura yucateca. Se cría en jobones, troncos huecos que protegen la
> colonia. El proyecto toma ese contexto para crear una marca ficticia,
> Sak P'o' Kaab, que combina jabón y miel.
>
> No se trabajó con una cooperativa real ni con metraje documental. El caso es
> simulado y el video es una recreación didáctica. Esa decisión está declarada en
> la interfaz, en el README y en la memoria.

### Diapositiva 3. Objetivos y alcance

> El objetivo general fue integrar una tienda funcional con una experiencia
> multimedia. Los objetivos específicos fueron: base de datos, API, tienda,
> AR, VR, video y documentación.
>
> Incluye catálogo, carrito, cupón, checkout simulado, AR, VR y video. No incluye
> pagos reales, login, panel administrativo ni reseñas inventadas. Preferí un
> alcance demostrable a prometer funciones que no pudiera explicar.

### Diapositiva 4. Arquitectura

> La arquitectura tiene tres capas. La tienda React corre en el puerto 5173 y usa
> un proxy `/api`. La API Express corre en el 3000 y se conecta a MySQL 8.4 en
> Docker. El visor AR/VR corre aparte en el 5174 con A-Frame y MindAR.
>
> Elegí MySQL 8 en Docker porque el proyecto usa comportamiento de MySQL 8 y
> XAMPP con MariaDB 10.4 no era equivalente. El monorepo con workspaces separa
> tienda, API y visor sin duplicar configuración.

### Diapositiva 5. Base de datos y compra

> La base tiene ocho tablas. Las principales son `products`, `product_variants`,
> `orders`, `order_items`, `coupons` y `order_status_history`.
>
> El flujo de compra es transaccional: se valida el cupón, se bloquea el
> inventario, se verifica el stock, se crea el pedido, se descuenta stock y se
> registra la redención y el historial. Si algo falla, la transacción se revierte.
> Eso evita vender stock que no existe.

### Diapositiva 6. Demo de tienda

> Voy a mostrar el flujo principal. Abro el catálogo, filtro por jabones, abro la
> ficha, elijo una variante y la agrego al carrito. Luego aplico el cupón
> `BIENVENIDA10`, que da 10 % desde $200, y confirmo el pedido simulado.
>
> La tienda es adaptable: a 390 px no hay desbordamiento horizontal. Los precios y
> el stock vienen de MySQL, no están escritos en el frontend.

### Diapositiva 7. API y MySQL

> Puedo verificar la API con `/api/health` y `/api/products`. El endpoint de salud
> consulta la base, no solo responde “ok”. El catálogo devuelve cuatro productos y
> seis variantes.
>
> La prueba `npm run test:commerce` valida cupón, mínimo, stock insuficiente y
> pedido. Al terminar elimina su pedido de prueba y restaura stock y cupón.

### Diapositiva 8. AR

> La etiqueta usa un image target de MindAR. Al detectarla, aparece una abeja
> animada y un jobón. El botón **Ver cosecha** abre el video móvil.
>
> La cámara requiere HTTPS en el teléfono; para pruebas se usa un túnel o un
> despliegue estático. El target y el video se validaron funcionalmente en un
> Galaxy A22. La evidencia formal de esa prueba es una tarea de cierre.

### Diapositiva 9. VR

> El recorrido VR usa A-Frame 1.8. Incluye jobón, abejas, mariposas, libélula,
> colibrí, lagartija, flores y colinas. Hay cuatro hotspots y tres zonas de
> teletransporte: inicio, jardín y jobón.
>
> En casco se apunta con la mirada durante 900 ms. En escritorio se usa el mouse.
> La narración sintética se reproduce bajo demanda y se puede pausar. La prueba
> headless pasó; falta validar la entrada WebXR y la comodidad en un dispositivo
> físico.

### Diapositiva 10. Video

> El video es una animación original de 720p generada con Python, Pillow y
> FFmpeg. Muestra la colonia, la preparación, la apertura del jobón, la recolección
> por gravedad, el filtrado, el cierre y las reservas.
>
> No es metraje documental. La voz es sintética y el rótulo de recreación
> didáctica aparece en la experiencia. Las prácticas varían entre comunidades; no
> se presenta una receta universal.

### Diapositiva 11. Pruebas y límites

> Verifiqué API, build de tienda, build del visor, smoke test de AR/VR y diseño
> móvil. Las capturas están organizadas por fecha en `docs/evidencias/`.
>
> Los límites son claros: falta el pase manual de los modelos en Blender, la
> evidencia formal de AR en teléfono, el checkout en teléfono y la prueba WebXR
> física. No hay pagos reales ni panel administrativo. El caso es simulado.

### Diapositiva 12. Conclusiones

> El proyecto integra una tienda funcional, una base de datos relacional, una API
> transaccional, AR, VR y video. Lo más valioso fue aprender a conectar esas
> piezas y a documentar con honestidad qué es simulado, qué es recreación y qué
> fue asistido por IA.
>
> La siguiente mejora sería cerrar las pruebas físicas y completar el pase manual
> de los modelos. Gracias.

## 4. Demo en vivo: orden exacto

### Antes de empezar

```powershell
cd C:\Users\tiojo\dev\proyecto_integrador_UNI
npm run db:up
npm run dev
```

En otra terminal:

```powershell
npm --prefix apps/ar-preview run dev
```

URLs:

- Tienda: <http://localhost:5173>
- API: <http://localhost:3000/api/health>
- Visor: <http://localhost:5174>
- AR: <http://localhost:5174/ar.html> (requiere HTTPS y cámara)
- VR: <http://localhost:5174/vr.html>

### Secuencia de 5 minutos

1. Abrir la portada y señalar la identidad visual.
2. Ir al catálogo y filtrar por **Jabones**.
3. Abrir la ficha de jabón y mostrar variantes y stock.
4. Agregar una variante al carrito.
5. Abrir el carrito, aplicar `BIENVENIDA10` y mostrar el descuento.
6. Confirmar el pedido y mostrar el número de pedido.
7. Abrir `/api/health` y `/api/products` en otra pestaña.
8. Abrir el visor 3D y el recorrido VR.
9. Abrir el video o la captura de AR si no hay cámara disponible.
10. Cerrar con arquitectura, autoría y límites.

### Plan de respaldo

- Si MySQL no arranca: mostrar capturas de `docs/evidencias/2026-11-10/` y
  `docs/evidencias/2026-11-25/`.
- Si la cámara o el túnel fallan: mostrar `ar-target-detectado.png` y
  `ar-video-modal.png`.
- Si WebXR no entra: mostrar `vr-final.png` y explicar la diferencia entre la
  prueba headless y la prueba física.
- Si el video no reproduce: abrir el MP4 local
  `assets/video/cosecha-melipona-recreacion.mp4`.
- Llevar copia del video, los GLB y las capturas en USB o nube.

## 5. Preguntas probables y respuestas cortas

**¿Por qué MySQL y no XAMPP?**

Porque el proyecto usa MySQL 8.4 y XAMPP trae MariaDB 10.4. Docker permite
reproducir la misma versión y el mismo esquema.

**¿Qué pasa si se cae la API?**

La tienda muestra error de red y el checkout no confirma. La base no se modifica
porque el pedido se crea en una transacción.

**¿Cómo evitas vender stock inexistente?**

Bloqueo las variantes dentro de la transacción, verifico stock y solo entonces
descuento. Si falla, hago rollback.

**¿El video es real?**

No. Es una recreación didáctica original. La voz es sintética y el rótulo lo dice.

**¿Los modelos son tuyos?**

La base se generó con scripts asistidos por IA. La autoría manual se sustenta con
el pase en Blender; mientras no esté completo, no lo presento como totalmente
manual.

**¿Por qué AR necesita HTTPS?**

Porque el navegador solo permite acceso a cámara en contextos seguros. En local se
puede probar con un túnel o un despliegue HTTPS.

**¿Qué es un image target?**

Una imagen que MindAR reconoce y usa como ancla para colocar el modelo 3D.

**¿Qué es WebXR?**

La API web para realidad virtual y aumentada. A-Frame la usa para entrar a VR
desde un casco o teléfono compatible.

**¿Qué falta?**

Pruebas físicas de AR/checkout/WebXR, evidencia formal en teléfono y el pase
manual de los modelos. No falta la funcionalidad principal.

**¿Qué aprendiste?**

A integrar frontend, API, base de datos, 3D y multimedia, y a documentar límites
sin inflar resultados.

## 6. Checklist final

- [ ] Base de datos `healthy`.
- [ ] API responde `/api/health`.
- [ ] Tienda abre en 5173.
- [ ] Visor abre en 5174.
- [ ] Carrito, cupón y checkout funcionan.
- [ ] `npm run build` pasa.
- [ ] `npm run test:commerce` pasa.
- [ ] Smoke test de AR/VR pasa.
- [ ] Capturas finales en `docs/evidencias/2026-11-25/`.
- [ ] Video y GLB respaldados en USB o nube.
- [ ] Memoria y guion revisados.
- [x] Presentación en PDF y versión navegable HTML.
- [ ] Confirmar si la materia solicita también formato PPTX.
- [ ] Ensayo cronometrado de 12–15 minutos.
- [ ] Plan de respaldo si falla internet, cámara o MySQL.

## 7. Frases que no se deben decir

- “Es una cooperativa real.”
- “El video es documental.”
- “Los modelos los hice completamente a mano” (hasta completar el pase).
- “La prueba WebXR física ya está validada” (hasta tener evidencia).
- “El pago es real.”
- “Los datos de mercado son de una encuesta propia” (no se hizo).
