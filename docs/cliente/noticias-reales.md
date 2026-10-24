# Noticias reales y comprobación de la portada (E2-08)

**Responsable:** Joaquín Luna Canela · **Sprint 2** · **Requisitos:** RF-01, RF-02, IR-01, IR-03, UI-02 · **Historias:** HU-01, HU-02
**Contenido que aporta:** el CADUS, a través de Miguel Ángel (contacto con el cliente, E2-09). Esta hoja recoge lo que hay que pedir, cómo cargarlo y qué comprobar.

> No se inventan comunicados. Hasta que el CADUS entregue y valide los textos reales, la portada sigue con los comunicados de ejemplo, que ya están marcados como tales (plan de riesgos del Sprint 2). La web oficial no permite la descarga automática, así que los textos hay que copiarlos a mano con permiso del CADUS.

## 1. Estado actual

- La portada y el listado de noticias muestran cuatro comunicados de ejemplo, uno por categoría: «Comunicado de ejemplo sobre becas / movilidad / normativa / eventos». Los crea `includes/setup.php` al activar el plugin y llevan la marca interna `_cadus_semilla`.
- El carrusel «¡Últimas noticias!» usa el **extracto** de cada entrada (si no tiene, recorta el cuerpo a unas 22 palabras), su categoría y su fecha de publicación.
- «¡Últimos eventos!» ya sale del calendario (HU-10, `calendario.php`) cuando The Events Calendar está activo; las noticias de la categoría Eventos solo se usan si el calendario no está disponible.
- Los contadores del banner («actas y normativas», «delegaciones» y «comunicados publicados») cuentan contenido publicado: al sustituir los ejemplos cambiarán solos.

## 2. Qué pedir al CADUS

Mínimo para la entrega: **cuatro comunicados reales, uno por categoría** (Becas, Movilidad, Normativa y Eventos) y permiso para publicarlos. Para cada uno:

| Dato | Detalle | Recibido |
|---|---|---|
| Título | Tal como lo publicaría el CADUS | |
| Categoría | Becas, Movilidad, Normativa o Eventos (IR-03) | |
| Fecha de publicación | La real, para que el orden y el filtro por año sean correctos | |
| Resumen | Una o dos frases (se guarda como extracto) | |
| Cuerpo | Texto final, sin datos personales de estudiantes | |
| Imagen destacada | Opcional, con permiso de uso | |
| Validado por | Persona del CADUS que da el visto bueno | |

Anotar en Discord (`#scrum`) quién validó cada comunicado y cuándo; sirve de evidencia para la entrega.

## 3. Cómo cargarlos

1. En WordPress: **Entradas**. Localizar los cuatro «Comunicado de ejemplo…».
2. **Editarlos en lugar de borrarlos**: cambiar título, categoría, fecha, extracto y cuerpo. Así conservan la marca `_cadus_semilla` y reactivar el plugin no los vuelve a crear (el README del plugin lo documenta). Si se mueven a la papelera, la activación puede recrearlos.
3. Rellenar el campo **Extracto** de cada entrada.
4. Si el CADUS entrega más de cuatro comunicados, añadir el resto como entradas nuevas con su categoría.
5. Vaciar la caché de WP Fastest Cache y revisar la portada con una ventana privada (sin sesión iniciada).

## 4. Comprobación del banner y de la portada

- [ ] Banner: el título, el lema y los botones «Enviar una consulta» y «Buscar mi delegación» llevan a sus páginas.
- [ ] Contadores del banner: coinciden con lo publicado en Entradas, Actas y Delegaciones.
- [ ] «Todo lo que necesitas»: los accesos enlazan bien y «Calendario y votaciones» ya no aparece como «En preparación».
- [ ] «¡Últimas noticias!»: aparecen los comunicados reales con su categoría; los filtros por categoría funcionan; no queda ningún «Comunicado de ejemplo».
- [ ] «¡Últimos eventos!» y, si hay votaciones abiertas o próximas, «Participa en las votaciones» (HU-11).
- [ ] Listado de noticias: filtro por palabra clave, categoría y año (HU-02) con los comunicados reales.
- [ ] Vista en móvil (unos 390 px) y con teclado, sin elementos cortados.
- [ ] Capturas a 1920×1080 con pie y códigos IR-01, UI-02, RF-01, RF-02, HU-01 y HU-02.

## 5. Textos de la portada que hay que validar con el CADUS

Están en el código y proceden de la web oficial o de una primera redacción. No los he cambiado: los decide el cliente.

| Dónde | Qué hay | Por qué revisarlo |
|---|---|---|
| `includes/portada_extra.php` · `cadus_shortcode_trabajo()` | Objetivos de la web oficial, entre ellos «Campaña Orgullo 2024» y «Organizar IV Jornadas de Formación del CADUS» | Están fechados y no corresponden al curso actual; el propio código avisa de que deben revisarse con el CADUS. |
| `includes/portada_extra.php` · `cadus_shortcode_contacto()` | Correo `dcadus@us.es`, teléfono `954 48 60 22` y «Av. de Chile s/n» | El documento de la entrega y las páginas del portal usan `cadus@us.es` y «Pabellón de Uruguay, Av. de Chile, s/n». Confirmar cuáles son los datos de contacto vigentes. |
| `includes/portada_extra.php` · `cadus_shortcode_intro()` | «Más de 40 años dando voz al alumnado» | Confirmar la cifra y el texto. |
| Fotos de la portada (`assets/fotos/`) | Fotografías tomadas de cadus.us.es | El README del plugin ya indica que hay que confirmar con el cliente su uso y la autorización de las personas que aparecen. |

Si el cliente pide cambios en esos textos, se editan en `includes/portada_extra.php` y se avisa a su autor (Codex en el reparto del plugin) antes de tocarlo.
