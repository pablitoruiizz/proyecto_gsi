# Hoja de carga para REMUS — DMS del CADUS

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/dms_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [DMS.rem](DMS.rem) (REMUS), versión 1.0, 2026-10-30. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

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
| OBJ-D01 | Documentación reunida | reunir en un único sitio los documentos internos del CADUS, organizados por tipo y con permisos por rol | Vital |
| OBJ-D02 | Búsqueda por metadatos | localizar un documento por sus metadatos (tipo, fecha, estado, curso, facultad) o con una búsqueda genérica | Vital |
| OBJ-D03 | Privacidad y conservación | proteger los expedientes de reclamaciones y mediaciones y conservarlos solo los 2 años que pide el cliente | Vital |
| OBJ-D04 | Constancia de votaciones | dejar constancia de las votaciones presenciales por delegación sin guardar datos personales innecesarios | Vital |

## 4. Requisitos de información

| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |
|---|---|---|---|
| IR-D01 | Documento | a cada documento del DMS, con estos datos: | Nombre y archivo; Tipo de documento (Acta, Normativa, Expediente o Votación); Fecha; Curso académico; Estado |
| IR-D02 | Acta | a un acta de pleno o de asamblea, con estos datos: | Pleno o asamblea; Fecha; Estado de aprobación (borrador o aprobada); Curso académico; Resumen del contenido (deseable) |
| IR-D03 | Normativa | a una norma o estatuto del CADUS, con estos datos: | Título; Año; Estado (vigente o derogada) |
| IR-D04 | Expediente | a una reclamación o mediación resuelta, con estos datos: | Código del ticket (CAD) o de la mediación (MED); Facultad; Fecha de resolución; Fecha de caducidad (resolución más 2 años) |
| IR-D05 | Registro de votación | al resultado de una votación presencial de asamblea, con estos datos: | Asamblea y número de votación; Fecha; Tipo de voto (nominal o secreto); Resultado; Por cada una de las 27 delegaciones: presente o ausente y si se comprobó su identidad; Voto nominal: el voto de cada delegación (sí, no o abstención); Voto secreto: solo el recuento total de sí, no y abstenciones |
| IR-D06 | Metadato | a una columna de una biblioteca que describe sus documentos, con estos datos: | Nombre de la columna; Tipo de columna (elección, fecha, texto, calculada); Valores permitidos |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-D01 | Ejecutiva del CADUS | a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios de los sitios (leen y escriben) |
| ACT-D02 | Delegado | a los delegados de las 27 delegaciones, que acceden con su correo @alum.us.es y solo leen |
| ACT-D03 | Estudiante | a los estudiantes de la Universidad de Sevilla, que solo leen la normativa vigente |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|
| UI-D01 | Formulario guiado de metadatos | pedir los metadatos de cada documento en pocos pasos, con listas de valores, para que una persona sin conocimientos informáticos pueda rellenarlos | RNF-D02 |
| UI-D02 | Vistas predefinidas | ofrecer vistas planas ya filtradas: normativa vigente, actas aprobadas, votaciones y expedientes caducados | RF-D05 |

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-D01 | Organización en sitios y carpetas | organizar los documentos en tres sitios (Documentación pública, Órganos de gobierno y Atención al estudiante) con una biblioteca por tipo de documento | DMS-HU-01 | Vital |
| RF-D02 | Tipo de documento obligatorio | exigir en todo documento el metadato Tipo de documento (Acta, Normativa, Expediente o Votación), además de los propios de su tipo | DMS-HU-02 | Vital |
| RF-D03 | Aprobación de actas | usar la aprobación de contenido para que un acta en borrador solo la vean su autor y la Ejecutiva, y los delegados solo vean las aprobadas | DMS-HU-04 | Vital |
| RF-D04 | Búsqueda genérica | buscar por el nombre y por el contenido de los documentos | DMS-HU-03 | Vital |
| RF-D05 | Búsqueda por metadatos | ofrecer en cada biblioteca una vista plana, sin carpetas, a la que se aplican filtros combinados (por ejemplo, tipo de documento y fecha); para buscar en todo un sitio se usa la búsqueda de SharePoint | DMS-HU-03 · DMS-HU-05 | Vital |
| RF-D06 | Permisos por rol | asignar permisos por sitio y biblioteca con los grupos Propietario, Integrante y Visitante | DMS-HU-01 | Vital |
| RF-D07 | Fecha de caducidad calculada | calcular la fecha de caducidad de un expediente como su fecha de resolución más 2 años | DMS-HU-06 | Vital |
| RF-D08 | Expedientes caducados | mostrar los expedientes cuya fecha de caducidad es anterior a hoy para retirarlos | DMS-HU-06 | Vital |
| RF-D09 | Plantillas | ofrecer plantillas de acta y de registro de votación para que todos los documentos tengan la misma estructura | DMS-HU-04 · DMS-HU-07 | Vital |
| RF-D10 | Resumen automático del acta | generar automáticamente un resumen del contenido del acta como metadato (deseable; solo si sobra tiempo) | Sin historia en este sprint | Importante |

