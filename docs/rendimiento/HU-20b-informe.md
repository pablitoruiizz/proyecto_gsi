# HU-20b · Caché y minificación con Lighthouse, antes y después (12/11/2026)

Medición hecha por Pablo con Claude. Herramienta: Lighthouse 12.6.1 en Chrome sin interfaz, perfil móvil de Lighthouse (emulación de móvil y red 4G lenta simulada), con el sitio local del equipo (WampServer, `http://localhost/proyecto_gsi/cms-wordpress`). Script: `scripts/pruebas/lighthouse.py`; resultados en bruto (mediana de 3 o 5 ejecuciones por página) en `docs/rendimiento/lighthouse-*.json`.

## Qué se cambió en WP Fastest Cache
| Ajuste | Antes | Después |
|---|---|---|
| Caché de páginas | activada en los ajustes, pero servida por PHP (cada visita arranca WordPress) | activada y servida como archivo estático por Apache (`.htaccess`) |
| Minificar HTML | no | **sí** |
| Minificar CSS | no | **sí** |
| Combinar CSS | no | no (se probó y se descartó: ver «Conclusiones») |
| Compresión Gzip | regla en `.htaccess` | regla en `.htaccess` (ver «Pendiente») |
| Caché del navegador (Leverage Browser Caching) | no | **sí** |
| Quitar emojis de WordPress | no | **sí** |
| Vaciar la caché al publicar y al actualizar | no | **sí** |
| No servir la caché a usuarios con sesión | sí | sí |

Las páginas privadas **no se cachean**: se comprobó que `/acceso/`, `/gestion/`, el buzón, el seguimiento de ticket y la mediación no generan archivo de caché (RN-03).

## Resultados (mediana de 5 ejecuciones, antes → después)
| Página | Rendimiento (0-100) | Respuesta del servidor | LCP | Peso | Peticiones |
|---|---|---|---|---|---|
| Inicio | 91 → 91 | 517 ms → 1 ms | 2.9 s → 3.0 s | 537 KB → 529 KB | 14 → 14 |
| Noticias | 90 → 84 | 586 ms → 3 ms | 3.0 s → 3.9 s | 523 KB → 514 KB | 15 → 15 |
| Delegaciones | 79 → 88 | 697 ms → 2 ms | 3.7 s → 3.5 s | 1302 KB → 1293 KB | 36 → 36 |
| Actas y normativa | 83 → 91 | 616 ms → 2 ms | 4.1 s → 3.0 s | 523 KB → 514 KB | 15 → 15 |
| Buzón | 73 → 74 | 4045 ms → 4182 ms | 4.1 s → 4.1 s | 743 KB → 744 KB | 19 → 19 |

Accesibilidad, buenas prácticas y SEO no cambian (accesibilidad 95–97 y buenas prácticas 100 en todas; SEO 92, salvo el buzón con 58 por ir con `noindex` a propósito).

## Conclusiones
1. **El tiempo de respuesta del servidor baja de unos 500–700 ms a 1–3 ms** en las páginas públicas, porque Apache entrega un archivo ya generado sin arrancar WordPress. Es la mejora real y estable.
2. **El peso baja un 1,7 %** (unos 9 KB por página) por la minificación; las peticiones no cambian al no combinar CSS.
3. **Las puntuaciones suben en Delegaciones (79 → 88) y Actas y normativa (83 → 91) y no cambian en Inicio (91); en Noticias baja de 90 a 84.** La diferencia de Noticias no viene de la configuración: el LCP simulado de Lighthouse salta en escalones (3,0 s o 3,9 s según la ejecución) y una ejecución suelta de Inicio dio 2,9 s sin la caché estática y 3,0 s con ella. Con 3 ejecuciones el mismo cambio dio entre 2,9 s y 4,1 s: **la variación entre ejecuciones (±1 s) es mayor que el efecto de la caché en este entorno**, así que no se puede afirmar que Noticias haya empeorado ni que Delegaciones haya mejorado solo por la caché.
4. **Combinar los CSS no compensa:** reduce 3 peticiones (14 → 11), pero genera un CSS único de unos 120 KB que bloquea el renderizado y no mejora el LCP (3,9–4,1 s con CSS combinado frente a 3,0–4,1 s sin combinar). Además es el ajuste que más suele romper estilos al cambiar de orden de carga. Se deja desactivado.
5. En todas las páginas el LCP es el título de la página (texto) y el 80 % de su tiempo es «retraso de renderizado»: el navegador espera a los CSS que bloquean el pintado. La mejora que falta es **comprimir con Gzip esos CSS** (ver «Pendiente») o reducir el CSS crítico.

## Hallazgos que no se resuelven con la caché
- **Las páginas sin caché tardan unos 3,7–4,4 s en responder en este equipo** (buzón, seguimiento, mediación, acceso, gestión, calendario y la primera visita de cualquier página): arrancar WordPress con 9 plugins incluye más de 2.500 archivos y 119 MB y tarda unos 2,7–3,0 s solo en `wp-load.php`, con o sin Xdebug (Xdebug en modo `develop` suma unos 0,25 s). Es un coste del entorno local (carpeta sincronizada con OneDrive y PHP de desarrollo); en un servidor con opcache y sin Xdebug será bastante menor, pero **hay que repetir esta medición en el servidor de la US** cuando se despliegue (E3-09, bloqueado por PHP 7.2/7.3).
- Esas páginas no se pueden cachear (son privadas o dinámicas), así que dependen de la velocidad real del servidor y de los plugins. Wordfence, Yoast, Fluent Forms y The Events Calendar son los más pesados al arrancar; si hace falta, desactivar en el frontal lo que no se use es la siguiente palanca.
- Delegaciones pesa 1,3 MB por los 25 escudos (PNG de 320 px, 1,6 MB en total; se cargan en diferido). Convertirlos a WebP y servirlos a su tamaño real es una tarea de optimización de imágenes (HU-20a, Miguel Ángel).

## Pendiente
1. **Gzip local:** el Apache de WampServer tiene `mod_deflate` desactivado. Se activó en `bin/apache/apache2.4.65/conf/httpd.conf` (con copia `httpd.conf.bak_antes_deflate`), pero hace falta **reiniciar los servicios de Wamp** para que surta efecto (el reinicio exige permisos de administrador). Tras reiniciar, repetir `python scripts/pruebas/lighthouse.py despues2` y comparar: es el cambio que más debería bajar el LCP.
2. **`.htaccess` en subcarpeta:** WP Fastest Cache escribe las reglas de caché para un sitio en la raíz del dominio; en este equipo (sitio en `/proyecto_gsi/cms-wordpress/`) hubo que corregir a mano la ruta de la caché en `.htaccess`, que no se versiona. En el servidor de la US, con el sitio en la raíz, WP Fastest Cache lo escribe bien; comprobar allí que la respuesta de una página pública tarda unos milisegundos y lleva la cabecera `Last-Modified`.
3. **Repetir la medición en el servidor de la US** (E3-09) con el mismo script.
