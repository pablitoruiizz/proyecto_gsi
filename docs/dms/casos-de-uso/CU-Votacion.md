# Casos de uso — Registro de votación

DMS del CADUS · Lab 4 · Universidad de Sevilla (GSI) · versión 1.1 · Autor: Álvaro Martínez Ocaña · Prueba cruzada: pendiente

## 1. Documento

Un registro de votación es el documento que deja la Ejecutiva del CADUS tras una votación presencial de asamblea, con un voto por delegación (27 delegaciones). No guarda el DNI de nadie y, si la votación es secreta, solo guarda el recuento total, sin vincular el voto a ninguna delegación. Solo lo ve la Ejecutiva.

| Dato | Valor |
|---|---|
| Sitio de SharePoint | CADUS Órganos de gobierno |
| Biblioteca | Votaciones |
| Casos de uso | CU-D06 Registrar el resultado de una votación presencial (Ejecutiva) y CU-D08 Consultar los registros de votaciones anteriores (Ejecutiva) |
| Reglas de negocio | RN-D04 Sin DNI y voto secreto separado del voto de cada delegación, RN-D05 Un voto por delegación y RN-D06 Tipo de documento rellenado en todos los documentos |
| Requisitos | RF-D01, RF-D02, RF-D05, RF-D06, RF-D09, IR-D05 y RNF-D01 |
| Documentos de ejemplo | Votación 1 (nominal, ejemplo).docx y Votación 2 (secreta, ejemplo).docx, de la asamblea de octubre, y un tercer registro de ejemplo de la asamblea de noviembre creado el 12/11/2026 para probar el filtrado |

## 2. Metadatos

| Metadato | Tipo de columna | Obligatorio |
|---|---|---|
| Tipo de documento | Elección (Votación) | Sí |
| Fecha | Fecha | Sí |
| Curso académico | Elección | No |
| Asamblea | Texto de una línea | Sí (desde el 12/11/2026) |
| Número de votación | Número (sin decimales) | Sí (desde el 12/11/2026) |
| Tipo de voto | Elección (Nominal, Secreto) | Sí |
| Resultado | Elección (Aprobada, Rechazada) | No |

«Asamblea» y «Número de votación» pasan a ser obligatorias porque identifican cada registro: una asamblea puede tener varias votaciones numeradas (RN-D05) y sin esos dos datos no se puede buscar ni distinguir un registro de otro (CU-D08).

## 3. Permisos

| Rol | Qué ve en Votaciones |
|---|---|
| Ejecutiva (Propietarios, cuenta del CADUS) | Control total: crea, edita, consulta y elimina registros. |
| Equipo del proyecto (Integrantes) | Editar, solo mientras se trabaja con datos de ejemplo. |
| Delegado (Visitantes, con la cuenta de su delegación) | Nada: la biblioteca tiene permisos exclusivos y no incluye el grupo Visitantes. |
| Estudiante | Nada: solo es visitante del sitio Documentación pública. |

La biblioteca rompe la herencia de permisos del sitio: «Esta biblioteca tiene permisos exclusivos». Conserva solo Propietarios (control total) e Integrantes (editar) y no incluye el grupo Visitantes, en el que irán los delegados (RF-D06, RN-D04).

## 4. Casos de uso

### CU-D06 Registrar el resultado de una votación presencial

| Campo | Contenido |
|---|---|
| Actor | Ejecutiva del CADUS |
| Cuándo | En cada asamblea con votación. |
| Escenario | En la asamblea de octubre se celebra la votación número 1, nominal. La Ejecutiva crea el registro a partir de la plantilla, marca qué delegaciones estaban presentes y si se comprobó su identidad, anota el voto de cada una y el resultado. |
| Precondición | Se ha celebrado la votación y se ha comprobado la identidad de los delegados presentes. |
| Postcondición | Queda constancia del resultado sin guardar el DNI. |

**Pasos**

1. La Ejecutiva del CADUS crea el registro a partir de la plantilla en la biblioteca Votaciones.
2. El sistema muestra una fila por cada delegación para indicar si está presente y si se comprobó su identidad.
3. La Ejecutiva del CADUS marca la presencia y la identidad de cada delegación y el tipo de voto.
4. El sistema, si el voto es nominal, solicita el voto de cada delegación; si es secreto, solo el recuento total.
5. La Ejecutiva del CADUS introduce el resultado.
6. El sistema guarda el registro visible solo para la Ejecutiva, sin números de DNI.

**Requisitos relacionados:** RF-D01, RF-D02, RF-D09, RN-D04, RN-D05, IR-D05 y ACT-D01.

### CU-D08 Consultar los registros de votaciones anteriores

| Campo | Contenido |
|---|---|
| Actor | Ejecutiva del CADUS |
| Cuándo | Cuando necesita comprobar qué se decidió en una votación de una asamblea anterior. |
| Escenario | Antes de la asamblea de noviembre, la Ejecutiva quiere saber qué se decidió en la votación nominal de la asamblea de octubre. Abre Votaciones, filtra por asamblea y por tipo de voto y abre el registro. |
| Precondición | Existen registros de votación guardados y quien consulta es miembro de la Ejecutiva. |
| Postcondición | La Ejecutiva ha abierto el registro de votación que buscaba. |

