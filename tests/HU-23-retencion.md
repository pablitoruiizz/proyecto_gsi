# Pruebas de HU-23 · Anonimización de tickets y mediaciones a los 2 años

**Requisitos:** HU-23 · RN-03 (privacidad de tickets y mediaciones) · plazo de conservación indicado por el CADUS en la entrevista del 26/10 (2 años desde que se resuelven)
**Código probado:** `cms-wordpress/wp-content/plugins/cadus-portal/includes/retencion.php` (tarea `cadus_retencion_diaria` de WP-Cron) y `scripts/pruebas/hu23_prueba_retencion.php`
**Quién prueba:** Álvaro Martínez Ocaña · **Fecha:** 12/11/2026 · **Versión probada:** rama `feature/hu-23-retencion` con `main` fusionado, plugin CADUS Portal, WordPress 7.1 local (XAMPP, base `bd_cadus`)

## Qué hace HU-23

Una tarea diaria busca los tickets (`cadus_ticket`) y las solicitudes de mediación (`cadus_mediacion`) **resueltos hace más de 2 años** y los **anonimiza** en lugar de borrarlos. Conserva la referencia, el tipo, el estado, el centro y el consentimiento (sirven para estadísticas) y elimina el correo, el solicitante, el texto escrito por el estudiante, las respuestas del equipo y los adjuntos.

- El plazo cuenta desde que el elemento pasa a *Cerrado* o *Cerrada* (se guarda en `_cadus_resuelto`), no desde que se creó. Un ticket abierto no se toca nunca; si se reabre, se borra la fecha y se vuelve a contar desde el siguiente cierre.
- Los elementos cerrados antes de existir HU-23 no tienen esa fecha y se usa su fecha de última modificación.
- Es idempotente: lo ya anonimizado lleva la marca `_cadus_anonimizado` y no se vuelve a tratar.

## Entorno

Se probó con el script `scripts/pruebas/hu23_prueba_retencion.php`, que crea elementos de ejemplo con el código `PRUEBA-HU23-*`, ejecuta la misma función que la tarea programada y comprueba el resultado. Se lanza por línea de comandos con el PHP de XAMPP y la base local; con el argumento `limpiar` borra los datos de ejemplo.

## Casos del script

| # | Caso | Resultado esperado | Resultado |
|---|---|---|---|
| A | Ticket cerrado hace 3 años, con un adjunto. | Se anonimiza y se borra el adjunto. | OK |
| B | Ticket cerrado hace 1 año. | Se conserva. | OK |
| C | Mediación cerrada hace 2 años y 5 días. | Se anonimiza. | OK |
| D | Mediación cerrada hace 6 meses. | Se conserva. | OK |
| E | Ticket cerrado a 5 días de cumplir 2 años. | Se conserva. | OK |
| F | Ticket abierto, creado hace 4 años. | Se conserva (el plazo cuenta desde el cierre). | OK |
| G | Ticket cerrado antes de HU-23 (sin fecha guardada). | Se anonimiza usando la fecha de última modificación. | OK |
| H | Ticket cerrado hace 3 años, en la papelera. | Se anonimiza. | OK |
| I | Ticket cerrado hace 3 años y reabierto después. | Se conserva y se borra la fecha de resolución. | OK |
| — | Simulación y ejecución real: 3 tickets y 1 mediación, 0 errores. | Coinciden con los casos A, C, G y H. | OK |
| — | Segunda ejecución inmediata. | No cambia nada (idempotente). | OK |

## Casos pendientes

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H23-2 | Con la Ejecutiva, abrir en el panel un elemento anonimizado. | Se ven referencia, tipo y estado; no hay correo, texto ni respuestas. | Pendiente de ejecutar. |
| H23-4 | Comprobar la tarea programada en el servidor del equipo. | El evento `cadus_retencion_diaria` existe y se ejecuta una vez al día. | Pendiente: no se ha desplegado en el servidor del equipo. |
| H23-6 | Prueba cruzada por otra persona del equipo. | Los casos del script salen OK en su entorno. | Pendiente. |

## Fallos y observaciones

| # | Caso | Qué ocurre | Corrección / issue |
|---|---|---|---|
| 1 | Alcance | Los tickets y mediaciones que no se cierran nunca no se anonimizan con esta regla. | Decidir con el Product Owner si hace falta un límite máximo. |
| 2 | Aviso de privacidad | El aviso dice «Después se eliminan» sin indicar el plazo de 2 años desde la resolución. | Pedir a Miguel Ángel que lo concrete. |
| 3 | Servidor | WP-Cron solo se dispara con visitas al sitio. | En el servidor del equipo, si WP-Cron está desactivado, programar una tarea del sistema. |

## Comprobaciones finales

- Los datos de ejemplo se borran con `limpiar` al terminar.
- Sin avisos de PHP revisados en `wp-content/debug.log`: no comprobado.

## Trazabilidad

| Requisito | Casos que lo cubren |
|---|---|
| HU-23 (anonimización a los 2 años de la resolución) | A–I y las comprobaciones finales del script |
| RN-03 (privacidad de tickets y mediaciones) | A, C, G, H (datos personales eliminados); H23-2 pendiente |
