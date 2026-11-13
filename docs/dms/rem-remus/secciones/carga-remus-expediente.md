# Hoja de carga para REMUS — DMS del CADUS · Expediente

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/dms_expediente_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [DMS-Expediente.rem](DMS-Expediente.rem) (REMUS), versión 1.1, 2026-11-12. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

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

## 4. Requisitos de información

| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |
|---|---|---|---|
| IR-D04 | Expediente | a una reclamación o mediación resuelta, con estos datos: | Código del ticket (CAD) o de la mediación (MED); Facultad; Fecha de resolución; Fecha de caducidad (resolución más 2 años) |

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
| RF-D07 | Fecha de caducidad calculada | calcular la fecha de caducidad de un expediente como su fecha de resolución más 2 años | DMS-HU-06 | Vital |
| RF-D08 | Expedientes caducados | mostrar los expedientes cuya fecha de caducidad es anterior a hoy para retirarlos | DMS-HU-06 | Vital |

## 8. Casos de uso

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

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| RNF-D04 | Conservación | conservar los expedientes 2 años desde su resolución y retirarlos en la primera revisión mensual posterior, de modo que el plazo máximo real es de 2 años y un mes (excepción aceptada por la periodicidad mensual de la revisión) | Vital |

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-D02 | Expedientes privados | Los expedientes de reclamaciones y mediaciones solo los ve la Ejecutiva (coherente con RN-03 del portal). |
| RN-D03 | Conservación de 2 años | Un expediente se retira en la primera revisión mensual posterior al cumplimiento de los 2 años desde su resolución, así que se conserva como máximo 2 años y un mes. Retirar significa eliminar el documento, sus versiones y su copia en la papelera de reciclaje. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-D01 | SharePoint de la Universidad de Sevilla | El DMS se construye en SharePoint de Microsoft 365 de la Universidad de Sevilla (uses0.sharepoint.com), con sitios, bibliotecas, columnas de metadatos, vistas y los grupos Propietarios, Integrantes y Visitantes. Los cuatro sitios (cadus-documentacion-publica, cadus-organos-de-gobierno, cadus-votaciones y cadus-atencion-al-estudiante) los creó Pablo; los otros cuatro integrantes son miembros de los tres primeros. |
| RC-D02 | Acceso con correo corporativo | Los estudiantes acceden con su correo corporativo @alum.us.es; cada delegado, con la cuenta de su delegación (correo institucional de la delegación, decisión del CADUS del 09/11/2026); la Ejecutiva, con la cuenta única del CADUS (dcadus@us.es). |
| RC-D03 | Documentación independiente | La documentación del DMS (requisitos, análisis, diseño, implementación y seguimiento SCRUM) es independiente de la del portal web. Se guarda en docs/dms del repositorio de GitHub y la coordinación diaria se hace en Discord. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-D01 | RF-D01, IR-D04 |
| OBJ-D02 | RF-D02 |
| OBJ-D03 | RF-D07, RF-D08, RNF-D04, RN-D02, RN-D03 |
| CU-D04 | RF-D01, RF-D02, RF-D07, RN-D02, IR-D04, ACT-D01 |
| CU-D05 | RF-D07, RF-D08, RN-D03, RNF-D04, ACT-D01 |
