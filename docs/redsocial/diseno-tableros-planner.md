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

## Decisión sobre el plan de la asamblea (RSI-HU-09)

**Decidido el 24/11/2026 por Joaquín, responsable de Planner: el plan «Preparación de la Asamblea» pasa al patrón Proceso de tareas.** Los planes de la Ejecutiva y de las delegaciones se quedan con el ciclo de vida de tareas.

### Por qué sí

- **Es el único plan que describe un proceso con etapas en orden.** Las cinco preguntas del método dan «Sí» a «ordenado» (sigue el calendario de la asamblea) y «No» a «cambia» (una tarea no deja de pertenecer a su etapa: se completa donde está).
- **El ciclo de vida repetía lo que Planner ya enseña.** El estado de cada tarea (No iniciada, En curso, Completada) ya se ve en su tarjeta y en la vista de Gráficos. Los cubos «En curso» y «Hecho» duplicaban esa información, mientras que los cubos por etapa añaden lo que faltaba: **cuándo** hay que hacer cada cosa.
- **Se apoya en las vistas que ya se usan.** La vista de Programación comprueba que las fechas caen antes de la asamblea, y los cubos numerados dejan el orden a la vista sin explicación (RNF-R02).
- **Cuesta poco.** Se renombran y reordenan los cubos del mismo plan (unos 20 minutos). Como el plan es el mismo, su identificador no cambia y los flujos de Power Automate que lo vigilan (RSI-HU-07) siguen funcionando.

### Qué se pierde y cómo se compensa

La columna «Hecho» desaparece como tal: una tarea completada se queda en su etapa. Se sigue viendo en la tarjeta (marca de completada y progreso) y en Gráficos, y CU-R02 (pasos 6 y 7: actualizar el estado y ver el avance) funciona igual, porque el estado es el progreso de la tarea y no el cubo.

### Diseño nuevo del plan «Preparación de la Asamblea»

Las fechas suponen la asamblea del evento de ejemplo del calendario, el 26/11/2026. Los responsables siguen siendo los cuatro integrantes.

| Cubo (etapa) | Tarea | Responsable | Fecha límite | Progreso | Origen |
|---|---|---|---|---|---|
| 1 · Convocatoria | Crear el evento de la asamblea en el calendario (ejemplo) | Joaquín | 21/11/2026 | Completada | Ya existe |
| 1 · Convocatoria | Enviar la convocatoria y el orden del día (ejemplo) | Pablo | 24/11/2026 | No iniciada | Ya existe |
| 2 · Preparación | Reservar la sala (ejemplo) | Marcos | 25/11/2026 | En curso | Ya existe |
| 2 · Preparación | Preparar la plantilla del acta en el DMS (ejemplo) | Álvaro | 25/11/2026 | No iniciada | Ya existe |
| 3 · Día de la asamblea | Pasar lista y abrir la sesión (ejemplo) | Pablo | 26/11/2026 | No iniciada | **Nueva** |
| 4 · Después (acta) | Subir el acta aprobada al DMS (ejemplo) | Álvaro | 28/11/2026 | No iniciada | **Nueva** |

Las dos tareas nuevas existen para que ninguna etapa quede vacía: un proceso con una etapa sin tareas no se lee como proceso. Los pasos para hacerlo están en [`configuracion-planner.md`](configuracion-planner.md#rehacer-el-plan-de-la-asamblea-como-proceso-de-tareas-rsi-hu-09).

### Estado

- **A 24/11/2026 no se ha cambiado nada en Planner.** Falta rehacer el plan y repetir la captura `08-planner.jpg` (Joaquín), reflejar los cubos nuevos en el UML de diseño (Álvaro) y actualizar el texto del documento (Pablo).
- **Al terminar,** cambiar en la tabla «Aplicación a los tres planes» la última columna del plan de la asamblea (ahora dice «el diseño actual usa el ciclo de vida») por «rehecho el DD/11/2026», y anotar lo mismo en [`colaboracion-microsoft365/planner/README.md`](../../colaboracion-microsoft365/planner/README.md).
- **Si no se hace antes de la entrega,** el documento sigue describiendo lo que hay en Planner (ciclo de vida) y esta decisión se cita como trabajo futuro.
