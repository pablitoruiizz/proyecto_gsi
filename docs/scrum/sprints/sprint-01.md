# Sprint 1 — Despliegue Base, Estructura Institucional y Portal CADUS V1

**Equipo:** 5 integrantes
**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla)
**Periodo:** 28/09/2026 – 18/10/2026 (entrega CMS V1)
**Estado:** Cerrado. Alcance completado (70 de 70 SP) el 18/10/2026; el Sprint 2 se dedica a las historias de participación (HU-09 a HU-12, HU-19)

## Objetivo del Sprint

Desplegar la plataforma base en WordPress, definir la identidad visual corporativa del CADUS y maquetar las secciones principales de información institucional, directorio de delegaciones y buzón de consultas.

## Reparto de tareas por integrante

> Historias de usuario tomadas del [Product Backlog](../backlog/product-backlog.md); trazabilidad completa con los requisitos en [REM-CADUS.md](../../requisitos/rem-remus/REM-CADUS.md).

### Miembro 1 — Product Owner & Dev Infraestructura
*Configuración base, tema, Git y BD*

| ID | Tarea concreta | SP |
|---|---|---:|
| PB-002 | Instalar/configurar WampServer, crear la BD `bd_cadus`, clonar el repositorio en `www` y preparar `wp-config.php` local. | 5 |
| PB-005 | Compartir el servidor con el equipo mediante Tailscale (WordPress + BD únicos) y documentar el uso de GitHub para el resto de archivos. | 5 |
| PB-006 | Crear el servidor de Discord del equipo (categorías INFO, SCRUM, DESARROLLO y VOZ) y documentarlo en el entorno de trabajo. | 3 |
| PB-007 | Seleccionar, instalar y configurar los plugins obligatorios (seguridad, caché, analítica, SEO) y de apoyo (formularios, campos, roles). | 5 |
| PB-008 | Elaborar el documento REM en REMUS (`CADUS.rem`) con trazabilidad entre requisitos. | 5 |
| HU-13 | Definir y configurar los roles del sitio (Administrador, Ejecutiva, Delegado, Estudiante, Anónimo) y sus capacidades. | 5 |
| HU-18 | Instalar/adaptar el tema base con la identidad visual del CADUS (colores, logotipo, tipografía). | 5 |
| **Subtotal** | | **33** |

### Miembro 2 — Scrum Master & Dev Portada
*Home, comunicados y banner*

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-01 | Crear categorías de noticias (Becas, Movilidad, Normativa, Eventos) y maquetar la portada con el listado de comunicados. | 5 |
| HU-02 | Implementar filtro por categoría y buscador por palabra clave/fecha en la portada. | 3 |
| **Subtotal** | | **8** |

### Miembro 3 — Dev Sección Institucional y Normativa
*Qué es CADUS, gobierno, estatutos y actas*

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-03 | Crear el tipo de contenido "Acta/Normativa" con flujo de estado borrador → aprobada por la Ejecutiva antes de publicarse. | 5 |
| HU-04 | Maquetar el repositorio de actas y normativas descargables, filtrable por fecha y tipo. | 3 |
| **Subtotal** | | **8** |

### Miembro 4 — Dev Directorio de Delegaciones de Alumnos
*Facultades, escuelas y fichas*

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-05 | Crear el tipo de contenido "Delegación" y maquetar el directorio agrupado por Facultad/Escuela. | 5 |
| HU-06 | Implementar la edición de ficha de delegación restringida al delegado asignado o Administrador (RN-04). | 3 |
| **Subtotal** | | **8** |

### Miembro 5 — Dev Atención al Estudiante y Buzón de Consultas
*Formularios, reclamaciones y FAQ*

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-07 | Formulario de consulta/reclamación con verificación de correo `@alum.us.es` (RN-02) y generación de código de ticket único. | 8 |
| HU-08 | Página de seguimiento del ticket por código, con estado e historial de respuestas. | 5 |
| **Subtotal** | | **13** |

**Capacidad total comprometida del Sprint:** 70 SP

## Definición de Hecho (DoD) — Sprint 1

- [ ] WordPress desplegado y accesible en local para los 5 integrantes, con el mismo esquema de BD.
- [ ] Roles y permisos configurados y verificados (Administrador, Ejecutiva, Delegado, Estudiante, Anónimo).
- [ ] Tema institucional aplicado (colores, logotipo, tipografía del CADUS).
- [ ] Portada con comunicados visibles, categorizados y filtrables.
- [ ] Sección institucional con al menos un acta/normativa de ejemplo publicada tras el flujo de aprobación.
- [ ] Directorio de delegaciones visible con al menos una ficha piloto por Facultad/Escuela.
- [ ] Buzón de consultas operativo: envío, generación de ticket y página de seguimiento.
- [ ] Volcado de BD exportado y compartido en `cms-wordpress/backup-db/` siguiendo la convención de nombres.
- [ ] Trazabilidad HU ↔ RF actualizada en el Product Backlog.
- [ ] Sprint Review y Retrospective documentadas.
- [ ] Sin secretos, credenciales ni datos personales reales en el repositorio.

## Plan de gestión de la base de datos (`.sql`)

Procedimiento resumido (guía completa en [`cms-wordpress/backup-db/README.md`](../../../cms-wordpress/backup-db/README.md)):

1. **Base de datos única y compartida:** `bd_cadus` vive en el servidor WampServer del equipo anfitrión y todo el equipo accede a ella mediante **Tailscale**; no hace falta que cada integrante importe un volcado.
2. Durante el sprint: cada integrante edita WordPress directamente desde su navegador, sobre la misma instancia.
3. Antes de un cambio grande o al cerrar una tarea con impacto en BD: exportar un volcado desde phpMyAdmin con la convención `bd_cadus_v<version>_sprint<NN>.sql` (p. ej. `bd_cadus_v1_sprint1.sql`).
4. Subir el volcado a `cms-wordpress/backup-db/` en **GitHub** (copia de seguridad y entrega); hacer `git pull` antes para no coincidir con otro volcado.
5. Los archivos (tema, plugins, documentación) se versionan en GitHub. Ver [entorno de trabajo](../../arquitectura/entorno-de-trabajo.md).

## Resultado del Sprint 1

- **Completado:** 70 de 70 SP. Las tareas técnicas (PB-002, PB-005, PB-006, PB-007, PB-008) se cerraron el 28/09, el 05/10 y el 18/10; las diez historias de usuario de contenido (HU-01 a HU-08, HU-13 y HU-18) se implementaron y probaron el 18/10.
- **Lección para la retrospectiva:** el burndown muestra una caída muy concentrada en el último día. El trabajo de contenido se dejó para el final del sprint; en el Sprint 2 hay que repartir las historias a lo largo de las dos semanas y actualizar el burndown cada día.
- **Calidad:** el código del plugin propio `cadus-portal` se revisó de forma cruzada (ver `cms-wordpress/wp-content/plugins/cadus-portal/README.md`) y se probó en el servidor compartido: validación de dominio del buzón, privacidad del seguimiento, permisos por rol y idempotencia de la configuración.
