# Plan de mercadotecnia digital — caso académico Sak P'o' Kaab

**Estado:** propuesta académica; no es una campaña publicada ni una cooperativa
real. No se realizaron entrevistas, colaboraciones ni mediciones de audiencia.
Los perfiles y mensajes siguientes son hipótesis que requerirían validación.

## 1. Posicionamiento

- **Beneficio central:** conocer la relación entre el jobón, la abeja melipona y
  los productos conceptuales mediante una experiencia web interactiva.
- **Fórmula:** Sak P'o' Kaab ayuda a personas interesadas en cultura y naturaleza
  a explorar una historia didáctica de la meliponicultura mediante una tienda
  simulada, una etiqueta AR y un recorrido VR.
- **Ángulo:** “Del jobón a la pantalla”: explorar el objeto y su contexto antes de
  recorrer el catálogo.
- **Tono:** claro, respetuoso, educativo y explícito sobre lo simulado.
- **Límite de comunicación:** no afirmar que existe una cooperativa, una alianza,
  un testimonio o una venta real. No presentar una práctica local como regla
  universal [1], [2].

## 2. Audiencia y supuestos

| Perfil hipotético | Necesidad por validar | Contenido útil |
| --- | --- | --- |
| Persona interesada en cultura yucateca | Entender qué es un jobón y cómo se representa sin simplificar la práctica | Video didáctico, fuentes y recorrido VR |
| Visitante de experiencias digitales | Probar AR/VR desde el teléfono o navegador | Instrucción de escaneo y acceso directo a la experiencia |
| Estudiante o docente | Revisar cómo se integran multimedia y comercio electrónico | Arquitectura, evidencias y recorrido de la tienda |

Estos perfiles no provienen de entrevistas ni de un estudio de mercado. Antes de
usarlos en una campaña real se recomienda hacer una prueba de comprensión y
usabilidad con participantes voluntarios, documentando fecha, consentimiento,
método y resultados.

## 3. Objetivos de campaña

1. Aumentar el descubrimiento del contenido educativo.
2. Llevar visitantes desde una pieza informativa hasta la etiqueta AR o el
   recorrido VR.
3. Demostrar el flujo del catálogo y el checkout simulado sin sugerir que existe
   venta comercial.
4. Detectar problemas de comprensión, acceso móvil y navegación mediante pruebas
   observadas y consentidas.

No hay línea base ni analítica instalada. Las métricas se definen como un plan de
medición, no como resultados actuales. Los objetivos numéricos se fijarán después
de obtener una línea base; no se atribuirán cifras al proyecto sin medición.

## 4. Calendario editorial de referencia

Calendario anual sugerido; las fechas señaladas son efemérides y no describen una
temporada biológica de cosecha. La cosecha y el manejo varían por comunidad y
condiciones locales [1], [2].

| Momento | Tema y pieza propuesta | Canal | Llamado a la acción | Dependencia |
| --- | --- | --- | --- | --- |
| 22 de abril — Día Internacional de la Madre Tierra [3] | Infografía educativa sobre hábitat y polinizadores; revisar cada afirmación con una fuente | Publicación social y sitio | Explorar el meliponario virtual | Revisión de fuentes y derechos de imagen |
| Mayo, alrededor del Día Mundial de las Abejas (20 de mayo) [2] | Video breve de la recreación didáctica y demostración de etiqueta AR | Video corto y sitio | Probar la etiqueta | Etiqueta disponible y prueba móvil |
| Junio–octubre — contenido evergreen | Una pieza por tema: jobón, colonia, fauna y materiales; sin atribuir una práctica única | Publicaciones educativas | Abrir el recorrido VR | Guion revisado y evidencia de funcionamiento |
| Noviembre–diciembre — demostración académica | Recorrido del catálogo conceptual y flujo de compra simulada | Sitio y presentación | Ver el flujo de demostración | Aviso visible de caso simulado y checkout de prueba |

La secuencia es un calendario de contenido propuesto, no una afirmación sobre
campañas realizadas ni sobre disponibilidad real de productos.

## 5. Colaboraciones propuestas

No hay creadores contactados ni acuerdos. Para una futura campaña se propone
buscar perfiles locales cuya actividad pública se centre en alguno de estos temas:

- divulgación de cultura e historia de Yucatán;
- biodiversidad, polinizadores o educación ambiental;
- ilustración, modelado 3D o experiencias digitales.

