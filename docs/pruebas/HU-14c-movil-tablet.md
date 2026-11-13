# HU-14c · Pruebas en móvil y tablet (12/11/2026)

Estado: **hecha la parte que se puede automatizar con emulación; falta probar en dispositivos reales** (lista al final). Son 28 inspecciones de páginas cargadas (14 páginas × 2 tamaños): no abren menús, no envían formularios y no incluyen `/gestion/` con la sesión iniciada. Script reproducible: `python scripts/pruebas/movil.py` (Chrome emulado con Playwright, con el sitio local arrancado).

## Qué se comprueba
En 14 páginas (portada, noticias, delegaciones, una ficha de delegación, actas y normativa, calendario, Atención al estudiante, buzón, seguimiento de ticket, mediación, preguntas frecuentes, votaciones, acceso y contacto) y con dos tamaños: **móvil 375 × 812** y **tablet 768 × 1024**, con pantalla táctil y densidad 2×:

- que no haya desplazamiento horizontal de la página ni elementos que se salgan por la derecha (se excluye todo elemento que esté dentro de un contenedor con `overflow` automático, de desplazamiento, oculto o recortado: los carruseles, pero también cualquier contenedor que recorte su contenido, que por tanto no se revisa);
- que los botones, enlaces, casillas y campos midan al menos 40 px para tocarlos con el dedo (el mínimo de WCAG 2.2 es 24 px; Apple y Google recomiendan 44–48 px). El script admite dos excepciones, que bajan el mínimo a 24 px: los enlaces de más de 12 caracteres dentro de un párrafo o una lista y las casillas de verificación;
- que los campos de formulario tengan letra de 16 px o más (en iOS, con menos, la página se amplía al tocar el campo);
- que la página responda 200.

## Qué se encontró (antes de corregir) y qué se hizo
| Hallazgo | Dónde | Corrección (`assets/cadus-interior.css`, bloque «toques en móvil y tablet») |
|---|---|---|
| Botón del menú (hamburguesa) de 18 × 18 px | todas las páginas | mínimo 44 × 44 px |
| Casilla de consentimiento de 13 × 13 px | buzón y mediación | casilla de 26 px con la etiqueta alineada |
| Teléfono y correo del pie de 26 px de alto, enlace «Delegaciones» del pie de 36 px | todas | zona táctil de 44 px |
| Controles del calendario (Buscar, Lista, Próximos, anterior, Hoy, siguiente) de 21–33 px | calendario | mínimo 44 px |
| Preguntas frecuentes de 26 px de alto | preguntas frecuentes | 44 px |
| Enlaces sueltos en fichas, tablas, títulos de listados, correo, teléfono y «¿Has olvidado tu contraseña?» de 21–30 px | ficha de delegación, actas, calendario, votaciones, acceso, contacto | relleno vertical hasta superar los 40 px |

No se encontró desplazamiento horizontal ni letra de campos menor de 16 px en ninguna página y tamaño; los campos del buzón y de la mediación ya cumplían.

## Resultado después de corregir
**28 de 28 comprobaciones correctas** (14 páginas × 2 tamaños), `0 páginas con algo que revisar`. Se revisaron además capturas de la ficha de delegación, el calendario y el buzón a 375 px: el diseño se mantiene y nada se solapa.

## Qué NO cubre la emulación (hay que probarlo en dispositivos reales)
Lo hace una persona con un móvil y una tablet reales; anotar modelo, sistema y navegador:

1. **Buzón de consultas (iPhone y Android):** abrir el teclado en cada campo (la página no debe saltar ni tapar el botón «Enviar»), marcar la casilla de consentimiento con el pulgar y enviar una consulta de prueba hasta recibir el código.
2. **Seguimiento de ticket:** escribir el código y el correo y consultar el estado; comprobar que el teclado correcto sale en el campo de correo.
3. **Mediación:** igual que el buzón, con un correo @alum.us.es.
4. **Calendario:** cambiar de vista (lista, mes), pasar de semana con «anterior» y «siguiente» y abrir un evento con el dedo.
5. **Menú:** abrir y cerrar el menú de hamburguesa, entrar en «Atención al estudiante» y en «Calendario» con sus submenús.
6. **Directorio de delegaciones:** usar el buscador con el teclado del móvil y abrir una ficha; pulsar el correo (abre la app de correo) y el Instagram (abre la app o el navegador).
7. **Gestión desde el portal** (con la cuenta de la Ejecutiva, en una tablet): crear una noticia y un evento, elegir fecha y hora con los selectores del sistema y subir un PDF de acta desde el almacenamiento del dispositivo.
8. **Orientación:** girar la pantalla en cada una y comprobar que no aparece desplazamiento horizontal.
9. **Navegador del móvil:** una vez en Chrome y otra en Safari (o el navegador de Samsung) en el caso de Android/iPhone.

Si algo falla, anotar la página, el dispositivo y una captura; la corrección va en `cadus-interior.css` y se vuelve a pasar `scripts/pruebas/movil.py`.

## Aviso al desplegar
WP Fastest Cache guarda el CSS minificado: tras cambiar un `.css` hay que usar **«Clear Cache and Minified CSS/JS»** en su pantalla de ajustes (o borrar `wp-content/cache`) para que el visitante reciba la versión nueva.
