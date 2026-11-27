# Sprint 4. Cierre de entrega y defensa

**Ventana planificada:** 2026-11-26 a 2026-12-02 (siete días).
**Estado:** en curso. La entrega final es 26–27 de noviembre; este sprint incluye
el cierre documental y la preparación de defensa posterior.

> Las fechas previas de Sprint 1–3 no forman tres semanas uniformes. Este registro
> conserva la desviación real y no reescribe retrospectivamente los sprints para
> aparentar cuatro semanas consecutivas.

## Objetivo

Cerrar las brechas de la guía que pueden completarse en repositorio, documentar
lo que depende de Joshua/equipo físico y preparar la exposición de 20 minutos,
preguntas y cambio en vivo.

## Sprint backlog

| Historia | Criterio de aceptación | Estimación propuesta | Estado al 2026-11-26 |
| --- | --- | ---: | --- |
| S4-01 Mapas y plan de mercadotecnia | Dos mapas y un plan con calendario, colaboración propuesta y medición sin datos inventados | 5 pts | Hecho |
| S4-02 Panel de pedidos de prueba | Solo lectura, máximo 25, sin PII, dev-only y cubierto por smoke de comercio | 5 pts | Hecho; build y smoke de comercio pasaron |
| S4-03 Manuales y anexos | Manual técnico, manual de usuario, declaración IA, 8–10 interacciones y memoria PDF/IEEE | 8 pts | Hecho en borrador; faltan reflexión de Joshua y nombre institucional |
| S4-04 Cierre multimedia | Logo SVG animado; renderer genera SRT, cama original y deriva social | 5 pts | Hecho técnico: MP4 maestro, móvil y vertical regenerados con SRT y cama sonora; falta aprobación auditiva de Joshua |
| S4-05 Evidencia y defensa | Evidencia física, presentación de 20 min, preguntas y cambio en vivo | 8 pts | Pendiente |

Las estimaciones son propuestas para el backlog y requieren validación de Joshua.

## Registro diario

### 2026-11-26

- Se contrastó el repositorio con la guía y se creó el plan de cierre.
- Se generaron dos mapas SVG y un plan de mercadotecnia con perfiles hipotéticos,
  sin entrevistas ni métricas observadas.
- Se implementó un panel local de pedidos `mock` de solo lectura; su endpoint
  omite datos personales y queda deshabilitado en producción.
- Se prepararon los manuales, declaración IA, anexo seleccionado de bitácora y
  memoria PDF. La portada conserva pendiente el nombre institucional oficial.
- Se añadió animación SVG del símbolo, generador SRT, generador de cama original y
  una exportación vertical configurada para FFmpeg. En la sesión local posterior se
  regeneraron el máster, el móvil y el vertical con esa mezcla y subtítulos.
- La prueba de comercio pasó en API estable; build de tienda, smoke AR/VR y cinco
  pruebas unitarias de utilidades multimedia pasaron.
- Captura desktop de la tienda guardada en `docs/evidencias/2026-11-26/`.
- En la sesión de trabajo remoto no se encontraron Blender ni FFmpeg en `PATH`; en
  la sesión local posterior se regeneraron los MP4 con FFmpeg. No se hizo prueba
  física de teléfono/visor.

## Review parcial

El panel de pedidos y los documentos de mercadotecnia están preparados. La cama
sonora está integrada y los MP4 maestro, móvil y vertical ya incluyen SRT; la
medición del máster fue -16.05 LUFS, -1.49 dBTP y LRA 3.40. Falta la escucha y
aprobación auditiva de Joshua. No se presenta ninguna prueba física como realizada.

## Retrospectiva provisional

- **Funcionó:** usar la rúbrica como lista de brechas concretas y verificar el
  panel con una prueba que limpia solo su pedido de prueba.
- **Debe mejorar:** las dependencias de FFmpeg/Blender y la evidencia física no se
  reservaron con suficiente antelación; el PDF todavía necesita datos oficiales
  de portada.
- **Acción:** Joshua escucha y aprueba la cama sonora, completa el pase manual,
  realiza las pruebas físicas y reemplaza el nombre institucional antes de cerrar
  la defensa.

Este cierre parcial se registra el 26 de noviembre; la retrospectiva final debe
actualizarse al terminar la semana y después de las pruebas físicas.
