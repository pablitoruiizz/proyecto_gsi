# Configuración de Planner en la red social (piloto) · guía para Joaquín (R-06)

Estado a 21/11/2026 (las pestañas de los tres planes existen a 22/11; solo el plan de la Asamblea tiene captura). Los tres equipos privados existen (ver [`configuracion-teams.md`](configuracion-teams.md)) y los cuatro integrantes son propietarios de los tres. Esta guía crea **un plan de Planner por equipo** (RF-R09). El diseño completo (planes, cubos, tareas, responsables, fechas y permisos) está en [`colaboracion-microsoft365/planner/README.md`](../../colaboracion-microsoft365/planner/README.md); aquí solo está cómo hacerlo, qué capturar y cómo probarlo.

Hazlo con tu cuenta (`joaluncan@alum.us.es`), que es propietaria. Los nombres exactos de los menús dependen de la versión de Teams: si algo no se parece a lo que dice esta guía, anota lo que ves en pantalla en lugar de adivinar, porque RC-R02 prevé que el tenant limite cosas y eso es contenido válido de la entrega.

## Orden de trabajo

Empieza por el equipo de la Asamblea, que es el de la captura obligatoria (`08-planner.jpg`). (El plan de la Asamblea se rehízo después como proceso de tareas: ver el último apartado.) Con los tres planes hechos son unos 20 o 30 minutos.

| Orden | Equipo | Plan | Captura |
|---|---|---|---|
| 1 | CADUS · Asamblea | Preparación de la asamblea | `08-planner.jpg` (y opcional `08b-planner-graficos.jpg`) |
| 2 | CADUS · Delegaciones | Seguimiento de las delegaciones | opcional |
| 3 | CADUS · Ejecutiva | Coordinación de la Ejecutiva | opcional |

## Pasos para cada plan

