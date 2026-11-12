# DMS: versión definitiva — qué hace cada uno

Escrito el 12/11/2026. Lo que dijo el profesor sobre lo entregado: **dividir los casos de uso por roles o secciones y añadir en ellos dos casos**. El enunciado del Lab 4 (diapositiva 7) exige solo 3-4 documentos, al menos 1 caso de uso por documento y al menos un documento con más de 1; la frase del profesor es una corrección verbal y la interpretamos como «dos casos en cada documento». Pablo lo confirma con el profesor (tarea D-09) antes del 13/11.

## Cómo lo interpretamos

- **Dividimos por secciones**, que coinciden con las bibliotecas de SharePoint y con quién las usa. Son 4 documentos de casos de uso y **cada uno lleva 2 casos**, 8 en total (hoy hay 6: acta y expediente ya tienen 2, normativa y votación tienen 1).
- Cada caso indica su actor (el rol), así que en cada documento se ve qué hace la Ejecutiva, el delegado o el estudiante.
- Para llegar a 2 casos en normativa y en votación proponemos dos casos nuevos (se pueden cambiar si el equipo prefiere otros):

| Documento | Caso 1 | Caso 2 |
|---|---|---|
| Acta | CU-D01 Redactar, aprobar y archivar un acta (Ejecutiva) | CU-D02 Consultar las actas aprobadas (delegado) |
| Normativa | CU-D03 Consultar la normativa vigente (estudiante o delegado) | **CU-D07 nuevo:** Publicar una nueva versión de una norma y derogar la anterior (Ejecutiva) |
| Expediente | CU-D04 Archivar un expediente resuelto (Ejecutiva) | CU-D05 Retirar los expedientes caducados (Ejecutiva) |
| Votación | CU-D06 Registrar el resultado de una votación presencial (Ejecutiva) | **CU-D08 nuevo:** Consultar los registros de votaciones anteriores (Ejecutiva) |

- **Un cambio de requisitos que afecta a todo:** el cliente decidió el 09/11 una cuenta por delegación, con el correo institucional de la delegación. Donde los documentos dicen que el delegado entra «con su correo `@alum.us.es`», pasa a «con la cuenta de su delegación».

## Reparto

| Persona | Qué hace | Entrega |
|---|---|---|
| **Pablo** (PO) | 1. Confirmar con el profesor la fecha y el alcance (D-09) antes del 13/11. 2. Pasar el REM a la versión 1.1 (único editor de `REM-DMS.md` y `dms_data.json`): CU-D07 y CU-D08 con sus requisitos, RN-D07 (por cada norma, una sola versión vigente; normas distintas pueden estar vigentes a la vez), cuenta por delegación en ACT-D02, CU-D02, CU-D03 y RC-D02 sin cambiar en bloque el correo del estudiante. 3. Regenerar `DMS.rem` y exportar el HTML y el PDF desde REMUS. 4. Añadir `dcadus@us.es` como propietaria de los tres sitios. 5. Probar CU-Normativa. | `REM-DMS.md`, `dms_data.json`, `DMS.rem` y su PDF |
| **Joaquín** (SM) | 1. Escribir el documento **CU-Normativa** con CU-D03 y CU-D07. 2. En SharePoint, añadir a Normativa las columnas «Norma» y «Versión», hacer CU-D07 (subir una versión nueva, pasar la anterior a Derogada, comprobar que la vista «Vigente» solo muestra la nueva) y capturarlo. 3. Probar CU-Votacion. 4. Actualizar el burndown y el backlog del DMS cada día. | `CU-Normativa`, captura, backlog y burndown al día |
| **Miguel Ángel** | 1. Escribir el documento **CU-Acta** con CU-D01 y CU-D02, con el delegado entrando con la cuenta de su delegación. 2. Validar con el CADUS los dos casos nuevos (antes del mediodía del 13/11, junto con Pablo) y preguntar si hay una cuenta de delegación de prueba; si no la hay, pasar temporalmente a un integrante a «Visitantes» y anotar que no es una cuenta real. 3. Probar con ese visitante los permisos de Votaciones y Expedientes, incluidos los enlaces directos. | `CU-Acta`, resultado de las pruebas de visitante |
| **Álvaro** | 1. Escribir el documento **CU-Votacion** con CU-D06 y CU-D08. 2. En SharePoint, hacer obligatorias «Asamblea» y «Número de votación» en Votaciones, hacer CU-D08 (filtrar los registros por asamblea y tipo de voto) y capturarlo. 3. Actualizar los **UML** de análisis y de diseño y el diagrama de casos de uso con los 8 casos y los roles (único editor de `diagramas_dms.py`). 4. Probar CU-Expediente y el rol estudiante. | `CU-Votacion`, captura, 3 diagramas |
| **Marcos** | 1. Escribir el documento **CU-Expediente** con CU-D04 y CU-D05. 2. Ejecutar CU-D05 en SharePoint de principio a fin (eliminar el expediente caducado con sus versiones y vaciar la papelera) y capturarlo; preparar un expediente caducado nuevo para repetir la prueba. 3. **Adaptar el generador y el empaquetado** (único editor de `build_doc_dms.py` y `empaquetar_dms.py`) a la versión 1.1 y a los 8 casos, con el documento final y el zip (D-08). 4. Probar CU-Acta. 5. Revisar que `REM-DMS.md`, el JSON y la hoja de REMUS dicen lo mismo. | `CU-Expediente`, capturas, generador, zip, revisión del REM |

