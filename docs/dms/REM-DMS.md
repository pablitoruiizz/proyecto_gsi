# REM del DMS del CADUS (versión 1.1)

Documento de requisitos del **sistema de gestión documental (DMS)** del CADUS. Es independiente del REM del CMS ([`docs/requisitos/rem-remus/REM-CADUS.md`](../requisitos/rem-remus/REM-CADUS.md)): tiene sus propios requisitos, análisis, diseño, implementación y seguimiento SCRUM, como pide el Lab 4.

## 1. Introducción

El portal web del CADUS (CMS) informa a los estudiantes; el DMS guarda y organiza los **documentos internos de gestión** del Consejo: actas, normativa, expedientes de reclamaciones y registros de votación. Cada tipo de documento se identifica con metadatos, se encuentra con búsquedas y filtros, y solo lo ve quien tiene permiso.

**Fuentes:** entrevista con el CADUS del 26/10/2026 ([`docs/cliente/entrevista-cliente.md`](../cliente/entrevista-cliente.md)), el REM del CMS (RN-01, RN-03, RNF-08) y el enunciado del Lab 4.

## 2. Participantes y actores

| Actor | Descripción | Rol en el DMS |
|---|---|---|
| Ejecutiva del CADUS | Todos sus miembros usan la cuenta única `dcadus@us.es` | **Propietario** (lee y escribe) |
| Delegado | Representa a una de las 27 delegaciones; la cuenta es de la delegación, no de la persona, y entra con el correo institucional de su delegación (decisión del CADUS del 09/11) | **Visitante** (solo lectura) |
| Estudiante | Estudiante de la US | **Visitante**, solo de la normativa pública |

El rol **Integrante** (lee y escribe) lo usa el equipo del proyecto, en los cuatro sitios y solo con datos de ejemplo. Para la Ejecutiva queda sin uso: el cliente indicó que todos los ejecutivos comparten la cuenta del CADUS. Se deja prevista para cuando haya cuentas personales.

## 3. Objetivos

| ID | Objetivo |
|---|---|
| OBJ-D01 | Reunir en un único sitio los documentos internos del CADUS, organizados por tipo y con permisos por rol. |
| OBJ-D02 | Localizar un documento por sus metadatos (tipo, fecha, estado, curso, facultad…) o por una búsqueda genérica. |
| OBJ-D03 | Proteger los expedientes de reclamaciones y mediaciones y conservarlos solo los 2 años que pide el cliente. |
| OBJ-D04 | Dejar constancia de las votaciones presenciales por delegación sin guardar datos personales innecesarios. |

## 4. Requisitos de información

| ID | Concepto | Datos |
|---|---|---|
| IR-D01 | Documento | Nombre, archivo, tipo de documento, fecha, curso académico, estado |
| IR-D02 | Acta | Pleno o asamblea, fecha, estado (borrador o aprobada), curso, resumen del contenido |
| IR-D03 | Normativa | Título, norma (identifica la misma norma entre versiones), versión, año, estado (vigente o derogada) |
| IR-D04 | Expediente | Código de ticket (`CAD-…`) o de mediación (`MED-…`), facultad, fecha de resolución, fecha de caducidad |
| IR-D05 | Registro de votación | Asamblea y número de votación (obligatorios), fecha, tipo de voto (nominal o secreto), resultado y, por cada una de las 27 delegaciones, si estaba presente y si se comprobó su identidad. **Voto nominal:** el voto de cada delegación (sí, no o abstención). **Voto secreto:** solo el recuento total de sí, no y abstenciones, sin vincularlo a ninguna delegación |
| IR-D06 | Metadato | Columna de un tipo de dato que se añade a los documentos para poder filtrar |

## 5. Requisitos funcionales

