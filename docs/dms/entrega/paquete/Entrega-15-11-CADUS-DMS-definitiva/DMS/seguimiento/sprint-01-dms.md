# Sprint 1 del DMS — Sitios, metadatos y entrega del DMS

**Equipo:** 5 integrantes (los mismos del CMS)
**Cliente:** CADUS. **Contacto:** Miguel Ángel Camacho Martín.
**Periodo:** 26/10/2026 – 08/11/2026 (dos semanas)
**Estado:** En curso. Compromiso: 24 SP (DMS-HU-01 a DMS-HU-07)
**Entrega:** domingo 08/11/2026

## Objetivo

Entregar un DMS funcional del CADUS con cuatro tipos de documento (acta, normativa, expediente y registro de votación), sus metadatos, búsquedas con filtros, permisos por rol y su documentación independiente de la del CMS: REM, UML de análisis y de diseño, capturas y seguimiento SCRUM.

## Reparto

| Historia | SP | Quién |
|---|---:|---|
| DMS-HU-01 Sitios, carpetas y permisos | 5 | Pablo |
| DMS-HU-02 Metadatos y tipos de documento | 5 | Joaquín |
| DMS-HU-03 Vista plana y filtros | 3 | Álvaro |
| DMS-HU-04 Actas: de borrador a aprobada | 3 | Miguel Ángel |
| DMS-HU-05 Normativa vigente | 2 | Joaquín |
| DMS-HU-06 Expedientes y caducidad | 3 | Marcos |
| DMS-HU-07 Registro de votación | 3 | Miguel Ángel |
| **Total** | **24** | |

| Integrante | DMS (SP) | CMS Sprint 3 (SP) | Total (SP) |
|---|---:|---:|---:|
| Pablo | 5 | 7 | 12 |
| Joaquín | 7 | 6 | 13 |
| Miguel Ángel | 6 | 7 | 13 |
| Álvaro | 3 | 8 | 11 |
| Marcos | 3 | 8 | 11 |

Las tareas de documentación D-01 a D-06 no llevan puntos ([product backlog](../backlog/product-backlog.md)). Álvaro tiene los UML (D-02 y D-03) además de sus 3 SP, y Pablo el REM y el documento (D-01 y D-06).

## Calendario

| Fecha | Hito |
|---|---|
| Lun 26/10 | Planning y entrevista; plataforma confirmada: SharePoint de Microsoft 365 de la US |
| Mié 28/10 | DMS-HU-01 y DMS-HU-02: sitios, carpetas, grupos y columnas creados |
| Dom 01/11 | Punto de control: historias 03 a 07 en marcha; REM (D-01) y UML (D-02, D-03) terminados; hito del burndown: 11 SP pendientes |
| Vie 06/11 | Todas las historias hechas; capturas y documento (D-04, D-06) |
| Dom 08/11 | **Entrega del DMS** y Sprint Review |

## Definición de Hecho (DoD)

- [ ] Los cuatro tipos de documento existen con sus metadatos y al menos un documento de ejemplo cada uno.
- [ ] Cada caso de uso (CU-D01 a CU-D06) se puede ejecutar de principio a fin, probado por otra persona.
- [ ] Permisos comprobados con cada rol: el delegado no ve borradores de actas, expedientes ni votaciones; el estudiante solo ve la normativa vigente.
- [ ] El registro de votación no contiene números de DNI, no repite delegaciones, distingue ausencia de abstención y, si la votación es secreta, no guarda el voto de cada delegación.
- [ ] REM, UML de análisis y de diseño, capturas explicadas y seguimiento SCRUM entregados, independientes de los del CMS.
- [ ] Burndown actualizado cada día en [`docs/dms/burndown/sprint-01.csv`](../burndown/sprint-01.csv).

## Riesgos

| Riesgo | Medida |
|---|---|
| Los permisos del SharePoint de la US pueden limitar crear sitios o grupos propios. | Comprobarlo el primer día en el entorno; si no se pueden crear sitios, se usan carpetas con permisos dentro de un único sitio. |
| Se acumula trabajo con el CMS (Sprint 3). | El DMS es sobre todo configuración y documentación; el reparto equilibra las dos cargas. |
| Los documentos de ejemplo incluyen datos personales. | Usar datos ficticios; el registro de votación no guarda DNI. |
