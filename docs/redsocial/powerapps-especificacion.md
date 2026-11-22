# PowerApps de la red social (R-13) · borrador de especificación

Borrador del 21/11/2026 de Álvaro para la entrega del 29/11 (RF-R12). Es una propuesta: no hay ninguna aplicación creada ni probada.

## Qué se comprobó del tenant (21/11/2026, cuenta de Álvaro)

- make.powerapps.com carga en el entorno «Productividad Personal US (default)» y ofrece crear aplicaciones (sin ninguna creada todavía).
- make.powerautomate.com carga y ofrece la plantilla «Notificar a un canal cuando se crea una nueva tarea de Planner», que pide conexiones de Planner, Office 365 Users y Microsoft Teams.
- **No comprobado:** que se pueda guardar y ejecutar una aplicación o un flujo, ni que los conectores de SharePoint, Planner y Teams no estén restringidos (RC-R02).

## Propuesta de aplicación (RF-R12)

Una aplicación de lienzo sencilla, «Estado de las delegaciones», sobre una lista de SharePoint del sitio del DMS o de un sitio propio de la red social.

| Pantalla | Qué hace | Requisito |
|---|---|---|
| Lista de delegaciones | Muestra las delegaciones con su estado (por ejemplo, «con canal», «sin canal», «baja») | RF-R12 · RF-R03 |
| Ficha de una delegación | Muestra su canal, su cuenta (solo el nombre de la delegación) y sus tareas pendientes | RF-R12 · RN-R04 |
| Alta o baja | Cambia el estado de una delegación; solo la Ejecutiva | CU-R05 · RN-R01 |

Datos: solo de ejemplo (RNF-R01). No se guardan datos de reclamaciones, mediaciones ni votaciones.

## Alternativa si el tenant no permite PowerApps

Documentar el mensaje de error con captura (RC-R02) y sustituir la aplicación por una vista de lista de SharePoint o por una pestaña de Planner con el estado en los cubos.

## Pasos y quién

1. Comprobar que se puede crear y guardar una aplicación de prueba (Álvaro, tras el Lab 8 del 23/11).
2. Crear la lista de ejemplo de delegaciones y la aplicación (Álvaro).
3. Capturas explicadas y UML actualizado (Álvaro y Joaquín, R-14).
4. Prueba cruzada por otra persona (Marcos o Pablo).