| ID | Descripción | CU |
|---|---|---|
| RF-D01 | Organizar los documentos en sitios y carpetas por tipo: Documentación pública, Órganos de gobierno, Votaciones y Atención al estudiante. | todos |
| RF-D02 | Todo documento lleva obligatoriamente el metadato **Tipo de documento** (Acta, Normativa, Expediente o Votación), además de los propios de su tipo. | todos |
| RF-D03 | Las actas usan la **aprobación de contenido** de la biblioteca: un acta en borrador solo la ven su autor y los aprobadores (la Ejecutiva); los delegados solo ven las aprobadas. | CU-D01, CU-D02 |
| RF-D04 | Búsqueda genérica por nombre y por contenido del documento. | CU-D02, CU-D03 |
| RF-D05 | Búsqueda por metadatos: en cada biblioteca, una **vista plana** sin carpetas a la que se aplican filtros combinados (por ejemplo, tipo de documento y fecha); para buscar en todo un sitio se usa la búsqueda de SharePoint. | CU-D02, CU-D03, CU-D07, CU-D08 |
| RF-D06 | Permisos por sitio y carpeta con los grupos Propietario, Integrante y Visitante. | todos |
| RF-D07 | La **fecha de caducidad** de un expediente es un metadato calculado: fecha de resolución más 2 años. | CU-D04, CU-D05 |
| RF-D08 | Vista de expedientes caducados (caducidad anterior a hoy) para retirarlos. | CU-D05 |
| RF-D09 | Plantillas de acta y de registro de votación para que todos los documentos tengan la misma estructura. | CU-D01, CU-D06 |
| RF-D10 | Resumen automático del contenido del acta como metadato generado (**deseable**: se implementa solo si sobra tiempo; no tiene historia en este sprint). | CU-D02 |

### Requisitos de interfaz

| ID | Descripción |
|---|---|
| UI-D01 | Formulario guiado de metadatos: pedirlos en pocos pasos y con listas de valores (RNF-D02). |
| UI-D02 | Vistas predefinidas: normativa vigente, actas aprobadas, votaciones y expedientes caducados (RF-D05). |

## 6. Requisitos no funcionales

| ID | Descripción |
|---|---|
| RNF-D01 | **Privacidad:** los expedientes y los registros de votación cumplen RGPD y LOPDGDD y no se guardan datos que no sean necesarios. |
| RNF-D02 | **Facilidad de uso:** una persona sin conocimientos informáticos debe poder subir un documento y rellenar sus metadatos con una guía de pocos pasos. |
| RNF-D03 | **Mantenibilidad:** la estructura de sitios, columnas y permisos queda documentada para el relevo entre cursos. |
| RNF-D04 | **Conservación:** los expedientes se conservan 2 años desde su resolución (entrevista, respuesta 10) y se retiran en la primera revisión mensual posterior; el plazo máximo real es de 2 años y un mes (decisión técnica del equipo por la periodicidad mensual; el CADUS todavía no la ha confirmado). |
| RNF-D05 | **Disponibilidad:** los documentos son accesibles durante las asambleas. |

## 7. Reglas de negocio

| ID | Regla |
|---|---|
| RN-D01 | Un acta solo es visible para los delegados cuando un miembro de la Ejecutiva la ha aprobado (coherente con RN-01 del CMS). |
| RN-D02 | Los expedientes de reclamaciones y mediaciones solo los ve la Ejecutiva (coherente con RN-03 del CMS). |
| RN-D03 | Un expediente se retira en la primera revisión mensual posterior al cumplimiento de los 2 años desde su resolución, así que se conserva como máximo 2 años y un mes. «Retirar» significa eliminar el documento, sus versiones y su copia en la papelera de reciclaje. |
| RN-D04 | El registro de votación **no guarda el número de DNI**: solo si se comprobó la identidad del delegado. En una votación **secreta** tampoco se guarda el voto de cada delegación: la lista de participación y el recuento van separados y no se pueden relacionar. |
| RN-D05 | En cada votación cuenta un voto por delegación (27 delegaciones), que representa a sus estudiantes; solo votan los delegados. La plantilla trae una fila por delegación con Presente o Ausente (la ausencia no es abstención) y una columna de voto que solo admite sí, no o abstención; cada asamblea puede tener varias votaciones numeradas. |
| RN-D06 | Para buscar por metadatos hay que haber rellenado el tipo de documento en todos los documentos. |
| RN-D07 | Por cada norma solo puede haber una versión vigente (puede haber varias normas distintas vigentes a la vez). Al publicar una versión nueva, la anterior pasa a Derogada y se conserva: no se borra. |

