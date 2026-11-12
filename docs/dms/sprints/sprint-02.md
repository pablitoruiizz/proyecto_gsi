# Sprint 2 del DMS — Versión definitiva

**Periodo:** 13/11/2026 – 15/11/2026 (la fecha de entrega se confirma con el profesor: tarea D-09)
**Compromiso:** DMS-HU-08 y DMS-HU-09 (4 SP) y las tareas D-07 a D-09, más cerrar lo que quedó del Sprint 1 del DMS: pruebas cruzadas y prueba con cuentas de visitante.

## Objetivo

Entregar los casos de uso divididos por secciones, con dos casos en cada documento (8 en total), con el REM y los UML al día y con pruebas hechas por quien no escribió cada documento. Reparto: [`reparto-version-definitiva.md`](../reparto-version-definitiva.md).

## Orden de trabajo

1. **Viernes 13/11, por la mañana (Pablo y Miguel Ángel):** cerrar identidad y reglas de CU-D07 y CU-D08 (ver «Decisiones previas»), confirmar la fecha y el alcance con el profesor, y subir `REM-DMS` y `dms_data.json` a 1.1. Hasta que esto no esté, el resto escribe sobre borradores.
2. **Viernes 13/11 (todos):** cada uno su documento de casos de uso y su captura; Marcos adapta el generador; Álvaro actualiza los diagramas.
3. **Sábado 14/11:** pruebas cruzadas, prueba con cuentas de visitante y de estudiante, cambios que salgan de ellas y exportación del REM desde REMUS.
4. **Domingo 15/11:** documento final y zip, y comprobación del contenido del zip frente a la lista del profesor.

Un único editor por archivo: `dms_data.json` y `REM-DMS.md` los edita Pablo, `diagramas_dms.py` Álvaro y `build_doc_dms.py` y `empaquetar_dms.py` Marcos; el resto pide los cambios por Discord.

## Decisiones previas

- **CU-D07 (Joaquín):** una norma tiene una columna «Norma» (identifica la misma norma entre revisiones) y «Versión». Publicar una versión nueva es subir un documento nuevo con Estado Vigente y pasar el anterior a Derogada. **RN-D07:** por cada norma solo puede haber una versión vigente (puede haber varias normas distintas vigentes); la versión derogada se conserva, no se borra.
- **CU-D08 (Álvaro):** solo la Ejecutiva consulta los registros de votaciones. Hay que hacer obligatorias en SharePoint las columnas «Asamblea» y «Número de votación» para que los registros se puedan encontrar y distinguir.
- **Delegado y estudiante:** el delegado entra con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11) y el estudiante con su correo `@alum.us.es`. No se sustituye el correo en bloque: se revisan `REM-DMS.md`, `dms_data.json` (ACT-D02, CU-D02, CU-D03 y RC-D02), `diagramas_dms.py` y los documentos.

## Pruebas (nadie prueba lo que escribió ni la historia principal de ese documento)

| Qué | Quién | Con qué cuenta |
|---|---|---|
| CU-Acta (CU-D01, CU-D02), incluido que un visitante no ve borradores | Marcos | propietario y visitante |
| CU-Normativa (CU-D03, CU-D07) | Pablo | propietario y visitante |
| CU-Expediente (CU-D04, CU-D05) | Álvaro | propietario; repetir CU-D05 con un expediente caducado nuevo |
| CU-Votacion (CU-D06, CU-D08) | Joaquín | propietario; comprobar que un visitante no ve la biblioteca |
| Permisos de Votaciones y Expedientes con un visitante, incluidos enlaces directos | Miguel Ángel | visitante |
| Rol estudiante (visitante solo de Documentación pública) | Álvaro | visitante |

Cada prueba se anota con fecha, nombre y resultado, y con ellas se actualiza el burndown.

## Definición de hecho

- [ ] 4 documentos de casos de uso con 2 casos cada uno (8 en total), por secciones.
- [ ] REM y UML con los 8 casos, los roles y la cuenta por delegación.
- [ ] Cada caso ejecutado en SharePoint, con captura explicada y códigos de requisito.
- [ ] Pruebas cruzadas hechas por otra persona y anotadas, también con un visitante y con el rol estudiante.
- [ ] Zip comprobado contra la lista del profesor.
- [ ] Burndown actualizado cada día en [`burndown/sprint-02.csv`](../burndown/sprint-02.csv).

## Riesgos

| Riesgo | Responsable | Medida |
|---|---|---|
| La fecha de entrega o el alcance («dos casos en cada documento») no están confirmados. | Pablo (D-09), antes del 13/11 | Se pregunta al profesor; si es mínimo 1 caso, se mantienen los 8 igualmente. |
| No hay cuenta de delegación de prueba. | Miguel Ángel, 13/11 | Se pasa temporalmente a un integrante a Visitantes y se anota que no es una cuenta de delegación real. |
| Carga conjunta con el Sprint 3 del CMS (25 SP pendientes el 12/11). | Joaquín | Se recorta primero HU-16a y HU-20b del CMS. |
| Un cambio tras una prueba obliga a rehacer documento, UML y captura. | Todos | Se congelan las decisiones el 14/11 a mediodía. |
| El despliegue del CMS en el servidor de la US (PHP 7.2/7.3) está bloqueado. | — | No afecta al DMS, que está en SharePoint; E3-09 pasó al siguiente sprint y el CMS se entrega desde el servidor del equipo. |