## 8. Casos de uso

### CU-D01 - Redactar, aprobar y archivar un acta

- **Evento disparador:** después de cada pleno o asamblea del CADUS
- **Precondición:** La Ejecutiva dispone de la plantilla de acta y del acta redactada
- **Postcondición:** El acta está aprobada y es visible para los delegados
- **Pasos:**
  1. Ejecutiva del CADUS crea el acta a partir de la plantilla en la biblioteca Actas
  2. El sistema guarda el acta como borrador visible solo para su autor y la Ejecutiva
  3. El sistema solicita el tipo de documento, la fecha, el curso académico y la asamblea
  4. Ejecutiva del CADUS rellena los metadatos y envía el acta a aprobación
  5. Ejecutiva del CADUS aprueba el acta
  6. El sistema publica el acta aprobada para los delegados

### CU-D02 - Consultar las actas aprobadas

- **Evento disparador:** antes de cada asamblea, para repasar lo acordado
- **Precondición:** El delegado ha iniciado sesión con su correo @alum.us.es
- **Postcondición:** El delegado ha abierto el acta que buscaba
- **Pasos:**
  1. Delegado abre la vista plana de actas aprobadas
  2. El sistema muestra solo las actas aprobadas, sin los borradores
  3. Delegado filtra por fecha, curso o palabra clave
  4. El sistema muestra las actas que cumplen los filtros
  5. Delegado abre el acta

### CU-D03 - Consultar la normativa vigente

- **Evento disparador:** cuando tienen una duda sobre sus derechos o el funcionamiento del CADUS
- **Precondición:** El usuario puede acceder al sitio Documentación pública
- **Postcondición:** El usuario ha leído la norma que buscaba
- **Pasos:**
  1. Delegado o el estudiante entra en el sitio Documentación pública; el delegado accede con su correo @alum.us.es
  2. Estudiante abre la vista de normativa vigente
  3. El sistema muestra las normas con estado vigente y oculta las derogadas
  4. Estudiante busca por palabra clave o filtra por año
  5. El sistema muestra las normas que cumplen la búsqueda
  6. Estudiante abre la norma

### CU-D04 - Archivar un expediente resuelto

- **Evento disparador:** cada vez que se resuelve una reclamación o una mediación
- **Precondición:** La Ejecutiva ha resuelto el ticket o la mediación
- **Postcondición:** El expediente está archivado con su fecha de caducidad
- **Pasos:**
  1. Ejecutiva del CADUS sube el expediente a la biblioteca Expedientes
  2. El sistema solicita el código, la facultad y la fecha de resolución
  3. Ejecutiva del CADUS rellena los metadatos
  4. El sistema calcula la fecha de caducidad (resolución más 2 años)
  5. El sistema guarda el expediente visible solo para la Ejecutiva

### CU-D05 - Retirar los expedientes caducados

- **Evento disparador:** una vez al mes
- **Precondición:** Existen expedientes con fecha de caducidad anterior a hoy
- **Postcondición:** Los expedientes caducados se han eliminado, con sus versiones y de la papelera
- **Pasos:**
  1. Ejecutiva del CADUS abre la vista de expedientes caducados
  2. El sistema muestra los expedientes cuya caducidad es anterior a hoy
  3. Ejecutiva del CADUS elimina cada expediente y vacía la papelera de reciclaje
  4. El sistema deja de conservar esos expedientes y sus versiones

### CU-D06 - Registrar el resultado de una votación presencial

