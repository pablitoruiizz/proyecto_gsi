# Hoja de carga para REMUS — Documento de Requisitos del Portal CADUS

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/cadus_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [CADUS.rem](CADUS.rem) (REMUS), versión 2.1, 2026-10-30. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

## 1. Organizaciones

| Nombre | Dirección |
|---|---|
| CADUS - Consejo de Alumnos de la Universidad de Sevilla | Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla |
| Equipo de proyecto GSI | Universidad de Sevilla - Gestión de Sistemas de Información (GSI) |

## 2. Personas

| Nombre | Rol |
|---|---|
| Delegación General del CADUS | Cliente y usuario (Ejecutiva del CADUS) |
| Pablo Ruiz Vidal | Product Owner y Dev Infraestructura |
| Joaquin Luna Canela | Scrum Master y Dev Portada |
| Miguel Angel Camacho Martin | Dev Sección Institucional y Normativa |
| Alvaro Martinez Ocaña | Dev Directorio de Delegaciones |
| Marcos-Paban Delgado Rodriguez | Dev Atención al Estudiante y Buzón |

## 3. Objetivos del sistema

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| OBJ-01 | Modernización del portal | rehacer el portal institucional del CADUS con un diseño actual, accesible y adaptado a dispositivos móviles | Vital |
| OBJ-02 | Información al estudiante | difundir noticias y comunicados clasificados por áreas: Becas, Movilidad, Normativa y Eventos | Vital |
| OBJ-03 | Transparencia institucional | publicar las actas de los plenos y las normativas, previa aprobación de la Ejecutiva | Vital |
| OBJ-04 | Visibilidad de las delegaciones | ofrecer un directorio de Delegaciones de Alumnos por Facultad o Escuela | Importante |
| OBJ-05 | Atención al estudiante | habilitar un buzón de consultas y reclamaciones con seguimiento y facilitar la solicitud de mediación estudiantil | Vital |
| OBJ-06 | Participación estudiantil | dar acceso al calendario de asambleas, eventos y votaciones estudiantiles | Importante |

## 4. Requisitos de información

| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |
|---|---|---|---|
| IR-01 | Página principal | a la página principal del portal, que deberá contener estos elementos: | Banner institucional del CADUS; Comunicados recientes: titular, resumen y categoría; Acceso destacado al directorio de delegaciones; Acceso destacado al buzón de consultas; Próximas asambleas, eventos y votaciones |
| IR-02 | Menús | a los menús del portal, que serán: | Inicio; Qué es el CADUS; Gobierno y estatutos; Actas y normativa; Noticias y comunicados; Delegaciones de alumnos; Calendario de asambleas, eventos y votaciones; Atención al estudiante: buzón de consultas, mediación y preguntas frecuentes |
| IR-03 | Noticias y comunicados | a las noticias y comunicados publicados por el CADUS, más específicamente: | Título; Cuerpo; Categoría: Becas, Movilidad, Normativa o Eventos; Fecha de publicación; Autor; Estado: borrador o publicada |
| IR-04 | Actas y normativas | a las actas de los plenos y a las normativas del CADUS, más específicamente: | Tipo: acta o normativa; Fecha; Archivo PDF; Estado de aprobación: borrador, pendiente o aprobada; Pleno asociado |
| IR-05 | Delegaciones de alumnos | a las delegaciones de alumnos de cada centro, más específicamente: | Facultad o Escuela; Delegado o representante responsable; Datos de contacto; Horario de atención; Enlaces de interés |
| IR-06 | Consultas y reclamaciones | a las consultas y reclamaciones enviadas por los estudiantes al buzón, más específicamente: | Código de seguimiento CAD-AAAA-NNNNN; Remitente con correo @alum.us.es; Tipo: consulta o reclamación académica; Asunto; Descripción; Estado: abierto, en proceso o cerrado; Historial de respuestas; Fecha del último aviso por correo al estudiante; Nivel de confidencialidad |
| IR-07 | Calendario | a las asambleas, eventos y votaciones estudiantiles, más específicamente: | Título; Tipo: asamblea, curso, evento o votación; Fecha y hora; Lugar; Descripción; Asamblea a la que se vincula (para las votaciones); Apertura y cierre de la votación |
| IR-08 | Solicitudes de mediación | a las solicitudes de mediación estudiantil, más específicamente: | Referencia de la solicitud (MED-AAAA-NNNNN); Solicitante; Correo @alum.us.es; Facultad o Escuela; Descripción del conflicto; Consentimiento RGPD; Fecha de la solicitud; Estado: pendiente, en proceso o cerrada |
| IR-09 | Usuarios y roles | a las personas con cuenta en el portal, más específicamente: | Nombre de la cuenta (la única del CADUS o la de un delegado); Correo de acceso: dcadus@us.es para la cuenta del CADUS o el correo de alumno (@alum.us.es) del delegado; Rol: estudiante, delegado, miembro de la Ejecutiva o administrador; Delegación asociada (si es delegado) |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-01 | Usuario anónimo | a los visitantes del portal que no han iniciado sesión y solo acceden a contenido público |
| ACT-02 | Estudiante US | a los estudiantes de la Universidad de Sevilla con correo institucional @alum.us.es |
| ACT-03 | Delegado de centro | a los representantes o delegados de alumnos responsables de la delegación de una Facultad o Escuela |
| ACT-04 | Miembro de la Ejecutiva | a los miembros de la Ejecutiva del CADUS que aprueban contenidos y atienden el buzón |
| ACT-05 | Administrador web | a las personas que gestionan usuarios, roles, categorías y la configuración técnica del portal |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|
| UI-01 | Diseño gráfico | basarse en la identidad visual del CADUS (colores, logotipo y tipografía institucionales) y adaptarse a móviles y tablets | HU-18 · RNF-02 |
| UI-02 | Página principal | contar con una página principal donde se coloquen estas secciones:  - Banner institucional del CADUS  - Comunicados recientes, clasificados por categoría  - Accesos destacados al directorio de delegaciones y al buzón de consultas  - Próximas asambleas, eventos y votaciones | HU-01 · HU-02 |
| UI-03 | Directorio de delegaciones | mostrar el directorio agrupado por Facultad o Escuela, con acceso a la ficha de cada delegación (contacto y horario de atención) | HU-05 · HU-06 |
| UI-04 | Buzón de consultas | ofrecer un formulario de consulta o reclamación, una pantalla de seguimiento mediante el código de ticket, una página de preguntas frecuentes y un aviso de privacidad enlazado desde los formularios | HU-07 · HU-08 · E2-16 |
| UI-05 | Ficha de acta o normativa | mostrar el detalle del documento (tipo, fecha y estado) y permitir su descarga en formato PDF | HU-03 · HU-04 |
| UI-06 | Calendario y votaciones | mostrar el calendario de asambleas y eventos (vista de mes y de lista) y las convocatorias de votación con su apertura y cierre, cada una vinculada a su asamblea | HU-10 · HU-11 |
| UI-07 | Solicitud de mediación | ofrecer un formulario de solicitud de mediación con consentimiento RGPD y una confirmación que entregue la referencia MED-AAAA-NNNNN sin mostrar los datos de la solicitud | HU-12 |
| UI-08 | Panel de administración por rol | mostrar a cada rol solo sus menús de administración y un escritorio con accesos directos a las tareas de su rol | HU-19a · HU-19b |

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-01 | Publicación de noticias categorizadas | permitir publicar noticias y comunicados clasificados por áreas: Becas, Movilidad, Normativa y Eventos | HU-01 | Vital |
| RF-02 | Búsqueda y filtrado de noticias | permitir filtrar y buscar las noticias por categoría, fecha y palabra clave | HU-02 · HU-16 | Importante |
| RF-03 | Repositorio de actas | ofrecer un repositorio de actas de plenos descargables en formato PDF | HU-03 · HU-04 | Vital |
| RF-04 | Repositorio de normativas | ofrecer un repositorio de normativas y reglamentos descargables en formato PDF | HU-04 | Vital |
| RF-05 | Aprobación previa de documentos | exigir la aprobación de un miembro de la Ejecutiva antes de publicar cualquier acta o normativa | HU-03 | Vital |
| RF-06 | Directorio de delegaciones | mostrar un directorio interactivo de Delegaciones de Alumnos por Facultad o Escuela | HU-05 | Vital |
| RF-07 | Ficha de delegación | permitir gestionar la ficha de cada delegación: contacto, horario de atención y enlaces | HU-06 | Importante |
| RF-08 | Buzón de consultas y reclamaciones | ofrecer un buzón digital de consultas y reclamaciones académicas | HU-07 | Vital |
| RF-09 | Código de seguimiento | generar un código de ticket único para cada consulta enviada y permitir su seguimiento | HU-07 · HU-08 | Vital |
| RF-10 | Gestión de tickets | ofrecer a la Ejecutiva un panel para gestionar y responder los tickets, filtrarlos por estado y por tipo, y avisar al estudiante por correo cuando hay una respuesta. El aviso solo incluye el código y el enlace de seguimiento, nunca el contenido. Además, el aviso de cada ticket nuevo llega al correo de la cuenta del CADUS (dcadus@us.es) | HU-09a (Sprint 2): módulo propio del buzón en lugar de SupportCandy | Vital |
| RF-11 | Calendario de asambleas y eventos | mostrar un calendario de asambleas, cursos y eventos del CADUS, y los anuncios de votación, con los próximos eventos en la página principal | HU-10 (Sprint 2) | Importante |
| RF-12 | Convocatorias de votación | permitir publicar convocatorias de votación vinculadas a una asamblea del calendario, con fecha y hora de apertura y de cierre, para informar de que se va a realizar la votación. Las votaciones son presenciales: solo votan los delegados, con un voto por delegación (sí, no o abstención), y el portal no recoge votos ni publica resultados | HU-11 (Sprint 2). HU-21 cancelada tras la entrevista | Importante |
| RF-13 | Solicitud de mediación | ofrecer un formulario de solicitud de mediación estudiantil que entregue al solicitante una referencia, y permitir a la Ejecutiva cambiar su estado (pendiente, en proceso o cerrada) | HU-12 (Sprint 2) | Importante |
| RF-14 | Roles y permisos | gestionar roles y permisos diferenciados: anónimo, estudiante, delegado, miembro de la Ejecutiva y administrador, con una cuenta única del CADUS (dcadus@us.es) que usan todos los miembros de la Ejecutiva y desde la que se da acceso a los delegados, y una cuenta por delegado con su correo de alumno (@alum.us.es). El delegado puede dar de alta a su sucesor cuando se da de baja, y cualquier miembro de la Ejecutiva también, con efecto inmediato: se revoca el acceso del anterior, se traspasa la ficha y queda una sola cuenta activa por delegación (hay 27 delegaciones y la cuenta representa a la delegación, no a la persona) | HU-13 · HU-22 · E2-01 (Sprint 2). Lista de delegados y sus correos pendiente de validar con el CADUS | Vital |
| RF-15 | Panel de administración | ofrecer un panel de administración de contenidos (noticias, actas, delegaciones, tickets, mediaciones, eventos y votaciones) restringido por rol, que muestre a cada rol solo sus menús y un escritorio con accesos directos | HU-19a · HU-19b (Sprint 2) | Vital |

