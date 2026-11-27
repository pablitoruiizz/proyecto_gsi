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

## Prueba de Power Automate por otra persona (R-12c · RSI-HU-07)

Hecha el 25/11/2026 por Marcos, con su cuenta de la US, sobre los dos flujos de Joaquín y el plan «Preparación de la Asamblea». Pruebas de la tabla de [`configuracion-power-automate.md`](configuracion-power-automate.md).

| # | Prueba | Resultado | Captura |
|---|---|---|---|
| 1 | Crear en el plan una tarea nueva con responsable y fecha | OK: tarea «Prueba de Marcos del flujo (ejemplo)», con vencimiento el 26/11/2026, creada a las 22:34; el aviso con su título y su fecha sale en General de CADUS · Asamblea a las 22:39 (5 minutos) | 12e-r12c-tarea-creada.jpg · 12f-r12c-aviso-en-general.jpg |
| 2 | Historial de ejecuciones del flujo 1 | OK: la ejecución de las 22:39 aparece como Correcto | 12g-r12c-historial-flujo1.jpg |
| 3 | Ejecutar a mano el flujo 2 con esa tarea sin completar, que vence mañana | OK: ejecución de las 22:49 Correcto; el mensaje «Tareas que vencen hoy o mañana…» en General incluye «Prueba de Marcos del flujo (ejemplo) · 26/11/2026» | 12h-r12c-historial-flujo2.jpg · 12i-r12c-tabla-con-tarea.jpg |
| 4 | Completar la tarea y volver a ejecutar el flujo 2 | OK: tarea marcada como completada en Planner; el mensaje nuevo de las 22:53 lista las otras 5 tareas pendientes y ya no incluye la de prueba | 12j-r12c-tabla-sin-tarea.jpg |
| 5 | Marcos figura como propietario de los dos flujos | OK: el flujo 1 aparece en «Compartido conmigo» (captura hecha antes de que Joaquín compartiera el flujo 2, el 25/11 durante la prueba) y en la página del flujo 2 figura como copropietario junto a Joaquín (JC y MR); puede abrir los dos y ver su historial (pruebas 2 y 3) | 12k-r12c-flujos-compartidos.jpg · 12l-r12c-copropietarios-flujo2.jpg |

Al terminar se borró la tarea de prueba, así que el plan queda como está documentado.

## Observaciones del 27/11/2026 (Claude, con la sesión de Teams de Pablo)

Solo lectura: no se creó ni se cambió nada. **No son una prueba de otra persona.**

| Qué | Resultado | Captura |
|---|---|---|
| Plan «Coordinación de la Ejecutiva» (CADUS · Ejecutiva) | Tres cubos (Por hacer, En curso y Hecho) y tres tareas con responsable y fecha, una completada | 08c-planner-ejecutiva.jpg |
| Plan «Seguimiento de las delegaciones» (CADUS · Delegaciones) | Dos tareas por hacer, una en curso y una completada | 08d-planner-delegaciones.jpg |
| Ejecución programada del flujo «Aviso de tareas que vencen» | El mensaje con la tabla de tareas pendientes aparece en General de CADUS · Asamblea a las 8:00 del 26/11 y a las 8:00 del 27/11/2026, a la hora programada | 12n-power-automate-ejecucion-programada-26-11.jpg · 12m-power-automate-ejecucion-programada-27-11.jpg |

## Prueba de PowerApps por otra persona (R-13 · RF-R12)

Hecha el 25/11/2026 por Marcos, con su cuenta de la US, después de que Álvaro le compartiera la aplicación «Estado de las delegaciones» ([`powerapps-especificacion.md`](powerapps-especificacion.md)).

| # | Prueba | Resultado | Captura |
|---|---|---|---|
| 1 | La aplicación aparece en la cuenta de Marcos | OK: en make.powerapps.com, Aplicaciones, «Compartidos conmigo», sale «Estado de las delegaciones», propietario Álvaro, tipo Lienzo | R13-04-app-compartida-con-marcos.jpg |
| 2 | Abrir la aplicación en modo de reproducción (apps.powerapps.com) con otra cuenta | OK: se abre fuera de Power Apps Studio. La primera vez pide permiso para la conexión de SharePoint con la cuenta de Marcos (leer y escribir registros); Marcos lo concedió (en la captura se ha tapado su correo) | R13-05-permiso-sharepoint-marcos.jpg |
| 3 | La aplicación lee la lista «Delegaciones CADUS» | OK: muestra las tres delegaciones de ejemplo (ETSII · Al día, Derecho · Pendiente de reunión, Biología · Sin contacto), y al elegir una sale su ficha con Título, Centro y Estado | R13-06-app-ejecutada-marcos.jpg · R13-07-detalle-derecho-marcos.jpg |

No se probó crear, editar ni borrar delegaciones, para no cambiar los datos de ejemplo. Tampoco se probó desde la pestaña de Teams.

## Prueba del plan de la asamblea rehecho por otra persona (RSI-HU-09)

Hecha el 26/11/2026 por Marcos, con su cuenta de la US, en Planner web sobre el plan «Preparación de la Asamblea» ya rehecho por Joaquín. Pruebas del apartado «Prueba de otra persona» de [`configuracion-planner.md`](configuracion-planner.md).

| # | Prueba | Resultado | Captura |
|---|---|---|---|
| 1 | Abrir el plan con su cuenta y mirar el Panel | OK: cuatro cubos en orden, 1 · Convocatoria (2 tareas), 2 · Preparación (2), 3 · Día de la asamblea (1) y 4 · Después (acta) (1). Las seis tareas tienen responsable y fecha: crear el evento (Joaquín, 21/11), enviar la convocatoria (Pablo, 24/11), plantilla del acta (Álvaro, 25/11), reservar la sala (Marcos, 25/11), pasar lista (Pablo, 26/11) y subir el acta (Álvaro, 28/11) | R09-01a-panel-cubos-1-a-3.jpg · R09-01b-panel-cubo-4.jpg · R09-01c-cuadricula-seis-tareas.jpg |
| 2 | Pasar una de sus tareas a «En curso» y luego a «Completada» | OK: «Reservar la sala (ejemplo)», de Marcos, ya estaba «En curso»; al pasarla a «Completado» la tarjeta sale tachada y se queda en 2 · Preparación, en «Tareas completadas». En Gráficos, las tareas restantes pasan de 6 a 5 y aparece «Completado». Al terminar se devolvió a «En curso», como estaba | R09-02a-graficos-antes.jpg · R09-02b-tarea-completada.jpg · R09-02c-se-queda-en-su-cubo.jpg · R09-02d-graficos-despues.jpg |
| 3 | Abrir la vista de programación (en Planner web se llama «Calendario») | OK: cada tarea sale en su fecha; las de 1 y 2 entre el 21 y el 25/11, la de 3 el 26/11 y la de 4 el 28/11, después de la asamblea | R09-03-calendario.jpg |

Detalle menor para Joaquín: la tarea de la etapa 3 se llama «Pasar lista y abrir la sesion(ejemplo)», sin tilde ni espacio antes del paréntesis; la guía la escribe «Pasar lista y abrir la sesión (ejemplo)».
