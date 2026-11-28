# Anexo: bitácora de uso de IA

**Proyecto:** Sak P'o' Kaab · **Alumno:** Joshua Israel Cabrera Camacho

Este anexo selecciona diez interacciones relevantes del registro ampliado en
`docs/bitacora-ia.md`. Las entradas históricas se resumen sin cambiar sus
resultados. La reflexión personal está al final de cada entrada y al cierre del
anexo.

## Interacciones seleccionadas

### 1. Entorno, repositorio y datos de demostración · 2026-10-28

- **Herramienta/modelo:** OpenCode; modelo histórico registrado como DeepSeek
  V4.1 Flash Free.
- **Solicitud:** preparar la base técnica y verificar qué herramientas estaban
  disponibles.
- **Resultado:** estructura de workspaces, esquema MySQL y API inicial.
- **Aceptado/corregido/descartado:** se aceptó MySQL 8 en Docker tras comprobar
  versiones; se descartó asumir que XAMPP/MariaDB era equivalente. Se verificó
  el entorno antes de ejecutar scripts.
- **Verificación:** MySQL quedó `healthy`; ocho tablas y el seed con cuatro
  productos y seis variantes se consultaron.
- **Reflexión personal de Joshua:** aquí entendí que no era “instala lo que sea y
  ya”. Si la base no es la misma, después nada cuadra. Docker me pareció más
  latoso de arrancar, pero más seguro que andar adivinando.

### 2. API, catálogo y corrección móvil · 2026-11-04

- **Herramienta/modelo:** OpenCode; modelo histórico registrado como DeepSeek
  V4.1 Flash Free.
- **Solicitud:** mostrar el catálogo desde una API y revisar errores de acentos y
  desbordamiento en teléfono.
- **Resultado:** endpoints Express, catálogo React, corrección UTF-8 y ajuste de
  ancho móvil.
- **Aceptado/corregido/descartado:** se aceptó la separación API/tienda; se
  corrigieron textos ASCII y reglas de grid después de probar; se descartó usar
  una captura de ventana que no emulaba el viewport real.
- **Verificación:** health, catálogo y ficha respondieron correctamente; prueba
  móvil a 390 px sin `scrollWidth` excedente.
- **Reflexión personal de Joshua:** el catálogo se ve fácil hasta que lo abres en
  el cel. Los acentos y que se saliera el contenido me enseñaron a no fiarme de
  la pantalla de la compu.

### 3. Modelos base de abeja y jobón · 2026-11-04

- **Herramienta/modelo:** OpenCode con scripts Python de Blender; modelo
  histórico registrado en el archivo ampliado.
- **Solicitud:** generar una base editable y exportable a GLB.
- **Resultado:** escena Blender, GLB de abeja con clip `SakPoKaab` y jobón con
  cavidad interior.
- **Aceptado/corregido/descartado:** se aceptó el blockout como base técnica; se
  corrigieron proporciones y exportación. No se aceptó como prueba de autoría
  manual final; el pase de Joshua sigue pendiente.
- **Verificación:** GLB reabiertos en Blender y clip de animación identificado.
- **Reflexión personal de Joshua:** el script me dio una base, no el modelo
  final. Si no lo muevo yo en Blender, en la defensa no puedo decir que lo hice
  a mano.

### 4. Visor A-Frame y escena del meliponario · 2026-11-05

- **Herramienta/modelo:** OpenCode; modelo histórico registrado como DeepSeek
  V4.1 Flash Free.
- **Solicitud:** ver los GLB en navegador y convertir el visor en una escena con
  jobón, vegetación y varias abejas.
- **Resultado:** visor A-Frame con entorno low-poly y movimiento `bee-wander`.
- **Aceptado/corregido/descartado:** se aceptó A-Frame como visor web; se
  ajustaron vuelo y composición después de revisar la escena; las referencias
  externas se usaron como orientación visual, no como modelos descargados.
- **Verificación:** build y smoke test pasaron; inspección headless confirmó que
  el tiempo y las posiciones de vuelo avanzaban.
- **Reflexión personal de Joshua:** A-Frame me sirvió porque lo veo en el
  navegador sin instalar un motor. Lo que me costó fue que se viera como
  meliponario y no como un montón de figuras.

### 5. Etiqueta y seguimiento MindAR · 2026-11-08

- **Herramienta/modelo:** OpenCode; modelo histórico registrado como DeepSeek
  V4.1 Flash Free.
- **Solicitud:** crear un target propio y mostrar el diorama de abeja/jobón al
  detectarlo.
- **Resultado:** etiqueta SVG/PNG, target `.mind` y página AR.
- **Aceptado/corregido/descartado:** se aceptó el diseño de etiqueta propio; se
  ajustó la escena y se dejó claro que el test de cámara virtual no sustituye una
  prueba física.
- **Verificación:** Chrome con cámara virtual emitió `targetFound`; la prueba
  física debe conservar evidencia por separado.
- **Reflexión personal de Joshua:** en la compu con cámara falsa sí detectaba la
  etiqueta. En el teléfono fue otro cuento: permisos, luz y que por HTTP de la
  red la cámara ni siquiera abre.

### 6. Video didáctico y narración · 2026-11-08

- **Herramienta/modelo:** OpenCode, Python/Pillow, FFmpeg y voz sintética es-MX.
- **Solicitud:** crear un video original porque no hay metraje del caso simulado.
- **Resultado:** seis escenas, narración y declaración visible de recreación.
- **Aceptado/corregido/descartado:** se aceptó una recreación con fuentes; se
  corrigió la lectura UTF-8 de PowerShell y se cambió la codificación para mejorar
  reproducción móvil; se descartó presentarlo como documental o testimonio.
