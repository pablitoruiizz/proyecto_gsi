# Pruebas de HU-14a y HU-15a · Móvil, tablet y accesibilidad de la portada

**Historias:** HU-14a (menús y portada en móvil y tablet, 3 SP) y HU-15a (contraste, foco visible, teclado y «Saltar al contenido», 3 SP) · **Requisitos:** RNF-02, RNF-03 · UI-01, UI-02
**Código:** `assets/cadus.css` (bloque «tablet y móvil (HU-14a)», al final), `includes/accesibilidad.php`, `assets/cadus-accesibilidad.css` y `assets/cadus-accesibilidad.js`.
**Quién prueba lo manual:** una persona distinta de Joaquín (prueba cruzada), en dispositivos reales.

> Estado: lo medido abajo se hizo en un **navegador (Chromium) sobre una réplica estática** de la portada y de las páginas interiores, con el mismo marcado y los mismos CSS y JS del plugin. No incluye la cabecera real de Blocksy, que solo existe dentro de WordPress, ni dispositivos reales, ni lector de pantalla. Eso queda en la segunda parte (casos manuales). Hasta pasar esos casos, HU-14a y HU-15a no deben darse por cerradas.

## 1. Qué se midió y qué resultado dio

Anchos: 320, 360, 390, 430, 600, 768, 820, 1024 y 1280 px (el hero, además, cada 40 px de 761 a 2600). Se midió sobre el último commit del equipo (con el pie y el directorio rediseñados y Blocksy 2.1.61), antes y después de estos cambios. Se contó: desbordes laterales, zonas táctiles menores de 44 px, solape del texto con los arcos del hero, contraste de todos los textos visibles, y para cada parada del tabulador el contraste y el recorte del anillo de foco.

| Comprobación | Antes | Después |
|---|---|---|
| Hero desde 761 px: los contadores («3 actas…, 27 delegaciones…, 4 comunicados…») y el botón «Buscar mi delegación» se solapaban con los arcos | Sí, en 30 de los 47 anchos medidos (de 761 a 1921 px). A 1280 px «4 comunicados publicados» quedaba tapado por los arcos | Ningún ancho con contadores o botones sobre los arcos. Solo entre 1521 y 1701 px la línea dorada «de la Universidad de Sevilla» toca como mucho 38 × 8 px la esquina redondeada del arco dorado |
| Desborde lateral a 320 px | El campo del buscador salía 18 px de la pantalla | Sin desbordes de 320 a 1280 px |
| Zonas táctiles menores de 44 px (de 320 a 1024 px) | 5 o 6: el enlace «¡Quiero saber más!» de cada noticia (20 px de alto) y «Subir» (19 px) | 0 de 320 a 390 px; 1 desde 430 px (el título enlazado de la primera noticia, de 28 px de alto, que es texto en línea). Los enlaces del pie nuevo miden 36 px y no se han tocado |
| «Nuestro trabajo» entre 761 y 1000 px | Reparto 8/4: «Vida Universitaria» en una columna de unos 280 px | Dos columnas iguales |
| Buscador entre 761 y 1000 px | El texto de ayuda del campo se cortaba | El campo ocupa su propia fila |
| Contraste de los textos | Sin fallos de texto en la portada. En las interiores, un enlace granate sobre el bloque granate del resultado del seguimiento (1:1) si el bloque llevara alguno; hoy no los lleva | Sin fallos |
| Foco visible, portada | 1 fallo: el botón «Ver actas y normativa» sobre la tarjeta granate (anillo oscuro, 1,63:1) | 0 fallos |
| Foco visible, interiores | 1 anillo recortado: «Descargar PDF» de la tabla de actas en móvil, cuya fila recorta lo que sobresale (el directorio rediseñado por el equipo ya no tiene el problema) | 0 fallos |
| Campos de texto | Sin borde: blanco sobre dorado (buscador) 1,74:1; gris claro sobre blanco 1,1:1 | Borde de 2 px en tinta: 8,9:1 y 15,4:1 (buscador de la portada, del directorio y campos del buzón) |
| «Saltar al contenido» | Primer foco, con el aspecto del tema; al activarlo el foco se quedaba en `<body>` | Primer foco, blanco sobre granate (9,45:1) y anillo con halo; al activarlo el foco pasa a `<main>` |
| Orden del tabulador | 50 o 51 paradas en la portada, igual que el orden visual, sin trampas | Igual |

### Contraste de la paleta (textos y anillos)

| Combinación | Contraste |
|---|---|
| Blanco sobre granate | 9,45:1 |
| Dorado sobre granate | 5,44:1 |
| Granate oscuro sobre dorado | 7,19:1 |
| Tinta sobre blanco / sobre gris | 15,43:1 / 13,66:1 |
| Granate sobre blanco / sobre gris | 9,45:1 / 8,37:1 |
| Blanco sobre tinta / dorado sobre tinta | 15,43:1 / 8,88:1 |
| Gris de texto secundario (`#4b5157`) sobre blanco / gris | 8,03:1 / 7,11:1 |
| Rojo de error (`#a4111f`) sobre blanco / gris | 7,84:1 / 6,94:1 |
| **Anillo tinta sobre granate** (antes del cambio) | **1,63:1** |
| **Borde blanco de un campo sobre dorado** (antes) | **1,74:1** |

