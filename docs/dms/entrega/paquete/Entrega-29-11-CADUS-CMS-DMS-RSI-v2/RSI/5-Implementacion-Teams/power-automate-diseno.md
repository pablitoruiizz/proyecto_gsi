# Power Automate · avisos de tareas de la red social

Documentación del artefacto de Power Automate de la Red Social Interna del CADUS (Lab 8, entrega del 29/11/2026), con lo que pide el README del área (en el repositorio de GitHub: `colaboracion-microsoft365/README.md`): objetivo, configuración, permisos y trazabilidad con historias y sprints.

| Dato | Valor |
|---|---|
| Objetivo | Que el canal del equipo se entere solo cuando se asigna una tarea nueva en Planner o cuando vence la fecha de una tarea, sin que nadie tenga que mirar el plan (OBJ-R02) |
| Herramienta | Power Automate (make.powerautomate.com), entorno «Productividad Personal US (default)» del tenant de la Universidad de Sevilla (RC-R01) |
| Historia y sprint | RSI-HU-07, Sprint 2 ([`docs/redsocial/scrum/sprint-02-rsi.md`](../seguimiento/sprint-02-rsi.md)) |
| Tarea del plan de trabajo | R-12 de [`plan-lab5.md`](../seguimiento/plan-lab5.md) |
| Responsables | Joaquín Luna Canela (crea los flujos) y Marcos (los prueba y es copropietario) |
| Requisitos | RF-R11, RNF-R01, RC-R02 |
| Casos de uso | CU-R02 Preparar una asamblea con tareas |
| Cómo se crea | [`docs/redsocial/configuracion-power-automate.md`](configuracion-power-automate.md) |
| Capturas | `12a` a `12d` en `docs/redsocial/capturas/` (nombres en la guía) |
| Estado | **Hecho el 25/11/2026.** Los dos flujos están creados en el tenant de la US (Joaquín), con capturas `12a` a `12d`, compartidos con Marcos como copropietario y probados por él con su cuenta (capturas `12e` a `12l`, `docs/redsocial/pruebas.md`). La ejecución programada del flujo 2 se observó sola a las 08:00 del 26 y del 27/11 (capturas `12n` y `12m`, hechas el 27/11 con la cuenta de Pablo); no se probó asignar después una tarea ya creada (ver «Limitaciones»). |

## Flujos

Los dos flujos vigilan el plan «Preparación de la Asamblea» del equipo CADUS · Asamblea y avisan en su canal General.

| Flujo | Cuándo se ejecuta | Qué hace | Conectores |
|---|---|---|---|
| Aviso de tarea nueva · Preparación de la asamblea | Cuando se crea una tarea en el plan | Lee la tarea y publica en el canal su título, su fecha límite y quién la creó | Planner, Office 365 Users, Microsoft Teams |
| Aviso de tareas que vencen · Preparación de la asamblea | Todos los días a las 08:00 (hora de Madrid) | Lista las tareas del plan, se queda con las no completadas que vencen hoy, mañana o ya han vencido y las publica en el canal en una tabla; si no hay ninguna, no publica nada | Planner, Microsoft Teams |

El primer flujo parte de la plantilla de Microsoft que ya ofrece el tenant. El segundo es programado porque Planner no tiene un disparador «vence la fecha»: hay que consultar las tareas cada día.

## Datos

Solo viajan por el flujo el título, la fecha límite y el nombre de quien creó la tarea, que son datos de ejemplo del plan (RNF-R01). Ningún flujo toca reclamaciones, mediaciones ni votaciones, y ninguno lee mensajes del canal.

## Permisos

| Quién | Qué puede hacer con los flujos |
|---|---|
| Joaquín (propietario) | Crearlos, editarlos y ver su historial de ejecuciones |
| Marcos (copropietario) | Verlos, ejecutarlos a mano y ver su historial; se añade con «Compartir» |
| Resto del equipo | Sin acceso: el flujo no es del equipo, es de las personas que figuran como propietarias |

Los flujos se ejecutan con las conexiones de la cuenta de quien los creó (Planner, Teams y Office 365 Users), y los mensajes salen en nombre de esa cuenta o del bot de Power Automate, según lo que permita el canal.

## Limitaciones

- **«Se asigna una tarea» se cumple cuando la asignación se hace al crear la tarea.** Si una tarea se crea sin responsable y se asigna después, el primer flujo no avisa. El disparador «Cuando se me asigna una tarea» sí avisaría, pero solo de las tareas de la persona que lo crea.
- **Los flujos dependen de la cuenta que los creó.** Si esa cuenta se desactiva, dejan de ejecutarse. Por eso se comparten con un segundo propietario, y al traspasar la red social a la Ejecutiva (RNF-R03) se reconstruyen con su cuenta siguiendo la guía.
- **El flujo programado consulta cada día, no en el instante.** Una tarea que vence hoy avisa a las 08:00.
- **Moderación del canal.** El canal General de la Asamblea no está moderado. En un canal moderado, como el de avisos de las delegaciones, el mensaje solo saldría si lo publica un propietario.
- **Si el tenant no permite crear o ejecutar flujos** (conector bloqueado, entorno restringido), se documenta el mensaje con captura (RC-R02) y se anota que Planner puede avisar por su cuenta a la persona asignada (a comprobar en su configuración de notificaciones), aunque ese aviso no llega al canal.

## Trazabilidad

| Requisito | Qué lo cubre |
|---|---|
| RF-R11 Avisos automáticos de tareas | Los dos flujos de la tabla «Flujos» |
| RC-R02 Límites del tenant | Mensaje de error y captura si algo no se puede crear o ejecutar |
| RNF-R01 Datos | Solo viajan datos de ejemplo del plan |
| CU-R02 Preparar una asamblea | El plan «Preparación de la Asamblea» ([`../planner/README.md`](planner-diseno.md)) es el que se vigila |