- **Verificación:** MP4 decodificado y medido; test headless verificó reproducción
  y pausa AR. En la sesión local posterior se integraron la cama sonora, el SRT y
  la salida vertical; la mezcla del máster midió -16.05 LUFS y -1.49 dBTP.
- **Reflexión personal de Joshua:** como no hay un meliponario real del caso, el
  video tenía que decir recreación. Si lo presento como documental me quemo. La
  voz se oye sintética y así lo voy a decir.

### 7. Meliponario VR, fauna y narración · 2026-11-08

- **Herramienta/modelo:** OpenCode y A-Frame 1.8; modelo histórico registrado en
  el archivo ampliado.
- **Solicitud:** ampliar la escena, añadir fauna, hotspots, teletransporte y voz.
- **Resultado:** cuatro hotspots, tres zonas de navegación y control de audio.
- **Aceptado/corregido/descartado:** se aceptó la navegación por mirada y se
  añadieron instrucciones para pantalla; la prueba headless no se presenta como
  validación física de comodidad o WebXR.
- **Verificación:** smoke test y navegador headless comprobaron hotspots,
  panel, audio y carga de modelos.
- **Reflexión personal de Joshua:** el recorrido se ve más vivo con la fauna,
  pero las fichas se quedaban abiertas y tapaban todo. En el visor además me
  salió la imagen casi negra, así que no lo doy por aprobado.

### 8. Carrito, cupón y pedido simulado · 2026-11-10

- **Herramienta/modelo:** OpenCode; modelo histórico registrado como DeepSeek
  V4.1 Flash Free.
- **Solicitud:** completar un checkout de demostración que modificara el stock de
  forma consistente.
- **Resultado:** validación Zod, transacción, bloqueo de stock, cupón e historial.
- **Aceptado/corregido/descartado:** se aceptó pago `mock`; se corrigió la prueba
  para limpiar solo su pedido y restaurar stock/cupón; no se añadió pasarela real.
- **Verificación:** casos de cupón, mínimo, stock insuficiente y pedido válido;
  la prueba limpia su propio registro.
- **Reflexión personal de Joshua:** esta parte sí la puedo explicar. El cupón
  baja el total, si no hay stock no pasa, y el pago es de mentira. No metí
  PayPal ni nada porque el caso es simulado.

### 9. Renders de producto y catálogo · 2026-11-10

- **Herramienta/modelo:** OpenCode con scripts de Blender.
- **Solicitud:** generar renders conceptuales y mostrarlos en tarjetas/fichas.
- **Resultado:** cuatro escenas de producto y WebP para la tienda.
- **Aceptado/corregido/descartado:** se aceptó el estudio de producto digital; se
  corrigieron encuadres y exposición; se descartó describir los renders como
  fotografías de productos reales.
- **Verificación:** renders generados, imágenes cargadas en tienda y evidencia de
  escritorio/móvil guardada.
- **Reflexión personal de Joshua:** se ven bien, pero no son fotos de frascos
  reales. Si me preguntan, digo que son renders conceptuales. La vela la tuve
  que reencuadrar porque la etiqueta no se leía.

### 10. Correcciones frente a la guía y documentación · 2026-11-26

- **Herramienta/modelo:** OpenCode, `opencode-go/gpt-6-luna`.
- **Solicitud:** revisar la guía del proyecto y cerrar brechas alcanzables en un
  día, manteniendo transparencia y pruebas.
- **Resultado:** plan y mapas de mercadotecnia; manuales; declaración de IA; panel
  local de pedidos simulados de solo lectura; SVG animado; utilidades de SRT y
  cama sonora; memoria con citas numeradas y PDF de trabajo; deck actualizado a 13
  diapositivas y captura de escritorio de tienda.
- **Aceptado/corregido/descartado:** se aceptó que el plan de marketing es
  hipotético; se evitó mostrar datos personales; se descartó inventar
  colaboradores, resultados de campaña o pruebas físicas. Se mantuvo explícito
  que el panel no es administración real.
- **Verificación:** `npm run test:commerce` pasó en API estable; cinco pruebas
  Python pasaron; `npm run build` y `npm --prefix apps/ar-preview run test:smoke`
  pasaron después de las ediciones; `test:production-panel` confirmó `404` en
  producción. Se generó una captura desktop. En la sesión local posterior se
  regeneraron los MP4 maestro, móvil y vertical con FFmpeg, SRT y cama sonora;
  falta la escucha y aprobación de Joshua.
- **Reflexión personal de Joshua:** acepté el plan de marketing como hipótesis y
  el panel de pedidos solo de prueba. No acepté inventar ventas, reseñas ni una
  comunidad real. Lo que corregí después de probar fue el video trabado y las
  fichas que no se quitaban.

## Reflexión final del alumno

1. Lo que más me cambió fue la base y el pedido. Antes pensaba que el catálogo
   era puro front. Ya vi que si el stock y el cupón no se cuidan en la misma
   transacción, la tienda miente.
2. Rechacé presentar el video como documental y los modelos como si yo los
   hubiera esculpido a mano. También corregí la idea de que el MP4 estaba mal:
   en el cel se trababa porque la AR seguía corriendo detrás.
3. Sin la bitácora puedo explicar la tienda, el carrito, el cupón y por qué no
   hay pago real. MindAR y Blender los tengo que repasar antes de la defensa.
4. Me falta la evidencia del Galaxy A22, el pase en Blender, escuchar la cama
   sonora y volver a probar el VR porque se vio casi negro. En el jurado lo digo
   tal cual y muestro lo que sí está probado.
