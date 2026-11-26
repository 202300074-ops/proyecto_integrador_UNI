# Sprint 3. Meliponario VR, documentación y defensa

Fechas propuestas: **2026-11-20 a 2026-11-25**; confirmar con el equipo.

## Objetivo del sprint

Completar el recorrido VR del meliponario, integrar narración y cerrar la memoria,
las evidencias y el ensayo de defensa antes de la entrega del 26–27 de noviembre.

## Sprint backlog

| Historia | Puntos | Estado |
| --- | --- | --- |
| S3-01 Meliponario navegable en VR | 8 | En curso: `/vr.html` funciona en escritorio y headless; falta probar con casco WebXR físico |
| S3-02 Narración del recorrido | 3 | En curso: narración y controles validados en headless; falta probar en WebXR físico |
| S3-03 Memoria y evidencias finales | 8 | Hecho: memoria, guion de defensa y evidencias finales; falta anexar evidencia física |
| S3-04 Preparación de la defensa | 5 | En curso: guion y PDF de 12 diapositivas listos; falta ensayo y respaldo físico |
| **Total** | **24** | **En curso** |

## Avance al 2026-11-08

- Se creó `apps/ar-preview/vr.html` con A-Frame 1.8 y entrada WebXR habilitada.
- La escena incluye el jobón, cuatro abejas, dos mariposas, libélula, colibrí,
  lagartija, flores, pasto, árbol y colinas.
- Cuatro hotspots abren información en un panel anclado a la cámara; tres marcas
  del suelo permiten teletransportarse entre el inicio, el jardín y el jobón.
- Una narración es-MX de ~43 s se reproduce bajo demanda desde controles HTML y un
  botón dentro de la escena; puede pausarse y reanudarse. Guion y fuentes en
  `docs/referencias-vr.md`.
- En casco se activan los puntos mirando durante 900 ms. En escritorio se puede
  mirar con el mouse y desplazarse con WASD.
- Build y smoke test pasaron. Chrome headless validó carga de modelos, hotspots,
  panel, teletransporte y ausencia de errores. Evidencia:
  `docs/evidencias/2026-11-08/vr-meliponario.png`.
- El control de narración reprodujo el MP3 hasta 2.98 s y lo pausó; falta validar
  la voz y los controles en el teléfono/casco real.
- Esta prueba no sustituye validar el botón de entrada y la comodidad con un casco
  o teléfono compatible con WebXR.

## Avance al 2026-11-25

- QA final: MySQL `healthy`, API `db: "up"`, cuatro productos y seis variantes.
- `npm run build` y `npm --prefix apps/ar-preview run build` pasan.
- `npm run test:commerce` pasa con `COMMERCE_SMOKE_OK` y limpia sus datos.
- `npm --prefix apps/ar-preview run test:smoke` pasa con
  `AR_PREVIEW_SMOKE_OK`.
- Revisión móvil por CDP a 390 × 844: `innerWidth = 390`, `scrollWidth = 390`,
  sin desbordamiento horizontal.
- Memoria consolidada en `docs/memoria.md`.
- Guion, demo, preguntas y checklist en `docs/defensa.md`; presentación HTML/PDF en
  `docs/presentacion.html` y `docs/presentacion.pdf`.
- Capturas finales en `docs/evidencias/2026-11-25/`.

## Tareas inmediatas

1. Abrir `/vr.html` por HTTPS en un dispositivo WebXR y comprobar entrada/salida,
   cursor de mirada y teletransporte.
2. Ajustar escala, altura de cámara y distancias de hotspots con el dispositivo.
3. Probar la narración y sus controles en WebXR físico.
4. Archivar la evidencia de AR/video y checkout en el Galaxy A22.
5. Completar el pase manual en Blender y registrar lmik3 solo como apoyo visual.
6. Ensayar la presentación de 12 diapositivas durante 12–15 minutos y preparar
   respaldos físicos del video y los GLB.

## Criterio de cierre

- El recorrido funciona en navegador y en al menos un dispositivo WebXR probado.
- Los hotspots y la navegación se pueden usar sin mareo ni pérdida de orientación.
- La narración puede iniciarse y detenerse desde la experiencia.
- Memoria y evidencias describen con precisión qué fue manual, asistido por scripts
  o apoyado por herramientas de IA.
- La demo de defensa está ensayada y cuenta con video y modelos de respaldo.
