# Especificación de Requisitos REM/REMUS — Portal CADUS

**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla)
**Sistema:** Portal web institucional (`www.cadus.us.es`) — CMS WordPress
**Versión del documento:** 0.1 (borrador inicial para Sprint-00/01)
**Estado:** Pendiente de validación con el cliente

> Este documento sigue la nomenclatura acordada en [README.md](README.md) de esta carpeta. La trazabilidad HU ↔ RF ↔ Sprint se completa en [`docs/scrum/backlog/product-backlog.md`](../../scrum/backlog/product-backlog.md).

---

## 1. Actores del sistema

| Actor | Descripción |
|---|---|
| **Usuario Anónimo** | Visitante sin autenticar. Accede a contenido público (noticias, actas publicadas, directorio, calendario). |
| **Estudiante US** | Usuario autenticado con correo institucional (`@alum.us.es`). Puede enviar consultas/reclamaciones y solicitudes de mediación. |
| **Representante/Delegado de Centro** | Estudiante con responsabilidad de delegación. Mantiene actualizada la ficha de su Facultad/Escuela en el directorio. |
| **Miembro de la Ejecutiva del CADUS** | Aprueba y publica actas/normativas, gestiona el buzón de consultas y las convocatorias de asamblea/votación. |
| **Administrador Web** | Gestiona usuarios, roles, categorías y configuración técnica del portal. |

---

## 2. Requisitos funcionales (RF-01 a RF-15)

| ID | Requisito | Actor(es) principal(es) |
|---|---|---|
| RF-01 | El sistema debe permitir publicar noticias/comunicados categorizados por área (Becas, Movilidad, Normativa, Eventos). | Ejecutiva, Administrador |
| RF-02 | El sistema debe permitir filtrar y buscar noticias por categoría, fecha y palabra clave. | Usuario Anónimo, Estudiante |
| RF-03 | El sistema debe ofrecer un repositorio de actas de plenos descargables en PDF. | Ejecutiva |
| RF-04 | El sistema debe ofrecer un repositorio de normativas y reglamentos descargables en PDF. | Ejecutiva |
| RF-05 | El sistema debe requerir aprobación previa de un miembro de la Ejecutiva antes de publicar cualquier acta o normativa. | Ejecutiva |
| RF-06 | El sistema debe mostrar un directorio interactivo de Delegaciones de Alumnos por Facultad/Escuela. | Usuario Anónimo, Estudiante |
| RF-07 | El sistema debe permitir gestionar la ficha de cada delegación (contacto, horario de atención, enlaces). | Delegado, Administrador |
| RF-08 | El sistema debe ofrecer un buzón digital de consultas y reclamaciones académicas. | Estudiante |
| RF-09 | El sistema debe generar un código/ticket de seguimiento único para cada consulta enviada. | Estudiante |
| RF-10 | El sistema debe ofrecer un panel de gestión y respuesta de tickets para la Ejecutiva. | Ejecutiva |
| RF-11 | El sistema debe mostrar un calendario de asambleas, eventos y votaciones estudiantiles. | Usuario Anónimo, Estudiante |
| RF-12 | El sistema debe permitir publicar convocatorias de votación vinculadas a una asamblea del calendario. | Ejecutiva |
| RF-13 | El sistema debe ofrecer un formulario de solicitud de mediación estudiantil. | Estudiante |
| RF-14 | El sistema debe gestionar roles y permisos diferenciados (Anónimo, Estudiante, Delegado, Ejecutiva, Administrador). | Administrador |
| RF-15 | El sistema debe ofrecer un panel de administración de contenidos (CRUD de noticias, actas y delegaciones) restringido por rol. | Administrador, Ejecutiva |

---

## 3. Requisitos de información (RI-01 a RI-06)

Modelo conceptual de datos mínimo que debe soportar el CMS:

| ID | Entidad | Atributos principales |
|---|---|---|
| RI-01 | **Entrada de noticia** | título, cuerpo, categoría, fecha de publicación, autor, estado (borrador/publicada) |
| RI-02 | **Acta/Documento** | tipo (acta/normativa), fecha, archivo PDF, estado de aprobación, pleno asociado |
| RI-03 | **Delegación** | Facultad/Escuela, delegado responsable, contacto, horario de atención |
| RI-04 | **Consulta/Ticket** | código de seguimiento, remitente, asunto, estado, historial de respuestas, nivel de confidencialidad |
| RI-05 | **Categoría** | nombre, tipo de contenido asociado (noticia o documento) |
| RI-06 | **Usuario/Rol** | nombre, correo institucional, rol asignado, delegación asociada (si aplica) |

---

## 4. Reglas de negocio (RN-01 a RN-05)

| ID | Regla |
|---|---|
| RN-01 | Toda acta o normativa requiere aprobación de un miembro de la Ejecutiva antes de publicarse (ver RF-05). |
| RN-02 | Solo se aceptan consultas y reclamaciones enviadas desde correo corporativo `@alum.us.es`. |
| RN-03 | Las reclamaciones académicas se tratan con privacidad estricta: solo son visibles para el remitente y la Ejecutiva. |
| RN-04 | Cada ficha de delegación solo puede ser editada por su delegado asignado o por un Administrador. |
| RN-05 | Toda votación publicada en el calendario debe estar vinculada a una convocatoria de asamblea previamente creada. |

---

## 5. Requisitos no funcionales (RNF-01 a RNF-08)

| ID | Requisito |
|---|---|
| RNF-01 | **Rendimiento:** tiempo de carga de página inferior a 3 s en condiciones estándar de red del campus. |
| RNF-02 | **Usabilidad móvil:** diseño responsive, funcional en dispositivos móviles y tablets. |
| RNF-03 | **Accesibilidad:** cumplimiento de WCAG 2.1 nivel AA. |
| RNF-04 | **Seguridad en formularios:** validación y sanitización de entradas, protección frente a spam e inyección. |
| RNF-05 | **Compatibilidad técnica:** PHP 8.x y MySQL 8.x sobre entorno XAMPP. |
| RNF-06 | **Disponibilidad:** estabilidad del entorno durante periodos críticos (matrícula, asambleas, votaciones). |
| RNF-07 | **Mantenibilidad:** configuración y código documentados para facilitar el relevo entre cursos académicos del CADUS. |
| RNF-08 | **Privacidad:** tratamiento de datos de consultas/reclamaciones conforme a RGPD. |

---

## 6. Trazabilidad

La trazabilidad HU (historia de usuario) ↔ RF/RN/RNF ↔ Sprint se mantiene en el [Product Backlog](../../scrum/backlog/product-backlog.md). Cada historia de usuario debe referenciar el/los requisito(s) que implementa.
