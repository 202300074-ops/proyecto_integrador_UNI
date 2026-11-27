# Anexo: bitácora de uso de IA

**Proyecto:** Sak P'o' Kaab · **Alumno:** Joshua Israel Cabrera Camacho

Este anexo selecciona diez interacciones relevantes del registro ampliado en
`docs/bitacora-ia.md`. Las entradas históricas se resumen sin cambiar sus
resultados. Joshua debe revisar cada descripción y completar las reflexiones
personales antes de entregar.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de escribir.

### 9. Renders de producto y catálogo · 2026-11-10

- **Herramienta/modelo:** OpenCode con scripts de Blender.
- **Solicitud:** generar renders conceptuales y mostrarlos en tarjetas/fichas.
- **Resultado:** cuatro escenas de producto y WebP para la tienda.
- **Aceptado/corregido/descartado:** se aceptó el estudio de producto digital; se
  corrigieron encuadres y exposición; se descartó describir los renders como
  fotografías de productos reales.
- **Verificación:** renders generados, imágenes cargadas en tienda y evidencia de
  escritorio/móvil guardada.
- **Reflexión personal de Joshua:** pendiente de escribir.

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
- **Reflexión personal de Joshua:** pendiente de revisar y completar con su
  explicación de qué decisiones aceptó, corrigió o no aceptaría.

## Reflexión final del alumno — completar antes de entregar

1. ¿Qué interacción cambió más tu comprensión técnica y por qué?
2. ¿Qué sugerencia de IA corregiste o rechazaste después de probarla?
3. ¿Qué parte puedes explicar sin consultar la bitácora?
4. ¿Qué se mantiene pendiente y cómo lo demostrarás ante el jurado?
