# Actualización del estado del CMS a 22/11/2026

> **Estado vigente:** este documento es del 22/11 y tiene añadidas las actualizaciones del 25, 26 y 27/11. El estado completo y vigente del CMS es el de `Entrega-final-CMS-CADUS` (a 27/11/2026, para la entrega del 29/11), que prevalece sobre este documento donde se contradigan.

Este documento prevalece sobre la adenda del Sprint 3 (`Adenda-CMS-Sprint3`, fechada el 15/11/2026) y sobre el estado de `seguimiento/product-backlog.md` donde se contradigan. Las pruebas están en `seguimiento/E3-04-pruebas-de-aceptacion.md`.

| Elemento | Estado a 15/11 (adenda) | Estado a 22/11 |
|---|---|---|
| HU-14 móvil y tablet | Hecho | Hecho: Pablo probó en su móvil real portada, buzón, calendario, mediación y menú. La tablet la da Pablo por comprobada y bien el 23/11 (HU-14c). La primera vez la portada salió sin estilos por la caché de WP Fastest Cache del WordPress local, no por el portal |
| HU-15 accesibilidad | Hecho | En curso (reabierta): el 23/11 Marcos (con Claude) comprobó el recorrido completo con teclado, el envío del buzón solo con teclado, Lighthouse de accesibilidad (97 / 96 / 96) y daltonismo; falta el lector de pantalla real (H15-3) y dos arreglos menores (contraste de la palabra decorativa del pie y enlazar los errores del formulario con su campo) |
| HU-16 buscar y filtrar | Hecho; H16-1 a H16-6 pendientes de navegador | Hecho: H16-1 a H16-6 probados con clics el 22/11 y H16-7 (búsqueda en tickets sin datos del estudiante) con `test-ejecutivo`, ejecutadas por Claude en nombre de Pablo (no son prueba cruzada) |
| E3-04 pruebas de aceptación | A medias | T1 y T2 parciales (funcionales, sin cronometrar con una persona externa); H17-3 parcial (el cortafuegos bloquea `<script>` antes de llegar al portal) |
| E3-09 despliegue en la US | Movido al siguiente sprint, bloqueado por PHP 7.2/7.3 | No se persigue: pendiente de hablar con la US sobre el despliegue web, sin saber si se hará |
| Pendientes de los sprints 1 a 3 | — | Lector de pantalla, cuentas por rol y prueba cruzada; datos reales de delegaciones (E2-01, E2-12); retrospectiva en grupo (E3-01); cuentas de delegado y volcado final (E3-02); documento final del CMS (E3-06). Nota del 23/11: la entrega final pasó del 07/12 al domingo 29/11 |

Las capturas de HU-22 (`capturas-sprint3/m01` a `m03`) tienen tapada la contraseña propuesta que mostraba el formulario.

## Actualización del 25/11/2026

Esta sección prevalece sobre la tabla anterior donde se contradigan; el estado vigente completo está en `Entrega-final-CMS-CADUS` (entrega final del 29/11).

| Elemento | Estado a 25/11 |
|---|---|
| E2-01 cuentas reales del CADUS | Descartada: depende del CADUS; se entrega con las cuentas actuales |
| E2-12 fichas reales | Cerrada: 27 fichas con los datos de la web del CADUS y edición restringida comprobada; faltan el teléfono en 7, el correo en 1 y el horario en las 27 |
| E3-09 despliegue en la US | Descartada: queda pendiente hablar con la US sobre el despliegue |
| HU-15 accesibilidad | Teclado, Lighthouse de accesibilidad y daltonismo (Marcos, 23/11), Narrador y arreglo de los errores de los formularios (PR #96, 25/11); falta repetir Lighthouse con el código actual y NVDA |
| Datos de prueba | Se borran antes del volcado (E3-02); no forman parte de la entrega |

## Actualización del 26 y 27/11/2026

| Elemento | Estado a 27/11 |
|---|---|
| HU-15 accesibilidad | Lighthouse de accesibilidad repetido con el código actual: 100 / 100 / 100 (Marcos, PR #98). NVDA probado el 27/11 según Pablo, sin registro paso a paso |
| HU-20 rendimiento | Portada en móvil: 98 con el contenido real (91 antes de optimizar y 99 después, 12/11). Se corrigió el límite de 8 MB de imágenes, que no se aplicaba a las subidas del editor de bloques |
| HU-22 relevo de la cuenta | H22-1 a H22-5 ejecutados con las cuentas de prueba (Pablo con Claude): todos OK |
| Pruebas de aceptación | 43 casos, todos OK (T1 a T3 cronometrados por Pablo el 27/11: 50, 10 y 18 s, límite 60 s; Pablo conoce el portal, no es una persona externa); el envío real del correo (P5) se probó el 27/11 y llegó con una hora de retraso |
