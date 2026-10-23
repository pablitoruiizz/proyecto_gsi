# CADUS Portal (plugin propio)

Plugin de WordPress del equipo que implementa las historias de usuario del Sprint 1 sobre WordPress 7.1 y PHP 8.x. Es el único plugin que se versiona en Git (los de terceros viven en el servidor compartido; ver `cms-wordpress/.gitignore`).

## Estructura

| Archivo | Contenido | Historias · requisitos |
|---|---|---|
| `cadus-portal.php` | Cabecera del plugin y carga de módulos | — |
| `includes/roles.php` | Roles `cadus_ejecutiva`, `cadus_delegado`, `cadus_estudiante` y capacidades de los tipos propios | HU-13 · RF-14 · RN-01, RN-03, RN-04 |
| `includes/admin.php` | Menús, barra superior y destino de inicio de sesión por rol | HU-19a |
| `includes/contenidos.php` | Actas y normativas, delegaciones, campos ACF, directorio y listado de actas | HU-03 a HU-06 · RF-03 a RF-07 · IR-04, IR-05 · UI-03, UI-05 |
| `includes/buzon.php` | Formulario del buzón, tickets privados, código de seguimiento y consulta de estado (**escrito por Codex**) | HU-07, HU-08 · RF-08, RF-09 · RN-02, RN-03 · UI-04 |
| `includes/setup.php` | Páginas, menú, noticias de ejemplo, tema Blocksy, paleta y logotipo provisional | HU-01, HU-02, HU-18 · RF-01, RF-02 · UI-01, UI-02 |
| `includes/calendario.php` | Integración con The Events Calendar: próximos eventos en la portada, «Calendario» en el menú y en los accesos, permisos de eventos para el Ejecutivo y su menú de administración | HU-10 · RF-11 · UI-02 |
| `includes/escritorio.php` | Panel «Accesos rápidos del CADUS» en el Escritorio, con tarjetas según los permisos de cada rol (actas pendientes, delegaciones propias, cifras de tickets sin datos personales) | HU-19b · RF-15 · RN-01, RN-03, RN-04 |
| `assets/` | Logotipo provisional y PDF de ejemplo | — |

## Roles y permisos (probados en el servidor)

| Capacidad | Administrador | Ejecutivo | Delegado | Estudiante |
|---|:-:|:-:|:-:|:-:|
| Publicar actas y normativas (RN-01) | sí | sí | no | no |
| Ver y gestionar tickets del buzón (RN-03) | sí | sí | no | no |
| Editar delegaciones propias (RN-04) | sí | sí | sí | no |
| Editar delegaciones ajenas | sí | sí | no | no |

Un delegado solo edita las delegaciones de las que es autor. Quien no puede publicar un acta solo puede guardarla como «Pendiente de revisión».

### Administración por rol (HU-19a)

- **Ejecutivo del CADUS** (`cadus_ejecutiva`): Escritorio, Entradas, Páginas, Medios, Actas, Delegaciones, Tickets y Perfil.
- **Delegado**: Escritorio, Delegaciones, Medios (incluida la subida de foto/PDF) y Perfil.
- **Estudiante**: solo Perfil.

Los menús y submenús se filtran mediante listas cerradas en `admin_menu` (prioridad 999). Se conservan los listados, la creación y las taxonomías correspondientes, según las capacidades existentes. La barra superior también usa una lista cerrada: cuenta, salida, navegación al sitio y creación de los contenidos permitidos. Los accesos de terceros quedan ocultos por defecto. Los filtros no se aplican a administradores, usuarios con varios roles ni roles ajenos al portal. No se añaden widgets ni accesos al Escritorio (HU-19b va aparte).

Sin un `redirect_to` explícito, el delegado inicia sesión en Delegaciones y el ejecutivo en el Escritorio. Los demás destinos conservan el comportamiento previo.

Ocultar menús no sustituye los permisos de WordPress. Se retira `moderate_comments` al rol ejecutivo, pero WordPress también permite gestionar comentarios con `edit_posts` y `edit_comment`: por eso se bloquean las pantallas `edit-comments.php` y `comment.php` (403), y se deniega `edit_comment` a los usuarios con un único rol CADUS. No se desactivan los comentarios públicos del sitio. La retirada de la capacidad del rol afecta a todos sus miembros; los usuarios multirrol conservan las capacidades que reciban de sus otros roles.

