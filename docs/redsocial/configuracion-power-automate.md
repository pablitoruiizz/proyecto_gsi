# Power Automate en la red social (RSI-HU-07, R-12) · guía para Joaquín

Estado a 24/11/2026. El plan «Preparación de la Asamblea» existe en el equipo CADUS · Asamblea (ver [`configuracion-planner.md`](configuracion-planner.md)). Esta guía crea **dos flujos** que avisan en el canal General de ese equipo (RF-R11): uno cuando se crea una tarea y otro cada día con las que vencen. El diseño (conectores, permisos y limitaciones) está en [`colaboracion-microsoft365/power-automate/README.md`](../../colaboracion-microsoft365/power-automate/README.md).

Hazlo con tu cuenta de la universidad. Los nombres exactos de los botones dependen de la versión y del idioma de Power Automate: si algo no se parece a lo que dice esta guía, **no adivines**: haz una captura de lo que ves. Y si el tenant no deja crear o ejecutar un flujo, eso también es contenido de la entrega (RC-R02): anota el mensaje literal y haz captura.

## Orden recomendado

1. Crea y prueba el flujo 1 **antes** de rehacer el plan de la asamblea (RSI-HU-09). Las dos tareas nuevas que pide ese rediseño sirven de prueba natural del flujo.
2. Crea el flujo 2.
3. Haz las capturas, comparte los flujos con Marcos y pídele la prueba.

## Antes de empezar

1. Entra en `https://make.powerautomate.com` y comprueba arriba a la derecha que el entorno es **Productividad Personal US (default)**.
2. Ten abierto Teams con el equipo CADUS · Asamblea y su pestaña de Planner, para ver el resultado.

## Flujo 1 · «Aviso de tarea nueva · Preparación de la asamblea»

Parte de una plantilla que el tenant ya ofrece.

1. En Power Automate, abre **Plantillas** y busca **Planner**. Elige **Notificar a un canal cuando se crea una nueva tarea de Planner** y pulsa **Continuar**.
2. Si te pide **conexiones** (Planner, Office 365 Users y Microsoft Teams), permítelas con tu cuenta. Si alguna da error de permisos, **para aquí**: captura del mensaje y pasa al apartado «Si el tenant no lo permite».
3. Pulsa **Crear flujo**. Se abre el editor con el disparador y las acciones.
4. En el **disparador** de Planner (cuando se crea una tarea), elige:
   - **Id. de grupo:** `CADUS · Asamblea`
   - **Id. del plan:** `Preparación de la Asamblea`
5. En la acción de **Microsoft Teams** (publicar un mensaje en un chat o canal), elige:
   - **Publicar como:** *Flow bot* (o tu usuario, si el bot no está permitido)
   - **Publicar en:** *Canal*
   - **Equipo:** `CADUS · Asamblea` · **Canal:** `General`
6. En el **mensaje** escribe el texto siguiente y, donde pone «…», inserta el **contenido dinámico** de la tarea (título, fecha de vencimiento y nombre de quien la creó) con el selector, sin escribirlo a mano:
   > Nueva tarea en «Preparación de la Asamblea»: … Fecha límite: … Creada por: … (aviso automático de ejemplo)
7. Pon nombre al flujo, arriba a la izquierda: **Aviso de tarea nueva · Preparación de la asamblea**. Pulsa **Guardar**. Si hay avisos de error en alguna acción, revisa los campos marcados.
8. **Comparte el flujo con Marcos:** en la página del flujo, **Compartir** (o **Propietarios**) y añade a Marcos como propietario.

### Probarlo

1. Abre la pestaña de Planner del equipo y crea una tarea nueva en el plan, con título, responsable y fecha. Sirven las dos tareas nuevas de la guía de HU-09, o una de prueba llamada `Prueba de aviso (ejemplo)`.
2. Espera entre uno y cinco minutos: debe salir un mensaje en el canal **General** de CADUS · Asamblea con el título y la fecha.
3. En la página del flujo, mira el **historial de ejecuciones**: la última debe poner **Correcto**.
4. Si la tarea era solo de prueba, bórrala.

**Capturas:**
- `12a-power-automate-flujo-tarea.jpg`: el flujo en el editor, con el disparador y las dos o tres acciones a la vista.
- `12b-power-automate-aviso-tarea.jpg`: el mensaje en el canal de Teams.

## Flujo 2 · «Aviso de tareas que vencen · Preparación de la asamblea»

Es un flujo programado porque Planner no tiene un disparador «vence la fecha».

