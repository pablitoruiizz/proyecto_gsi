# Pruebas de la Red Social Interna (Teams)

Registro de la configuración del piloto y de las pruebas con cuentas distintas. Solo datos de ejemplo (RNF-R01). Autor de la configuración: Marcos-Paban Delgado Rodríguez, con su cuenta, que es propietaria de los tres equipos.

## Configuración del 21/11/2026 (R-05)

| Paso | Equipo | Qué se hizo | Resultado | Captura | Requisitos |
|---|---|---|---|---|---|
| 1 | CADUS · Ejecutiva | Canal estándar «Preparación de avisos» | OK: el equipo tiene General y Preparación de avisos | 10-ejecutiva-canales.jpg | RF-R02 |
| 3 | CADUS · Delegaciones | Moderación del canal General: «Solo los propietarios pueden publicar mensajes» | OK | 03-delegaciones-avisos.jpg | RF-R05 · RN-R01 |
| 4 | CADUS · Delegaciones | Renombrar el canal General a «Avisos» | OK: Teams permite cambiar el nombre (no ofrece descripción en esa ventana) | 11-delegaciones-avisos-renombrado.jpg | RF-R05 |
| 5 | CADUS · Delegaciones | Canales privados «Delegación · ETSII» (con Álvaro), «Delegación · Derecho» (con Marcos) y «Delegación · Biología» (con Joaquín) | OK: los tres aparecen con candado | 04-delegaciones-canales-privados.jpg | RF-R03 · CU-R05 |
| 6 | CADUS · Delegaciones | Patrón para las 27 delegaciones | Se crean 3 de ejemplo; el límite de canales privados por equipo es el motivo de usar tres equipos | — | RC-R02 |
| 7 | CADUS · Asamblea | Canal estándar «Cursos» | OK | 06-asamblea-calendario.jpg | RF-R04 |
| 8 | CADUS · Asamblea | Pestaña «Calendario del canal» en General y evento «Asamblea Noviembre» el 26/11/2026 de 17:00 a 18:00 | OK | 06-asamblea-calendario.jpg | RF-R08 · CU-R02 |
| 9 | CADUS · Asamblea | Pestaña de SharePoint en General que abre el sitio del DMS «CADUS Órganos de gobierno» (actas y plantilla de acta) | OK: los documentos se abren desde el DMS, no se copian a Teams | 07-archivos-dms.jpg | RF-R07 · RN-R03 · CU-R03 |

## Pruebas con otra cuenta (pendientes)

| Fecha | Quién | Qué | Resultado |
|---|---|---|---|
| 21/11/2026 | Joaquín, con su cuenta | En CADUS · Delegaciones solo ve «Avisos» y su propio canal privado, no los de las otras delegaciones (captura 05-vista-miembro.jpg) | OK: ve «Avisos» y «Delegación · Biología»; no aparecen «Delegación · ETSII» ni «Delegación · Derecho». Joaquín es propietario del equipo, pero un canal privado solo lo ven sus miembros, así que la prueba vale para RN-R02. |
| | Una cuenta que sea solo miembro | No puede iniciar una conversación en «Avisos» | PENDIENTE: los cuatro integrantes son propietarios desde el 20/11; hace falta pasar a uno a miembro durante la prueba |