La migración de roles se ejecuta en `init` (prioridad 5) únicamente si `cadus_roles_version` difiere de `CADUS_ROLES_VERSION` (`'2'`). Actualiza el nombre visible sin cambiar el identificador, mantiene capacidades personalizadas salvo la retirada explícita y guarda la versión al terminar. La activación llama al mismo registro idempotente y también guarda esa versión; no hace falta reactivar ni ejecutar la siembra para migrar un sitio existente.

Comprobación manual: probar los tres roles, un administrador y un usuario multirrol; revisar menús y barra tanto en administración como en la web, subida de medios del delegado, destinos de login con/sin `redirect_to` y rechazo de las URL de comentarios. Tras el primer acceso, verificar `cadus_roles_version = '2'`, el nombre «Ejecutivo del CADUS» y la ausencia de `moderate_comments` en ese rol.

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
- **Código del ticket** `CAD-AAAA-ID-32hex`: ID único y 128 bits aleatorios. Los códigos anteriores `CAD-AAAA-ID` siguen siendo compatibles. El seguimiento exige código **y** correo, con un límite de 10 intentos por IP cada 15 minutos.
- **Validación del correo `@alum.us.es` en servidor** (RN-02), además de la del navegador.
- **Los tickets no son públicos** (`public => false`, sin REST) y solo los ven quienes tienen permisos sobre ellos (RN-03).

## Revisión cruzada (Claude y Codex)

El trabajo se repartió: Claude escribió roles, contenidos y configuración; Codex escribió el buzón. Después cada uno revisó el código del otro.

| Revisó | Hallazgos | Resultado |
|---|---|---|
| Codex sobre el código de Claude | 9 (5 de severidad media con efecto real) | Corregidos: error 500 con `?tipo[]=`, borrado del contenido por defecto en cada activación, ajustes del equipo sobrescritos al reactivar, ejemplos recreados al renombrarlos, búsqueda de noticias que incluía páginas y actas, actas sin fecha omitidas y sin paginación, enlace al PDF perdido sin ACF, orden de enlaces y rol borrado y recreado en cada activación |
| Claude sobre el código de Codex | Sin fallos bloqueantes | Verificado que `FLUENTFORM` existe, que WP Fastest Cache respeta `DONOTCACHEPAGE` y que los ganchos de Fluent Forms existen; prueba funcional completa del buzón (rechazo de correo ajeno, código mostrado al estudiante, seguimiento con código y correo correctos y respuesta genérica con un correo incorrecto) |

## Identidad visual (HU-18)

Paleta tomada del portal oficial cadus.us.es: **granate `#8d0739`** como color principal, **dorado `#faba09`** para botones y avisos, y grises neutros (`#212529` texto, `#666` secundario, `#dbdbdb` bordes, `#f1f1f1` fondos). La aplica `cadus_aplicar_diseno()` (en `includes/setup.php`): en la primera activación y, en sitios ya montados, una sola vez por `CADUS_DISENO_VERSION` mediante `init`. Refresca la caché CSS de Blocksy para que se vea al instante. El logotipo (`assets/logo-cadus.png`) es provisional hasta que el CADUS facilite el oficial. Tipografía: el portal oficial usa Nunito; no se ha cargado para no depender de Google Fonts (RGPD) y queda como mejora.

## Portada inmersiva (HU-01, HU-18 · extra del Sprint 2)

Reparto: **Codex** escribió el marcado y los datos (`includes/inicio.php`: hero, accesos, buscador, pasos y migración de la portada, con contadores reales y caché de 5 minutos) y **Claude** la capa visual (`includes/estilo.php`, `assets/cadus.css`, `assets/cadus.js`) y la galería (`includes/galeria.php`). Después Codex revisó el trabajo de Claude y se aplicaron sus correcciones (foco visible, movimiento que se detiene a los 4 s, sticky de los pasos, migración conservadora, movimiento reducido).

