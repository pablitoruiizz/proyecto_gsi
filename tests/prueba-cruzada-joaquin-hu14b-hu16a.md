# Prueba cruzada de Joaquín · HU-14b (H14-2 y H14-3) y HU-16a (H16-1 a H16-6)

Plan: [plan del 23/11](../docs/scrum/plan-23-11.md). Las dos historias son de Álvaro, así que las prueba Joaquín. Los casos y sus resultados esperados salen de [`E3-04-pruebas-de-aceptacion.md`](E3-04-pruebas-de-aceptacion.md) y de [`HU-14b-movil-tablet.md`](HU-14b-movil-tablet.md); allí constan los resultados que ya anotaron Claude y Pablo el 22/11 con el navegador integrado. Esta hoja es la **repetición humana**, con clics reales, y la deja anotada con fecha, persona y resultado.

> **Estado:** guion preparado el 24/11/2026; **ningún caso está ejecutado**. La columna «Resultado» se rellena a mano al probar. Un caso que no se pueda ejecutar se anota como «Pendiente» con el motivo, nunca como OK.

## Antes de empezar

1. Actualiza `main` (`git pull`) y comprueba en el pie de la portada que tienes la versión nueva.
2. Entorno: el WordPress de WampServer, en `http://localhost/proyecto_gsi/cms-wordpress/` o, por Tailscale, en `http://100.106.47.100/proyecto_gsi/cms-wordpress/`. Si usas WP Fastest Cache, vacíala antes (Ajustes › WP Fastest Cache › Borrar la caché).
3. Navegador: Chrome o Edge. **Modo dispositivo:** pulsa `F12`, luego `Ctrl + Mayús + M`, y en la barra de arriba elige **Dimensiones: Responsive** y escribe el ancho: **390** (móvil) o **768** (tablet).
4. Datos de ejemplo: 27 delegaciones, 4 noticias del 14 al 17/10/2026 y 2 documentos en Actas y normativa. Si en tu sitio son otros, adapta las fechas manteniendo la idea y anótalo.
5. **Comprobar que no hay scroll lateral:** en la consola del navegador (`F12 › Consola`) escribe `scrollTo(500,0); scrollX`. Si da `0`, la página no se desplaza hacia los lados. (No uses `scrollWidth`: con el recorte de la portada da valores mayores aunque no haya scroll.)

## HU-14b · Directorio y ficha en móvil y tablet

| ID | Qué hacer | Resultado esperado | Resultado |
|---|---|---|---|
| H14-2 | **A 390 px:** abre `/delegaciones/`. Baja por toda la página. Comprueba el scroll lateral (punto 5). Escribe `ETSII` en el buscador; borra y escribe `educacion` (sin tilde); borra y escribe `zzzz`; borra el texto.<br>**A 768 px:** repite el recorrido | Una columna de tarjetas a 390 px y dos a 768 px, con nombre, centro y «Ver ficha», sin textos cortados ni scroll lateral. El contador dice «27 delegaciones de centro». `ETSII` deja «1 delegación encontrada»; `educacion` encuentra las de Educación (ignora tildes y mayúsculas); `zzzz` muestra «No hay ninguna delegación con esa búsqueda. Prueba con otra palabra.»; al borrar vuelven las 27 | |
| H14-3 | **A 390 px y a 768 px:** desde el listado pulsa «Ver ficha» de la ETSII (la que tiene más datos). Mira la ficha entera sin desplazarte hacia los lados. Comprueba que el correo y el teléfono son enlaces y que caben bien en el dedo (no hace falta abrirlos). Pulsa «← Volver al listado».<br>Después abre la ficha de una delegación sin datos (por ejemplo la de Derecho) | Delegado, correo, teléfono, Instagram y lista de miembros visibles; ningún texto cortado ni scroll lateral; correo y teléfono enlazados y fáciles de tocar con el dedo; «Volver al listado» lleva a `/delegaciones/`. La ficha sin datos se lee bien y no deja campos vacíos a medias. **La parte de tablet era la que faltaba** | |

## HU-16a · Búsqueda y filtros de noticias y actas

