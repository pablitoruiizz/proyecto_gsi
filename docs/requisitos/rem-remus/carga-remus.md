# Hoja de carga para REMUS — Proyecto CADUS

Contenido de [`REM-CADUS.md`](REM-CADUS.md) organizado en el orden y con los campos que pide **REMUS** (REquirements Manager, Universidad de Sevilla), para pasarlo al archivo `.rem` copiando y pegando.

> [!NOTE]
> Un `.rem` es una base de datos de Microsoft Access (formato Jet), no un texto: solo se puede crear y editar desde el propio REMUS. Por eso este documento es la **fuente de la que se carga el `.rem`**, y se actualiza cuando cambien los requisitos. Versión de partida: **0.1**, 05/10/2026.

## Cómo crear el `.rem`

1. Clonar o descargar [REMUS](https://github.com/amador-duran-toro/remus) y ejecutar `bin/remus.exe` (Windows).
2. Descargar la plantilla vacía en español: [`base/remus_base_empty_spanish.rem`](https://raw.githubusercontent.com/amador-duran-toro/remus/master/base/remus_base_empty_spanish.rem) (guardar como `CADUS.rem` y no editar la original).
3. Abrir `CADUS.rem` en REMUS e introducir las secciones de este documento en el orden indicado (apartados 1 a 8).
4. Guardar en `docs/requisitos/rem-remus/CADUS.rem` y exportar el HTML si la entrega lo pide.

> [!WARNING]
> `CADUS.rem` es un archivo binario: Git no puede fusionar cambios de dos personas. **Una sola persona (el Product Owner) edita el `.rem`**; el resto propone cambios en este documento o en `REM-CADUS.md`. Antes de subirlo, `git pull`, y no pisar la versión de otra persona.

## Valores comunes a todos los requisitos

| Campo REMUS | Valor de partida |
|---|---|
| Versión | 0.1 (mayor 0, menor 1) |
| Fecha | 05/10/2026 |
| Autores | Equipo del proyecto (5 integrantes) |
| Fuentes | CADUS — Delegación General |
| Estado | En construcción |
| Estabilidad | Media |
| Importancia | Vital / Importante, según la tabla de cada apartado (los nombres exactos son los del desplegable de REMUS) |
| Urgencia | Inmediatamente (Sprint 1) · Hay presión (Sprint 2) · Puede esperar (Sprint 3 y 4) |

## 1. Organización

| Campo | Valor |
|---|---|
| Nombre | CADUS — Consejo de Alumnos de la Universidad de Sevilla |
| Dirección | Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla |
| Correo | cadus@us.es |
| Teléfono / Fax | — |

## 2. Stakeholders

| Nombre | Rol | Desarrollador | Cliente | Usuario |
|---|---|---|---|---|
| Delegación General del CADUS | Cliente / usuario de la Ejecutiva | No | Sí | Sí |
| `[Nombre Apellido 1]` | Scrum Master & Dev Infraestructura | Sí | No | No |
| `[Nombre Apellido 2]` | Product Owner & Dev Portada | Sí | No | No |
| `[Nombre Apellido 3]` | Dev Sección Institucional y Normativa | Sí | No | No |
| `[Nombre Apellido 4]` | Dev Directorio de Delegaciones | Sí | No | No |
| `[Nombre Apellido 5]` | Dev Atención al Estudiante y Buzón | Sí | No | No |

## 3. Actores

| ID | Nombre | Rol / descripción |
|---|---|---|
| ACT-01 | Usuario Anónimo | Visitante sin autenticar. Accede a contenido público: noticias, actas publicadas, directorio, calendario. |
| ACT-02 | Estudiante US | Usuario con correo institucional `@alum.us.es`. Puede enviar consultas, reclamaciones y solicitudes de mediación. |
| ACT-03 | Representante/Delegado de Centro | Estudiante responsable de una delegación; mantiene la ficha de su Facultad/Escuela. |
| ACT-04 | Miembro de la Ejecutiva del CADUS | Aprueba y publica actas/normativas, gestiona el buzón y las convocatorias. |
| ACT-05 | Administrador Web | Gestiona usuarios, roles, categorías y configuración técnica. |

## 4. Objetivos

> Derivados por el equipo del encargo del proyecto (modernizar el portal del CADUS). Pendientes de validar con el cliente.

| ID | Nombre | Descripción | Importancia |
|---|---|---|---|
| OBJ-01 | Modernizar el portal institucional | Rehacer `www.cadus.us.es` con un portal actual, accesible y adaptado a móvil. | Vital |
| OBJ-02 | Informar a los estudiantes | Difundir noticias y comunicados categorizados por áreas (Becas, Movilidad, Normativa, Eventos). | Vital |
| OBJ-03 | Dar transparencia institucional | Publicar actas de plenos y normativas, previa aprobación de la Ejecutiva. | Vital |
| OBJ-04 | Dar visibilidad a las delegaciones | Ofrecer un directorio de Delegaciones de Alumnos por Facultad/Escuela. | Importante |
| OBJ-05 | Atender al estudiante | Habilitar un buzón de consultas y reclamaciones con seguimiento, y facilitar la mediación estudiantil. | Vital |
| OBJ-06 | Fomentar la participación | Dar acceso al calendario de asambleas, eventos y votaciones. | Importante |

## 5. Requisitos de información

Los tiempos de vida y las ocurrencias están **por estimar** (marcar como TBD en REMUS).

| ID | Nombre | Concepto relevante | Datos específicos | Importancia |
|---|---|---|---|---|
| RI-01 | Entrada de noticia | Noticia o comunicado publicado por el CADUS | título, cuerpo, categoría, fecha de publicación, autor, estado (borrador/publicada) | Vital |
| RI-02 | Acta/Documento | Acta de pleno o normativa en PDF | tipo (acta/normativa), fecha, archivo PDF, estado de aprobación, pleno asociado | Vital |
| RI-03 | Delegación | Delegación de alumnos de una Facultad/Escuela | Facultad/Escuela, delegado responsable, contacto, horario de atención | Importante |
| RI-04 | Consulta/Ticket | Consulta o reclamación de un estudiante | código de seguimiento, remitente, asunto, estado, historial de respuestas, nivel de confidencialidad | Vital |
| RI-05 | Categoría | Clasificación temática de noticias y documentos | nombre, tipo de contenido asociado (noticia o documento) | Importante |
| RI-06 | Usuario/Rol | Persona con cuenta en el sitio | nombre, correo institucional, rol asignado, delegación asociada (si aplica) | Vital |

## 6. Requisitos funcionales

| ID | Nombre | Descripción | Historia(s) | Importancia | Urgencia |
|---|---|---|---|---|---|
| RF-01 | Publicar noticias categorizadas | El sistema debe permitir publicar noticias/comunicados categorizados por área (Becas, Movilidad, Normativa, Eventos). | HU-01 | Vital | Inmediatamente |
| RF-02 | Filtrar y buscar noticias | El sistema debe permitir filtrar y buscar noticias por categoría, fecha y palabra clave. | HU-02, HU-16 | Importante | Inmediatamente |
| RF-03 | Repositorio de actas | El sistema debe ofrecer un repositorio de actas de plenos descargables en PDF. | HU-03, HU-04 | Vital | Inmediatamente |
| RF-04 | Repositorio de normativas | El sistema debe ofrecer un repositorio de normativas y reglamentos descargables en PDF. | HU-04 | Vital | Inmediatamente |
| RF-05 | Aprobación previa de documentos | El sistema debe requerir la aprobación de un miembro de la Ejecutiva antes de publicar cualquier acta o normativa. | HU-03 | Vital | Inmediatamente |
| RF-06 | Directorio de delegaciones | El sistema debe mostrar un directorio interactivo de Delegaciones de Alumnos por Facultad/Escuela. | HU-05 | Vital | Inmediatamente |
| RF-07 | Ficha de delegación | El sistema debe permitir gestionar la ficha de cada delegación (contacto, horario de atención, enlaces). | HU-06 | Importante | Inmediatamente |
| RF-08 | Buzón de consultas y reclamaciones | El sistema debe ofrecer un buzón digital de consultas y reclamaciones académicas. | HU-07 | Vital | Inmediatamente |
| RF-09 | Código de seguimiento | El sistema debe generar un código/ticket de seguimiento único para cada consulta enviada. | HU-07, HU-08 | Vital | Inmediatamente |
| RF-10 | Gestión de tickets | El sistema debe ofrecer un panel de gestión y respuesta de tickets para la Ejecutiva. | HU-09 | Vital | Hay presión |
| RF-11 | Calendario | El sistema debe mostrar un calendario de asambleas, eventos y votaciones estudiantiles. | HU-10 | Importante | Hay presión |
| RF-12 | Convocatorias de votación | El sistema debe permitir publicar convocatorias de votación vinculadas a una asamblea del calendario. | HU-11 | Importante | Hay presión |
| RF-13 | Solicitud de mediación | El sistema debe ofrecer un formulario de solicitud de mediación estudiantil. | HU-12 | Importante | Hay presión |
| RF-14 | Roles y permisos | El sistema debe gestionar roles y permisos diferenciados (Anónimo, Estudiante, Delegado, Ejecutiva, Administrador). | HU-13 | Vital | Inmediatamente |
| RF-15 | Panel de administración | El sistema debe ofrecer un panel de administración de contenidos (CRUD de noticias, actas y delegaciones) restringido por rol. | HU-19 | Vital | Hay presión |

## 7. Requisitos no funcionales

| ID | Nombre | Descripción | Importancia |
|---|---|---|---|
| RNF-01 | Rendimiento | Tiempo de carga de página inferior a 3 s en condiciones estándar de red del campus. | Importante |
| RNF-02 | Usabilidad móvil | Diseño responsive, funcional en móviles y tablets. | Vital |
| RNF-03 | Accesibilidad | Cumplimiento de WCAG 2.1 nivel AA. | Importante |
| RNF-04 | Seguridad en formularios | Validación y sanitización de entradas, protección frente a spam e inyección. | Vital |
| RNF-05 | Compatibilidad técnica | PHP 8.x y MySQL 8.x sobre servidor Apache local (WampServer; compatible con XAMPP). | Importante |
| RNF-06 | Disponibilidad | Estabilidad del entorno durante periodos críticos (matrícula, asambleas, votaciones). | Importante |
| RNF-07 | Mantenibilidad | Configuración y código documentados para facilitar el relevo entre cursos del CADUS. | Importante |
| RNF-08 | Privacidad | Tratamiento de datos de consultas/reclamaciones conforme a RGPD. | Vital |

## 8. Restricciones (reglas de negocio y del proyecto)

| ID | Nombre | Descripción |
|---|---|---|
| RN-01 | Aprobación de documentos | Toda acta o normativa requiere aprobación de un miembro de la Ejecutiva antes de publicarse. |
| RN-02 | Correo institucional | Solo se aceptan consultas y reclamaciones enviadas desde correo `@alum.us.es`. |
| RN-03 | Privacidad de reclamaciones | Las reclamaciones son visibles solo para el remitente y la Ejecutiva. |
| RN-04 | Edición de fichas | Cada ficha de delegación solo puede ser editada por su delegado asignado o un Administrador. |
| RN-05 | Votaciones vinculadas | Toda votación del calendario debe estar vinculada a una convocatoria de asamblea previa. |
| RC-01 | Entorno compartido con Tailscale | WordPress y la base de datos `bd_cadus` se alojan en un único servidor local (WampServer) al que accede todo el equipo mediante **Tailscale** (VPN privada), trabajando a la vez sobre la misma instancia. Acceso limitado a la red de Tailscale, cuentas de WordPress individuales y puerto de BD no expuesto. Disponible solo con el equipo anfitrión encendido. |
| RC-02 | Gestión de configuración con GitHub | Todo el contenido en forma de archivo (tema, plugins, documentación, SCRUM, REM, maquetas) se versiona en GitHub. No se versionan `wp-config.php`, `wp-content/uploads/` ni credenciales. Los volcados de BD son copia de seguridad y de entrega, no mecanismo de sincronización. |

## 9. Trazabilidad (enlaces que crear en REMUS)

En REMUS se crean desde la matriz de trazabilidad (origen → destino).

| Origen | Destino |
|---|---|
| OBJ-01 | RNF-01, RNF-02, RNF-03, RNF-05 |
| OBJ-02 | RF-01, RF-02, RI-01, RI-05 |
| OBJ-03 | RF-03, RF-04, RF-05, RI-02, RN-01 |
| OBJ-04 | RF-06, RF-07, RI-03, RN-04 |
| OBJ-05 | RF-08, RF-09, RF-10, RF-13, RI-04, RN-02, RN-03, RNF-04, RNF-08 |
| OBJ-06 | RF-11, RF-12, RN-05 |
| RF-14 | RI-06, ACT-01, ACT-02, ACT-03, ACT-04, ACT-05 |
| RF-15 | RI-01, RI-02, RI-03 |
| RC-01, RC-02 | RNF-06, RNF-07 |

## Pendiente de completar

- Nombres reales de los stakeholders del equipo.
- Estimar tiempos de vida y ocurrencias de los requisitos de información.
- Casos de uso (REMUS los modela con precondición, postcondición, evento disparador y pasos): se añadirán a medida que se implementen las historias de usuario.
- Validar los objetivos con el cliente.
