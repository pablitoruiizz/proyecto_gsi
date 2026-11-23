# Diseño de los tableros de Planner con patrones (Lab 6)

Aplicación a la red social del CADUS del Lab 6, «Designing Board Based Panels» (Joaquín Peña, Universidad de Sevilla), que explica los patrones de diseño para tableros de gestión del trabajo colaborativo (listas, tarjetas y vistas de Planner o Trello). Este documento justifica el diseño de los tres planes de Planner que ya existen (ver [`colaboracion-microsoft365/planner/README.md`](../../colaboracion-microsoft365/planner/README.md)) y deja anotada una mejora.

## El método del Lab 6: cinco preguntas para diseñar un tablero

| Nº | Pregunta | Qué se decide |
|---|---|---|
| 1 | ¿**Qué** gestionar? | Una acción (tareas) o un recurso (información) |
| 2 | ¿**Dónde** poner el foco? | El nivel de abstracción: qué representa una tarjeta |
| 3 | ¿**Cómo** observarlo? | El criterio de clasificación: qué representan las listas (cubos en Planner) |
| 4 | ¿El criterio está **ordenado**? | Precedencia semántica: sí si las listas tienen un orden natural |
| 5 | ¿Cambia con el tiempo? | Flujo de tarjetas: sí si las tarjetas se mueven de una lista a otra |

## Catálogo de patrones (tabla del Lab 6)

| Patrón | Para qué sirve | Qué gestiona | Precedencia semántica | Flujo de tarjetas |
|---|---|---|---|---|
| Ciclo de vida de la información o los recursos | Varios recursos a la vez en distintas fases | Recursos | Sí | Sí |
| Información ordenada (proceso de información) | Listas con un criterio de orden | Recursos | Sí | No |
| **Ciclo de vida de tareas** (Task Lifecycle) | Gestionar tareas, cómo evolucionan, y vigilarlas | Tareas | Sí | Sí |
| **Proceso de tareas** (Task Process) | Guía secuenciada de tareas dividida en las etapas de un proyecto | Tareas | Sí | No |
| Información o recursos asignados | Clasificación que puede cambiar con el tiempo | Recursos | No | Sí |
| Información categorizada | Categorías que no cambian | Recursos | No | No |
| **Tareas asignadas** (Assigned Tasks) | Cambiar el contenedor de una tarea para asignarla a una persona u otra | Tareas | No | Sí |
| **Tareas categorizadas** (Categorized Tasks) | Varias listas de tareas pendientes | Tareas | No | No |

En la red social solo gestionamos tareas, así que solo importan los cuatro patrones en negrita.

## Aplicación a los tres planes

Los tres planes comparten la herramienta (Planner como pestaña de un equipo de Teams, RC-R01) y la regla RNF-R02: que cualquiera los entienda sin explicación.

| Plan | 1 Qué | 2 Nivel | 3 Criterio | 4 Ordenado | 5 Cambia | Patrón |
|---|---|---|---|---|---|---|
| Coordinación de la Ejecutiva | Tareas | Una tarjeta es una tarea de preparación (un aviso, una revisión) | Estado del trabajo: Por hacer, En curso, Hecho | Sí | Sí: la tarea pasa de un cubo al siguiente | **Ciclo de vida de tareas** |
| Seguimiento de las delegaciones | Tareas | Una tarjeta es lo que debe hacer una delegación (confirmar asistencia, leer un aviso) | Estado del trabajo, igual que arriba | Sí | Sí | **Ciclo de vida de tareas** |
| Preparación de la asamblea | Tareas | Una tarjeta es un paso de la preparación | Etapa del proyecto: antes, durante y después de la asamblea | Sí, sigue el calendario | No: una tarea pertenece a su etapa y se completa donde está | **Proceso de tareas** (el diseño actual usa el ciclo de vida) |

### Por qué no «Tareas asignadas» ni «Tareas categorizadas» en el plan de las delegaciones

La idea natural era un cubo por delegación (criterio «quién»), es decir, tareas asignadas o categorizadas. Se descarta por dos razones:

- Hay **27 delegaciones**: 27 cubos hacen el tablero inmanejable.
- Planner no tiene permisos por tarea: todos los miembros ven todas las tareas del plan (limitación ya documentada). Separar por delegación no aporta privacidad, así que no compensa.

La delegación a la que va cada tarea se indica en el título («· Delegación ETSII») y en el responsable; se filtra por persona en la vista del tablero. Lo que interesa seguir es el avance, y eso lo da el ciclo de vida.

## Qué vistas de Planner se usan para qué

| Vista | Uso en la red social |
|---|---|
| Tablero (cubos y tarjetas) | Trabajo diario de la Ejecutiva y las delegaciones; es la captura `08-planner.jpg` |
| Gráficos | Avance por estado y por persona, para la reunión de la Ejecutiva (CU-R02) |
| Programación (calendario) | Comprobar que las fechas de las tareas caen antes de la asamblea |

## Estado y mejora pendiente

- **Hoy:** los tres planes usan el ciclo de vida de tareas (cubos Por hacer, En curso y Hecho). Es coherente con RNF-R02 y está documentado y capturado.
- **Mejora propuesta (la decide Joaquín, que es el responsable de Planner):** pasar el plan de la asamblea al patrón **Proceso de tareas**, con cubos por etapa: 1 · Convocatoria, 2 · Preparación, 3 · Día de la asamblea y 4 · Después (acta). Es el único plan que describe un proceso con etapas en orden. Costaría unos 20 minutos de Planner y repetir la captura `08-planner.jpg`; además habría que reflejar los cubos nuevos en el UML de diseño. Si no se hace antes de la entrega, el documento sigue describiendo lo que hay (ciclo de vida) y esta mejora se cita como trabajo futuro.
- **No se ha cambiado nada en Planner** al redactar este documento.
