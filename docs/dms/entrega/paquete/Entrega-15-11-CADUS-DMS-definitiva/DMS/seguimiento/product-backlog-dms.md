# Product Backlog del DMS

Seguimiento SCRUM del DMS, independiente del del CMS ([`docs/scrum/`](../../scrum/backlog/product-backlog.md)). Requisitos y casos de uso: [`REM-DMS.md`](../REM-DMS.md).

## Historias de usuario

| ID | Historia | Requisitos | Prioridad | SP | Estado | Sprint | Responsable |
|---|---|---|---|---:|---|---|---|
| DMS-HU-01 | Como miembro de la Ejecutiva, quiero un DMS con los sitios Documentación pública, Órganos de gobierno y Atención al estudiante, con sus carpetas y permisos por rol. | RF-D01, RF-D06, RN-D02 | Alta | 5 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Pablo |
| DMS-HU-02 | Como miembro de la Ejecutiva, quiero columnas de metadatos y tipos de documento para identificar cada documento. | RF-D02, RN-D06 | Alta | 5 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Joaquín |
| DMS-HU-03 | Como Delegado o Estudiante, quiero buscar por texto y filtrar por metadatos en una vista plana. | RF-D04, RF-D05 | Alta | 3 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Álvaro |
| DMS-HU-04 | Como miembro de la Ejecutiva, quiero aprobar las actas con la aprobación de contenido de la biblioteca para que los delegados solo vean las aprobadas. | RF-D03, RF-D09, RN-D01 | Alta | 3 | En curso (falta probar con una cuenta de delegado) | Sprint-01 | Miguel Ángel |
| DMS-HU-05 | Como Estudiante, quiero consultar la normativa vigente y que la derogada no aparezca. | RF-D01, RF-D05 | Media | 2 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Joaquín |
| DMS-HU-06 | Como miembro de la Ejecutiva, quiero archivar expedientes con su fecha de caducidad calculada y ver los caducados para retirarlos. | RF-D07, RF-D08, RN-D03 | Alta | 3 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Marcos |
| DMS-HU-07 | Como miembro de la Ejecutiva, quiero registrar el resultado de una votación por delegación sin guardar el DNI y, si es secreta, sin guardar el voto de cada delegación. | RF-D09, RN-D04, RN-D05 | Media | 3 | Configurada el 30/10 (falta prueba cruzada) | Sprint-01 | Miguel Ángel |
| DMS-HU-08 | Como miembro de la Ejecutiva, quiero publicar una nueva versión de una norma y derogar la anterior, para que solo haya una versión vigente (CU-D07). | RF-D02, RF-D05, RF-D06, RN-D06, RN-D07 | Media | 2 | Ejecutada el 13/11 (Pablo con Claude); falta la prueba cruzada | Sprint-02 | Joaquín |
| DMS-HU-09 | Como miembro de la Ejecutiva, quiero consultar los registros de votaciones anteriores filtrándolos por asamblea y tipo de voto (CU-D08). | RF-D05, RF-D06, RN-D04, RN-D05, RN-D06, RNF-D01 | Media | 2 | Ejecutada el 13/11 (Pablo con Claude); falta la prueba cruzada | Sprint-02 | Álvaro |

**Total: 28 SP** (24 del Sprint 1 y 4 del Sprint 2, la versión definitiva). El requisito deseable RF-D10 (resumen automático del acta) no tiene historia: se hará solo si sobra tiempo.

## Tareas de documentación (sin puntos)

| ID | Tarea | Responsable |
|---|---|---|
| D-01 | REM del DMS en REMUS (`DMS.rem`) a partir de [`REM-DMS.md`](../REM-DMS.md). | Pablo |
| D-02 | UML de análisis: documentos, carpetas, roles, búsqueda y metadatos. | Álvaro |
| D-03 | UML de diseño: del análisis al diseño (sitios, grupos de permisos, columnas, vista plana). | Álvaro |
| D-04 | Capturas de la implementación, explicadas una a una (cada uno las de su historia). | Todos |
| D-05 | Seguimiento SCRUM del DMS: backlog, sprint backlog y burndown diario. | Joaquín |
| D-06 | Documento de la entrega del DMS con la trazabilidad REM ↔ análisis ↔ diseño ↔ implementación. | Pablo |
| D-07 | Versión definitiva: un documento de casos de uso por sección con 2 casos cada uno, REM 1.1 y UML con los 8 casos. Reparto en [`reparto-version-definitiva.md`](../reparto-version-definitiva.md). | Todos |
| D-08 | Adaptar el generador (`build_doc_dms.py`) y el empaquetado (`empaquetar_dms.py`) a la versión 1.1 y a los 8 casos de uso. | Marcos |
| D-09 | Confirmar con el profesor la fecha de entrega de la versión definitiva y el alcance («dos casos en cada documento»). | Pablo, antes del 13/11 |

## Roadmap

- **Sprint-01 del DMS** (26/10 – 08/11/2026, dos semanas): DMS-HU-01 a DMS-HU-07 y las tareas D-01 a D-06. Entrega el 08/11.
- **Sprint-02 del DMS** (13/11 – 15/11/2026): DMS-HU-08, DMS-HU-09 y las tareas D-07 a D-09 (versión definitiva). Plan en [`sprints/sprint-02.md`](../sprints/sprint-02.md).
