# CADUS Portal (plugin propio)

Plugin de WordPress del equipo que implementa las historias de usuario del Sprint 1 sobre WordPress 7.1 y PHP 8.x. Es el único plugin que se versiona en Git (los de terceros viven en el servidor compartido; ver `cms-wordpress/.gitignore`).

## Estructura

| Archivo | Contenido | Historias · requisitos |
|---|---|---|
| `cadus-portal.php` | Cabecera del plugin y carga de módulos | — |
| `includes/roles.php` | Roles `cadus_ejecutiva`, `cadus_delegado`, `cadus_estudiante` y capacidades de los tipos propios | HU-13 · RF-14 · RN-01, RN-03, RN-04 |
| `includes/contenidos.php` | Actas y normativas, delegaciones, campos ACF, directorio y listado de actas | HU-03 a HU-06 · RF-03 a RF-07 · IR-04, IR-05 · UI-03, UI-05 |
| `includes/buzon.php` | Formulario del buzón, tickets privados, código de seguimiento y consulta de estado (**escrito por Codex**) | HU-07, HU-08 · RF-08, RF-09 · RN-02, RN-03 · UI-04 |
| `includes/setup.php` | Páginas, menú, noticias de ejemplo, tema Blocksy, paleta y logotipo provisional | HU-01, HU-02, HU-18 · RF-01, RF-02 · UI-01, UI-02 |
| `assets/` | Logotipo provisional y PDF de ejemplo | — |

## Roles y permisos (probados en el servidor)

| Capacidad | Administrador | Ejecutiva | Delegado | Estudiante |
|---|:-:|:-:|:-:|:-:|
| Publicar actas y normativas (RN-01) | sí | sí | no | no |
| Ver y gestionar tickets del buzón (RN-03) | sí | sí | no | no |
| Editar delegaciones propias (RN-04) | sí | sí | sí | no |
| Editar delegaciones ajenas | sí | sí | no | no |

Un delegado solo edita las delegaciones de las que es autor. Quien no puede publicar un acta solo puede guardarla como «Pendiente de revisión».

## Shortcodes

| Shortcode | Uso |
|---|---|
| `[cadus_ultimas_noticias n="3"]` | Comunicados recientes (portada) |
| `[cadus_noticias]` | Listado con filtro por categoría, año y palabra clave |
| `[cadus_actas]` | Tabla de actas y normativas con filtro por tipo y descarga en PDF |
| `[cadus_directorio]` | Directorio de delegaciones agrupado por facultad o escuela |
| `[cadus_buzon]` | Formulario del buzón (Fluent Forms) con aviso de privacidad |
| `[cadus_seguimiento]` | Consulta del estado de un ticket con código y correo |

## Cómo se configura el sitio

Al **activar** el plugin se ejecuta `cadus_portal_activar()`: crea o completa los roles, fija los enlaces por nombre, registra los tipos de contenido y siembra páginas, menú, noticias, actas y delegaciones de ejemplo.

- **Idempotente:** volver a activarlo no duplica nada. Cada elemento sembrado lleva la marca `_cadus_semilla`, de modo que renombrar un ejemplo no provoca que se vuelva a crear.
- **Ajustes iniciales solo la primera vez:** tema, paleta, logotipo, descripción, ubicación del menú y portada se aplican únicamente en la primera activación; después no se pisan los cambios del equipo.
- **Contenido de ejemplo:** los textos están marcados como «ejemplo» y deben sustituirse por contenido real validado con el cliente.

Requisitos: ACF, Fluent Forms y el tema Blocksy instalados, `mod_rewrite` activo y el `.htaccess` de WordPress.

## Decisiones técnicas

- **Aprobación de actas (RN-01)** con los estados nativos de WordPress y una capacidad propia `publish_cadus_actas`, sin plugin de flujo de trabajo adicional.
- **Código del ticket** `CAD-AAAA-NNNNN` derivado del ID único del ticket: no se repite aunque se envíen formularios a la vez. No es correlativo y es predecible, por lo que el seguimiento exige código **y** correo, con un límite de 10 intentos por IP cada 15 minutos.
- **Validación del correo `@alum.us.es` en servidor** (RN-02), además de la del navegador.
- **Los tickets no son públicos** (`public => false`, sin REST) y solo los ven quienes tienen permisos sobre ellos (RN-03).

## Revisión cruzada (Claude y Codex)

El trabajo se repartió: Claude escribió roles, contenidos y configuración; Codex escribió el buzón. Después cada uno revisó el código del otro.

| Revisó | Hallazgos | Resultado |
|---|---|---|
| Codex sobre el código de Claude | 9 (5 de severidad media con efecto real) | Corregidos: error 500 con `?tipo[]=`, borrado del contenido por defecto en cada activación, ajustes del equipo sobrescritos al reactivar, ejemplos recreados al renombrarlos, búsqueda de noticias que incluía páginas y actas, actas sin fecha omitidas y sin paginación, enlace al PDF perdido sin ACF, orden de enlaces y rol borrado y recreado en cada activación |
| Claude sobre el código de Codex | Sin fallos bloqueantes | Verificado que `FLUENTFORM` existe, que WP Fastest Cache respeta `DONOTCACHEPAGE` y que los ganchos de Fluent Forms existen; prueba funcional completa del buzón (rechazo de correo ajeno, código mostrado al estudiante, seguimiento con código y correo correctos y respuesta genérica con un correo incorrecto) |