- **Evento disparador:** en cada asamblea con votación
- **Precondición:** Se ha celebrado la votación y se ha comprobado la identidad de los delegados presentes
- **Postcondición:** Queda constancia del resultado sin guardar el DNI
- **Pasos:**
  1. Ejecutiva del CADUS crea el registro a partir de la plantilla en la biblioteca Votaciones
  2. El sistema muestra una fila por cada delegación para indicar si está presente y si se comprobó su identidad
  3. Ejecutiva del CADUS marca la presencia y la identidad de cada delegación y el tipo de voto
  4. El sistema si el voto es nominal, solicita el voto de cada delegación; si es secreto, solo el recuento total
  5. Ejecutiva del CADUS introduce el resultado
  6. El sistema guarda el registro visible solo para la Ejecutiva, sin números de DNI

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| RNF-D01 | Privacidad | cumplir el RGPD y la LOPDGDD en los expedientes y los registros de votación, sin guardar datos que no sean necesarios | Vital |
| RNF-D02 | Facilidad de uso | permitir que una persona sin conocimientos informáticos suba un documento y rellene sus metadatos con una guía de pocos pasos | Vital |
| RNF-D03 | Mantenibilidad | dejar documentada la estructura de sitios, columnas y permisos para el relevo entre cursos | Importante |
| RNF-D04 | Conservación | conservar los expedientes 2 años desde su resolución y retirarlos en la primera revisión mensual posterior, de modo que el plazo máximo real es de 2 años y un mes (excepción aceptada por la periodicidad mensual de la revisión) | Vital |
| RNF-D05 | Disponibilidad | mantener los documentos accesibles durante las asambleas | Importante |

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-D01 | Actas aprobadas | Un acta solo es visible para los delegados cuando un miembro de la Ejecutiva la ha aprobado (coherente con RN-01 del portal). |
| RN-D02 | Expedientes privados | Los expedientes de reclamaciones y mediaciones solo los ve la Ejecutiva (coherente con RN-03 del portal). |
| RN-D03 | Conservación de 2 años | Un expediente se retira en la primera revisión mensual posterior al cumplimiento de los 2 años desde su resolución, así que se conserva como máximo 2 años y un mes. Retirar significa eliminar el documento, sus versiones y su copia en la papelera de reciclaje. |
| RN-D04 | Votación sin DNI | El registro de votación no guarda el número de DNI: solo si se comprobó la identidad del delegado. En una votación secreta tampoco se guarda el voto de cada delegación: la lista de participación y el recuento van separados y no se pueden relacionar. |
| RN-D05 | Un voto por delegación | En cada votación cuenta un voto por delegación (27 delegaciones), que representa a sus estudiantes; solo votan los delegados. La plantilla trae una fila por delegación con presente o ausente (la ausencia no es abstención) y cada asamblea puede tener varias votaciones numeradas. |
| RN-D06 | Tipo de documento | Para buscar por metadatos hay que haber rellenado el tipo de documento en todos los documentos. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-D01 | SharePoint de la Universidad de Sevilla | El DMS se construye en SharePoint de Microsoft 365 de la Universidad de Sevilla (uses0.sharepoint.com), con sitios, bibliotecas, columnas de metadatos, vistas y los grupos Propietarios, Integrantes y Visitantes. Los tres sitios (cadus-documentacion-publica, cadus-organos-de-gobierno y cadus-atencion-al-estudiante) los creó Pablo y los otros cuatro integrantes son miembros. |
| RC-D02 | Acceso con correo corporativo | Los delegados y los estudiantes acceden con su correo corporativo @alum.us.es; la Ejecutiva, con la cuenta única del CADUS (dcadus@us.es). |
| RC-D03 | Documentación independiente | La documentación del DMS (requisitos, análisis, diseño, implementación y seguimiento SCRUM) es independiente de la del portal web. Se guarda en docs/dms del repositorio de GitHub y la coordinación diaria se hace en Discord. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-D01 | RF-D01, RF-D06, RF-D09, IR-D01, IR-D02, IR-D03, IR-D04, IR-D05, RNF-D03, RNF-D05 |
| OBJ-D02 | RF-D02, RF-D04, RF-D05, IR-D06, UI-D02, RN-D06 |
| OBJ-D03 | RF-D03, RF-D07, RF-D08, RNF-D01, RNF-D04, RN-D01, RN-D02, RN-D03 |
| OBJ-D04 | RN-D04, RN-D05, IR-D05, RF-D09 |
| CU-D01 | RF-D01, RF-D02, RF-D03, RF-D09, RN-D01, IR-D02, ACT-D01 |
| CU-D02 | RF-D03, RF-D04, RF-D05, RF-D06, RF-D10, RN-D01, IR-D02, ACT-D02 |
| CU-D03 | RF-D04, RF-D05, RF-D06, IR-D03, ACT-D03, ACT-D02 |
| CU-D04 | RF-D01, RF-D02, RF-D07, RN-D02, IR-D04, ACT-D01 |
| CU-D05 | RF-D07, RF-D08, RN-D03, RNF-D04, ACT-D01 |
| CU-D06 | RF-D01, RF-D02, RF-D09, RN-D04, RN-D05, IR-D05, ACT-D01 |
| UI-D01 | RNF-D02, RF-D02 |
| RNF-D01 | RN-D02, RN-D04 |
