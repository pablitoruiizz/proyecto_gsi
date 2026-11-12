# DMS: versión definitiva — qué hace cada uno

Escrito el 12/11/2026. Lo que pidió el profesor sobre lo entregado: **dividir los casos de uso por roles o secciones y añadir en ellos dos casos** (cada documento de casos de uso debe tener dos casos de uso).

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
| **Pablo** (PO) | 1. Pasar el REM a la versión 1.1: nuevos CU-D07 y CU-D08 con sus requisitos, regla RN-D07 (una sola versión vigente por norma), cuenta por delegación en ACT-D02, RC-D02 y CU-D02. 2. Regenerar `DMS.rem` y exportar el HTML y el PDF desde REMUS. 3. Añadir `dcadus@us.es` como propietaria de los tres sitios. 4. Montar el documento final y el zip. | `REM-DMS.md`, `dms_data.json`, `DMS.rem` y su PDF, zip |
| **Joaquín** (SM) | 1. Escribir el documento **CU-Normativa** con CU-D03 y CU-D07. 2. Hacer CU-D07 en SharePoint (subir una versión nueva, pasar la anterior a Derogada, comprobar que la vista «Vigente» solo muestra la nueva) y capturarlo. 3. Actualizar el burndown y el backlog del DMS cada día. | `CU-Normativa`, captura, backlog y burndown al día |
| **Miguel Ángel** | 1. Escribir el documento **CU-Acta** con CU-D01 y CU-D02 y cambiar «correo @alum.us.es» por «cuenta de la delegación». 2. Preguntar al CADUS si hay una cuenta de delegación de prueba para comprobar que un delegado no ve borradores de actas; si no la hay, pasar a un integrante a «Visitantes» para la prueba. 3. Validar con el CADUS los dos casos nuevos. | `CU-Acta`, resultado de la prueba de visitante |
| **Álvaro** | 1. Escribir el documento **CU-Votacion** con CU-D06 y CU-D08. 2. Hacer CU-D08 en SharePoint (filtrar los registros por asamblea y tipo de voto) y capturarlo. 3. Actualizar los **UML** de análisis y de diseño y el diagrama de casos de uso con los 8 casos y los roles. | `CU-Votacion`, captura, 3 diagramas |
| **Marcos** | 1. Escribir el documento **CU-Expediente** con CU-D04 y CU-D05. 2. Ejecutar CU-D05 en SharePoint de principio a fin (eliminar el expediente caducado con sus versiones y vaciar la papelera) y capturarlo. 3. Revisar que `REM-DMS.md`, el JSON y la hoja de REMUS dicen lo mismo. | `CU-Expediente`, capturas, revisión del REM |

### Cada documento de casos de uso

Mismo formato que los actuales (`docs/dms/entrega/casos-de-uso/CU-*.docx`), con estas partes:
1. **Documento:** qué es, sitio y biblioteca de SharePoint, reglas de negocio.
2. **Metadatos:** tabla con el tipo de columna y si es obligatorio.
3. **Permisos:** qué ve cada rol.
4. **Los 2 casos de uso:** actor, cuándo (como un escenario con su momento, como en las diapositivas del Lab 4), precondición, postcondición, pasos numerados y requisitos relacionados.
5. **Implementación en SharePoint:** una captura por caso, explicada, con los códigos de requisito.

Se escriben en `docs/dms/casos-de-uso/<nombre>.md` y Pablo los pasa al generador; el texto de los casos sale de `scripts/remus/dms_data.json`.

### Pruebas cruzadas (nadie prueba lo suyo)

| Prueba | Quién |
|---|---|
| CU-Votacion (CU-D06 y CU-D08) | Pablo |
| CU-Normativa (CU-D03 y CU-D07) | Álvaro |
| CU-Expediente (CU-D04 y CU-D05) | Joaquín |
| CU-Acta (CU-D01 y CU-D02) | Marcos |
| Permisos con un visitante (ningún delegado ve borradores, votaciones ni expedientes) | Miguel Ángel |

Cada prueba se anota con fecha y nombre; con ellas se actualiza el burndown del DMS.

## Calendario

| Fecha | Qué |
|---|---|
| Vie 13/11 | Cada uno su documento de casos de uso y su captura; Pablo, el REM 1.1 y `DMS.rem` |
| Sáb 14/11 | Pruebas cruzadas; Álvaro, los UML; Pablo exporta el REM desde REMUS |
| Dom 15/11 | Documento final y zip del DMS, junto con el cierre del Sprint 3 del CMS |

La fecha de entrega de la versión definitiva del DMS hay que confirmarla con el profesor; este calendario asume el 15/11.

## Además, lo que queda del CMS (Sprint 3, hasta el 15/11)

Sin empezar según el repositorio: Pablo, HU-17b, HU-14c y HU-20b; Joaquín, HU-14a y HU-15a; Miguel Ángel, HU-15c y HU-20a; Álvaro, HU-14b, HU-16a y HU-23. Si el tiempo no llega, se recorta primero HU-16a y HU-20b. El despliegue en el servidor de la US (E3-09) está bloqueado por la versión de PHP.
