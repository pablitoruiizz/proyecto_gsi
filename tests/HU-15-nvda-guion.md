# Guion de la prueba con NVDA (HU-15 · H15-3)

**Estado a 27/11/2026: sin ejecutar.** El 27/11 se descargó NVDA 2026.3.1 (firmado por NV Access) y se arrancó en una copia portable, y NVDA llegó a leer la ventana de Chrome; pero no se pudo recorrer la página con el teclado porque las herramientas que se usaron para manejar Chrome no entregan sus teclas a la ventana activa del sistema, que es la que NVDA escucha. Hace falta una persona con el teclado delante. Se desinstaló todo y no quedan restos en el equipo.

**Quién:** cualquier persona del equipo, unos 15 minutos. **Qué se anota:** lo que NVDA dice en cada paso (se puede copiar con el *Visor de voz*: menú NVDA › Herramientas › Visor de voz) y si es correcto, en la fila H15-3 de `E3-04-pruebas-de-aceptacion.md`, con fecha y nombre.

## Preparación
1. Descargar NVDA de https://www.nvaccess.org/download/ (instalar o crear una copia portable) y arrancarlo.
2. Abrir Chrome en `http://localhost/proyecto_gsi/cms-wordpress/atencion-al-estudiante/buzon-de-consultas/` (con el servidor del equipo encendido).

## Buzón de consultas (HU-15a/b)
| # | Qué hacer | Qué debe decir NVDA |
|---|---|---|
| 1 | Pulsar Tab una vez | «Saltar al contenido», enlace |
| 2 | Pulsar Intro en ese enlace | El foco pasa al contenido principal y NVDA lo anuncia |
| 3 | Recorrer los campos con Tab | Cada campo se lee con su etiqueta y su tipo («Nombre y apellidos», «Correo universitario», «Facultad o Escuela», «Asunto», «Tipo», «Descripción», casilla del consentimiento) |
| 4 | Pulsar el botón de enviar con el formulario vacío | Los errores se anuncian y están enlazados con su campo (arreglo del PR #96) |
| 5 | Rellenar con datos de ejemplo (correo `@alum.us.es`) y enviar | Se anuncia el resultado y el código de seguimiento `CAD-…` |

## Seguimiento de ticket (HU-15b)
| # | Qué hacer | Qué debe decir NVDA |
|---|---|---|
| 6 | Abrir `…/atencion-al-estudiante/seguimiento-de-ticket/` y recorrer los dos campos | La ayuda de cada campo se lee junto a él («Empieza por CAD-…», «El mismo correo @alum.us.es…») |
| 7 | Consultar con el código del paso 5 | El foco pasa al resultado y NVDA empieza leyéndolo (estado y respuestas) |

## Al terminar
Borrar el ticket de prueba desde **Tickets del buzón** en el panel y cerrar NVDA. Si algo no se lee bien, anotar el texto exacto y el elemento, y abrir una issue.