**Pasos**

1. La Ejecutiva del CADUS abre la biblioteca Votaciones.
2. El sistema muestra la vista plana con todos los registros, solo a la Ejecutiva.
3. La Ejecutiva del CADUS filtra por asamblea y por tipo de voto.
4. El sistema muestra los registros que cumplen los filtros, identificados por su asamblea y su número de votación.
5. La Ejecutiva del CADUS abre el registro.

**Requisitos relacionados:** RF-D05, RF-D06, RN-D04, RN-D05, RN-D06, RNF-D01 y ACT-D01.

## 5. Implementación en SharePoint

![Biblioteca Votaciones con las columnas propias del registro de votación.](../capturas/06-votaciones.jpg)

La biblioteca Votaciones añade a las columnas comunes las de Asamblea, Número de votación, Tipo de voto (Nominal o Secreto) y Resultado. Los registros de ejemplo no contienen números de DNI y, en el de voto secreto, solo el recuento total. Corresponde a CU-D06, RN-D04 y RN-D05 (DMS-HU-07). En la biblioteca «Plantillas» del mismo sitio hay una plantilla de acta y otra de registro de votación con una fila por cada una de las 27 delegaciones (RF-D09).

![Permisos exclusivos de la biblioteca Votaciones.](../capturas/07-permisos-votaciones.jpg)

La biblioteca rompe la herencia de permisos y no incluye el grupo Visitantes, para que los delegados no vean los registros de votación (RF-D06, RN-D04).

![Columna Asamblea: «Esta columna debe contener información» en Sí.](../capturas/13a-votaciones-asamblea-obligatoria.jpg)

![Columna Número de votación: «Esta columna debe contener información» en Sí.](../capturas/13b-votaciones-numero-obligatorio.jpg)

Las columnas «Asamblea» y «Número de votación» son obligatorias desde el 12/11/2026, de modo que todo registro nuevo queda identificado y se puede encontrar en CU-D08 (RN-D05, RN-D06). «Tipo de voto» ya lo era.

![CU-D08: vista de Votaciones filtrada por asamblea y por tipo de voto.](../capturas/14-votaciones-consulta.jpg)

Con los filtros de las cabeceras «Asamblea» (Asamblea de octubre) y «Tipo de voto» (Nominal) la lista se reduce a un único registro: la votación 1 de la asamblea de octubre, nominal, aprobada. Son los pasos 2 a 4 de CU-D08 (RF-D05).

![CU-D08: el registro encontrado, identificado por su nombre.](../capturas/14b-votaciones-consulta-nombre.jpg)

La misma lista filtrada muestra el nombre del documento («Votación 1 de la asamblea del 26-10-2026…»). Es el registro que se abre en el paso 5.

## 6. Pruebas

| Fecha | Quién | Qué | Resultado |
|---|---|---|---|
| 12/11/2026 | Álvaro | Hacer obligatorias «Asamblea» y «Número de votación» en la biblioteca Votaciones | OK. Las dos columnas tienen «Esta columna debe contener información» en Sí (capturas 13a y 13b). |
| 12/11/2026 | Álvaro | CU-D08 pasos 1 a 4, con la cuenta de un miembro del sitio (Integrantes). Se parte de 3 registros: 2 de la asamblea de octubre (votación 1 nominal y votación 2 secreta) y 1 de la asamblea de noviembre. | OK. Con el filtro «Asamblea de octubre» quedan 2 registros; al añadir «Tipo de voto: Nominal» queda 1, la votación 1 de octubre (capturas 14 y 14b). |
| 12/11/2026 | Álvaro | CU-D08 paso 5: abrir el registro | FALLO ABIERTO. El registro se localiza con los filtros, pero su contenido no se pudo abrir: Word en línea dice «No se puede abrir este documento para editarlo», la vista previa de SharePoint dice «No se puede obtener una vista previa de este archivo» y tampoco se abre al descargarlo. Los documentos de ejemplo los creó Pablo por la API: hay que comprobar si son ficheros Word válidos. |
| Pendiente | Otra persona del equipo | CU-D08 completo, con la cuenta propietaria (el reparto pide la cuenta propietaria; la prueba del 12/11 se hizo con una cuenta de miembro) | PENDIENTE |
| Pendiente | Equipo | CU-D06: crear un registro desde la plantilla y comprobar que no guarda DNI y que en el voto secreto no hay voto por delegación | PENDIENTE: no se ha ejecutado de principio a fin. |
| Pendiente | Álvaro | Rol estudiante y rol delegado: no ven la biblioteca Votaciones ni por enlace directo | PENDIENTE: falta la cuenta de visitante. |

**Limitaciones**

- La prueba de CU-D08 se hizo con la cuenta de un miembro del sitio, no con la propietaria.
- Los documentos de ejemplo no se abren (ni en el navegador, ni en vista previa, ni descargados), por lo que el paso 5 de CU-D08 no se ha podido completar. Es un problema de los ficheros de ejemplo, no de los filtros ni de los permisos.
- Los registros son de ejemplo y no contienen datos personales ni DNI.
- El tercer registro (asamblea de noviembre) se creó solo para probar el filtrado.
