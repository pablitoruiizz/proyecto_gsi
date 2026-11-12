# Revisión pedida a Codex: delegaciones con escudos, buscador, pie y arreglos de HU-24 (12/11/2026)

Revisión de SOLO LECTURA (no edites archivos, no hagas commit y no ejecutes `scripts/pruebas/*.php`, que crean y borran datos). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías.

## Contexto
Portal del CADUS en WordPress 7.1.4 con el plugin propio `cms-wordpress/wp-content/plugins/cadus-portal`. Cambios de hoy:

1. **Directorio de delegaciones** (`includes/delegaciones.php`, `data/delegaciones.json`, `assets/escudos/*.png`, `scripts/entrega/cargar_delegaciones.php`, y los cambios en `includes/contenidos.php` y `includes/setup.php`): 27 delegaciones copiadas de www.cadus.us.es/delegaciones/ con miembros, correo, teléfono, Instagram y escudo (campo ACF de imagen). La carga es idempotente y solo rellena campos vacíos.
2. **Directorio y ficha** (`cadus_shortcode_directorio`, `cadus_ficha_en_contenido`): tarjetas con escudo, buscador en el navegador (script en línea que filtra por `data-buscar`), miembros en la ficha.
3. **Pie global** (`includes/portada_extra.php` `cadus_shortcode_contacto`, `assets/cadus.css`): tres columnas, Instagram @igcadus (único enlace social), enlaces externos.
4. **Menú**: etiquetas más cortas y «Más» en lugar de «More» (`includes/estilo.php`, `includes/setup.php`).
5. **Arreglos de HU-24** que pidió la revisión anterior (`includes/gestion.php`): capacidades al crear actas y delegaciones, PDF con tipo real obligatorio, ficha que avisa a la caché, «Sin asignar», aviso por sesión (`cadus_gestion_clave_msg`), recuperación de lo escrito tras un error (`cadus_gestion_previo`, `cadus_gestion_rellenar` con `WP_HTML_Tag_Processor`), cambio de cuenta de una ficha, campos Instagram y miembros. Pruebas ampliadas en `scripts/pruebas/gestion.php` (84 correctas, incluidas peticiones HTTP reales).

## Qué revisar
1. **Seguridad**: XSS o inyección en el buscador (`data-buscar`, el script), en las tarjetas, en la ficha (Instagram, miembros, correo) y en `cadus_gestion_rellenar` (¿se puede romper el HTML con lo guardado en el transient o con el valor de un campo?). Validación de `cuenta` al reasignar una ficha, y de `instagram`. ¿Alguna ruta permite a un delegado cambiar su cuenta, el centro o el título?
2. **Idempotencia de la carga** (`cadus_delegaciones_cargar`): duplicados, semillas, qué pasa si se edita el título de una ficha, qué pasa con el escudo si se borra el adjunto, uso de `cadus_adjuntar` con el título «Escudo de …».
3. **Privacidad**: los nombres de los miembros son datos personales publicados también en la web oficial. ¿Se incluye información en `data-buscar` que no debería quedar en el HTML? ¿Qué mejoras recomiendas (por ejemplo base jurídica, derecho de supresión, no indexar)?
4. **Accesibilidad (HU-15, DUA)**: buscador (etiqueta, `aria-live`, foco, mensajes), tarjetas con imagen decorativa, contraste del pie (texto blanco y dorado sobre `#8d0739`, enlaces subrayados solo al pasar el ratón: ¿se distingue un enlace sin subrayado sin depender del color?), objetivos táctiles, enlaces externos, orden de encabezados (h2/h3) del pie y de la ficha.
5. **Rendimiento (HU-20)**: tamaño de los escudos, `loading=lazy`, consultas por tarjeta (`get_attached_file`, `cadus_campo` repetidos) en el directorio con 27 fichas.
6. **Corrección funcional**: orden del menú tras cambiar títulos, `cadus_gestion_rellenar` con varias fichas en el mismo panel, mensajes por sesión con `wp_get_session_token`.
7. **Pruebas**: qué casos siguen sin cubrirse en `scripts/pruebas/gestion.php` y si falta una prueba de la carga de delegaciones.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