- **Dirección:** «cartel plano» (skill *design-taste-frontend*): colores planos, tipografía muy pesada y arcos de la Real Fábrica de Tabacos. Movimiento según las reglas de Emil Kowalski (*animate*): solo `transform` y `opacity`, `cubic-bezier(0.23,1,0.32,1)`, botones con `scale(0.97)`, hover solo con puntero fino y variante `prefers-reduced-motion`.
- **Todo cuelga de `body.cadus-portada`**, clase que añade `estilo.php` cuando la página contiene `[cadus_hero]`. Cada sección lleva su variante (`cadus-seccion--accesos|galeria|buscador|noticias|pasos`).
- **Fotos** (`assets/fotos/`, optimizadas a 1400 px): proceden de cadus.us.es y son del CADUS. Confirmar con el cliente su uso y la autorización de las personas que aparecen. Los originales descargados (152 archivos, 216 MB) están en `docs/recursos/fotos-cadus-original/`, fuera de Git.
- **Caché:** WP Fastest Cache guarda HTML con la versión antigua de los archivos. Tras cambiar `cadus.css` o `cadus.js`, vaciar la caché (Ajustes de WP Fastest Cache → Delete Cache).
- **Logotipo y colores:** logotipo oficial y paleta (granate `#8d0739`, dorado `#faba09`) tomados de cadus.us.es. La migración de diseño (`cadus_aplicar_diseno`) solo se ejecuta desde el panel, con Blocksy activo, y no pisa una paleta o un logotipo que el equipo haya cambiado.

## Privacidad de los tickets y las solicitudes de mediación (RN-03 / HU-12)

Implementación en `includes/buzon.php`, `includes/mediacion.php` (autor: Álvaro) y `includes/privacidad.php` (cargado desde el buzón). Los helpers de privacidad comparten una lista cerrada: **`cadus_ticket` y `cadus_mediacion`**. Se aplica a todos los tickets, incluidas las consultas, y a todas las solicitudes de mediación.

- Solo `cadus_ejecutiva` y `administrator` pueden gestionar ambos tipos en el panel. Todos los miembros de Ejecutiva pueden gestionar todos los registros; no hay asignación exclusiva por autor (`post_author=0`). Se deniegan capacidades a otros roles aunque reciban una concesión accidental; el filtro cubre tanto `cadus_mediacion` como `cadus_mediaciones`. Las URL públicas, vistas previas, búsquedas manipuladas y consultas de widgets excluyen ambos tipos y sus hijos, incluso con sesión de Ejecutiva. `?post_type=cadus_mediacion` y `?cadus_mediacion=` responden 404.
- Ninguno tiene REST, archivo público, revisiones ni exportación WXR. Se excluyen de los sitemaps de WordPress y Yoast. Los medios cuyo padre sea un ticket o una mediación tampoco se devuelven mediante REST, ni individualmente ni en colecciones. Los listados del panel muestran referencia, estado y fecha; títulos y etiquetas accesibles omiten asunto, nombre, correo, centro y descripción. Los detalles se consultan en la ficha autorizada. Se conserva borrar en lote, pero se desactiva editar en lote y la edición rápida. Los widgets actuales del Escritorio solo consultan entradas/páginas.
- Fluent Forms valida el envío, pero los campos se mantienen **solo en memoria**, separados por ID de formulario, durante la creación del registro privado. Su `response` se inserta vacío, sin IP, URL de origen, navegador ni vínculo al usuario, y luego se eliminan la entrada y sus metadatos/detalles, también en el camino de spam. El texto, nombre y correo quedan únicamente en el CPT y sus metadatos privados. Si falla la creación, se devuelve un error y no se conserva una copia de recuperación en Fluent Forms. Se usan las opciones `cadus_buzon_form_id` y `cadus_mediacion_form_id`, sin fijar los ID 3 y 4. Antes de probar había cero solicitudes y cero entradas FF; no se borraron datos reales. En otra BD hay que revisar las entradas históricas antes de purgarlas.
- Ambos formularios **no envían correos ni avisos automáticos**. Se deshabilitan por código sus feeds de notificación e integración de Fluent Forms, sin cambiar ajustes ni afectar otros formularios. Si se añade un aviso a la Ejecutiva, su contenido debe limitarse al código y al enlace autenticado del panel; nunca asunto, descripción, respuesta, correo del alumno ni `Reply-To` del alumno. El código no registra contenido en `error_log`. Esto no sustituye la política de logs y copias de seguridad del servidor.
- Seguimiento mediante POST con **código + correo**, nonce, respuesta genérica para combinaciones incorrectas y máximo diez intentos por IP cada quince minutos. El correo se normaliza y se compara mediante `hash_equals` sobre hashes de longitud fija, incluso cuando no existe el código; no se promete tiempo constante de toda la consulta SQL. Los códigos nuevos añaden 128 bits aleatorios: `CAD-año-ID-32hex`. Los anteriores siguen funcionando y conservan su mayor riesgo de adivinación. El resultado muestra asunto, estado y respuestas, nunca el correo ni la descripción original.
- Mediación conserva la validación en servidor de `@alum.us.es`, campos obligatorios, consentimiento y centro perteneciente a la taxonomía `cadus_centro`. Comprueba el nonce de FF (la librería no lo verifica por defecto) y exige honeypot presente y vacío. Añade un límite de **10 intentos de envío con campos válidos por IP cada 15 minutos**, con bloqueo concurrente y una clave HMAC temporal, sin IP en claro ni cabeceras de proxy aportadas por el cliente. Es independiente del seguimiento: el antispam nativo de FF cuenta entradas/IP y deja de ser eficaz cuando se purgan. El nonce público y el honeypot no acreditan identidad. La lista visible de centros se obtiene al crear el formulario; tras cambiar la taxonomía hay que actualizar sus opciones en el editor.
- Las referencias nuevas de mediación son `MED-año-ID-32hex` (128 bits aleatorios); la confirmación comprueba también el correo del envío y muestra solo la referencia. Fuerza confirmación en la misma página aunque se configure una redirección. No existe seguimiento público de mediaciones: la referencia no concede acceso. Las referencias antiguas no se modifican.
- Seguimiento, páginas de ambos formularios, respuestas de envío y fichas/listados privados usan `DONOTCACHEPAGE`, `Cache-Control: no-store, no-cache, must-revalidate, private, max-age=0`, `Referrer-Policy: no-referrer`, `X-Robots-Tag` y exclusión explícita de WP Fastest Cache. **La constante sola no basta** con la combinación local Wordfence/Blocksy. Se retiró la caché anterior de los formularios mediante la API del plugin y se comprueba que mediación no la regenera tras GET/POST/GET. Al desplegar, retirar las copias previas de páginas con `[cadus_seguimiento]`, `[cadus_buzon]`, `[cadus_mediacion]` o sus formularios FF incrustados antes de abrir el servicio.

