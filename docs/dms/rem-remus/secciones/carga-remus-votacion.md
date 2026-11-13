# Hoja de carga para REMUS — DMS del CADUS · Votación

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/dms_votacion_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [DMS-Votacion.rem](DMS-Votacion.rem) (REMUS), versión 1.1, 2026-11-12. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

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
| IR-D05 | Registro de votación | al resultado de una votación presencial de asamblea, con estos datos: | Asamblea y número de votación (los dos obligatorios, para encontrar y distinguir cada registro); Fecha; Tipo de voto (nominal o secreto); Resultado; Por cada una de las 27 delegaciones: presente o ausente y si se comprobó su identidad; Voto nominal: el voto de cada delegación (sí, no o abstención); Voto secreto: solo el recuento total de sí, no y abstenciones |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-D01 | Ejecutiva del CADUS | a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios de los sitios (leen y escriben) |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-D01 | Organización en sitios y carpetas | organizar los documentos en cuatro sitios (Documentación pública, Órganos de gobierno, Votaciones y Atención al estudiante) con una biblioteca por tipo de documento | DMS-HU-01 | Vital |
| RF-D02 | Tipo de documento obligatorio | exigir en todo documento el metadato Tipo de documento (Acta, Normativa, Expediente o Votación), además de los propios de su tipo | DMS-HU-02 | Vital |
| RF-D05 | Búsqueda por metadatos | ofrecer en cada biblioteca una vista plana, sin carpetas, a la que se aplican filtros combinados (por ejemplo, tipo de documento y fecha); para buscar en todo un sitio se usa la búsqueda de SharePoint | DMS-HU-03 · DMS-HU-05 | Vital |
| RF-D06 | Permisos por rol | asignar permisos por sitio y biblioteca con los grupos Propietario, Integrante y Visitante | DMS-HU-01 | Vital |
| RF-D09 | Plantillas | ofrecer plantillas de acta y de registro de votación para que todos los documentos tengan la misma estructura | DMS-HU-04 · DMS-HU-07 | Vital |

## 8. Casos de uso

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

### CU-D08 - Consultar los registros de votaciones anteriores

- **Evento disparador:** cuando la Ejecutiva necesita comprobar qué se decidió en una votación de una asamblea anterior
- **Precondición:** Existen registros de votación guardados y quien consulta es miembro de la Ejecutiva
- **Postcondición:** La Ejecutiva ha abierto el registro de votación que buscaba
- **Pasos:**
  1. Ejecutiva del CADUS abre la biblioteca Votaciones
  2. El sistema muestra la vista plana con todos los registros, solo a la Ejecutiva
  3. Ejecutiva del CADUS filtra por asamblea y por tipo de voto
  4. El sistema muestra los registros que cumplen los filtros, identificados por su asamblea y su número de votación
  5. Ejecutiva del CADUS abre el registro

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| RNF-D01 | Privacidad | cumplir el RGPD y la LOPDGDD en los expedientes y los registros de votación, sin guardar datos que no sean necesarios | Vital |

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-D04 | Votación sin DNI | El registro de votación no guarda el número de DNI: solo si se comprobó la identidad del delegado. En una votación secreta tampoco se guarda el voto de cada delegación: la lista de participación y el recuento van separados y no se pueden relacionar. |
| RN-D05 | Un voto por delegación | En cada votación cuenta un voto por delegación (27 delegaciones), que representa a sus estudiantes; solo votan los delegados. La plantilla trae una fila por delegación con presente o ausente (la ausencia no es abstención) y cada asamblea puede tener varias votaciones numeradas. |
| RN-D06 | Tipo de documento | Para buscar por metadatos hay que haber rellenado el tipo de documento en todos los documentos. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-D01 | SharePoint de la Universidad de Sevilla | El DMS se construye en SharePoint de Microsoft 365 de la Universidad de Sevilla (uses0.sharepoint.com), con sitios, bibliotecas, columnas de metadatos, vistas y los grupos Propietarios, Integrantes y Visitantes. Los cuatro sitios (cadus-documentacion-publica, cadus-organos-de-gobierno, cadus-votaciones y cadus-atencion-al-estudiante) los creó Pablo; los otros cuatro integrantes son miembros de los tres primeros. |
| RC-D02 | Acceso con correo corporativo | Los estudiantes acceden con su correo corporativo @alum.us.es; cada delegado, con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11/2026); la Ejecutiva, con la cuenta única del CADUS (dcadus@us.es). |
| RC-D03 | Documentación independiente | La documentación del DMS (requisitos, análisis, diseño, implementación y seguimiento SCRUM) es independiente de la del portal web. Se guarda en docs/dms del repositorio de GitHub y la coordinación diaria se hace en Discord. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-D01 | RF-D01, RF-D06, RF-D09, IR-D05 |
| OBJ-D02 | RF-D02, RF-D05, RN-D06 |
| OBJ-D03 | RNF-D01 |
| OBJ-D04 | RN-D04, RN-D05, IR-D05, RF-D09 |
| CU-D06 | RF-D01, RF-D02, RF-D09, RN-D04, RN-D05, IR-D05, ACT-D01 |
| CU-D08 | RF-D05, RF-D06, RN-D04, RN-D05, RN-D06, RNF-D01, IR-D05, ACT-D01 |
| RNF-D01 | RN-D04 |