1. Abre el equipo y su canal **General**.
2. Pulsa el **+** junto a las pestañas del canal (Añadir una pestaña) y elige **Planner**.
3. Elige **Crear un plan nuevo**, escribe el nombre de la tabla de arriba y guárdalo. No hace falta publicar nada en el canal.
4. En el tablero crea tres cubos con estos nombres exactos: **Por hacer**, **En curso** y **Hecho**. Si Planner trae cubos por defecto con otros nombres, renómbralos o bórralos.
5. Crea las tareas de la tabla del plan en el [README de Planner](../../colaboracion-microsoft365/planner/README.md#tareas-de-ejemplo-ir-r05). Para cada una: el **título** tal cual (termina en «(ejemplo)»), el **cubo**, **Asignar** a su responsable, la **fecha límite** y el **progreso** (No iniciada, En curso o Completada). Si el evento «Asamblea de noviembre (ejemplo)» del calendario de Marcos no cae el 28/11, mueve las fechas en la misma proporción.
6. Comprueba que el tablero enseña las tareas en sus cubos, con su responsable y su fecha.

## Captura obligatoria: `08-planner.jpg` (RF-R09 · CU-R02)

Del plan «Preparación de la asamblea»: el tablero entero con los tres cubos, las cuatro tareas y, en cada una, su responsable y su fecha límite visibles. El estado de cada tarea se ve en su tarjeta. El generador del documento (`scripts/redsocial/build_doc_rsi.py`) la espera con ese nombre y con este pie: «Plan «Preparación de la asamblea» con cubos y tareas asignadas a distintas personas».

Guárdala en `docs/redsocial/capturas/08-planner.jpg` (JPG, como las de `01` y `02`). Para el CU-R02 completo conviene además `08b-planner-graficos.jpg`, con la vista de gráficos de Planner (avance por estado y por persona), que es el paso 5 del caso de uso; el generador todavía no la usa, así que es un extra que se puede pedir a Pablo.

## Qué anotar si algo no se puede

- **El tenant no deja añadir Planner a un canal.** Prueba en el canal General del equipo (es el que dice esta guía). Si ninguno lo permite, anota el mensaje de error literal, el equipo y el canal.
- **Planner no aparece o está desactivado.** Lo mismo: mensaje y captura del error. El Business Case y el documento ya lo prevén como limitación del tenant, y las tareas se describen en el README de Planner.
- **Un plan no se puede compartir en el canal.** Anótalo y deja el plan creado desde la pestaña, aunque no se vea en el canal.

Pásale a Pablo lo que anotes para la sección «Pendiente y limitaciones» del documento.

## Pruebas (R-10): las hace otra persona, no Joaquín

La regla del equipo es que nadie prueba lo que escribió. Quien pruebe lo hace con **su cuenta**, y anota fecha, nombre y resultado en `docs/redsocial/pruebas.md`. Antes de la prueba haz la captura `08-planner.jpg`, porque la prueba cambia el estado de tareas.

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| 1 | Abrir cada uno de los tres planes con una cuenta propietaria | Se ven los tres cubos y las tareas del README con su responsable y su fecha | |
| 2 | Abrir una tarea asignada a esa persona y pasarla a «En curso» y luego a «Completada» | El progreso cambia y se refleja en el tablero y en los gráficos (CU-R02, pasos 4 y 5) | |
| 3 | Filtrar el plan por su propio nombre | Solo salen sus tareas (CU-R04, paso 3) | |
| 4 | Con una cuenta que sea solo miembro del equipo (poner temporalmente a un integrante como miembro, o usar una cuenta de ejemplo): abrir el plan y editar su tarea | Ve el plan y puede cambiar su tarea; **y también puede editar las de los demás**, que es la limitación documentada | |
| 5 | Con una cuenta que no sea miembro de los equipos (RN-R05): intentar abrir el plan | No puede abrirlo. Si no hay una cuenta así, se anota «no probado» | |

Tras las pruebas, devuelve las tareas a los estados de la tabla del README para que los planes queden como están documentados.

## Al terminar

1. Cambia en el [README de Planner](../../colaboracion-microsoft365/planner/README.md) la fila «Estado» y la columna «Estado» de las tablas de tareas por lo que haya quedado.
2. Sube las capturas a `docs/redsocial/capturas/`.
3. Avisa a Pablo: el estado de R-06 en `build_doc_rsi.py` dice «Pendiente (Joaquín)» y lo cambia él, que es el único editor de ese archivo.
4. Todo lo que no se haya podido hacer o probar se dice en el documento; lo no probado por otra persona, también.

## Rehacer el plan de la asamblea como proceso de tareas (RSI-HU-09)

Decidido el 24/11/2026 (razones en [`diseno-tableros-planner.md`](diseno-tableros-planner.md#decisión-sobre-el-plan-de-la-asamblea-rsi-hu-09)): el plan «Preparación de la Asamblea» pasa de «Por hacer, En curso y Hecho» a cuatro cubos por etapa. Se hace **sobre el mismo plan** (no se crea otro), para que los flujos de Power Automate que lo vigilan sigan funcionando. Son unos 20 minutos. En Teams los cubos se llaman **depósitos**.

Si vas a crear también el flujo 1 de [`configuracion-power-automate.md`](configuracion-power-automate.md), hazlo **antes** de crear las dos tareas nuevas de este apartado: así cada una dispara un aviso y tienes la prueba del flujo hecha.

1. Abre el equipo CADUS · Asamblea, canal General, y la pestaña del plan en la vista **Panel**.
2. **Renombra** los depósitos (pulsa su nombre, o los tres puntos del depósito y *Cambiar nombre*):
   - **Por hacer** pasa a **1 · Convocatoria**
   - **En curso** pasa a **2 · Preparación**
   - **Hecho** pasa a **3 · Día de la asamblea**
3. Pulsa **Agregar nuevo depósito**, llámalo **4 · Después (acta)** y colócalo el último. Los cuatro deben quedar de izquierda a derecha en orden del 1 al 4 (arrastra los depósitos si hace falta).
4. **Mueve** las cuatro tareas que ya existen arrastrándolas a su etapa:
   - Crear el evento de la asamblea en el calendario (ejemplo) a **1 · Convocatoria**
   - Enviar la convocatoria y el orden del día (ejemplo) a **1 · Convocatoria**
   - Reservar la sala (ejemplo) a **2 · Preparación**
   - Preparar la plantilla del acta en el DMS (ejemplo) a **2 · Preparación**
5. **Crea las dos tareas nuevas**, con responsable, fecha y progreso «No iniciada»:
   - En **3 · Día de la asamblea**: *Pasar lista y abrir la sesión (ejemplo)*, Pablo, 26/11/2026
   - En **4 · Después (acta)**: *Subir el acta aprobada al DMS (ejemplo)*, Álvaro, 28/11/2026
6. **Comprueba** que el Panel enseña cuatro columnas con tareas, que **Gráficos** sigue mostrando el avance por estado y por persona y que **Programación** pone las fechas antes y después del 26/11.
7. **Captura:** vuelve a hacer `08-planner.jpg` con el Panel completo (las cuatro columnas, y en cada tarea su responsable y su fecha) y sustituye la que hay en `docs/redsocial/capturas/`. Conviene también `08b-planner-graficos.jpg` con Gráficos.
8. **Actualiza la documentación:** las dos frases del apartado «Estado» de [`diseno-tableros-planner.md`](diseno-tableros-planner.md) y la fila «Estado» y la tabla de la asamblea de [`colaboracion-microsoft365/planner/README.md`](../../colaboracion-microsoft365/planner/README.md), con los cubos y las tareas nuevas.
9. **Avisa:** a Álvaro, para que refleje los cuatro cubos en el UML de diseño (R-14a), y a Pablo, para el documento. Este texto sirve para el apartado de Planner:
   > El plan «Preparación de la Asamblea» sigue el patrón Proceso de tareas del Laboratorio 6: sus cuatro cubos son las etapas de la asamblea (1 · Convocatoria, 2 · Preparación, 3 · Día de la asamblea y 4 · Después (acta)) y cada tarea, con su responsable y su fecha límite, se completa en la etapa a la que pertenece. Los planes de la Ejecutiva y de las delegaciones usan el ciclo de vida de tareas (Por hacer, En curso y Hecho).
10. **Cierra la historia** en el burndown solo cuando esté en `main` con su captura y la haya probado otra persona: `python scripts/redsocial/scrum_rsi_sprint.py --hecho RSI-HU-09`.

### Prueba de otra persona

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| 1 | Abrir el plan con su cuenta y mirar el Panel | Ve cuatro cubos en orden (1 · Convocatoria a 4 · Después (acta)) y seis tareas con responsable y fecha | |
| 2 | Pasar una de sus tareas a «En curso» y luego a «Completada» | El progreso cambia en la tarjeta y en Gráficos; la tarea se queda en su cubo | |
| 3 | Abrir la vista Programación | Las tareas aparecen en sus fechas, las de «1» y «2» antes del 26/11 y la de «4» después | |

## Reglas para hacerlo

- Solo datos de ejemplo: nada de nombres reales de delegados ni de reclamaciones, mediaciones o votaciones (RNF-R01).
- Cada captura lleva un pie que dice qué requisito demuestra.
- Un único editor por archivo: no cambies `configuracion-teams.md` ni `plan-lab5.md`; pide los cambios a Pablo.
