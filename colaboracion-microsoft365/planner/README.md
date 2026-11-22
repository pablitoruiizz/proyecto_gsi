# Planner · planes de tareas de la red social

Documentación del artefacto de Planner de la Red Social Interna del CADUS (Lab 5, Microsoft Teams), con lo que pide el [README del área](../README.md): objetivo, configuración, permisos y trazabilidad con historias y sprints.

| Dato | Valor |
|---|---|
| Objetivo | Que las tareas de preparación de las asambleas y de los cursos estén a la vista y asignadas a quien corresponde (OBJ-R02) |
| Herramienta | Planner, como pestaña de cada equipo de Teams del tenant de la Universidad de Sevilla (RC-R01) |
| Tarea y entrega | R-06 de [`plan-lab5.md`](../../docs/redsocial/plan-lab5.md), entrega del 22/11/2026 (Teams y Planner) |
| Responsable | Joaquín Luna Canela |
| Requisitos | RF-R09, IR-R05, UI-R02, RNF-R02, RNF-R03 |
| Casos de uso | CU-R02 Preparar una asamblea con tareas y CU-R04 Consultar avisos, calendario y tareas |
| Cómo se crea | [`docs/redsocial/configuracion-planner.md`](../../docs/redsocial/configuracion-planner.md) |
| Captura | `docs/redsocial/capturas/08-planner.jpg` |
| Estado | **Diseñado el 21/11/2026. Estado a 22/11: las pestañas de Planner de los tres equipos existen; solo el plan «Preparación de la Asamblea» tiene captura (`08-planner.jpg`).** Las columnas «Estado» de las tablas de tareas son las del diseño y no se han actualizado con lo que haya en Planner. Nota: el evento del calendario cae el 26/11 y la tarea «Preparar la plantilla del acta» vencía el 27/11, después de la asamblea; el 22/11/2026 se cambió su vencimiento en Planner al 25/11 (el diseño inicial decía 27/11) |

## Planes

Un plan por equipo (RF-R09), con los mismos tres cubos, para que cualquiera los entienda sin explicación (RNF-R02).

| Plan | Equipo de Teams (grupo) | Para qué sirve | Cubos |
|---|---|---|---|
| Coordinación de la Ejecutiva | CADUS · Ejecutiva | Preparar lo que luego se publica en los avisos (RF-R02) | Por hacer · En curso · Hecho |
| Seguimiento de las delegaciones | CADUS · Delegaciones | Pedir y seguir lo que cada delegación debe hacer (RF-R03) | Por hacer · En curso · Hecho |
| Preparación de la asamblea | CADUS · Asamblea | Preparar una asamblea o un curso con tareas y fechas (RF-R04, CU-R02) | Por hacer · En curso · Hecho |

## Tareas de ejemplo (IR-R05)

Son datos de ejemplo: ni nombres de delegados reales ni nada de reclamaciones, mediaciones o votaciones (RNF-R01). Las fechas suponen que el evento «Asamblea de noviembre (ejemplo)» del calendario cae el 28/11/2026; si Marcos le puso otra fecha, se mueven en la misma proporción. Los responsables son los cuatro integrantes del equipo, que hacen de Ejecutiva y de delegaciones en el piloto.

### Coordinación de la Ejecutiva

| Cubo | Tarea | Responsable | Fecha límite | Estado |
|---|---|---|---|---|
| Por hacer | Redactar el aviso de la asamblea de noviembre (ejemplo) | Pablo | 24/11/2026 | No iniciada |
| En curso | Revisar el aviso antes de publicarlo (ejemplo) | Joaquín | 25/11/2026 | En curso |
| Hecho | Comprobar los propietarios del equipo (ejemplo) | Marcos | 21/11/2026 | Completada |

### Seguimiento de las delegaciones

| Cubo | Tarea | Responsable | Fecha límite | Estado |
|---|---|---|---|---|
| Por hacer | Confirmar la asistencia a la asamblea · Delegación ETSII (ejemplo) | Álvaro | 26/11/2026 | No iniciada |
| Por hacer | Confirmar la asistencia a la asamblea · Delegación Derecho (ejemplo) | Marcos | 26/11/2026 | No iniciada |
| En curso | Confirmar la asistencia a la asamblea · Delegación Biología (ejemplo) | Joaquín | 26/11/2026 | En curso |
| Hecho | Leer el aviso de la convocatoria (ejemplo) | Joaquín | 23/11/2026 | Completada |

### Preparación de la asamblea

| Cubo | Tarea | Responsable | Fecha límite | Estado |
|---|---|---|---|---|
| Por hacer | Enviar la convocatoria y el orden del día (ejemplo) | Pablo | 24/11/2026 | No iniciada |
| Por hacer | Preparar la plantilla del acta en el DMS (ejemplo) | Álvaro | 25/11/2026 (ajustada en Planner el 22/11; el diseño decía 27/11) | No iniciada |
| En curso | Reservar la sala (ejemplo) | Marcos | 25/11/2026 | En curso |
| Hecho | Crear el evento de la asamblea en el calendario (ejemplo) | Joaquín | 21/11/2026 | Completada |

Las tareas se reparten entre los cubos y los estados a propósito: así la captura y los gráficos de Planner enseñan el avance (CU-R02, pasos 4 y 5) y una delegación ve solo lo suyo al filtrar por su nombre (CU-R04, paso 3).

## Permisos

Un plan de Planner pertenece al grupo de Microsoft 365 del equipo y hereda sus roles (comprobar en el tenant):

| Rol en Teams | Qué puede hacer en el plan |
|---|---|
| Propietario (Ejecutiva y administrador del equipo) | Ver y editar el plan, crear cubos y tareas y asignarlas |
| Miembro (delegaciones) | Ver el plan y editar tareas, entre ellas las suyas |
| Invitado | Nadie lo es en el piloto |
| Estudiante | Sin acceso: no es miembro ni invitado (RN-R05) |

## Limitaciones

- **Todos los miembros ven y pueden editar todas las tareas del plan.** Planner no tiene permisos por tarea. Por eso el plan de Delegaciones no contiene nada que una delegación no deba ver de otra, y no se guardan en Planner datos personales (RNF-R01, RN-R02).
- **Planner en canales privados.** Si el tenant no deja añadir la pestaña a un canal privado, se añade en el canal General del equipo y se anota el mensaje de error (RC-R02).
- **Avisos automáticos** de tareas asignadas o vencidas (RF-R11) son del Sprint 2, con Power Automate, y dependen de que el tenant lo ofrezca.
- **Traspaso.** Al terminar el proyecto, los planes pasan a la Ejecutiva con el equipo (RNF-R03).
