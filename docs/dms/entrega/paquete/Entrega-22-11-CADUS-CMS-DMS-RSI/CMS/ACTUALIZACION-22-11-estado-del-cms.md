# Actualización del estado del CMS a 22/11/2026

Este documento prevalece sobre la adenda del Sprint 3 (`Adenda-CMS-Sprint3`, fechada el 15/11/2026) y sobre el estado de `seguimiento/product-backlog.md` donde se contradigan. Las pruebas están en `seguimiento/E3-04-pruebas-de-aceptacion.md`.

| Elemento | Estado a 15/11 (adenda) | Estado a 22/11 |
|---|---|---|
| HU-14 móvil y tablet | Hecho | Hecho: Pablo probó en su móvil real portada, buzón, calendario, mediación y menú. Falta una tablet real y la prueba cruzada (Pablo programó HU-14c). La primera vez la portada salió sin estilos por la caché de WP Fastest Cache del WordPress local, no por el portal |
| HU-15 accesibilidad | Hecho | En curso (reabierta): «Saltar al contenido», foco y etiquetas del buzón comprobados; faltan el lector de pantalla real, el recorrido completo con teclado y Lighthouse |
| HU-16 buscar y filtrar | Hecho; H16-1 a H16-6 pendientes de navegador | Hecho: H16-1 a H16-6 probados con clics el 22/11 y H16-7 (búsqueda en tickets sin datos del estudiante) con `test-ejecutivo`, ejecutadas por Claude en nombre de Pablo (no son prueba cruzada) |
| E3-04 pruebas de aceptación | A medias | T1 y T2 parciales (funcionales, sin cronometrar con una persona externa); H17-3 parcial (el cortafuegos bloquea `<script>` antes de llegar al portal) |
| E3-09 despliegue en la US | Movido al siguiente sprint, bloqueado por PHP 7.2/7.3 | No se persigue: pendiente de hablar con la US sobre el despliegue web, sin saber si se hará |
| Pendientes de los sprints 1 a 3 | — | Lector de pantalla, tablet real, cuentas por rol y prueba cruzada; datos reales de delegaciones (E2-01, E2-12); retrospectiva en grupo (E3-01); cuentas de delegado y volcado final (E3-02); documento final del CMS (E3-06, 07/12) |

Las capturas de HU-22 (`capturas-sprint3/m01` a `m03`) tienen tapada la contraseña propuesta que mostraba el formulario.
