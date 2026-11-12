# Especificación de Requisitos REM/REMUS — Portal CADUS

**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla)
**Sistema:** Portal web institucional (`www.cadus.us.es`) — CMS WordPress
**Versión del documento:** 2.3 (revisión del Sprint 3, 12/11/2026) · en REMUS: `CADUS.rem` versión 2.3
**Estado:** Revisado con las respuestas de la entrevista con el CADUS del 26/10/2026 ([`entrevista-cliente.md`](../../cliente/entrevista-cliente.md)). El plazo de respuesta de los tickets se aclaró con el CADUS el 09/11/2026. Queda por aclarar la lista de delegados.

> Este documento sigue la nomenclatura acordada en [README.md](README.md) de esta carpeta. La trazabilidad HU ↔ RF ↔ Sprint se completa en [`docs/scrum/backlog/product-backlog.md`](../../scrum/backlog/product-backlog.md).

---

## 1. Actores del sistema

| Actor | Descripción |
|---|---|
| **Usuario Anónimo** | Visitante sin autenticar. Accede a contenido público (noticias, actas publicadas, directorio, calendario). |
| **Estudiante US** | Estudiante de la Universidad de Sevilla con correo institucional (`@alum.us.es`). Puede enviar consultas, reclamaciones y solicitudes de mediación sin necesidad de cuenta en el portal. |
| **Representante/Delegado de Centro** | Estudiante con responsabilidad de delegación. Mantiene actualizada la ficha de su Facultad/Escuela en el directorio y puede dar de alta a su sucesor cuando se da de baja. |
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
| RF-08 | El sistema debe ofrecer un buzón digital de consultas y reclamaciones académicas que solo pida los datos mínimos del estudiante: nombre y apellidos, Facultad o Escuela y correo de la US. | Estudiante |
| RF-09 | El sistema debe generar un código/ticket de seguimiento único para cada consulta enviada. | Estudiante |
| RF-10 | El sistema debe ofrecer un panel de gestión y respuesta de tickets para la Ejecutiva, con filtros por estado y por tipo, búsqueda por código o por asunto (sin mirar la descripción ni los datos del estudiante) y aviso por correo al estudiante cuando hay respuesta (el aviso no incluye el contenido). El aviso de cada ticket nuevo llega al correo de la cuenta del CADUS (dcadus@us.es), solo con el código, el tipo, la fecha y el enlace al panel. | Ejecutiva |
| RF-11 | El sistema debe mostrar un calendario de asambleas, cursos y eventos del CADUS, y los anuncios de votación, con los próximos eventos en la página principal. | Usuario Anónimo, Estudiante |
| RF-12 | El sistema debe permitir publicar convocatorias de votación vinculadas a una asamblea del calendario, con apertura y cierre, para informar de que se va a realizar la votación. Las votaciones son presenciales (solo votan los delegados, un voto por delegación): el portal no recoge votos ni publica resultados. | Ejecutiva |
| RF-13 | El sistema debe ofrecer un formulario de solicitud de mediación estudiantil que entregue una referencia (MED-AAAA-NNNNN); la Ejecutiva gestiona su estado (pendiente, en proceso, cerrada). | Estudiante, Ejecutiva |
| RF-14 | El sistema debe gestionar roles y permisos diferenciados: anónimo, estudiante, delegado, miembro de la Ejecutiva y administrador, con una cuenta única del CADUS (dcadus@us.es) que usan todos los miembros de la Ejecutiva y desde la que se da acceso a los delegados, y una cuenta por delegación con el correo institucional de la delegación (no el correo personal del delegado). El relevo lo hace el delegado saliente o cualquier miembro de la Ejecutiva, con efecto inmediato: la cuenta no cambia, se le pone una contraseña nueva y se cierran las sesiones abiertas, de modo que el equipo anterior pierde el acceso y la ficha sigue en la misma cuenta; queda una sola cuenta activa por delegación (hay 27 delegaciones y la cuenta representa a la delegación, no a la persona). | Administrador, Ejecutiva, Delegado |
| RF-15 | El sistema debe ofrecer un panel de administración de contenidos (noticias, actas, delegaciones, tickets, mediaciones, eventos y votaciones) restringido por rol, con solo los menús de cada rol y un escritorio de accesos directos. | Administrador, Ejecutiva, Delegado |

