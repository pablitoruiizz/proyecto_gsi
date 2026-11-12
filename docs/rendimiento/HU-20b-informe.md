# HU-20b · Caché y minificación con Lighthouse, antes y después (12/11/2026)

Medición hecha por Pablo con Claude. Herramienta: Lighthouse 12.6.1 en Chrome sin interfaz, perfil móvil de Lighthouse (emulación de móvil y red 4G lenta simulada), con el sitio local del equipo (WampServer, `http://localhost/proyecto_gsi/cms-wordpress`). Script: `scripts/pruebas/lighthouse.py`; resultados en bruto (mediana de 3 o 5 ejecuciones por página) en `docs/rendimiento/lighthouse-*.json`.

## Qué se cambió en WP Fastest Cache
| Ajuste | Antes | Después |
|---|---|---|
| Caché de páginas | activada en los ajustes, pero servida por PHP (cada visita arranca WordPress) | activada y servida como archivo estático por Apache (`.htaccess`) |
| Minificar HTML | no | **sí** |
| Minificar CSS | no | **sí** |
| Combinar CSS | no | no (se probó y se descartó: ver «Conclusiones») |
| Compresión Gzip | regla en `.htaccess`, pero sin efecto (el servidor local no tenía `mod_deflate`) | **activa** (`mod_deflate` habilitado) |
| Caché del navegador (Leverage Browser Caching) | no | **sí** |
| Quitar emojis de WordPress | no | **sí** |
| Vaciar la caché al publicar y al actualizar | no | **sí** |
| No servir la caché a usuarios con sesión | sí | sí |

Las páginas privadas **no se cachean**: se comprobó que `/acceso/`, `/gestion/`, el buzón, el seguimiento de ticket y la mediación no generan archivo de caché (RN-03).

## Resultados (mediana de 5 ejecuciones, antes → después)
| Página | Rendimiento (0-100) | Respuesta del servidor | LCP | Peso | Peticiones |
|---|---|---|---|---|---|
| Inicio | 91 → 99 | 517 ms → 8 ms | 2.9 s → 1.9 s | 537 KB → 311 KB | 14 → 14 |
| Noticias | 90 → 99 | 586 ms → 7 ms | 3.0 s → 2.0 s | 523 KB → 310 KB | 15 → 15 |
| Delegaciones | 79 → 97 | 697 ms → 8 ms | 3.7 s → 2.5 s | 1302 KB → 1092 KB | 36 → 37 |
| Actas y normativa | 83 → 99 | 616 ms → 10 ms | 4.1 s → 2.0 s | 523 KB → 309 KB | 15 → 15 |
| Buzón | 73 → 74 | 4045 ms → 4182 ms | 4.1 s → 4.1 s | 743 KB → 744 KB | 19 → 19 |

Accesibilidad (95–97), buenas prácticas (100) y SEO (92) no cambian; el buzón queda en SEO 58 por ir con `noindex` a propósito (cabecera `X-Robots-Tag`). El buzón no se cachea (es privado), por eso no mejora: su tiempo de respuesta (4 s) es el de WordPress sin caché en este equipo.

Fases de la medición, para entender qué aporta cada ajuste (mediana de 3 a 5 ejecuciones, Inicio y Noticias):

| Fase | Rendimiento | Respuesta del servidor | Peso | LCP |
|---|---|---|---|---|
| Antes (caché servida por PHP, sin minificar) | 91 y 90 | 520–590 ms | 540 KB | 2,9–3,0 s |
| Caché estática + minificado, **sin** Gzip | 91 y 84 | 1–3 ms | 527–542 KB | 3,0–3,9 s |
| Caché estática + minificado + **Gzip** | **99 y 99** | 7 ms | **317 KB** | **1,9–2,0 s** |

