# Hoja de carga para REMUS — DMS del CADUS · Normativa

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/dms_normativa_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [DMS-Normativa.rem](DMS-Normativa.rem) (REMUS), versión 1.1, 2026-11-12. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

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

## 4. Requisitos de información

| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |
|---|---|---|---|
| IR-D03 | Normativa | a una norma o estatuto del CADUS, con estos datos: | Título; Norma (identifica la misma norma entre sus versiones); Versión; Año; Estado (vigente o derogada) |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-D01 | Ejecutiva del CADUS | a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios de los sitios (leen y escriben) |
| ACT-D02 | Delegado | a los delegados de las 27 delegaciones, que acceden con la cuenta de su delegación (correo institucional de la delegación; una cuenta por delegación, no por persona) y solo leen |
| ACT-D03 | Estudiante | a los estudiantes de la Universidad de Sevilla, que solo leen la normativa vigente |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-D02 | Tipo de documento obligatorio | exigir en todo documento el metadato Tipo de documento (Acta, Normativa, Expediente o Votación), además de los propios de su tipo | DMS-HU-02 | Vital |
| RF-D04 | Búsqueda genérica | buscar por el nombre y por el contenido de los documentos | DMS-HU-03 | Vital |
| RF-D05 | Búsqueda por metadatos | ofrecer en cada biblioteca una vista plana, sin carpetas, a la que se aplican filtros combinados (por ejemplo, tipo de documento y fecha); para buscar en todo un sitio se usa la búsqueda de SharePoint | DMS-HU-03 · DMS-HU-05 | Vital |
| RF-D06 | Permisos por rol | asignar permisos por sitio y biblioteca con los grupos Propietario, Integrante y Visitante | DMS-HU-01 | Vital |

## 8. Casos de uso

### CU-D03 - Consultar la normativa vigente

- **Evento disparador:** cuando tienen una duda sobre sus derechos o el funcionamiento del CADUS
- **Precondición:** El usuario puede acceder al sitio Documentación pública
- **Postcondición:** El usuario ha leído la norma que buscaba
- **Pasos:**
  1. Delegado o el estudiante entra en el sitio Documentación pública; el delegado accede con la cuenta de su delegación y el estudiante con su correo @alum.us.es
  2. Estudiante abre la vista de normativa vigente
  3. El sistema muestra las normas con estado vigente y oculta las derogadas
  4. Estudiante busca por palabra clave o filtra por año
  5. El sistema muestra las normas que cumplen la búsqueda
  6. Estudiante abre la norma

### CU-D07 - Publicar una nueva versión de una norma y derogar la anterior

- **Evento disparador:** cuando la Ejecutiva aprueba la revisión de una norma ya publicada
- **Precondición:** La norma anterior está en la biblioteca Normativa con estado Vigente y la Ejecutiva dispone del documento de la versión nueva
- **Postcondición:** La versión nueva es la única vigente de su norma y la anterior queda derogada y conservada
- **Pasos:**
  1. Ejecutiva del CADUS sube el documento de la versión nueva a la biblioteca Normativa
  2. El sistema solicita el tipo de documento, la norma, la versión, la fecha, el curso académico y el estado
  3. Ejecutiva del CADUS rellena los metadatos con la misma norma, la versión nueva y el estado Vigente
  4. Ejecutiva del CADUS abre la versión anterior de esa norma y cambia su estado a Derogada
  5. El sistema muestra en la vista de normativa vigente solo la versión nueva y conserva la derogada, sin borrarla

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-D06 | Tipo de documento | Para buscar por metadatos hay que haber rellenado el tipo de documento en todos los documentos. |
| RN-D07 | Una versión vigente por norma | Por cada norma solo puede haber una versión vigente (puede haber varias normas distintas vigentes a la vez). Al publicar una versión nueva, la anterior pasa a Derogada y se conserva: no se borra. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-D01 | SharePoint de la Universidad de Sevilla | El DMS se construye en SharePoint de Microsoft 365 de la Universidad de Sevilla (uses0.sharepoint.com), con sitios, bibliotecas, columnas de metadatos, vistas y los grupos Propietarios, Integrantes y Visitantes. Los cuatro sitios (cadus-documentacion-publica, cadus-organos-de-gobierno, cadus-votaciones y cadus-atencion-al-estudiante) los creó Pablo; los otros cuatro integrantes son miembros de los tres primeros. |
| RC-D02 | Acceso con correo corporativo | Los estudiantes acceden con su correo corporativo @alum.us.es; cada delegado, con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11/2026); la Ejecutiva, con la cuenta única del CADUS (dcadus@us.es). |
| RC-D03 | Documentación independiente | La documentación del DMS (requisitos, análisis, diseño, implementación y seguimiento SCRUM) es independiente de la del portal web. Se guarda en docs/dms del repositorio de GitHub y la coordinación diaria se hace en Discord. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-D01 | RF-D06, IR-D03 |
| OBJ-D02 | RF-D02, RF-D04, RF-D05, RN-D06, RN-D07 |
| CU-D03 | RF-D04, RF-D05, RF-D06, IR-D03, ACT-D03, ACT-D02 |
| CU-D07 | RF-D02, RF-D05, RF-D06, RN-D06, RN-D07, IR-D03, ACT-D01 |
