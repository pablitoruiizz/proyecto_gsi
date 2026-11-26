# Pruebas de la Red Social Interna (Teams)

Registro de la configuración del piloto y de las pruebas con cuentas distintas. Solo datos de ejemplo (RNF-R01). Autor de la configuración: Marcos-Paban Delgado Rodríguez, con su cuenta, que es propietaria de los tres equipos.

## Configuración del 21/11/2026 (R-05)

| Paso | Equipo | Qué se hizo | Resultado | Captura | Requisitos |
|---|---|---|---|---|---|
| 1 | CADUS · Ejecutiva | Canal estándar «Preparación de avisos» | OK: el equipo tiene General y Preparación de avisos | 10-ejecutiva-canales.jpg | RF-R02 |
| 3 | CADUS · Delegaciones | Moderación del canal General: «Solo los propietarios pueden publicar mensajes» | OK | 03-delegaciones-avisos.jpg | RF-R05 · RN-R01 |
| 4 | CADUS · Delegaciones | Renombrar el canal General a «Avisos» | OK: Teams permite cambiar el nombre (no ofrece descripción en esa ventana) | 11-delegaciones-avisos-renombrado.jpg | RF-R05 |
| 5 | CADUS · Delegaciones | Canales privados «Delegación · ETSII» (con Álvaro), «Delegación · Derecho» (con Marcos) y «Delegación · Biología» (con Joaquín) | OK: los tres aparecen con candado | 04-delegaciones-canales-privados.jpg | RF-R03 · CU-R05 |
| 6 | CADUS · Delegaciones | Patrón para las 27 delegaciones | Se crean 3 de ejemplo; los tres equipos se justifican por la separación de miembros, permisos y herramientas (el límite de canales del tenant no se ha comprobado; revisado por Pablo el 22/11) | — | RC-R02 |
| 7 | CADUS · Asamblea | Canal estándar «Cursos» | OK | 06-asamblea-calendario.jpg | RF-R04 |
| 8 | CADUS · Asamblea | Pestaña «Calendario del canal» en General y evento «Asamblea Noviembre» el 26/11/2026 de 17:00 a 18:00 | OK | 06-asamblea-calendario.jpg | RF-R08 · CU-R02 |
| 9 | CADUS · Asamblea | Pestaña de SharePoint en General que abre el sitio del DMS «CADUS Órganos de gobierno» (actas y plantilla de acta) | OK: los documentos se abren desde el DMS, no se copian a Teams | 07-archivos-dms.jpg | RF-R07 · RN-R03 · CU-R03 |

## Pruebas con otra cuenta

| Fecha | Quién | Qué | Resultado |
|---|---|---|---|
| 21/11/2026 | Joaquín, con su cuenta | En CADUS · Delegaciones solo ve «Avisos» y su propio canal privado, no los de las otras delegaciones (captura 05-vista-miembro.jpg) | OK: ve «Avisos» y «Delegación · Biología»; no aparecen «Delegación · ETSII» ni «Delegación · Derecho». Joaquín es propietario del equipo, pero un canal privado solo lo ven sus miembros, así que la prueba vale para RN-R02. |
| 22/11/2026 | Álvaro, con su cuenta de la US como **Miembro** (no propietario) de CADUS · Delegaciones; se le bajó de Propietario para la prueba (por orden de Pablo, desde Teams) y se le volvió a subir al terminar | 1) No puede iniciar una conversación en «Avisos». 2) Solo ve «Avisos» y el canal privado del que es miembro, no los de las otras delegaciones (capturas 05b y 05c) | OK: 1) en «Avisos» no puede publicar y Teams muestra «Solo los moderadores del canal pueden publicar en este canal.» (RN-R01, captura 05b). 2) En la lista de canales solo ve «Avisos» y «Delegación · ETSII» (del que es miembro); no ve «Delegación · Derecho» ni «Delegación · Biología» (RN-R02, captura 05c). Las capturas no muestran el rol: la prueba se hizo con el rol de Miembro, como consta en esta fila. Álvaro vuelve a ser Propietario (comprobado en Teams el 22/11). |

## Revisión del caso de negocio (RSI-HU-01)

Revisión de Álvaro Martínez Ocaña (con Claude) del 26/11/2026 sobre `business-case.md` (versión del 22/11/2026, autor Pablo, con el párrafo de Planner del 24/11). Se comprobó cada afirmación sobre el CADUS contra `docs/cliente/entrevista-cliente.md` y el estado del resto de la red social contra el repositorio. El orden de los apartados frente a la diapositiva 11 del Lab 5 no se pudo comprobar con el texto del PDF (las diapositivas son imágenes); el documento sigue el índice que declara (1.1 a 1.7).

| Nº | Apartado | Qué se comprobó | Resultado |
|---|---|---|---|
| 1 | 1.2 Situación actual | Cuenta única `dcadus@us.es`, 27 delegaciones con una cuenta por delegación, asambleas presenciales con un voto por delegación y cursos | OK: constan en la entrevista (preguntas 1 a 6 y 16). Lo que no consta (herramientas actuales, presupuesto, Teams en las cuentas de delegación) está marcado «(por confirmar)» |
| 2 | 1.4 Drivers | «Todas las consultas con total privacidad» | OK: pregunta 9 de la entrevista |
| 3 | 1.3 Diseño de los tableros de Planner | Coherencia con `diseno-tableros-planner.md` | OK: mismos patrones y mismos cuatro cubos del plan de la asamblea. El UML de diseño ya los recoge (26/11) |
| 4 | Preguntas abiertas, punto 5 | «Álvaro comprobó que sus páginas de creación cargan; no que se pueda guardar y ejecutar» | **Desactualizado:** el 25/11 se guardó y ejecutó en vista previa la aplicación de PowerApps (capturas R13-01 a R13-03) y hay capturas de los dos flujos de Power Automate (12a a 12d). Propuesta: «El tenant permite guardar y ejecutar una aplicación de lienzo y flujos de Power Automate (25/11/2026); no se ha comprobado publicar la aplicación» |
| 5 | 1.6 Riesgos, fila «No se pueden crear equipos o usar Power Automate y PowerApps» | Estado del riesgo | **Desactualizado** por lo mismo: añadir que el 25/11 se comprobó que sí se pueden usar |
| 6 | 1.7.1 Personas, fila de Álvaro | Papel en el proyecto | **Incompleto:** además de revisar el UML, hizo la aplicación de PowerApps (R-13) y actualizó el UML de diseño (R-14a). Propuesta: «UML de análisis y de diseño; aplicación de PowerApps» |
| 7 | Cabecera | «Revisión: pendiente de otra persona del equipo» | Cambiar a «Revisión: Álvaro Martínez Ocaña, 26/11/2026 (`pruebas.md`)» |

Conclusión: el caso de negocio no afirma hechos del CADUS sin respaldo. Los puntos 4 a 7 son correcciones de estado que debe hacer su editor (Pablo).
