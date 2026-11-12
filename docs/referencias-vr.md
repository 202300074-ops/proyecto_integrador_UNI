# Guion y referencias del recorrido VR

## Criterio

La narración es sintética y didáctica. Describe la escena estilizada y sus
elementos generales; no se presenta como una visita real ni como testimonio de una
comunidad. Las prácticas de manejo pueden variar entre comunidades.

## Guion

> Bienvenido al meliponario de Sak P'o' Kaab. Este espacio reúne jobones, flores
> y fauna de jardín alrededor de las abejas meliponas, polinizadoras nativas sin
> aguijón. Observa cómo las abejas visitan distintas flores y ayudan al transporte
> del polen. Los jobones ofrecen cavidades protegidas para sus colonias. El cuidado
> del hábitat y el conocimiento comunitario ayudan a mantener esta relación; las
> prácticas varían entre comunidades. Acércate a los puntos dorados para explorar.
> Esta escena es una recreación educativa, no representa un sitio real.

## Audio

- Voz sintética Microsoft Sabina (es-MX), generada con `System.Speech`.
- Fuente editable: `scripts/generate_vr_narration.ps1`.
- Máster WAV: `assets/audio/narracion-recorrido-vr.wav`.
- Derivado para el navegador: `assets/audio/narracion-recorrido-vr.mp3`, mono,
  96 kbit/s, ~43 s.
- El audio comienza solo cuando el usuario activa **Escuchar recorrido**; el mismo
  control pausa y reanuda la narración.

## Fuentes de contexto

- The Nature Conservancy México, *Manejo tradicional de la abeja de los pueblos
  mayas*:
  <https://www.nature.org/content/dam/tnc/nature/en/documents/mexico/Manejo_tradicional_de_la_abeja_de_los_pueblos_mayas.pdf>
- SEMARNAT, *La meliponicultura en México* (2023):
  <https://biblioteca.semarnat.gob.mx/janium/Documentos/Ciga/libros2023/CD008608.pdf>

Las fuentes orientan el contexto sobre la abeja y el jobón. El texto del recorrido
no atribuye una práctica particular a todas las comunidades.
