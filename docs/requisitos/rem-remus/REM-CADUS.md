# Especificación de Requisitos REM/REMUS — Portal CADUS

**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla)
**Sistema:** Portal web institucional (`www.cadus.us.es`) — CMS WordPress
**Versión del documento:** 2.0 (revisión del Sprint 2, 24/10/2026) · en REMUS: `CADUS.rem` versión 2.0
**Estado:** Pendiente de validación con el cliente. La entrevista con el CADUS (E2-09) no se ha realizado en el Sprint 2 y pasa al Sprint 3.

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
| RF-10 | El sistema debe ofrecer un panel de gestión y respuesta de tickets para la Ejecutiva, con filtros por estado y por tipo y aviso por correo al estudiante cuando hay respuesta (el aviso no incluye el contenido). | Ejecutiva |
| RF-11 | El sistema debe mostrar un calendario de asambleas, eventos y votaciones estudiantiles. | Usuario Anónimo, Estudiante |
| RF-12 | El sistema debe permitir publicar convocatorias de votación vinculadas a una asamblea del calendario, con apertura y cierre; solo se vota mientras está abierta. | Ejecutiva |
| RF-13 | El sistema debe ofrecer un formulario de solicitud de mediación estudiantil que entregue una referencia (MED-AAAA-NNNNN); la Ejecutiva gestiona su estado (pendiente, en proceso, cerrada). | Estudiante, Ejecutiva |
| RF-14 | El sistema debe gestionar roles y permisos diferenciados (Anónimo, Estudiante, Delegado, Ejecutiva, Administrador), con cuentas institucionales: una del CADUS y una por delegación. | Administrador |
| RF-15 | El sistema debe ofrecer un panel de administración de contenidos (noticias, actas, delegaciones, tickets, mediaciones, eventos y votaciones) restringido por rol, con solo los menús de cada rol y un escritorio de accesos directos. | Administrador, Ejecutiva, Delegado |

---

## 3. Requisitos de información (RI-01 a RI-08)

Modelo conceptual de datos mínimo que debe soportar el CMS:

| ID | Entidad | Atributos principales |
|---|---|---|
| RI-01 | **Entrada de noticia** | título, cuerpo, categoría, fecha de publicación, autor, estado (borrador/publicada) |
| RI-02 | **Acta/Documento** | tipo (acta/normativa), fecha, archivo PDF, estado de aprobación, pleno asociado |
| RI-03 | **Delegación** | Facultad/Escuela, delegado responsable, contacto, horario de atención |
| RI-04 | **Consulta/Ticket** | código de seguimiento (CAD-AAAA-NNNNN), remitente, tipo (consulta o reclamación académica), asunto, descripción, estado, historial de respuestas, fecha del último aviso, nivel de confidencialidad |
| RI-05 | **Categoría** | nombre, tipo de contenido asociado (noticia o documento) |
| RI-06 | **Usuario/Rol** | nombre de la cuenta institucional, correo institucional del órgano, rol asignado, delegación asociada (si aplica) |
| RI-07 | **Solicitud de mediación** | referencia, solicitante, correo `@alum.us.es`, Facultad/Escuela, descripción, consentimiento RGPD, fecha, estado |
| RI-08 | **Convocatoria de votación** | título, descripción, asamblea vinculada, apertura, cierre, papeleta (encuesta asociada) |

---

## 4. Reglas de negocio (RN-01 a RN-05)

| ID | Regla |
|---|---|
| RN-01 | Toda acta o normativa requiere aprobación de un miembro de la Ejecutiva antes de publicarse (ver RF-05). |
| RN-02 | Solo se aceptan consultas, reclamaciones y solicitudes de mediación enviadas desde correo corporativo `@alum.us.es`. |
| RN-03 | Las reclamaciones académicas y las solicitudes de mediación se tratan con privacidad estricta: solo son visibles para el remitente y la Ejecutiva; no aparecen en la web pública, el buscador ni la API, y los avisos por correo no incluyen su contenido. |
| RN-04 | Cada ficha de delegación solo puede ser editada por la cuenta de su delegación o por un Administrador. |
| RN-05 | Toda votación publicada en el calendario debe estar vinculada a una convocatoria de asamblea previamente creada. |

---

## 5. Requisitos no funcionales (RNF-01 a RNF-08)