---

## 3. Requisitos de información (IR-01 a IR-09)

Modelo conceptual de datos mínimo que debe soportar el CMS (los mismos códigos que en REMUS):

| ID | Entidad | Atributos principales |
|---|---|---|
| IR-01 | **Página principal** | banner institucional, comunicados recientes (titular, resumen y categoría), accesos destacados al directorio y al buzón, próximas asambleas, eventos y votaciones |
| IR-02 | **Menús** | Inicio, Qué es el CADUS, Gobierno y estatutos, Actas y normativa, Noticias y comunicados, Delegaciones de alumnos, Calendario, Atención al estudiante (buzón, mediación y preguntas frecuentes) |
| IR-03 | **Noticia y comunicado** | título, cuerpo, categoría (Becas, Movilidad, Normativa o Eventos), fecha de publicación, autor, estado (borrador/publicada) |
| IR-04 | **Acta/Documento** | tipo (acta/normativa), fecha, archivo PDF, estado de aprobación, pleno asociado |
| IR-05 | **Delegación** | Facultad/Escuela, delegado responsable, contacto, horario de atención, enlaces de interés |
| IR-06 | **Consulta/Ticket** | código de seguimiento (CAD-AAAA-NNNNN), remitente (nombre y apellidos, Facultad o Escuela y correo `@alum.us.es`: los datos mínimos), tipo (consulta o reclamación académica), asunto, descripción, consentimiento RGPD, estado, historial de respuestas, fecha del aviso a la cuenta del CADUS y del último aviso al estudiante, nivel de confidencialidad |
| IR-07 | **Calendario y votaciones** | título, tipo (asamblea, curso, evento o votación), fecha y hora, lugar, descripción, asamblea a la que se vincula (votaciones), apertura y cierre de la votación |
| IR-08 | **Solicitud de mediación** | referencia (MED-AAAA-NNNNN), solicitante, correo `@alum.us.es`, Facultad/Escuela, descripción, consentimiento RGPD, fecha, estado (pendiente, en proceso o cerrada) |
| IR-09 | **Usuario/Rol** | nombre de la cuenta (la única del CADUS o la de un delegado), correo de acceso (dcadus@us.es o el correo de alumno del delegado), rol asignado, delegación asociada (si aplica) |

Las categorías de noticias y de documentos son un atributo de IR-03 e IR-04, no una entidad aparte.

## 3 bis. Requisitos de interfaz (UI-01 a UI-10) y casos de uso (UC-01 a UC-04)

| ID | Requisito de interfaz | Historias |
|---|---|---|
| UI-01 | Diseño gráfico basado en la identidad visual del CADUS (colores, logotipo y tipografía), adaptado a móviles y tablets | HU-18 · RNF-02 |
| UI-02 | Página principal con banner, comunicados recientes por categoría, accesos al directorio y al buzón y próximas asambleas, eventos y votaciones | HU-01 · HU-02 |
| UI-03 | Directorio agrupado por Facultad o Escuela, con la ficha de cada delegación | HU-05 · HU-06 |
| UI-04 | Buzón de consultas: formulario con los datos mínimos, seguimiento por código, preguntas frecuentes y aviso de privacidad; todos los campos con etiqueta visible y ayuda asociada | HU-07 · HU-08 · E2-16 · HU-15b · E3-08 |
| UI-05 | Ficha de acta o normativa con descarga en PDF | HU-03 · HU-04 |
| UI-06 | Calendario de asambleas y eventos (mes y lista) y convocatorias de votación con apertura y cierre, vinculadas a su asamblea | HU-10 · HU-11 |
| UI-07 | Solicitud de mediación con consentimiento RGPD y confirmación con la referencia MED-AAAA-NNNNN, sin repetir los datos | HU-12 |
| UI-08 | Panel de administración con solo los menús de cada rol y un escritorio con accesos directos | HU-19a · HU-19b |
| UI-09 | Acceso al portal: apartado «Acceder» en el menú que lleva a un inicio de sesión dentro del portal y, una vez dentro, «Gestión» y «Salir» según el rol | HU-24 · RF-14 |
| UI-10 | Gestión desde el portal: formularios sencillos para crear noticias, eventos del calendario, actas y normativas con su PDF y gestionar las delegaciones; cada delegación edita solo su ficha | HU-24 · RF-15 |