## 8. Casos de uso

Los casos de uso se dividen por secciones (acta, normativa, expediente y votación) y cada sección tiene dos, ocho en total, como pidió el profesor y exige el Lab 4 (al menos uno por documento).

| ID | Caso de uso | Actor | Cuándo | Documento | Requisitos |
|---|---|---|---|---|---|
| CU-D01 | Redactar, aprobar y archivar un acta | Ejecutiva | Después de cada pleno o asamblea | Acta | RF-D01, RF-D02, RF-D03, RF-D09, RN-D01 |
| CU-D02 | Consultar las actas aprobadas | Delegado | Antes de cada asamblea, para repasar lo acordado | Acta | RF-D03, RF-D04, RF-D05, RF-D06, RF-D10 |
| CU-D03 | Consultar la normativa vigente | Estudiante o delegado (ACT-D03, ACT-D02) | Cuando tienen una duda sobre sus derechos o el funcionamiento del CADUS | Normativa | RF-D04, RF-D05, RF-D06 |
| CU-D04 | Archivar un expediente resuelto | Ejecutiva | Cada vez que se resuelve una reclamación o una mediación | Expediente | RF-D01, RF-D02, RF-D07, RN-D02 |
| CU-D05 | Retirar los expedientes caducados | Ejecutiva | Una vez al mes | Expediente | RF-D07, RF-D08, RN-D03 |
| CU-D06 | Registrar el resultado de una votación presencial | Ejecutiva | En cada asamblea con votación | Registro de votación | RF-D01, RF-D02, RF-D09, RN-D04, RN-D05 |
| CU-D07 | Publicar una nueva versión de una norma y derogar la anterior | Ejecutiva | Cuando se aprueba la revisión de una norma ya publicada | Normativa | RF-D02, RF-D05, RF-D06, RN-D06, RN-D07 |
| CU-D08 | Consultar los registros de votaciones anteriores | Ejecutiva | Cuando necesita comprobar qué se decidió en una votación anterior | Registro de votación | RF-D05, RF-D06, RN-D04, RN-D05, RN-D06, RNF-D01 |

### Detalle

**CU-D01 Redactar, aprobar y archivar un acta.** Un ejecutivo crea el acta a partir de la plantilla en la carpeta *Actas* con estado Borrador y tipo Acta. Cuando la Ejecutiva la aprueba, cambia el estado a Aprobada y rellena la fecha y el curso. *Resultado:* el acta es visible para los delegados.

**CU-D02 Consultar las actas aprobadas.** El delegado entra en el sitio, aplica el filtro tipo Acta y estado Aprobada, y opcionalmente una fecha o una palabra clave. *Resultado:* abre el acta que busca.

**CU-D03 Consultar la normativa vigente.** El usuario filtra por tipo Normativa y estado Vigente o busca por palabra clave. *Resultado:* lee el documento. La normativa derogada no aparece en la vista de vigentes.

**CU-D04 Archivar un expediente resuelto.** Cuando se resuelve un ticket o una mediación, un ejecutivo guarda el expediente en el sitio *Atención al estudiante* con su código, la facultad y la fecha de resolución. *Resultado:* la caducidad se calcula sola (resolución + 2 años).

**CU-D05 Retirar los expedientes caducados.** Cada mes la Ejecutiva abre la vista de caducados, elimina cada expediente con sus versiones y vacía la papelera. *Resultado:* ningún expediente se conserva más de 2 años y un mes.

**CU-D06 Registrar el resultado de una votación presencial.** Tras una votación en asamblea, un ejecutivo rellena la plantilla: la lista de delegaciones presentes y si se comprobó su identidad y, según el tipo de voto, el voto de cada delegación (nominal) o solo el recuento total (secreto). *Resultado:* queda constancia sin guardar el DNI y, en las votaciones secretas, sin poder saber qué votó cada delegación.