| ID | Requisito |
|---|---|
| RNF-01 | **Rendimiento:** tiempo de carga de página inferior a 3 s en condiciones estándar de red del campus. |
| RNF-02 | **Usabilidad móvil:** diseño responsive, funcional en dispositivos móviles y tablets. |
| RNF-03 | **Accesibilidad:** cumplimiento de WCAG 2.1 nivel AA. |
| RNF-04 | **Seguridad en formularios:** validación y sanitización de entradas, protección frente a spam e inyección. |
| RNF-05 | **Compatibilidad técnica:** PHP 8.x y MySQL 8.x sobre servidor Apache local (WampServer; compatible con XAMPP). |
| RNF-06 | **Disponibilidad:** estabilidad del entorno durante periodos críticos (matrícula, asambleas, votaciones). |
| RNF-07 | **Mantenibilidad:** configuración y código documentados para facilitar el relevo entre cursos académicos del CADUS. |
| RNF-08 | **Privacidad:** tratamiento de datos de consultas, reclamaciones y mediaciones conforme a RGPD y LOPDGDD, con consentimiento en cada formulario y aviso de privacidad público. Plazo de conservación pendiente de validar con el CADUS. |

---

## 6. Restricciones del proyecto (RC-01 a RC-03)

Restricciones sobre el entorno de desarrollo y la gestión de la configuración (en REMUS, requisitos de restricción).

| ID | Restricción |
|---|---|
| RC-01 | **Entorno de desarrollo compartido con Tailscale:** WordPress y su base de datos MySQL (`bd_cadus`) se alojan en un único servidor local (WampServer) en el equipo de un integrante. El resto del equipo accede a él mediante **Tailscale** (VPN privada), de modo que los 5 integrantes trabajan a la vez sobre la misma instancia de WordPress y la misma base de datos. El acceso web se limita a la red de Tailscale, cada integrante usa su propia cuenta de WordPress (rol Administrador) y el puerto de la base de datos no se expone. El servidor solo está disponible mientras el equipo anfitrión esté encendido. |
| RC-02 | **Gestión de configuración con GitHub:** todo el contenido en forma de archivo (código del tema y plugins, documentación, artefactos SCRUM, REM/REMUS, maquetas) se versiona en el repositorio GitHub del proyecto. No se versionan `wp-config.php`, `wp-content/uploads/` ni credenciales. Los volcados de la base de datos (`cms-wordpress/backup-db/`) se mantienen como copia de seguridad y para la entrega, no como mecanismo de sincronización entre integrantes. |
| RC-03 | **Coordinación del equipo con Discord:** el equipo se coordina en un servidor de Discord (*GSI - CADUS*) organizado en categorías: INFO (anuncios, entorno y recursos), SCRUM (daily, sprint-review y retrospectiva), DESARROLLO (un canal por área: infra-y-bd, portada, institucional-y-normativa, delegaciones y buzon-y-faq, además de github y avisos-servidor) y VOZ (Sala de trabajo y Daily) para las reuniones y el trabajo a distancia. |

---

## 7. Revisión del Sprint 2 (E2-15)

La revisión prevista tras la entrevista con el CADUS (E2-09) no ha podido hacerse porque la entrevista no se ha realizado. En su lugar, el REM se ha actualizado con las decisiones tomadas al construir el Sprint 2, y se marca qué falta validar con el cliente.

**Cambios incorporados (versión 2.0):**

- RF-10 · HU-09a: la gestión de tickets se hace con el módulo propio del buzón (no con SupportCandy), con filtros por estado y tipo y aviso por correo al estudiante sin el contenido de la respuesta.
- RF-12 · RN-05 · HU-11: las votaciones tienen apertura y cierre y siempre van vinculadas a una asamblea del calendario.
- RF-13 · HU-12: la mediación entrega una referencia MED-AAAA-NNNNN y la Ejecutiva gestiona su estado; RN-02 y RN-03 se amplían a las solicitudes de mediación.
- RF-14 · RN-04 · E2-01: cuentas institucionales (una del CADUS y una por delegación) en lugar de cuentas personales.
- RF-15 · HU-19a/b: menús de administración por rol y escritorio con accesos directos.
- RNF-08 · E2-16: aviso de privacidad público y consentimiento en cada formulario.
- Requisitos de información: datos nuevos del ticket, la mediación, la votación y las cuentas.

**Pendiente de validar con el CADUS (entrevista E2-09, Sprint 3):**

- Plazo de conservación de los datos del buzón y de la mediación (RNF-08).
- Lista de cuentas reales de las delegaciones y del CADUS (RF-14).
- Prioridades del backlog para el Sprint 3 y conformidad con los requisitos de esta versión.
- Logotipo e identidad visual oficiales (UI-01).

El proyecto REMUS se regenera desde [`scripts/remus/cadus_data.json`](../../../scripts/remus/cadus_data.json) con `scripts/remus/build_rem.ps1`; la hoja [`carga-remus.md`](carga-remus.md) recoge su contenido.

## 8. Trazabilidad

La trazabilidad HU (historia de usuario) ↔ RF/RN/RNF ↔ Sprint se mantiene en el [Product Backlog](../../scrum/backlog/product-backlog.md). Cada historia de usuario debe referenciar el/los requisito(s) que implementa.