**Criterios de selección:** revisar publicaciones y fuentes, audiencia y
comentarios pertinentes, política de publicidad, consentimiento para uso de
imagen, costo/contraprestación y disposición a revisar el contexto cultural.
Registrar cada contacto solo después de realizarlo; identificar toda
colaboración pagada o patrocinada. No usar testimonios ni nombres como si ya
existiera una alianza.

## 6. Embudo de comercio electrónico

1. **Descubrimiento:** pieza educativa enlaza al proyecto.
2. **Exploración:** visitante consulta historia y catálogo conceptual.
3. **Interacción:** abre AR o recorre VR; se informa si la experiencia requiere
   cámara o visor.
4. **Intención:** consulta ficha, variante y stock de demostración.
5. **Prueba funcional:** agrega al carrito, aplica cupón y confirma un pedido
   simulado.
6. **Aprendizaje:** registra errores de navegación en una prueba consentida; no
   presenta el pedido de prueba como venta.

El mapa de estrategias de comercio electrónico está en
[`mapa-comercio-electronico.svg`](./mapa-comercio-electronico.svg); el de
mercadotecnia digital, en [`mapa-mercadotecnia.svg`](./mapa-mercadotecnia.svg).

## 7. Métricas y método de medición

| Métrica | Definición | Cómo medirla | Estado |
| --- | --- | --- | --- |
| Alcance de contenido | Impresiones únicas por publicación, según la plataforma | Exportar el reporte nativo de cada plataforma | Sin dato; no hay campaña publicada |
| CTR al proyecto | Clics al enlace ÷ impresiones del enlace | UTM por pieza y reporte de plataforma | Sin dato; no hay campaña publicada |
| Apertura de ficha | Sesiones que abren ficha ÷ sesiones de catálogo | Evento `view_item` equivalente, solo con consentimiento y analítica configurada [4] | No instrumentado |
| Agregado al carrito | Sesiones con agregado ÷ sesiones de catálogo | Evento `add_to_cart` o registro de prueba consentida [4] | No instrumentado |
| Inicio de checkout | Sesiones con checkout iniciado ÷ sesiones con carrito | Evento `begin_checkout` [4] | No instrumentado |
| Finalización de compra simulada | Pedidos de prueba confirmados ÷ checkouts iniciados | Datos de entorno de prueba; nunca reportar como venta real | No hay línea base de campaña |
| Éxito de AR | Intentos que detectan el target ÷ intentos observados | Lista de prueba con dispositivo, luz y resultado | Falta archivar evidencia física |
| Uso de VR/audio | Inicios y finalizaciones observados por prueba | Lista de cotejo; sin analítica de usuario real | Falta validar con visor físico |

Las tasas se reportarán con denominador, periodo, dispositivo y tamaño de
muestra. Las pruebas con personas requieren consentimiento y no se generalizarán
como estudio de mercado si la muestra no lo permite.

## 8. Referencias

[1] Secretaría de Medio Ambiente y Recursos Naturales, *La meliponicultura en
México: un acercamiento a las prácticas tradicionales y a las perspectivas de su
manejo contemporáneo*. México: SEMARNAT, 2023. [En línea]. Disponible:
<https://biblioteca.semarnat.gob.mx/janium/Documentos/Ciga/libros2023/CD008608.pdf>.
Consultado: 26-nov-2026.

[2] Food and Agriculture Organization of the United Nations, “World Bee Day | 20
May.” [En línea]. Disponible: <https://www.un.org/observances/bee-day>.
Consultado: 26-nov-2026.

[3] United Nations, “International Mother Earth Day.” [En línea]. Disponible:
<https://www.un.org/en/observances/earth-day>. Consultado: 26-nov-2026.

[4] Google, “Measure ecommerce,” *Google Analytics for Developers*. [En línea].
Disponible:
<https://developers.google.com/analytics/devguides/collection/ga4/ecommerce>.
Consultado: 26-nov-2026.

[5] The Nature Conservancy México, *Manejo tradicional de la abeja de los pueblos
mayas*. [En línea]. Disponible:
<https://www.tncmx.org/content/dam/tnc/nature/en/documents/mexico/Manejo_tradicional_de_la_abeja_de_los_pueblos_mayas.pdf>.
Consultado: 26-nov-2026.