## Conclusiones
1. **El efecto grande llega al combinar las tres cosas.** La caché estática baja la respuesta del servidor de ~500–700 ms a unos 7 ms, pero por sí sola no mueve la puntuación porque el LCP depende del CSS que bloquea el pintado. Con el **Gzip** activo, el CSS y el HTML viajan comprimidos: el peso de las páginas públicas baja de ~530 KB a ~317 KB (**−40 %**), el primer pintado de 2,6 s a 1,4 s y el LCP de 3–4 s a 2 s. Resultado: Rendimiento 91 → 99 en Inicio, 90 → 99 en Noticias, 79 → 97 en Delegaciones y 83 → 99 en Actas y normativa.
2. **Sin Gzip la medición engaña:** con la caché y el minificado solos, Noticias parecía empeorar (90 → 84). No era la configuración sino el LCP simulado de Lighthouse, que salta en escalones y varía ±1 s entre ejecuciones cuando el CSS pesa casi 120 KB sin comprimir.
3. **Combinar los CSS no compensa:** reduce 3 peticiones (14 → 11), pero genera un CSS único de unos 120 KB que bloquea el renderizado y no mejora el LCP; además es el ajuste que más suele romper estilos. Se deja desactivado.
4. En todas las páginas públicas el LCP es el título de la página (texto): ya no hay imágenes grandes en el camino crítico salvo en Delegaciones (25 escudos, 1,1 MB cargados en diferido).

## Hallazgos que no se resuelven con la caché
- **Las páginas sin caché tardan unos 3,7–4,4 s en responder en este equipo** (buzón, seguimiento, mediación, acceso, gestión, calendario y la primera visita de cualquier página): arrancar WordPress con 9 plugins incluye más de 2.500 archivos y 119 MB y tarda unos 2,7–3,0 s solo en `wp-load.php`, con o sin Xdebug (Xdebug en modo `develop` suma unos 0,25 s). Es un coste del entorno local (carpeta sincronizada con OneDrive y PHP de desarrollo); en un servidor con opcache y sin Xdebug será bastante menor, pero **hay que repetir esta medición en el servidor de la US** cuando se despliegue (E3-09, bloqueado por PHP 7.2/7.3).
- Esas páginas no se pueden cachear (son privadas o dinámicas), así que dependen de la velocidad real del servidor y de los plugins. Wordfence, Yoast, Fluent Forms y The Events Calendar son los más pesados al arrancar; si hace falta, desactivar en el frontal lo que no se use es la siguiente palanca.
- Delegaciones pesa 1,3 MB por los 25 escudos (PNG de 320 px, 1,6 MB en total; se cargan en diferido). Convertirlos a WebP y servirlos a su tamaño real es una tarea de optimización de imágenes (HU-20a, Miguel Ángel).

## Pendiente
1. **Gzip local aplicado:** el Apache de WampServer tenía `mod_deflate` desactivado; se activó en `bin/apache/apache2.4.65/conf/httpd.conf` (copia `httpd.conf.bak_antes_deflate`, junto con `mod_filter` y `mod_expires`) y se reinició Wamp. En el servidor de la US hay que comprobar que la compresión está activa (cabecera `Content-Encoding: gzip` en una página y en un CSS).
2. **`.htaccess` en subcarpeta:** WP Fastest Cache escribe las reglas de caché para un sitio en la raíz del dominio; en este equipo (sitio en `/proyecto_gsi/cms-wordpress/`) hubo que corregir a mano la ruta de la caché en `.htaccess`, que no se versiona. En el servidor de la US, con el sitio en la raíz, WP Fastest Cache lo escribe bien; comprobar allí que una página pública responde en milisegundos y lleva `Last-Modified`.
3. **Repetir la medición en el servidor de la US** (E3-09) con el mismo script (`python scripts/pruebas/lighthouse.py <etiqueta>`).
4. Tras cambiar un `.css` hay que usar «Clear Cache and Minified CSS/JS» en WP Fastest Cache para que el visitante reciba la versión nueva.
