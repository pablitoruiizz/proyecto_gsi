# Product Backlog

> Mantener este backlog priorizado y refinado en cada Sprint Planning.
> Nomenclatura: `PB-XXX` para tareas técnicas/infraestructura, `HU-XXX` para historias de usuario (ver [convenciones REM/REMUS](../../requisitos/rem-remus/README.md)). Estimación en Puntos de Historia, escala Fibonacci (1, 2, 3, 5, 8).
> Trazabilidad de cada historia con su requisito funcional en [REM-CADUS.md](../../requisitos/rem-remus/REM-CADUS.md).

## Tareas de infraestructura (Sprint-00)

| ID | Ítem | Sistema | Prioridad | SP | Estado | Sprint | Dependencias | Responsable |
|---|---|---|---|---:|---|---|---|---|
| PB-001 | Definir estructura base del repositorio | Requisitos/SCRUM | Alta | 3 | Hecho | Sprint-00 | Ninguna | `[Nombre]` |
| PB-002 | Configurar CMS local WordPress en XAMPP | CMS | Alta | 5 | Pendiente | Sprint-01 | PB-001 | `[Nombre]` |
| PB-003 | Diseñar estructura documental inicial en SharePoint | DMS | Media | 5 | Pendiente | Sprint-01 | PB-001 | `[Nombre]` |
| PB-004 | Configurar equipo y canales en Teams | Colaboración | Media | 3 | Pendiente | Sprint-01 | PB-001 | `[Nombre]` |

## Historias de usuario

| ID | Historia de usuario | Requisito(s) | Prioridad | SP | Estado | Sprint | Responsable |
|---|---|---|---|---:|---|---|---|
| HU-01 | Como Ejecutiva, quiero publicar noticias categorizadas (Becas, Movilidad, Normativa, Eventos) para informar a los estudiantes. | RF-01 | Alta | 5 | Pendiente | Sprint-02 | `[Nombre]` |
| HU-02 | Como Estudiante, quiero filtrar y buscar noticias por categoría, fecha y palabra clave. | RF-02 | Media | 3 | Pendiente | Sprint-02 | `[Nombre]` |
| HU-03 | Como Ejecutiva, quiero subir actas de pleno en PDF y enviarlas a aprobación antes de publicarlas. | RF-03, RF-05, RN-01 | Alta | 5 | Pendiente | Sprint-02 | `[Nombre]` |
| HU-04 | Como Estudiante, quiero descargar actas y normativas en PDF organizadas por fecha y tipo. | RF-03, RF-04 | Alta | 3 | Pendiente | Sprint-02 | `[Nombre]` |
| HU-05 | Como Estudiante, quiero consultar el directorio de delegaciones por Facultad/Escuela. | RF-06 | Alta | 5 | Pendiente | Sprint-03 | `[Nombre]` |
| HU-06 | Como Delegado, quiero mantener actualizada la ficha de contacto y horario de mi delegación. | RF-07, RN-04 | Media | 3 | Pendiente | Sprint-03 | `[Nombre]` |
| HU-07 | Como Estudiante, quiero enviar una consulta o reclamación académica desde un buzón digital y recibir un código de ticket. | RF-08, RF-09, RN-02 | Alta | 8 | Pendiente | Sprint-03 | `[Nombre]` |
| HU-08 | Como Estudiante, quiero hacer seguimiento del estado de mi consulta con el código de ticket. | RF-09 | Alta | 5 | Pendiente | Sprint-03 | `[Nombre]` |
| HU-09 | Como Ejecutiva, quiero gestionar y responder tickets desde un panel, respetando la privacidad de las reclamaciones. | RF-10, RN-03 | Alta | 8 | Pendiente | Sprint-04 | `[Nombre]` |
| HU-10 | Como Estudiante, quiero consultar el calendario de asambleas y eventos del CADUS. | RF-11 | Media | 3 | Pendiente | Sprint-04 | `[Nombre]` |
| HU-11 | Como Ejecutiva, quiero publicar convocatorias de votación vinculadas a una asamblea del calendario. | RF-12, RN-05 | Media | 5 | Pendiente | Sprint-04 | `[Nombre]` |
| HU-12 | Como Estudiante, quiero solicitar mediación estudiantil mediante un formulario. | RF-13 | Media | 5 | Pendiente | Sprint-04 | `[Nombre]` |
| HU-13 | Como Administrador, quiero gestionar roles y permisos de usuario (Anónimo, Estudiante, Delegado, Ejecutiva, Administrador). | RF-14 | Alta | 5 | Pendiente | Sprint-01 | `[Nombre]` |
| HU-14 | Como Usuario, quiero navegar el portal desde el móvil sin pérdida de funcionalidad. | RNF-02 | Alta | 8 | Pendiente | Sprint-05 | `[Nombre]` |
| HU-15 | Como Usuario, quiero que el sitio cumpla el nivel de accesibilidad WCAG 2.1 AA. | RNF-03 | Media | 8 | Pendiente | Sprint-05 | `[Nombre]` |
| HU-16 | Como Administrador, quiero buscar y filtrar contenido del panel por palabra clave y fecha. | RF-02, RF-15 | Media | 5 | Pendiente | Sprint-05 | `[Nombre]` |
| HU-17 | Como Administrador, quiero que los formularios estén protegidos frente a spam e inyección de datos. | RNF-04, RNF-08 | Alta | 5 | Pendiente | Sprint-05 | `[Nombre]` |
| HU-18 | Como Equipo, quiero configurar el tema base y la identidad visual institucional del CADUS. | RNF-02 | Alta | 5 | Pendiente | Sprint-01 | `[Nombre]` |
| HU-19 | Como Administrador, quiero un panel de administración de contenidos (CRUD noticias/actas/delegaciones) restringido por rol. | RF-15 | Alta | 8 | Pendiente | Sprint-02 | `[Nombre]` |
| HU-20 | Como Equipo, quiero optimizar el rendimiento (caché, imágenes) antes de la entrega final. | RNF-01, RNF-06 | Media | 5 | Pendiente | Sprint-06 | `[Nombre]` |

## Roadmap por versiones

### V1 — Estructura base, tema y gestión de contenidos
- **Sprint-01** (estructura base, tema, roles): PB-002, PB-003, PB-004, HU-13, HU-18
- **Sprint-02** (gestión de contenidos): HU-01, HU-02, HU-03, HU-04, HU-19
- **Sprint-03** (directorio y buzón de atención): HU-05, HU-06, HU-07, HU-08

### V2 — Participación, optimización, seguridad y entrega
- **Sprint-04** (participación estudiantil): HU-09, HU-10, HU-11, HU-12
- **Sprint-05** (optimización, filtros, accesibilidad y seguridad): HU-14, HU-15, HU-16, HU-17
- **Sprint-06** (entrega final): HU-20 + pruebas de aceptación, revisión de DoD y documentación final

## Reglas mínimas
- Priorizar por valor para cliente y riesgo.
- Cada ítem debe vincularse a una issue y sprint.
- Revisar estimaciones y estado en cada Daily/Review.
