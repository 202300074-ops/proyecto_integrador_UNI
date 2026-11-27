# Plan secuencial de cierre

**Actualizado:** 2026-11-27  
**Propósito:** cerrar los pendientes del proyecto con una sola línea de trabajo.
Este plan organiza el cierre posterior al Sprint 4; no cambia el historial de los
sprints académicos anteriores. Los sprints de este plan son puertas operativas de
cierre y no se anotarán retroactivamente como sprints semanales del curso.

## Regla de avance

- Solo hay un sprint activo a la vez.
- No se inicia el siguiente sprint hasta revisar sus criterios de aceptación y
  guardar la evidencia del sprint activo.
- Si una tarea depende del teléfono, del visor, del oído o de una decisión de
  Joshua, permanece abierta hasta que esa comprobación o decisión ocurra. Un build
  o una prueba headless no reemplaza una prueba física.
- Si un sprint queda bloqueado por un tercero o por equipo no disponible, se
  registra el bloqueo; no se declara cerrado para avanzar de todos modos.

## Fecha de entrega: verificación previa

El correo del programa dice que la entrega del proyecto es el **26–27 de noviembre
de 2026** y que la exposición será entre el **30 de noviembre y el 4 de diciembre**;
el día y la hora de exposición se asignarán. La guía DOCX, en cambio, indica en su
última regla que **todo se entrega el día de la presentación**. Los documentos no
aclaran si hay una entrega anticipada el 26–27 y otra final el día de exposición.
Tampoco especifican una hora de subida ni un formato PPTX. La hora de 4:30 p. m.
se mencionó en la conversación de trabajo, pero no aparece como instrucción formal
en el correo ni en la guía.

**No mezclar hitos:** preguntar al docente si el 26–27 es una entrega inicial o si
todo el paquete se entrega el día asignado para la presentación; confirmar canal,
hora y formatos. No asumir que todos los pendientes físicos deben estar subidos
hoy ni que los nueve sprints caben en el día de entrega.

## Requisito de Scrum de la guía

La guía pide **cuatro sprints de una semana**, cada uno con revisión propia y
retrospectiva; también solicita backlog, sprints, burndown y retrospectivas en el
documento. Los sprints operativos de este plan no reemplazan ni alteran ese
historial. Los registros académicos se actualizarán solo con trabajo y fechas que
realmente ocurran.

## Sprints, en orden obligatorio

### Sprint 0 — Confirmar y cumplir la entrega de hoy

**Estado:** activo; depende de aclaración del docente o de una instrucción oficial
adicional.

**Trabajo:** aclarar la diferencia entre la fecha de entrega del correo (26–27) y
la regla de la guía (todo el día de la presentación); confirmar canal, hora,
formatos, qué materias se acreditan y qué archivos corresponden a cada fecha.
GitHub confirmó público `202300074-ops/proyecto_integrador_UNI` el 2026-11-27;
verificar que el commit final esté publicado. Después, subir lo solicitado en el
plazo confirmado y guardar el comprobante.

**Criterio de cierre:** respuesta/instrucción oficial guardada, paquete de entrega
identificado y subida realizada con evidencia de recepción. No dar por oficial la
hora de 4:30 p. m. sin una instrucción que la respalde.

### Sprint 1 — Publicación HTTPS en Vercel

**Estado:** GitHub reporta `Vercel: success` para `b735403`; el fallo de ruta era
del intento anterior `c8fbd24`. El sprint sigue pendiente hasta registrar y probar
el dominio público de producción.

**Trabajo:** obtener el dominio del deployment `b735403` desde Vercel; probar la
URL de producción y las rutas `/ar.html` y `/vr.html`, además del target, modelos,
video y audio.

**Criterio de cierre:** despliegue `Ready`, URL HTTPS anotada y rutas/recursos
cargados sin error. No se declara aprobada la cámara AR todavía; esa prueba física
pertenece al Sprint 2.

### Sprint 2 — Prueba móvil de tienda, AR y checkout

**Bloqueado hasta cerrar Sprint 1.**

**Trabajo:** en un teléfono real, revisar tienda y renders, cámara y permiso,
detección de etiqueta, abeja/jobón, apertura/cierre del video y fluidez después de
la pausa/reanudación de MindAR; confirmar que las ventanas conservan un único
control de cierre (sin X redundante); completar el checkout simulado.

**Criterio de cierre:** recorrido completo ejecutado en el dispositivo; defectos
corregidos o registrados con decisión; evidencia guardada sin exponer datos
personales ni crear pedidos reales.

### Sprint 3 — Diagnóstico y aceptación visual de WebXR

**Bloqueado hasta cerrar Sprint 2.**

