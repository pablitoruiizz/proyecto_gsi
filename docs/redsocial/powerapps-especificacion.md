# PowerApps de la red social (R-13) · aplicación «Estado de las delegaciones»

Prueba de Álvaro del 25/11/2026 para la entrega del 29/11 (RF-R12). Es una aplicación de prueba con datos de ejemplo, en el espacio personal de Álvaro; no está publicada. Álvaro la compartió con Marcos el 25/11/2026 para la prueba cruzada (Lab 8); la prueba de Marcos se anota en [`pruebas.md`](pruebas.md).

## Qué se hizo y se comprobó (25/11/2026, cuenta de la US de Álvaro, entorno «Productividad Personal US (default)»)

1. **Lista de SharePoint «Delegaciones CADUS»** en «Mis listas» de Álvaro, con las columnas Título, Centro y Estado (texto) y tres filas de ejemplo: Delegación de ETSII (Al día), Delegación de Derecho (Pendiente de reunión) y Delegación de Biología (Sin contacto). Sin datos personales (RNF-R01). Captura: `capturas/R13-01-lista-delegaciones-sharepoint.jpg`.
2. **Aplicación de lienzo «Estado de las delegaciones»**, generada desde la lista (Integrar > Power Apps > Crear una aplicación) y **guardada** en Power Apps Studio. Captura: `capturas/R13-02-app-guardada-power-apps-studio.jpg`.
3. **Ejecución en vista previa** dentro de Power Apps Studio: la aplicación lee la lista y muestra las tres delegaciones con su centro y estado. Captura: `capturas/R13-03-app-ejecutada-vista-previa.jpg`.

Conclusión: el tenant permite crear una lista de SharePoint, crear y guardar una aplicación de lienzo y ejecutarla en vista previa (RC-R02, en lo que respecta al conector de SharePoint).

## Qué NO se ha comprobado

- Publicar la aplicación (no se pulsó «Publicar»).
- Ejecutarla desde una cuenta distinta de la de Álvaro (está compartida con Marcos desde el 25/11; falta que Marcos la abra y anote el resultado), o desde la pestaña de Teams.
- Los conectores de Planner y Teams, y cualquier flujo de Power Automate: en la cuenta de Álvaro no hay flujos, propios ni compartidos; el flujo de R-12 (Joaquín) no se ha podido probar desde su cuenta.
- Las pantallas de la propuesta original (ficha con canal y tareas, alta y baja solo para la Ejecutiva, CU-R05 · RN-R01): la aplicación generada es la plantilla de tres pantallas de PowerApps (lista, detalle y formulario) sin personalizar ni restringir por rol.

## Diferencias con el borrador del 21/11

- La lista tiene solo tres columnas (el borrador hablaba de canal, cuenta y tareas pendientes). Son suficientes para RF-R12 como demostración; ampliarla queda como mejora.
- La lista no está en el sitio del DMS ni en uno propio de la red social, sino en el espacio personal de Álvaro. Si se quiere en un sitio del CADUS, hay que crearla allí y volver a conectar la aplicación.

## Para el documento de la entrega

Explicar las tres capturas una a una (lista, aplicación guardada, aplicación en ejecución), decir que es una prueba con datos de ejemplo y repetir la lista de «no comprobado» de arriba.

## Pendiente

1. Prueba cruzada de Marcos: abrir la aplicación con su cuenta (ya compartida el 25/11) y anotar el resultado, con captura, en `pruebas.md`.
2. UML de diseño: hecho el 26/11 (R-14a): la caja de herramientas ya recogía PowerApps, y los planes de Planner llevan su patrón y los cubos del plan de la asamblea como Proceso de tareas (`scripts/redsocial/diagramas_rsi.py`, `img/uml-rsi-diseno.png`).
3. Flujo de Power Automate (R-12): lo prueba Joaquín o lo comparte con Álvaro.