| Caso de uso | Actor principal | Resumen |
|---|---|---|
| UC-01 Enviar consulta o reclamación | Estudiante US | Se piden los datos mínimos, se verifica el correo `@alum.us.es` (RN-02) y que el envío no es automático (RNF-04), se registra el ticket privado (RN-03), se avisa a la cuenta del CADUS sin datos del estudiante y se entrega el código de seguimiento |
| UC-02 Aprobar y publicar un acta | Miembro de la Ejecutiva | El acta pasa de borrador a pendiente y a aprobada; solo entonces se publica y se puede descargar |
| UC-03 Convocar una votación | Miembro de la Ejecutiva | Se crea la convocatoria vinculada a una asamblea del calendario, con apertura y cierre (RN-05); el portal solo la anuncia, porque la votación es presencial |
| UC-04 Solicitar una mediación estudiantil | Estudiante US | Se verifica el correo, se registra la solicitud como privada (RN-03) y se entrega la referencia; la Ejecutiva gestiona su estado |

---

## 4. Reglas de negocio (RN-01 a RN-05)

| ID | Regla |
|---|---|
| RN-01 | Todo contenido pasa por la Ejecutiva antes de publicarse; en particular, toda acta o normativa requiere la aprobación de un miembro de la Ejecutiva (ver RF-05). |
| RN-02 | Solo se aceptan consultas, reclamaciones y solicitudes de mediación enviadas desde correo corporativo `@alum.us.es`. |
| RN-03 | Todas las consultas, reclamaciones y solicitudes de mediación se tratan con total privacidad: solo son visibles para el remitente y la Ejecutiva; no aparecen en la web pública, el buscador ni la API, y los avisos por correo no incluyen su contenido. |
| RN-04 | Cada ficha de delegación solo puede ser editada por la cuenta de esa delegación o por la cuenta del CADUS (administrador). |
| RN-05 | Toda votación publicada en el calendario debe estar vinculada a una convocatoria de asamblea previamente creada. |

---

## 5. Requisitos no funcionales (RNF-01 a RNF-09)

| ID | Requisito |
|---|---|
| RNF-01 | **Rendimiento:** tiempo de carga de página inferior a 3 s en condiciones estándar de red del campus. |
| RNF-02 | **Usabilidad móvil:** diseño responsive, funcional en móviles, tablets y ordenadores. |
| RNF-03 | **Accesibilidad:** cumplimiento de WCAG 2.1 nivel AA y de las pautas del Diseño Universal para el Aprendizaje (DUA), con atención a las personas ciegas y daltónicas: campos de formulario con etiqueta y ayuda asociadas, textos alternativos, jerarquía de encabezados sin saltos, mensajes de error anunciados y uso completo con teclado y con lector de pantalla. |
| RNF-04 | **Seguridad en formularios:** validación y sanitización de entradas, protección frente a spam e inyección. El buzón y la mediación exigen un campo trampa oculto (honeypot) vacío y un nonce válido, y admiten como máximo 10 envíos por dirección IP cada 15 minutos. |
| RNF-05 | **Compatibilidad técnica:** PHP 8.x y MySQL 8.x sobre servidor Apache local (WampServer; compatible con XAMPP). |
| RNF-06 | **Disponibilidad:** estabilidad del entorno durante periodos críticos (matrícula, asambleas, votaciones). |
| RNF-07 | **Mantenibilidad:** configuración y código documentados para facilitar el relevo entre cursos académicos del CADUS. |
| RNF-08 | **Privacidad:** tratamiento de datos de consultas, reclamaciones y mediaciones conforme a RGPD y LOPDGDD, con consentimiento en cada formulario y aviso de privacidad público. Los tickets y las mediaciones se conservan 2 años desde que se resuelven y después se borran o anonimizan; solo se piden nombre y apellidos, facultad y correo de la US. La Ejecutiva responde en un máximo de 4 días hábiles, contados desde que revisa el ticket (aclarado con el CADUS el 09/11/2026); el plazo se publica en el buzón, en la confirmación del ticket y en la FAQ. |
| RNF-09 | **Facilidad de uso:** un estudiante debe poder completar en menos de un minuto cada una de estas tres operaciones: crear un ticket en el buzón, consultar el calendario y consultar las asambleas, los eventos y las últimas noticias. |

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
- RF-14 · RN-04 · E2-01: Una cuenta única del CADUS (dcadus@us.es) que usan todos los miembros de la Ejecutiva y desde la que se da acceso a los delegados, y una cuenta por delegación con el correo institucional de la delegación (no el correo personal del delegado).
- RF-15 · HU-19a/b: menús de administración por rol y escritorio con accesos directos.
- RNF-08 · E2-16: aviso de privacidad público y consentimiento en cada formulario.
- Requisitos de información: datos nuevos del ticket, la mediación, la votación y las cuentas; se usan en todo el documento los códigos IR de REMUS.
- Requisitos de interfaz UI-06 (calendario y votaciones), UI-07 (mediación) y UI-08 (panel de administración por rol), y casos de uso UC-03 (convocar una votación) y UC-04 (solicitar una mediación), con sus trazas.