### Cada documento de casos de uso

Mismo formato que los actuales (`docs/dms/entrega/casos-de-uso/CU-*.docx`), con estas partes:
1. **Documento:** qué es, sitio y biblioteca de SharePoint, reglas de negocio.
2. **Metadatos:** tabla con el tipo de columna y si es obligatorio.
3. **Permisos:** qué ve cada rol.
4. **Los 2 casos de uso:** actor, cuándo (como un escenario con su momento, como en las diapositivas del Lab 4), precondición, postcondición, pasos numerados y requisitos relacionados.
5. **Implementación en SharePoint:** una captura por caso, explicada, con los códigos de requisito.

Cada uno escribe su documento en `docs/dms/casos-de-uso/<nombre>.md`. Los pasos de cada caso salen de `scripts/remus/dms_data.json` (lo edita Pablo: se le piden los cambios por Discord), y Marcos adapta el generador para que lea los 8 casos y los asigne a su documento.

### Pruebas cruzadas (nadie prueba lo suyo)

| Prueba | Quién |
|---|---|
| CU-Acta (CU-D01 y CU-D02) y que un visitante no ve borradores | Marcos |
| CU-Normativa (CU-D03 y CU-D07) | Pablo |
| CU-Expediente (CU-D04 y CU-D05) y rol estudiante | Álvaro |
| CU-Votacion (CU-D06 y CU-D08) | Joaquín |
| Permisos de Votaciones y Expedientes con un visitante, enlaces directos incluidos | Miguel Ángel |

Nadie prueba lo que escribió ni la historia principal de ese documento. Cada prueba se anota con fecha, nombre y resultado; con ellas se actualiza el burndown del DMS (Sprint 2 del DMS: [`sprints/sprint-02.md`](sprints/sprint-02.md)). Sin una cuenta de delegación real, la prueba con un visitante no demuestra que funcione esa cuenta: se anota así.

## Calendario

| Fecha | Qué |
|---|---|
| Vie 13/11, mañana | Pablo y Miguel Ángel cierran identidad y reglas de CU-D07 y CU-D08, y Pablo pregunta al profesor la fecha y el alcance |
| Vie 13/11 | Cada uno su documento de casos de uso y su captura; Pablo, el REM 1.1 y `DMS.rem`; Marcos, el generador; Álvaro, los diagramas |
| Sáb 14/11 | Pruebas cruzadas y de visitante y estudiante; Pablo exporta el REM desde REMUS; decisiones congeladas a mediodía |
| Dom 15/11 | Documento final y zip del DMS (Marcos), comprobados contra la lista del profesor, junto con el cierre del Sprint 3 del CMS |

La fecha de entrega de la versión definitiva del DMS hay que confirmarla con el profesor; este calendario asume el 15/11.

## Además, lo que queda del CMS (Sprint 3, hasta el 15/11)

Sin empezar según el repositorio: Pablo, HU-17b, HU-14c y HU-20b; Joaquín, HU-14a y HU-15a; Miguel Ángel, HU-15c y HU-20a; Álvaro, HU-14b, HU-16a y HU-23. Si el tiempo no llega, se recorta primero HU-16a y HU-20b. El despliegue en el servidor de la US (E3-09) está bloqueado por la versión de PHP y pasó al siguiente sprint: es un bloqueo del CMS, no del DMS en SharePoint, y no cuenta como trabajo de este fin de semana.