Cambios RN-03 en el archivo de Álvaro, limitados a cinco puntos: `cadus_mediacion_crear()` recupera los campos desde memoria; esa función añade aleatoriedad a la referencia; `cadus_mediacion_mensaje_confirmacion()` coteja el correo y corrige el comentario sobre recuperación en FF; `cadus_mediacion_columnas()` minimiza el listado; `cadus_mediacion_columna()` convierte la referencia en enlace a la ficha. Las defensas transversales, nonce, honeypot, límite y caché residen en `privacidad.php`.

Pruebas reproducibles desde la raíz del repositorio, con el sitio local arrancado (sin navegador):

```powershell
python scripts/pruebas/rn03_http.py
# Reprueba acotada del panel tras la corrección de aria-label de WordPress 7.1:
python scripts/pruebas/rn03_http.py --panel
python scripts/pruebas/privacidad_tickets.py
python scripts/pruebas/rn03_mediacion.py
& 'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe' scripts/pruebas/rn03_mediacion.php status
& 'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe' scripts/pruebas/rn03_inspeccion.php
& 'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe' -l cms-wordpress/wp-content/plugins/cadus-portal/includes/buzon.php
& 'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe' -l cms-wordpress/wp-content/plugins/cadus-portal/includes/privacidad.php
& 'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe' -l cms-wordpress/wp-content/plugins/cadus-portal/includes/mediacion.php
curl.exe -I http://localhost/proyecto_gsi/cms-wordpress/atencion-al-estudiante/seguimiento-de-ticket/
```

La batería crea tickets, un adjunto sin fichero y, si faltan, cuentas temporales de los roles probados. Intercepta `wp_mail` en la prueba PHP; no cambia contraseñas ni ajustes existentes. Usa `prueba@alum.us.es` o correo vacío para cuentas auxiliares, cookies en memoria y elimina sus sesiones, cuentas y tickets en `finally`. No ejecutar simultáneamente con otra batería que espere cero tickets. Si se interrumpe el proceso, ejecutar `rn03_auditoria.php cleanup`; las sesiones temporales de cuentas existentes caducan a los treinta minutos. La prueba HTTP de seguimiento consume un intento real de localhost: esperar la ventana si se repite diez veces.