## 7 bis. Revisión del Sprint 3 (E3-05)

La entrevista con el CADUS se hizo el 26/10/2026. La versión 2.1 recogió sus respuestas, la versión 2.2 añade lo construido en el Sprint 3 y la versión 2.3 publica el plazo de respuesta de los tickets.

**Cambios incorporados (versiones 2.1 a 2.3):**

- RN-03: la privacidad se amplía de las reclamaciones y las mediaciones a **todas** las consultas del buzón.
- RN-01: la aprobación de la Ejecutiva se amplía de las actas y la normativa a **todo** el contenido publicado.
- RNF-08 · HU-23: se cierra el plazo de conservación: 2 años desde que el ticket o la mediación se resuelven; después se borran o anonimizan.
- RF-08 · IR-06 · UI-04 · E3-08: el buzón pide los datos mínimos (nombre y apellidos, Facultad o Escuela y correo de la US).
- RF-10 · E3-08 · HU-16b: aviso de cada ticket nuevo a la cuenta del CADUS (dcadus@us.es) sin datos del estudiante, y búsqueda del panel por código o por asunto.
- RF-14 · RN-04 · HU-22: relevo de delegados (el delegado o un miembro de la Ejecutiva dan de alta al sucesor, con una sola cuenta activa por delegación).
- RF-11 · RF-12 · IR-07 · UC-03: el calendario incluye cursos; las votaciones son presenciales y el portal solo las anuncia (HU-21 cancelada).
- RNF-03 · HU-15: accesibilidad WCAG 2.1 AA con las pautas DUA y atención a personas ciegas y daltónicas.
- RNF-04 · HU-17a: campo trampa, nonce y límite de envíos en el buzón y la mediación.
- RNF-09 (nuevo) · E3-04: regla de las tres operaciones en menos de un minuto.
- RNF-08 · E3-08: plazo de respuesta aclarado el 09/11/2026 (máximo 4 días hábiles desde que la Ejecutiva revisa el ticket) y publicado en el buzón, la confirmación y la FAQ.

**Pendiente de aclarar con el CADUS:**

- Lista de delegados y de sus correos de alumno (RF-14).
- Logotipo e identidad visual oficiales (UI-01).

El proyecto REMUS se regenera desde [`scripts/remus/cadus_data.json`](../../../scripts/remus/cadus_data.json) con `scripts/remus/build_rem.ps1`; la hoja [`carga-remus.md`](carga-remus.md) recoge su contenido.

## 8. Trazabilidad

La trazabilidad HU (historia de usuario) ↔ RF/RN/RNF ↔ Sprint se mantiene en el [Product Backlog](../../scrum/backlog/product-backlog.md). Cada historia de usuario debe referenciar el/los requisito(s) que implementa.