1. En **Mis flujos**, pulsa **Nuevo flujo** y elige **Flujo de nube programado**. Ponle el nombre **Aviso de tareas que vencen · Preparación de la asamblea**, empieza **mañana a las 08:00**, repite **cada 1 día** y créalo. Comprueba en el disparador que la zona horaria es la de Madrid.
2. Añade la acción de **Planner** que **enumera las tareas** de un plan (puede llamarse *Enumerar tareas* u *Obtener tareas*). Elige el mismo grupo y el mismo plan que en el flujo 1.
3. Añade **Filtrar matriz** (*Filter array*):
   - **De:** la lista de tareas de la acción anterior (selector de contenido dinámico).
   - **Condición:** abre la edición **avanzada** y escribe
     `@and(not(equals(item()?['percentComplete'], 100)), not(empty(item()?['dueDateTime'])), lessOrEquals(item()?['dueDateTime'], addDays(utcNow(), 1)))`
     que significa: no completada, con fecha y que vence hoy, mañana o antes. Si tu editor llama de otra forma a los campos (*title*, *dueDateTime*, *percentComplete*), usa los que te ofrezca el selector en lugar de escribirlos.
4. Añade **Crear tabla HTML** con la salida del filtro, en columnas personalizadas: **Tarea** = el título de la tarea y **Vence** = su fecha de vencimiento.
5. Añade una **Condición**: la cantidad de elementos de la salida del filtro (`length(...)`) **es mayor que** 0.
   - **Si es verdadero:** acción de Microsoft Teams que publica en el canal General de CADUS · Asamblea el texto «Tareas que vencen hoy o mañana, o ya vencidas, y no están completadas (aviso automático de ejemplo):» seguido de la tabla HTML.
   - **Si es falso:** no hagas nada.
6. **Guarda** y comparte el flujo con Marcos como propietario.

### Probarlo

1. Deja en el plan una tarea sin completar con vencimiento mañana (o ya vencida).
2. En la página del flujo, pulsa **Probar**, elige **Manualmente** y **Ejecutar flujo**.
3. Debe salir en el canal un mensaje con la tabla y esa tarea, y una tarea completada no debe salir.

**Capturas:**
- `12c-power-automate-flujo-vencimiento.jpg`: el flujo en el editor con todas sus acciones.
- `12d-power-automate-aviso-vencimiento.jpg`: el mensaje con la tabla en el canal.

Los nombres `12a` a `12d` son una propuesta para dejar el `13` a la aplicación de PowerApps de Álvaro; Pablo los confirma al montar el documento.

## Si el tenant no lo permite

| Qué pasa | Qué hacer |
|---|---|
| Power Automate no carga o no deja crear flujos | Captura del mensaje, el entorno y tu cuenta |
| Una conexión (Planner, Teams u Office 365 Users) da error de permisos | Captura del mensaje y de qué conexión era; pásalo a Pablo |
| El flujo se guarda pero no se ejecuta o falla | Captura del historial de ejecuciones con el error y de la acción que falló |
| El mensaje no sale en el canal | Prueba a publicar «como usuario» en lugar de como *Flow bot*; si sigue sin salir, anota el error |

En cualquiera de los casos, la historia se documenta con el mensaje del tenant (RC-R02). Pasa a Pablo lo que anotes para la sección «Pendiente y limitaciones» del documento.

## Prueba de otra persona (R-12c): la hace Marcos, no Joaquín

Quien prueba lo hace con su cuenta y anota fecha, nombre y resultado en [`pruebas.md`](pruebas.md). Antes de probar, haz tú las capturas.

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| 1 | Crear en el plan una tarea nueva con responsable y fecha | En uno a cinco minutos sale un mensaje en el canal General de CADUS · Asamblea con su título y su fecha | |
| 2 | Abrir el historial de ejecuciones del flujo 1 | La ejecución aparece como Correcto | |
| 3 | Ejecutar a mano el flujo 2 con una tarea sin completar que vence mañana | Sale un mensaje con una tabla que incluye esa tarea | |
| 4 | Completar esa tarea y volver a ejecutar el flujo 2 | No sale ningún mensaje (o la tabla ya no la incluye) | |
| 5 | Comprobar que Marcos figura como propietario de los dos flujos | Puede abrirlos y ver su historial | |

Después de las pruebas, borra las tareas de prueba para dejar el plan como está documentado.

## Al terminar

1. Cambia en el [README de Power Automate](../../colaboracion-microsoft365/power-automate/README.md) la fila «Estado» y la columna «Cuándo se ejecuta» si algo cambió.
2. Sube las capturas a `docs/redsocial/capturas/`.
3. Cierra RSI-HU-07 en el burndown **solo** cuando esté en `main`, con sus capturas y probada por otra persona: `python scripts/redsocial/scrum_rsi_sprint.py --hecho RSI-HU-07`.
4. Avisa a Pablo de qué funciona, qué no y qué no se pudo probar, para el documento.

## Reglas

- Solo datos de ejemplo; nada de reclamaciones, mediaciones ni votaciones (RNF-R01).
- No pegues nunca contraseñas, enlaces de conexión ni identificadores en el repositorio. Las capturas muestran flujos, no credenciales.
- Un único editor por archivo compartido: pide los cambios en `plan-lab5.md` o en el documento a Pablo.