La batería `rn03_mediacion.py` reutiliza el transporte HTTP y añade su helper `rn03_mediacion.php`: envío real por el servicio FF y por AJAX anónimo, rechazo de nonce/dominio/centro/consentimiento/honeypot inválidos, límite, ausencia de INSERT sensible, capacidades incluso concedidas por error, consultas REST y adjuntos, sitemaps, caché y panel. Incluye fallo de creación y purga alternativa de spam (`rn03_mediacion.php fallos`). Crea **dos cuentas nuevas de Ejecutiva**, más administrador, delegado y estudiante temporales; comprueba que ambas Ejecutivas leen la misma ficha y que el listado no contiene datos personales. Borra en `finally` solicitudes, adjuntos, entradas FF y usuarios/sesiones, y restaura los contadores previos de localhost. En caso de interrupción: `rn03_mediacion.php cleanup`. `status` informa de los contadores finales sin mostrar datos personales ni credenciales. No ejecutar baterías en paralelo.

Validación local del 23/10/2026, WordPress 7.1: `privacidad_tickets.py` → **40 correctas, 0 fallos**; `rn03_http.py --panel` → **FALLOS: 0**; `rn03_mediacion.py` → **FALLOS: 0**; las tres comprobaciones adicionales de `rn03_mediacion.php fallos` → **true**. `php -l` correcto en `privacidad.php`, `mediacion.php` y el nuevo helper. Limpieza final: cero tickets, solicitudes, entradas/detalles/metadatos FF y cuentas temporales. No se modificaron las pruebas de Claude.

Evidencia y revisión independiente: `scripts/pruebas/RN03_AUDITORIA.md`, `rn03_resultados.txt`, `rn03_reprueba_panel.txt` y `RN03_REVISION_PRUEBAS.md`. El endpoint `/wp-json/wp/v2/users` devolvió **401 anónimo**, sin listado; no se modificó.

Decisiones pendientes del equipo: plazo de retención de tickets, mediaciones y backups; eventual sustitución de códigos antiguos; verificación de la propiedad del correo (el dominio no demuestra que pertenezca al solicitante); ajuste del límite de envíos para redes universitarias con IP compartida; sincronización automática de centros; y almacenamiento privado de ficheros si se incorporan adjuntos. Actualmente los formularios no admiten ficheros: bloquear una URL de WordPress no protege por sí solo un fichero estático en `uploads`.

Referencias técnicas: [registro de tipos de WordPress](https://developer.wordpress.org/reference/functions/register_post_type/) y [ciclo de envío de Fluent Forms](https://developers.fluentforms.com/submission-lifecycle/), contrastados con el código instalado.

## Secciones de la portada tomadas de cadus.us.es

La portada reproduce lo principal de la web oficial, con el estilo propio del portal:

| Shortcode | Sección | Datos |
|---|---|---|
| `[cadus_intro]` | «Más de 40 años dando voz al alumnado» (texto de la web oficial) | fijo |
| `[cadus_novedades]` | «¡Últimas noticias!»: filtros por categoría y carrusel | entradas publicadas y categorías reales (caché de 5 min) |
| `[cadus_eventos]` | «¡Últimos eventos!» | entradas de la categoría Eventos; `cadus_eventos_origen()` es el único punto a cambiar cuando llegue el calendario (HU-10) |
| `[cadus_trabajo]` | «Nuestro trabajo»: cuatro listas de objetivos | texto de la web oficial (de 2024): revisar con el CADUS |
| `[cadus_contacto]` | Cierre: dirección, teléfono, correo, Instagram y enlaces | fijo; enlaces a la web oficial marcados como tales |

Marcado y datos: Codex (`includes/portada_extra.php`). Estilo y JS: Claude (`assets/cadus.css`, `assets/cadus.js`). La portada se reescribe sola (migración v2 en `inicio.php`) si no la ha editado el equipo. El JS añade el filtrado (con un aviso `role="status"` del número de noticias) y los botones del carrusel; sin JS la lista se desplaza en horizontal y se ve completa. Contrastes comprobados: todos los textos cumplen WCAG AA (mínimo 5,4:1). La revisión cruzada de Codex sobre el CSS y el JS quedó pendiente por límite de uso de Codex.
