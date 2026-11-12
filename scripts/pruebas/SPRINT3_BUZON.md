# Pruebas del Sprint 3 del buzón (HU-17a, HU-16b, HU-15b, E3-08)

Ejecutadas el 11 y el 12/11/2026 en el entorno local (WampServer, Apache 2.4.65 con PHP 8.3.28, también en la línea de comandos), con WordPress 7.1 y Fluent Forms 6.2.16.

## Baterías y resultados

| Batería | Qué comprueba | Correctas | Fallos |
|---|---|---|---|
| `hu15b_accesibilidad.py` | HU-15b: en las siete páginas de Atención al estudiante (incluida la respuesta del seguimiento), idioma, título, región `<main>`, un único h1, jerarquía de encabezados sin saltos, texto alternativo, etiquetas de los campos, texto de botones y enlaces, y que la respuesta del seguimiento reciba el foco y se anuncie. Lista lo que anuncia un lector de pantalla en los formularios. | 59 | 0 |
| `sprint3_buzon.py` | HU-17a (nonce, campo trampa y límite de envíos), E3-08 (datos mínimos, centros del desplegable, un único aviso a la Ejecutiva sin datos del ticket, sin copia en Fluent Forms) y HU-16b (búsqueda en el panel por asunto y código, nunca por descripción, correo o nombre), por CLI y por HTTP. | 81 | 0 |
| `privacidad_tickets.py` | RN-03 como visitante anónimo: URLs directas, búsqueda, feeds, sitemaps y API REST no muestran tickets. | 43 | 0 |
| `rn03_http.py` | RN-03 con un ticket real enviado por Fluent Forms: rutas directas (incluido `/?p=ID&feed=rss2`), rutas públicas, REST y panel para el visitante anónimo y cinco cuentas (administrador, dos de la Ejecutiva, delegado y estudiante), seguimiento y limpieza final. | 254 | 0 |
| `rn03_mediacion.py` | Lo mismo para las solicitudes de mediación estudiantil, más los errores no cacheables del formulario y la limpieza de cuentas temporales. | 316 | 0 |

Las salidas completas están en `Desktop\sprint3-revision\salidas` y el HTML analizado por la batería de accesibilidad en `Desktop\sprint3-revision\html`. Todas las baterías terminan sin tickets, solicitudes, entradas de Fluent Forms ni usuarios de prueba.

## Hallazgos y correcciones

- **Salto de h1 a h3 en Atención al estudiante (HU-15b).** Las tarjetas de la página (Buzón de consultas, Seguimiento de ticket, etc.) son h3 y colgaban directamente del h1 de la página. Se añade el encabezado h2 «Servicios de atención» encima de las tarjetas, tanto al crear la página (`cadus_portal_configurar`) como en las instalaciones existentes (`cadus_actualizar_atencion`, versión 3), solo si la página conserva las tarjetas y aún no tiene ningún h2. La jerarquía queda `h1 > h2 > h3 > h3 > h3 > h3 > h2`.
- **Feed de entradas privadas (RN-03).** `/?p=ID&feed=rss2` sobre un ticket o una solicitud de mediación devolvía HTTP 200 a cualquier visitante, con un feed de comentarios vacío: título «Comentarios en:» sin nombre, sin enlace y sin elementos. No llevaba datos del ticket (ni asunto, ni código, ni descripción, ni correo), pero confirmaba que el ID existía. Ahora el `template_redirect` de prioridad -1 de `privacidad.php` trata ese feed (y el de un adjunto de un ticket) como el resto de rutas privadas y responde 404. `/feed/`, `/comments/feed/` y el feed de una noticia pública siguen dando 200.

## Lo que anuncia un lector de pantalla

Recorrido con el tabulador según la salida de `hu15b_accesibilidad.py`.

**Buzón de consultas**

1. campo de texto: «Nombre y apellidos», obligatorio
2. campo de correo: «Correo universitario», obligatorio
3. desplegable: «Facultad o Escuela», obligatorio
4. campo de texto: «Asunto», obligatorio
5. desplegable: «Tipo», obligatorio
6. área de texto: «Descripción», obligatorio
7. casilla: «Consiento el tratamiento de mis datos por el CADUS para gestionar esta consulta o reclamación, conforme al RGPD.», obligatorio
8. botón: «Enviar al CADUS»

**Seguimiento de ticket**

1. campo de texto: «Código de seguimiento», obligatorio. Ayuda: Empieza por CAD- y lo recibiste al enviar tu consulta.
2. campo de correo: «Correo universitario», obligatorio. Ayuda: El mismo correo @alum.us.es con el que enviaste la consulta.
3. botón: «Consultar seguimiento»

**Mediación estudiantil**

1. campo de texto: «Nombre y apellidos», obligatorio
2. campo de correo: «Correo universitario», obligatorio
3. desplegable: «Facultad o Escuela», obligatorio
4. área de texto: «Descripción del conflicto», obligatorio
5. casilla: «Consiento el tratamiento de mis datos por el CADUS para gestionar esta solicitud de mediación, conforme al RGPD.», obligatorio
6. botón: «Solicitar mediación»

## Qué queda fuera

- La prueba con un lector de pantalla real y en dispositivos físicos, que corresponde a E3-04 y HU-14c.
- El contraste, el foco visible y el daltonismo, que corresponden a HU-15a y HU-15c.
