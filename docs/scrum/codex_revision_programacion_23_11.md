# Revisión de la programación del 23/11/2026

Revisión de SOLO LECTURA: no edites archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni en el WordPress, y no toques `cms-wordpress/.htaccess` ni los `.sql`. Responde en español, con hallazgos por gravedad (alta, media, baja), cada uno con archivo y línea, el fallo concreto y cómo corregirlo. Al final di si se puede fusionar tal cual.

Se trata de código escrito el 23/11 para sustituir los contenidos de ejemplo del portal del CADUS (WordPress, PHP 8.x) por contenido real de www.cadus.us.es. Revisa:

1. `cms-wordpress/wp-content/plugins/cadus-portal/includes/setup.php`: las funciones nuevas `cadus_noticias_cargar()` y `cadus_documentos_cargar()` y su llamada desde `cadus_portal_configurar()`; también que al quitar las noticias, el acta y el reglamento de ejemplo no se haya roto nada (el acta pendiente de ejemplo sigue sembrándose y usa `$pdf`). Mira:
   - idempotencia (la marca `_cadus_semilla` y `cadus_buscar_semilla`) y qué pasa si se activa el plugin varias veces o si el contenido ya existe con otro título;
   - seguridad: se guarda HTML procedente de un JSON (`wp_kses_post`, `esc_url`), la ruta `archivo` del JSON usada por `cadus_adjuntar()` (¿puede salirse de `data/`?) y `wp_set_object_terms` con un término que puede no existir;
   - uso correcto de `term_exists` y `wp_insert_term` (devuelven arrays o `WP_Error`), de los bloques (`cadus_b_p`, `cadus_b_h`, `cadus_b_html`) y de `post_date` sin zona horaria.
2. `cms-wordpress/wp-content/plugins/cadus-portal/data/noticias.json` y `data/documentos.json`: que sean JSON válido, que cada `archivo` de `documentos.json` exista en `data/actas/` o `data/normativa/`, que las fechas (`YYYYMMDD`) y los tipos coincidan con lo que espera `contenidos.php` (campos `fecha`, `pleno`, `archivo_pdf` y la taxonomía `cadus_tipo_documento`), y que las categorías de las noticias existan o se creen.
3. `scripts/entrega/cargar_eventos_ejemplo.php`: la consulta directa `$existe` con `$wpdb->prepare`, que el script se pueda repetir sin duplicar (eventos pasados incluidos), el uso de `tribe_create_event` y `tribe_update_event` con `EventAllDay`, las fechas de varios días, el borrado de `$retirados` y de `--quitar`, y que la votación quede vinculada a la asamblea futura (`_cadus_vot_asamblea`) cumpliendo RN-05 (solo las asambleas admiten votaciones).
4. `scripts/dms/empaquetar_dms.py`: la opción nueva `--final` (variables `FINAL`, `FECHA`, `NOMBRE`) y la línea de `diseno-tableros-planner.md` añadida a `RSI_FILES`; que no rompa las variantes anteriores (`--con-cms`, `--con-rsi` sin `--final`).
5. `scripts/scrum/crear_rsi.py`: la historia nueva RSI-HU-09 y que el script siga siendo idempotente.

Después, busca contradicciones entre el código y la documentación que lo describe: `scripts/entrega/README.md` y los comentarios de las funciones. No leas ni cites `tests/cuentas-de-prueba-local.md`.

## Resultado (23/11/2026)

Codex no recomendó fusionar tal cual y señaló 7 hallazgos (1 alto, 5 medios y 1 bajo). Se corrigieron todos:

| Hallazgo | Corrección |
|---|---|
| Alto: el script de eventos identificaba por título y podía actualizar o borrar eventos ajenos | Marca `_cadus_semilla` en cada evento y votación; solo se actualiza y borra lo marcado (con `--quitar`, solo lo marcado) y se adopta por título solo lo que dejó la versión anterior del script |
| Medio: los ejemplos antiguos seguían en instalaciones existentes | Nueva `cadus_ejemplos_retirar()`: retira solo los ejemplos con la marca de siembra y «ejemplo» en el título; conserva el acta pendiente de ejemplo |
| Medio: una carga incompleta quedaba marcada como terminada | Sin PDF o sin categoría no se publica ni se marca; si ya existía sin PDF, se repone |
| Medio: la ruta del JSON podía salirse de `data/` | Se exige un PDF cuyo `realpath` esté dentro de `data/actas` o `data/normativa` |
| Medio: `--final` solo no generaba el paquete completo | `--final` implica `--con-rsi` |
| Medio: la votación se actualizaba sin la validación RN-05 | Se comprueba `cadus_votaciones_es_asamblea()` y los resultados de crear el evento y de marcarlo como asamblea; si falla, no se toca la votación y el script termina con error |
| Bajo: el comentario y el README prometían de más | Texto corregido |

Comprobado después: el script de eventos se ejecuta dos veces sin duplicar (la primera adopta los eventos sin marca), los cargadores del plugin son idempotentes (8 noticias, 11 actas, 1 acta pendiente antes y después) y la migración retira un ejemplo antiguo pero no una noticia real con la misma marca.
