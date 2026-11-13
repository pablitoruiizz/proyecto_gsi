# Entorno SharePoint del DMS

Tenant de la Universidad de Sevilla: `https://uses0.sharepoint.com`. Los sitios los creó Pablo con la plantilla «Equipo estándar» (sitio de grupo, privado): tres el 26/10/2026 y el cuarto, CADUS Votaciones, el 13/11/2026. Se configuraron por la API REST de SharePoint desde su sesión (el 30/10 los tres primeros; el 13/11 el cuarto y las columnas de Normativa).

| Sitio | Dirección | Bibliotecas |
|---|---|---|
| CADUS Documentación pública | https://uses0.sharepoint.com/sites/cadus-documentacion-publica | Normativa |
| CADUS Órganos de gobierno | https://uses0.sharepoint.com/sites/cadus-organos-de-gobierno | Actas, Plantillas (plantilla de acta) |
| CADUS Votaciones | https://uses0.sharepoint.com/sites/cadus-votaciones | Votaciones, Plantillas (plantilla de registro de votación) |
| CADUS Atención al estudiante | https://uses0.sharepoint.com/sites/cadus-atencion-al-estudiante | Expedientes |

## Acceso

Los cuatro sitios tienen a Pablo como propietario y, como integrantes (grupo Integrantes, edición), a Joaquín Luna Canela, Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. En CADUS Votaciones los cuatro están en el grupo Integrantes de SharePoint (comprobado el 13/11/2026 por la API); la cabecera del sitio puede seguir mostrando «1 miembro» porque cuenta el grupo de Microsoft 365, no el grupo de SharePoint. Los tres grupos de permisos de cada sitio son los del Lab 4: Propietarios, Integrantes y Visitantes (vacío por ahora).

## Configuración

- **Normativa:** columnas Tipo de documento (obligatoria), Fecha, Curso académico, Estado (obligatoria), Norma (texto, obligatoria) y Versión (número, obligatoria); vista «Vigente». Las dos últimas se añadieron el 13/11/2026 para CU-D07, que se ejecutó ese día con una versión 2 del Reglamento de votaciones (la v1 pasó a Derogada).
- **Actas:** las mismas columnas más Asamblea; aprobación de contenido y borradores visibles solo para autor y aprobadores; vista «Aprobadas».
- **Votaciones (sitio propio desde el 13/11/2026):** columnas comunes más Asamblea, Número de votación, Tipo de voto y Resultado; Asamblea, Número de votación y Tipo de voto son obligatorias (CU-D08); vista «Todas las votaciones». Los permisos son los de los grupos predefinidos del sitio, sin romper la herencia; el grupo Visitantes está vacío. Antes la biblioteca estaba en Órganos de gobierno con permisos exclusivos; se movió porque el Lab 4 concede los permisos sobre el sitio. La biblioteca antigua y su plantilla se enviaron a la papelera de SharePoint (recuperables) tras comprobar el traslado.
- **Plantillas:** en Órganos de gobierno, la plantilla de acta; en Votaciones, la plantilla de registro de votación (27 filas).
- **Expedientes:** columnas comunes más Código, Facultad, Estado, Fecha de resolución (obligatoria) y Fecha de caducidad (calculada, resolución + 2 años); vista «Caducados»; permisos exclusivos (sin Visitantes).
- Documentos de ejemplo ficticios en todas las bibliotecas, sin datos personales ni DNI. **Corregido el 12/11/2026:** los de la carga del 30/10 pesaban 2 bytes (el contenido era `{}`, un fallo de la subida por la API) y no se abrían en Word en línea, en la vista previa ni descargados. Se sustituyeron por Word válidos generados con `scripts/dms/generar_ejemplos_docx.py` (ahora 9: Normativa 4, Actas 2, Votaciones 2 y Expedientes 1), con el mismo nombre y metadatos; el acta aprobada conserva su estado y el borrador sigue en borrador. El archivo «Votacion 1 de la asamblea de noviembre.docx», que subió un compañero con el mismo fallo, no se trasladó al sitio nuevo y quedó en la biblioteca antigua, ya en la papelera.

## Pendiente

- Añadir la cuenta del CADUS (`dcadus@us.es`) como propietaria de los cuatro sitios.
- Añadir a los delegados y estudiantes como visitantes cuando existan sus cuentas, y probar con ellas que un delegado no ve borradores de actas, votaciones ni expedientes.
- Prueba cruzada de cada caso de uso por otra persona del equipo.
- Los miembros del equipo ven también Votaciones y Expedientes (Integrantes); mientras solo contengan documentos de ejemplo no hay datos personales reales.
- Cuando entreguen el portal, añadir la cuenta del CADUS como propietaria de CADUS Votaciones (la cabecera muestra «1 miembro»).