**CU-D07 Publicar una nueva versión de una norma y derogar la anterior.** Cuando la Ejecutiva aprueba la revisión de una norma, sube el documento nuevo a la biblioteca *Normativa* y rellena sus metadatos con la misma *Norma*, la *Versión* nueva y el estado Vigente; después abre la versión anterior de esa norma y cambia su estado a Derogada. *Resultado:* la vista de normativa vigente solo muestra la versión nueva y la derogada se conserva (RN-D07).

**CU-D08 Consultar los registros de votaciones anteriores.** La Ejecutiva abre la biblioteca *Votaciones*, que solo ella puede ver, y filtra la vista plana por asamblea y por tipo de voto. *Resultado:* abre el registro que buscaba, identificado por su asamblea y su número de votación.

## 9. Metadatos

| Metadato | Tipo de columna | Se usa en |
|---|---|---|
| Tipo de documento | Elección (Acta, Normativa, Expediente, Votación) | todos |
| Fecha | Fecha | todos |
| Curso académico | Elección | todos |
| Estado | Elección (Borrador, Aprobada, Vigente, Derogada, Resuelto) | Acta, Normativa, Expediente |
| Asamblea | Texto (obligatorio en Votación) | Acta, Votación |
| Norma | Texto (identifica la misma norma entre versiones) | Normativa |
| Versión | Número (1, 2, 3…) | Normativa |
| Número de votación | Número (obligatorio) | Votación |
| Tipo de voto | Elección (Nominal, Secreto) | Votación |
| Resultado | Elección (Aprobada, Rechazada) | Votación |
| Facultad | Elección | Expediente |
| Fecha de resolución | Fecha | Expediente |
| Fecha de caducidad | **Calculada** (resolución + 2 años) | Expediente |
| Resumen | Generado automáticamente | Acta (deseable) |

## 10. Bibliotecas y vistas

Las columnas viven en cada **biblioteca de documentos**, no en el sitio, y cada vista plana filtra dentro de su biblioteca. Para buscar en todo un sitio se usa la búsqueda de SharePoint.

| Sitio | Biblioteca | Tipo de documento | Columnas propias | Vistas |
|---|---|---|---|---|
| Documentación pública | Normativa | Normativa | Fecha, Curso académico, Norma, Versión, Estado | Vigente (plana, filtrada por Estado) |
| Órganos de gobierno | Actas | Acta | Fecha, Curso académico, Asamblea, Estado de aprobación, Resumen | Aprobadas (plana) |
| Votaciones | Votaciones | Votación | Fecha, Curso académico, Asamblea, Número de votación, Tipo de voto, Resultado | Todas (plana) |
| Atención al estudiante | Expedientes | Expediente | Facultad, Fecha de resolución, Fecha de caducidad (calculada), Estado | Caducados (plana, caducidad anterior a hoy) |

## 11. Roles y permisos

| Sitio | Carpetas | Propietario (cuenta del CADUS) | Visitante |
|---|---|---|---|
| Documentación pública | Normativa | lee y escribe | Estudiantes y delegados: lectura |
| Órganos de gobierno | Biblioteca **Actas** (con aprobación de contenido) | lee y escribe | Delegados: lectura de las actas aprobadas |
| Votaciones | Votaciones (sitio propio, grupo Visitantes vacío) | lee y escribe | nadie (solo la Ejecutiva) |
| Atención al estudiante | Expedientes | lee y escribe | nadie |

## 12. Restricciones del entorno

| ID | Restricción |
|---|---|
| RC-D01 | Plataforma: **SharePoint de Microsoft 365 de la Universidad de Sevilla**, con sitios, carpetas, columnas de metadatos, vistas y los grupos Propietario, Integrante y Visitante. |
| RC-D02 | Los estudiantes acceden con su correo corporativo `@alum.us.es`; cada delegado, con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11). |
| RC-D03 | La documentación del DMS (REM, análisis, diseño, implementación y SCRUM) es independiente de la del CMS. |