Se prueban **con clics en el formulario**, no con la dirección escrita a mano, y se termina cada caso con el botón **Filtrar**. Cuando puedas, envía también uno con el teclado (Tab hasta el botón e Intro).

| ID | Qué hacer | Resultado esperado | Resultado |
|---|---|---|---|
| H16-1 | En `/noticias/` (Noticias y comunicados), escribe `becas` en «Palabra clave» y pulsa Filtrar | Solo sale el comunicado sobre becas (de 4) | |
| H16-2 | En `/noticias/`, pon **Desde** 15/10/2026 y **Hasta** 16/10/2026 y pulsa Filtrar | Salen las noticias del 15 y del 16, con los dos extremos incluidos | |
| H16-3 | En `/noticias/`, pon **Desde** 16/10/2026 y **Hasta** 14/10/2026 (al revés) y pulsa Filtrar | Sin error: se ordena el rango y salen las 3 noticias del 14 al 16 | |
| H16-4 | En `/actas-y-normativa/`, escribe `pleno`, pon **Desde** 01/10/2026 y elige el tipo **Acta**; pulsa Filtrar. Luego pulsa el chip **Normativa** | Sale solo el acta del pleno. Al pulsar «Normativa» se conservan la palabra y la fecha y sale «No hay documentos publicados para este filtro» | |
| H16-5 | En `/actas-y-normativa/`, pon **Desde** 01/01/2027 y **Hasta** 31/12/2027 con tipo **Acta** y pulsa Filtrar | Mensaje «No hay documentos publicados para este filtro» | |
| H16-6 | En `/actas-y-normativa/`, con un filtro puesto y el tipo **Acta** elegido, pulsa **Quitar filtros** | Vuelve el listado completo y se mantiene el tipo (la dirección acaba en `?tipo=acta`) | |

## Comprobación del pie (arreglo menor de HU-15)

Marcos midió con Lighthouse un fallo de contraste en `p.cadus-contacto__marca` (la palabra decorativa «CADUS» del pie, 1,32:1). En `main` ese elemento ya **no es un `<p>` con texto**: es un `<div aria-hidden="true">` cuya palabra sale de CSS (`::before`), así que Lighthouse no la evalúa, y por ser decorativa tampoco le aplica el contraste. Lo más probable es que lo que vio Marcos fuera una copia local, o una página en caché, sin esa versión. Para cerrarlo:

| Qué hacer | Resultado esperado | Resultado |
|---|---|---|
| Con `main` actualizado y la caché vaciada, abre la portada, haz clic derecho en la palabra grande del pie › Inspeccionar | Aparece `div.cadus-contacto__marca` con `aria-hidden="true"` y **sin texto** dentro | |
| `F12 › Lighthouse`, solo **Accesibilidad**, en la portada | 100 o muy cerca, y **sin** el fallo `color-contrast` de `cadus-contacto__marca` | |

Si Lighthouse sigue marcando ese elemento, no lo tapes: anota la puntuación y la pantalla y avisa, porque entonces el problema está en otra copia o en la caché.

## Cómo anotar los resultados

Escribe en la columna «Resultado» de arriba: **OK**, **Fallo** o **Pendiente** (con el motivo), la fecha, el ancho probado y tu nombre. Un ejemplo: «OK (DD/11/2026, Joaquín, Chrome a 390 y 768 px, con clics)». Si algo falla, anota **qué esperabas y qué pasó** y avisa a Álvaro: no arregles su código sin avisarle.

Cuando termines, copia el resultado a estos sitios, como línea añadida y sin tocar lo que ya hay:

- En [`E3-04-pruebas-de-aceptacion.md`](E3-04-pruebas-de-aceptacion.md), al final de la celda «Resultado» de cada fila H14-2, H14-3 y H16-1 a H16-6: `Prueba cruzada (Joaquín, DD/11/2026): …`.
- En [`HU-14b-movil-tablet.md`](HU-14b-movil-tablet.md), en las filas de H14-2 y H14-3, lo mismo; y si H14-3 a 768 px sale bien, la parte «falta la tablet» deja de estar pendiente.
- La cabecera de E3-04 dice «No hay prueba cruzada completa»: esa frase la cambia quien lleve el documento cuando todas las pruebas cruzadas estén hechas, no tú solo.