Los textos pasan AA (4,5:1) con margen; los fallos eran de componentes (WCAG 1.4.11, 3:1).

## 2. Archivos cambiados

| Archivo | Cambio |
|---|---|
| `assets/cadus.css` | Solo añadidos al final: límite de ancho de contadores y botones del hero junto a los arcos, buscador que puede encogerse, dos columnas en «Nuestro trabajo» y campo del buscador en fila propia en tablet, zonas táctiles de 44 px (noticias y «Subir») y menú plegable de Blocksy más alto |
| `assets/cadus-accesibilidad.css` (nuevo) | Enlace «Saltar al contenido», anillo de foco de dos tonos, botón de la tarjeta granate, borde de los campos, anillo interior en «Descargar PDF» en móvil |
| `assets/cadus-accesibilidad.js` (nuevo) | El foco pasa a `<main>` al usar «Saltar al contenido» |
| `includes/accesibilidad.php` (nuevo) | Carga el CSS y el JS anteriores y traduce los textos accesibles del menú plegable de Blocksy (`Menu`, `Close drawer`, `Offcanvas modal`, `Expand dropdown menu`, `Search modal`, `Close search modal`, `Go to top`) |
| `cadus-portal.php`, `README.md` | Una línea para cargar el módulo y su documentación |

No se tocó `cadus-interior.css` (HU-14b y HU-15c): las correcciones de las páginas interiores van en `cadus-accesibilidad.css`, que se carga después.

## 3. Casos manuales (dispositivos reales)

Antes de empezar: actualizar el repositorio en el servidor, **vaciar la caché de WP Fastest Cache** y comprobar en el código fuente de la portada que se cargan `cadus-accesibilidad.css` y `cadus-accesibilidad.js`.

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| 1 | Móvil (hasta 430 px): recorrer la portada de arriba abajo | Sin desplazamiento horizontal; hero, accesos, noticias, eventos, galería de 2 columnas, buscador, pasos y pie legibles | |
| 2 | Móvil: carrusel de noticias | Se desliza con el dedo y los filtros por categoría funcionan | |
| 3 | Móvil y tablet: abrir el menú plegable | Se abre y se cierra; cada elemento mide unos 48 px de alto y es fácil de pulsar | |
| 4 | Móvil: botón de abrir el menú y botón de cerrar | Zona táctil de al menos 44 px | |
| 5 | Tablet vertical (768 px) y horizontal (1024 px): hero | Los contadores y los botones quedan a la izquierda de los arcos, sin taparse | |
| 6 | Tablet: «Nuestro trabajo» y buscador | Dos columnas iguales; el campo del buscador ocupa una fila y se lee entero | |
| 7 | Teclado: primera pulsación del tabulador | Aparece «Saltar al contenido», blanco sobre granate, arriba a la izquierda | |
| 8 | Teclado: Intro sobre «Saltar al contenido» y luego el tabulador | El foco va al contenido principal y la siguiente parada es el primer control de la página (no la cabecera) | |
| 9 | Teclado: recorrer toda la portada | Cada elemento enfocado muestra un anillo bien visible, también sobre granate, dorado y fondos oscuros; orden igual al visual; sin trampas | |
| 10 | Teclado: carrusel y filtros | El carrusel se desplaza con las flechas al enfocarlo; los filtros se activan con Intro y con Espacio | |
| 11 | Teclado: menú plegable | Se abre y cierra con teclado (Escape cierra) y el foco no se pierde | |
| 12 | Móvil: tabla de actas, tabulador hasta «Descargar PDF» | El anillo del botón se ve entero, dentro del botón | |
| 13 | Buscador de la portada, buscador del directorio y buzón | Los campos tienen un borde oscuro visible | |
| 14 | Lector de pantalla (NVDA o TalkBack): menú | Se anuncian «Menú», «Cerrar el menú» y «Desplegar el submenú», en español | |
| 15 | Zoom al 200 % y al 400 % | Sin desplazamiento horizontal y sin texto cortado | |

## 4. Lo que no cubre este documento
- **No se probó en dispositivos reales ni con lector de pantalla**: son los casos 1 a 15.
- **La cabecera y el menú plegable los genera Blocksy**; sus ajustes se hicieron leyendo su CSS y su PHP, no viéndolos funcionar. Si algo no se ve como se espera (casos 3, 4, 11 y 14), ahí es donde hay que mirar.
- **Auditoría con Lighthouse y axe, daltonismo y pautas DUA** son de HU-15c, no de esta tarea.
- **El contraste del pie y de las secciones se midió sobre datos de ejemplo**: si el cliente cambia los colores definitivos, hay que repetirlo.
