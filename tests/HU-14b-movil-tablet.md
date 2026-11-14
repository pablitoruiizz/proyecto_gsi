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

## Pendiente (en el WordPress real)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H14-2 | Directorio en móvil y tablet reales o con el modo dispositivo. | Tarjetas legibles, buscador usable, sin textos cortados. | Pendiente |
| H14-3 | Ficha de una delegación: datos, enlaces y «Volver al listado». | Todo visible y funcional. | Pendiente |
| H14-4 | Tabla de actas y normativa en móvil. | Cada fila como tarjeta con Fecha, Documento, Tipo y PDF completos. | Pendiente |
