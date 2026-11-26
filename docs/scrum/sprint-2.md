# Sprint 2. Realidad aumentada, video y compra básica

Fechas propuestas: **2026-11-09 a 2026-11-19**.
Trabajo adelantado: el modelado 3D asistido por scripts y la exportación se
iniciaron el 2026-11-04.

## Objetivo del sprint

Tener una etiqueta de realidad aumentada que reconozca una imagen, muestre la
abeja animada y reproduzca el video de la cosecha; además, dejar funcionando el
carrito y el cupón en su flujo básico.

## Sprint backlog

| Historia | Puntos | Estado |
| --- | --- | --- |
| S2-01 Carrito con variantes y cantidades | 5 | Hecho: variantes, cantidades, subtotal y evidencia UI |
| S2-02 Cupón `BIENVENIDA10` | 3 | Hecho: 10 % desde $200, validado en API y UI |
| S2-03 Pedido simulado en MySQL | 5 | Hecho: pedido, stock, redención e historial en transacción |
| S2-04 Etiqueta AR con abeja animada | 8 | Funcionalmente validado por Joshua en el Galaxy A22; falta archivar evidencia |
| S2-05 Video de cosecha dentro de la AR | 5 | Reproducción sin trabas validada en el Galaxy A22; falta archivar evidencia |
| S2-06 Video editado con Python + FFmpeg | 8 | Hecho: recreación 720p con narración sintética y fuentes |
| **Total** | **34** | **21 hechos, 13 validados funcionalmente con evidencia pendiente** |

## Avance al 2026-11-10

- Blender 5.2.3 y FFmpeg 9.0.2 instalados y verificados.
- `scripts/blender_model.py` genera `assets/models/modelo.blend`, `abeja.glb` y
  `jobon.glb`, además de previews Workbench.
- La abeja exporta un clip `SakPoKaab` y tiene 9,908 triángulos; el jobón tiene
  14,852 triángulos. Ambos GLB se importaron en una escena Blender limpia; el
  clip ya se verificó en el visor y en la página AR de escritorio.
- `scripts/blender_render_eevee.py` genera cuatro renders finales en
  `docs/evidencias/2026-11-04/`.
- `apps/ar-preview` sirve ambos GLB en un visor A-Frame. La prueba
  `npm --prefix apps/ar-preview run test:smoke` pasó y el build se completó.
- La escena del visor incluye árbol, arbusto, flores, pasto, rocas, colinas y
  cuatro abejas con trayectorias propias. El jobón está al pie del árbol.
- Se revisó visualmente en Chrome headless con WebGL por SwiftShader y se
  verificó por DevTools que las abejas y el `mixer` avanzan sin errores de
  consola. Evidencia: `docs/evidencias/2026-11-08/visor-escena.png`.
- Se documentaron referencias visuales en `docs/referencias-3d.md`.
- `assets/targets/etiqueta-sakpokaab.svg` y su PNG componen la etiqueta; MindAR
  compiló el archivo `assets/targets/etiqueta-sakpokaab.mind`.
- `/ar.html` inicia MindAR y muestra el diorama 3D; una cámara virtual de Chrome
  detectó el target (`targetFound`). Evidencia:
  `docs/evidencias/2026-11-08/ar-target-detectado.png`.
- `assets/video/cosecha-melipona-recreacion.mp4` genera una recreación didáctica
  original de 53.4 s, 720p/24 fps, H.264 Baseline/AAC. Python/Pillow dibuja la
  animación y FFmpeg normaliza/mezcla una narración sintética es-MX. La AR descarga
  el derivado 640 × 360 `cosecha-melipona-recreacion-mobile.mp4` antes de habilitar
  **Ver cosecha** y pausa el tracking durante la reproducción. El modal está
  integrado en `/ar.html`; storyboard en
  `docs/evidencias/2026-11-08/storyboard-cosecha.png`.
- Joshua validó la etiqueta y el video en el Galaxy A22: el target se reconoce y
  el video se reproduce sin trabarse. La evidencia formal de esa prueba queda
  pendiente de archivar.
- El script de render asigna un mundo crema explícito porque el archivo de escena
  no tenía `scene.world`.
- La escena generada por scripts sigue siendo una base asistida; falta que Joshua
  realice y documente modificaciones manuales sustanciales para la autoría.
- Se implementó el carrito con variantes y cantidades, el cupón `BIENVENIDA10` y
  el checkout simulado. La API expone `POST /api/coupons/validate` y
  `POST /api/orders`.
- El pedido usa transacción y bloqueo de stock, guarda `orders`, `order_items`,
  `coupon_redemptions` y `order_status_history`, y descuenta el inventario.
- `npm run test:commerce` valida cupón válido, mínimo no alcanzado, stock
  insuficiente y pedido correcto; al terminar limpia el pedido de prueba y
  restaura inventario y contador del cupón.
- Una prueba de UI en Chrome headless agregó una variante, abrió el carrito,
  aplicó el cupón y confirmó un pedido de $320 con descuento de $32 y total de
  $288. Evidencias: `docs/evidencias/2026-11-10/carrito-cupon.png` y
  `pedido-simulado.png`.
- Se renderizaron los cuatro productos a 1600 × 2000 con Cycles CPU y se
  integraron versiones WebP en las tarjetas y la ficha de la tienda. Evidencias:
  `docs/evidencias/2026-11-10/producto-*-final.png`.

## Tareas inmediatas

1. Abrir `assets/models/modelo.blend`, modificar la abeja y el jobón manualmente y
   guardar evidencia del proceso.
2. Archivar la evidencia de la prueba en el Galaxy A22.
3. Probar carrito y checkout en el teléfono y documentar la demo de defensa.

## Riesgos

- La AR necesita HTTPS para la cámara del teléfono; se probará con Netlify o
  cloudflared.
- El video ya está validado en el teléfono; falta guardar la evidencia formal.
- El modelo generado con scripts no debe presentarse como autoría manual final;
  falta el pase de Joshua y la evidencia de sus modificaciones. Los renders
  mejorados con herramientas de IA deben declararse como apoyo visual.
- El smoke test HTTP, build y validación en teléfono pasaron; falta conservar la
  captura o grabación de la prueba real.

## Criterio de cierre

- La etiqueta se reconoce en el Galaxy A22 y muestra la abeja.
- El video se reproduce desde la experiencia AR.
- El carrito suma variantes y el cupón aplica el descuento.
- Todo tiene evidencia y se puede explicar en la defensa.

## Sprint review y retrospectiva — borrador basado en el registro

**Resultado observable:** el carrito, el cupón y el pedido simulado funcionan en
API/UI; la etiqueta AR y el video fueron validados funcionalmente en el Galaxy
A22 según el registro del alumno. El storyboard, la detección del target y las
capturas de compra están vinculados en las secciones anteriores.

**Qué funcionó:** separar los assets del visor y usar un smoke test facilitó
comprobar la integración; la prueba de comercio verifica stock, cupón y limpieza
de sus propios datos.

**Qué mejorar:** la evidencia formal de las pruebas físicas se dejó para el cierre;
el pase manual de Blender tampoco se capturó junto con la generación inicial.

**Acción propuesta para el sprint siguiente:** agendar la prueba física al inicio
del sprint y guardar capturas/notas inmediatamente. Joshua debe revisar este
borrador y añadir su reflexión personal; no es una retrospectiva escrita por el
alumno.
