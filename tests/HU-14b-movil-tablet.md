# Pruebas de HU-14b · Directorio, tablas y fichas en móvil y tablet

**Requisitos:** HU-14 (móvil, tablet y ordenador) · **Código:** `cms-wordpress/wp-content/plugins/cadus-portal/assets/cadus-interior.css`
**Quién prueba:** Álvaro Martínez Ocaña · **Fecha:** 14/11/2026

## Qué se cambió

En móvil (hasta 760 px) la tabla de actas y normativa se apila en tarjetas, pero cada tarjeta se salía por la derecha y se cortaban la fecha, el tipo y el botón PDF. Causa: las celdas tenían `width: 100%` más relleno sin `box-sizing: border-box`. Se añadió `border-box`, `min-width: 0` y ajuste de línea en las celdas, y la etiqueta de cada celda ya no se parte.

## Comprobación hecha (maqueta estática)

Se cargaron los tres CSS reales del plugin con el mismo HTML que generan el directorio, la tabla y la ficha (textos largos incluidos) y se midió el desbordamiento con Chromium.

| Ancho | Antes | Después |
|---|---|---|
| 320 px | celdas fuera de la pantalla | sin desbordamiento |
| 390 px | celdas fuera de la pantalla (fecha, tipo y PDF cortados) | sin desbordamiento |
| 768 px | sin desbordamiento | sin desbordamiento |

Directorio (tarjetas) y fichas: sin desbordamiento en los tres anchos; el directorio se ve en una columna en móvil.

## Comprobación en el WordPress local (15/11/2026)

Hecha con el navegador integrado emulando 390 × 844 y 768 × 1024, sobre la rama `feature/hu-14b-directorio-movil` y el CSS nuevo cargado. Se midió con el propio navegador que no hay desbordamiento horizontal.

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H14-2 | Directorio de delegaciones a 390 y 768 px. | Tarjetas legibles, sin textos cortados ni scroll horizontal. | OK. 6 tarjetas, una columna a 390 px y dos a 768 px, sin desbordamiento. No se probó el buscador con texto. |
| H14-3 | Ficha de una delegación y «Volver al listado». | Datos visibles y botón funcional. | Parcial. La ficha de Facultad de Derecho solo dice «Ficha pendiente de completar», sin datos, así que no se probaron filas con textos largos. El botón «← Volver al listado» enlaza al directorio y mide 44 px de alto. |
| H14-4 | Tabla de actas y normativa a 390 px. | Cada fila como tarjeta con Fecha, Documento, Tipo y PDF completos. | OK. 2 filas, todas las celdas dentro de la pantalla y botón «Descargar PDF» completo. |

Pendiente: repetirlo con el modo dispositivo de Chrome o Edge (F12), probar el buscador del directorio y una ficha con todos los datos rellenos.