## 8. Casos de uso

### UC-01 - Enviar consulta o reclamación

- **Evento disparador:** cuando un estudiante necesita plantear una consulta o reclamación académica
- **Precondición:** El estudiante dispone de un correo institucional @alum.us.es
- **Postcondición:** Se ha registrado el ticket y el estudiante conoce su código de seguimiento
- **Pasos:**
  1. El sistema solicita el asunto y el detalle de la consulta o reclamación
  2. Estudiante US indica el asunto y el detalle
  3. El sistema verifica que el correo pertenece al dominio @alum.us.es
  4. El sistema registra el ticket con su nivel de confidencialidad y genera su código de seguimiento único
  5. El sistema muestra al estudiante el código para consultar más adelante el estado de su ticket

### UC-02 - Aprobar y publicar un acta

- **Evento disparador:** tras la celebración de un pleno
- **Precondición:** El acta está subida en formato PDF en estado borrador
- **Postcondición:** El acta queda publicada y disponible para su descarga
- **Pasos:**
  1. Miembro de la Ejecutiva sube el acta en PDF y la envía a aprobación
  2. El sistema registra el acta como pendiente de aprobación
  3. Miembro de la Ejecutiva revisa el acta y la aprueba
  4. El sistema cambia el estado del acta a aprobada y la publica en el repositorio
  5. El sistema permite su descarga en PDF a cualquier visitante del portal