## 13. Del análisis al diseño

| Concepto del análisis | Concepto del diseño |
|---|---|
| Documento | Documento (con columnas de metadatos) |
| Carpeta | Sitio o carpeta (los sitios permiten asignar permisos de golpe) |
| Rol (Ejecutiva, Delegado, Estudiante) | Grupo de permisos (Propietario, Integrante, Visitante) |
| Búsqueda | Búsqueda genérica y filtros por metadatos sobre una vista plana |
| Metadato | Columna del sitio |
| Permiso | Permiso del sitio según el grupo |

## 14. Trazabilidad

| Caso de uso | Requisitos | Historia del DMS |
|---|---|---|
| CU-D01 | RF-D01, RF-D02, RF-D03, RF-D09 | DMS-HU-01, DMS-HU-02, DMS-HU-04 |
| CU-D02 | RF-D03 a RF-D06, RF-D10 | DMS-HU-03, DMS-HU-04 |
| CU-D03 | RF-D04 a RF-D06 | DMS-HU-03, DMS-HU-05 |
| CU-D04 | RF-D01, RF-D02, RF-D07 | DMS-HU-06 |
| CU-D05 | RF-D07, RF-D08 | DMS-HU-06 |
| CU-D06 | RF-D01, RF-D02, RF-D09 | DMS-HU-07 |
| CU-D07 | RF-D02, RF-D05, RF-D06 | DMS-HU-08 |
| CU-D08 | RF-D05, RF-D06 | DMS-HU-09 |

| Regla o requisito no funcional | Se comprueba en |
|---|---|
| RN-D01 | DMS-HU-04 (aprobación de contenido) |
| RN-D02, RNF-D01 | DMS-HU-01 (permisos del sitio Atención al estudiante) |
| RN-D03, RNF-D04 | DMS-HU-06 (vista de caducados y revisión mensual) |
| RN-D04, RN-D05 | DMS-HU-07 (plantilla de votación) y DMS-HU-09 (consulta de registros) |
| RN-D06 | DMS-HU-02 (columna Tipo de documento obligatoria) |
| RN-D07 | DMS-HU-08 (versión vigente única por norma) |
| RNF-D02, RNF-D03 | Documentación del DMS (D-04, D-06) |
| RNF-D05 | Prueba de acceso durante la asamblea (D-04) |

## 15. El REM en varios archivos de REMUS

El profesor pidió dividir los casos de uso por secciones o roles, con dos casos en cada una, y comentó que lo normal es que el DMS salga con más de un `.rem`. Por eso el REM está en **cinco proyectos de REMUS** que salen de la misma fuente (`scripts/remus/dms_data.json`):

| Archivo | Contenido |
|---|---|
| `DMS.rem` | REM completo del DMS: los 8 casos de uso, todos los requisitos, reglas, actores y la trazabilidad global. |
| `secciones/DMS-Acta.rem` | Sección Acta: CU-D01 y CU-D02. |
| `secciones/DMS-Normativa.rem` | Sección Normativa: CU-D03 y CU-D07. |
| `secciones/DMS-Expediente.rem` | Sección Expediente: CU-D04 y CU-D05. |
| `secciones/DMS-Votacion.rem` | Sección Votación: CU-D06 y CU-D08. |

Cada `.rem` de sección lleva solo los dos casos de uso de su documento y los requisitos de información, funcionales, no funcionales, de interfaz, reglas, actores y objetivos que esos casos citan, con su trazabilidad; el entorno de trabajo y el glosario son comunes. Los códigos son los mismos que en `DMS.rem`, así que un requisito se identifica igual en todos los archivos. Se regeneran con `python scripts/dms/dividir_rem.py` (junto con `DMS.rem`, que genera `build_rem.ps1`); cada uno tiene su hoja legible en `docs/dms/rem-remus/secciones/carga-remus-<seccion>.md`.
