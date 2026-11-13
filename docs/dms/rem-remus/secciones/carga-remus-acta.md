# Hoja de carga para REMUS — DMS del CADUS · Acta

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/dms_acta_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [DMS-Acta.rem](DMS-Acta.rem) (REMUS), versión 1.1, 2026-11-12. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

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
| IR-D02 | Acta | a un acta de pleno o de asamblea, con estos datos: | Pleno o asamblea; Fecha; Estado de aprobación (borrador o aprobada); Curso académico; Resumen del contenido (deseable) |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-D01 | Ejecutiva del CADUS | a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios de los sitios (leen y escriben) |
| ACT-D02 | Delegado | a los delegados de las 27 delegaciones, que acceden con la cuenta de su delegación (correo institucional de la delegación; una cuenta por delegación, no por persona) y solo leen |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|
| UI-D02 | Vistas predefinidas | ofrecer vistas planas ya filtradas: normativa vigente, actas aprobadas, votaciones y expedientes caducados | RF-D05 |

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-D01 | Organización en sitios y carpetas | organizar los documentos en cuatro sitios (Documentación pública, Órganos de gobierno, Votaciones y Atención al estudiante) con una biblioteca por tipo de documento | DMS-HU-01 | Vital |
| RF-D02 | Tipo de documento obligatorio | exigir en todo documento el metadato Tipo de documento (Acta, Normativa, Expediente o Votación), además de los propios de su tipo | DMS-HU-02 | Vital |
| RF-D03 | Aprobación de actas | usar la aprobación de contenido para que un acta en borrador solo la vean su autor y la Ejecutiva, y los delegados solo vean las aprobadas | DMS-HU-04 | Vital |
| RF-D04 | Búsqueda genérica | buscar por el nombre y por el contenido de los documentos | DMS-HU-03 | Vital |
| RF-D05 | Búsqueda por metadatos | ofrecer en cada biblioteca una vista plana, sin carpetas, a la que se aplican filtros combinados (por ejemplo, tipo de documento y fecha); para buscar en todo un sitio se usa la búsqueda de SharePoint | DMS-HU-03 · DMS-HU-05 | Vital |
| RF-D06 | Permisos por rol | asignar permisos por sitio y biblioteca con los grupos Propietario, Integrante y Visitante | DMS-HU-01 | Vital |
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
- **Precondición:** El delegado ha iniciado sesión con la cuenta de su delegación
- **Postcondición:** El delegado ha abierto el acta que buscaba
- **Pasos:**
  1. Delegado abre la vista plana de actas aprobadas
  2. El sistema muestra solo las actas aprobadas, sin los borradores
  3. Delegado filtra por fecha, curso o palabra clave
  4. El sistema muestra las actas que cumplen los filtros
  5. Delegado abre el acta

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-D01 | Actas aprobadas | Un acta solo es visible para los delegados cuando un miembro de la Ejecutiva la ha aprobado (coherente con RN-01 del portal). |
| RN-D06 | Tipo de documento | Para buscar por metadatos hay que haber rellenado el tipo de documento en todos los documentos. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-D01 | SharePoint de la Universidad de Sevilla | El DMS se construye en SharePoint de Microsoft 365 de la Universidad de Sevilla (uses0.sharepoint.com), con sitios, bibliotecas, columnas de metadatos, vistas y los grupos Propietarios, Integrantes y Visitantes. Los cuatro sitios (cadus-documentacion-publica, cadus-organos-de-gobierno, cadus-votaciones y cadus-atencion-al-estudiante) los creó Pablo; los otros cuatro integrantes son miembros de los cuatro (grupo Integrantes). |
| RC-D02 | Acceso con correo corporativo | Los estudiantes acceden con su correo corporativo @alum.us.es; cada delegado, con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11/2026); la Ejecutiva, con la cuenta única del CADUS (dcadus@us.es). |
| RC-D03 | Documentación independiente | La documentación del DMS (requisitos, análisis, diseño, implementación y seguimiento SCRUM) es independiente de la del portal web. Se guarda en docs/dms del repositorio de GitHub y la coordinación diaria se hace en Discord. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-D01 | RF-D01, RF-D06, RF-D09, IR-D02 |
| OBJ-D02 | RF-D02, RF-D04, RF-D05, UI-D02, RN-D06 |
| OBJ-D03 | RF-D03, RN-D01 |
| OBJ-D04 | RF-D09 |
| CU-D01 | RF-D01, RF-D02, RF-D03, RF-D09, RN-D01, RN-D06, IR-D02, ACT-D01 |
| CU-D02 | RF-D03, RF-D04, RF-D05, RF-D06, RF-D10, RN-D01, IR-D02, UI-D02, ACT-D02 |