### UC-03 - Convocar una votación

- **Evento disparador:** cuando se convoca una asamblea en la que el alumnado debe votar
- **Precondición:** La asamblea está creada en el calendario
- **Postcondición:** La convocatoria queda publicada y solo se puede votar entre su apertura y su cierre
- **Pasos:**
  1. Miembro de la Ejecutiva crea la convocatoria de votación, la vincula a una asamblea e indica la apertura y el cierre
  2. El sistema comprueba que la asamblea existe en el calendario (RN-05)
  3. El sistema publica la convocatoria en el calendario y en la portada
  4. El sistema permite votar solo mientras la convocatoria está abierta

### UC-04 - Solicitar una mediación estudiantil

- **Evento disparador:** cuando un estudiante necesita la intervención del CADUS en un conflicto
- **Precondición:** El estudiante dispone de un correo institucional @alum.us.es
- **Postcondición:** La solicitud queda registrada en privado y el estudiante conoce su referencia
- **Pasos:**
  1. Estudiante US describe el conflicto, indica su Facultad o Escuela y acepta el tratamiento de datos
  2. El sistema verifica que el correo pertenece al dominio @alum.us.es (RN-02)
  3. El sistema registra la solicitud como privada, solo visible para la Ejecutiva (RN-03)
  4. El sistema muestra la referencia MED-AAAA-NNNNN sin repetir los datos de la solicitud
  5. Miembro de la Ejecutiva gestiona la solicitud y cambia su estado a pendiente, en proceso o cerrada

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| RNF-01 | Rendimiento | cargar cada página en menos de 3 segundos en condiciones estándar de red del campus | Importante |
| RNF-02 | Usabilidad móvil | adaptarse a móviles, tablets y ordenadores mediante un diseño responsive | Vital |
| RNF-03 | Accesibilidad | cumplir el nivel AA de las pautas de accesibilidad WCAG 2.1 y las pautas del Diseño Universal para el Aprendizaje (DUA), con atención a las personas ciegas y daltónicas | Importante |
| RNF-04 | Seguridad en formularios | validar y sanear las entradas de todos los formularios y protegerse frente a spam e inyección | Vital |
| RNF-05 | Compatibilidad técnica | funcionar con PHP 8.x y MySQL 8.x sobre un servidor Apache local (WampServer, compatible con XAMPP) | Importante |
| RNF-06 | Disponibilidad | mantenerse estable durante los periodos críticos: matrícula, asambleas y votaciones | Importante |
| RNF-07 | Mantenibilidad | contar con configuración y código documentados para facilitar el relevo entre cursos del CADUS | Importante |
| RNF-08 | Privacidad | tratar los datos de consultas, reclamaciones y solicitudes de mediación conforme al RGPD y la LOPDGDD, con consentimiento expreso en cada formulario y un aviso de privacidad público. Los tickets y las mediaciones se conservan 2 años desde que se resuelven y después se borran o anonimizan; solo se piden nombre y apellidos, facultad y correo de la US. El plazo de respuesta («al menos 4 días») está pendiente de aclarar con el CADUS | Vital |

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-01 | Aprobación de documentos | Todo contenido pasa por la Ejecutiva antes de publicarse; en particular, toda acta o normativa requiere la aprobación de un miembro de la Ejecutiva. |
| RN-02 | Correo institucional | Solo se aceptan consultas, reclamaciones y solicitudes de mediación enviadas desde un correo corporativo @alum.us.es. |
| RN-03 | Privacidad de reclamaciones | Todas las consultas, reclamaciones y solicitudes de mediación se tratan con total privacidad: solo son visibles para el remitente y para la Ejecutiva, no aparecen en la web pública, en el buscador ni en la API, y los avisos por correo no incluyen su contenido. |
| RN-04 | Edición de fichas | Cada ficha de delegación solo puede ser editada por la cuenta del delegado de esa delegación o por la cuenta del CADUS (administrador). |
| RN-05 | Votaciones vinculadas | Toda votación publicada en el calendario debe estar vinculada a una convocatoria de asamblea previamente creada. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-01 | Servidor compartido con Tailscale | WordPress y la base de datos bd_cadus se alojan en un único servidor local (WampServer) en el equipo de un integrante. El resto del equipo accede mediante Tailscale (VPN privada), de modo que los cinco integrantes trabajan a la vez sobre la misma instancia. El acceso web se limita a la red de Tailscale, cada integrante usa su propia cuenta de WordPress y el puerto de la base de datos no se expone. El servidor solo está disponible mientras el equipo anfitrión esté encendido. |
| RC-02 | Control de versiones con GitHub | Todo el contenido en forma de archivo (tema, plugins, documentación, artefactos SCRUM, requisitos y maquetas) se versiona en el repositorio de GitHub del proyecto. No se versionan wp-config.php, wp-content/uploads ni credenciales. Los volcados de la base de datos son copia de seguridad y de entrega, no mecanismo de sincronización. |
| RC-03 | Coordinación del equipo con Discord | El equipo se coordina en un servidor de Discord (GSI - CADUS) organizado en categorías: INFO (anuncios, entorno y recursos), SCRUM (daily, sprint-review y retrospectiva), DESARROLLO (un canal por área: infra-y-bd, portada, institucional-y-normativa, delegaciones y buzon-y-faq, además de github y avisos-servidor) y VOZ (Sala de trabajo y Daily) para las reuniones y el trabajo a distancia. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-01 | UI-01, RNF-01, RNF-02, RNF-03, RNF-05 |
| OBJ-02 | RF-01, RF-02, IR-03, UI-02 |
| OBJ-03 | RF-03, RF-04, RF-05, IR-04, RN-01, UI-05 |
| OBJ-04 | RF-06, RF-07, IR-05, RN-04, UI-03 |
| OBJ-05 | RF-08, RF-09, RF-10, RF-13, IR-06, IR-08, RN-02, RN-03, RNF-04, RNF-08, UI-04, UI-07, UC-04 |
| OBJ-06 | RF-11, RF-12, IR-07, RN-05, UI-06, UC-03 |
| UI-02 | IR-01, IR-02 |
| RF-08 | UC-01 |
| RF-09 | UC-01 |
| RF-03 | UC-02 |
| RF-05 | UC-02 |
| RF-14 | IR-09 |
| RF-10 | IR-06, RN-03 |
| RF-12 | IR-07, RN-05, UC-03 |
| RF-13 | IR-08, RN-02, RN-03, UC-04 |
| RF-15 | IR-03, IR-04, IR-05, UI-08 |
| RC-01 | RNF-06, RNF-07 |
| RC-02 | RNF-07 |
| RC-03 | RNF-07 |