**Trabajo:** comparar `/vr.html` en vista normal e inmersiva; registrar teléfono,
sistema, navegador/versión, visor, URL y commit; probar imagen, hotspots,
teletransporte y narración. Investigar el render casi negro y fragmentado de la
captura del 2026-11-27; comparar otro dispositivo compatible si está disponible.

**Criterio de cierre:** visualización legible y navegación/audio comprobados en
un dispositivo identificado, con evidencia archivada. Si el dispositivo no es
compatible, el sprint no se marca como VR aprobada: se documenta el límite y se
valida el plan de demostración alternativa con Joshua.

### Sprint 4 — Pase manual de abeja y jobón en Blender

**Bloqueado hasta cerrar Sprint 3.**

**Trabajo:** Joshua realiza cambios propios de geometría, material o detalle en
los modelos y exporta los GLB; conservar capturas del proceso y registrar
lmik3 únicamente como apoyo visual, si se utiliza.

**Criterio de cierre:** cambios propios explicables, archivos Blender guardados,
GLB exportados y reabiertos en el visor, evidencia de antes/después archivada.

### Sprint 5 — Aprobación de cama sonora y derivados

**Bloqueado hasta cerrar Sprint 4.**

**Trabajo:** escuchar los MP4 maestro, móvil y vertical; evaluar volumen,
inteligibilidad de narración, mezcla y subtítulos; ajustar y regenerar derivados si
se requiere.

**Criterio de cierre:** Joshua registra aprobación explícita de las versiones
finales, o se documentan los cambios pendientes; archivos finales y SRT
identificados y reproducidos correctamente.

### Sprint 6 — Cierre de memoria y datos institucionales

**Bloqueado hasta cerrar Sprint 5.**

**Trabajo:** confirmar nombre institucional oficial; revisar que cifras, límites,
pruebas y resultados en memoria, guion y presentación coincidan con la evidencia;
regenerar HTML/PDF después de la confirmación. Revisar la estructura de la guía:
portada; problema e introducción; objetivos; alcance y requerimientos con historias
y criterios; Scrum; desarrollo y evidencias por unidad; pruebas y resultados;
conclusiones; referencias IEEE; manuales; declaración de IA y bitácora con 8–10
interacciones.

**Criterio de cierre:** portada sin marcador pendiente, conteos y resultados
coherentes con el producto, PDF/HTML abiertos y revisados.

### Sprint 7 — Reflexión personal de la bitácora de IA

**Bloqueado hasta cerrar Sprint 6.**

**Trabajo:** Joshua completa con palabras propias la reflexión de
`docs/bitacora-ia.md`.

**Criterio de cierre:** reflexión escrita por Joshua, revisada por él y guardada;
no se sustituye por texto inventado por el asistente.

### Sprint 8 — Confirmación de formato de presentación

**Bloqueado hasta cerrar Sprint 7.**

**Trabajo:** confirmar en la consigna el formato de la presentación. La guía pide
una presentación, pero no especifica PPTX; si se pide ese formato, prepararlo y
revisar que coincida con la versión aprobada.

**Criterio de cierre:** respuesta documentada: PPTX requerido y entregado, o no
requerido según la instrucción docente.

### Sprint 9 — Ensayo, respaldo y contingencias de defensa

**Bloqueado hasta cerrar Sprint 8.**

**Trabajo:** ensayo cronometrado de 20 minutos más 5 minutos por cada materia
adicional, preguntas durante al menos 15 minutos y cambio pequeño en vivo de unos
10 minutos. Confirmar cuántas materias se presentan. Respaldar video, GLB y
evidencias; preparar alternativa si fallan red, cámara, Vercel o MySQL.

**Criterio de cierre:** tiempos registrados, demo practicada, respaldo abierto en
el equipo y en copia externa, contingencia probada y checklist de `docs/defensa.md`
actualizado.

## Estado actual del plan

- **Sprint activo:** Sprint 0, pendiente de aclarar con el docente si el paquete se
  entrega el 26–27 o el día de exposición, además de hora, canal, formatos y
  materias a acreditar. El repositorio es público; falta publicar los cambios
  locales que aún no aparecen en `origin/main`.
- **Pendientes bloqueados:** Sprints 1–9; no iniciar el siguiente hasta cerrar el
  activo con evidencia revisada.
- El correo confirma que el programa asignará fecha y hora de exposición dentro
  del 30 de noviembre al 4 de diciembre; todavía no hay asignación concreta.
- Las actualizaciones documentales de esta sesión están guardadas localmente; si
  la entrega se hace con el repositorio de GitHub, deben subirse antes de usarlo
  como evidencia de entrega.
