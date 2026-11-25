# Hoja de carga para REMUS — Red Social Interna del CADUS

> Archivo **generado** por [scripts/remus/build_rem.ps1](../../../scripts/remus/README.md) a partir de scripts/remus/rsi_data.json. No editar a mano: modificar el JSON y regenerar.

Contenido del proyecto [RSI.rem](RSI.rem) (REMUS), versión 1.0, 2026-11-16. Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.

## 1. Organizaciones

| Nombre | Dirección |
|---|---|
| CADUS - Consejo de Alumnos de la Universidad de Sevilla | Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla |
| Equipo de proyecto GSI | Universidad de Sevilla - Gestión de Sistemas de Información (GSI) |

## 2. Personas

| Nombre | Rol |
|---|---|
| Delegación General del CADUS | Cliente y usuario (Ejecutiva del CADUS) |
| Pablo Ruiz Vidal | Product Owner, Business Case y REM |
| Joaquin Luna Canela | Scrum Master y Planner |
| Alvaro Martinez Ocaña | Dev UML de análisis y de diseño |
| Marcos-Paban Delgado Rodriguez | Dev configuración de Teams y capturas |

## 3. Objetivos del sistema

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| OBJ-R01 | Espacio propio por grupo | que la Ejecutiva y cada delegación tengan un lugar propio y privado donde hablar y compartir archivos | Vital |
| OBJ-R02 | Tareas a la vista | que las tareas de preparación de las asambleas y de los cursos estén a la vista y asignadas a quien corresponde | Vital |
| OBJ-R03 | Avisos y calendario unificados | que los avisos y el calendario del CADUS estén en un solo sitio | Vital |
| OBJ-R04 | Documentos sin duplicar | que los documentos internos sigan en el gestor documental (DMS) y se enlacen desde la red social, sin copias | Vital |
| OBJ-R05 | Lo interno, solo para quien corresponde | que lo interno no se mezcle con lo que ve cualquier estudiante: los grupos son privados y solo entran las cuentas autorizadas | Vital |

## 4. Requisitos de información

| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |
|---|---|---|---|
| IR-R01 | Grupo | a cada grupo o subgrupo del equipo, con estos datos: | Nombre; Tipo (Ejecutiva, Delegaciones, subgrupo de centro o Asamblea); Descripción; Propietarios; Miembros |
| IR-R02 | Canal | a cada canal de un grupo, con estos datos: | Nombre; Grupo al que pertenece; Tipo (estándar o privado); Quién puede publicar; Herramientas ancladas |
| IR-R03 | Herramienta | a cada herramienta del equipo, con estos datos: | Nombre (Archivos, Calendario, Planner, Forms, Power Automate o PowerApps); Para qué se usa; Grupo o canal donde está; Quién la gestiona |
| IR-R04 | Rol y permiso | a cada rol del equipo, con estos datos: | Rol (propietario, miembro o invitado); Acciones permitidas (leer, publicar, gestionar canales, administrar miembros); Grupo o canal sobre el que se aplica |
| IR-R05 | Plan y tarea | a cada plan de tareas y a sus tareas, con estos datos: | Plan y grupo al que pertenece; Cubo; Tarea; Responsable; Fecha límite; Estado |

## 5. Actores

| Código | Nombre | Representa… |
|---|---|---|
| ACT-R01 | Ejecutiva del CADUS | a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios del equipo (administran miembros y canales, publican avisos y reparten tareas) |
| ACT-R02 | Delegación de centro | a cada una de las 27 delegaciones, que acceden con la cuenta de su delegación (una cuenta por delegación, no por persona) y son miembros: leen los avisos, participan en su canal y gestionan sus tareas |
| ACT-R03 | Administrador del equipo | a la persona del equipo del proyecto que crea el equipo en Teams y lo configura (Pablo Ruiz Vidal); al terminar el proyecto lo traspasa a la Ejecutiva |

## 6. Requisitos de interfaz de usuario

| Código | Nombre | El sistema deberá | Historias |
|---|---|---|---|
| UI-R01 | Grupos y canales con nombres claros | ordenar el equipo por grupos y canales con nombres que se entiendan sin explicación (por ejemplo, «Delegaciones · ETSII»), para que una persona sin experiencia en Teams encuentre su canal | RNF-R02 |
| UI-R02 | Herramientas ancladas en cada canal | anclar en cada canal, como pestañas, las herramientas que se usan allí (archivos, tareas y calendario) | RNF-R02 |

## 7. Requisitos funcionales

| Código | Nombre | El sistema deberá | Historias | Importancia |
|---|---|---|---|---|
| RF-R01 | Equipos del CADUS | crear tres equipos privados, que son los grupos principales: «CADUS · Ejecutiva», «CADUS · Delegaciones» y «CADUS · Asamblea». Se usan tres equipos, y no uno con todos los canales, porque cada grupo tiene miembros, permisos y herramientas distintos y así los canales privados de las 27 delegaciones quedan en un solo equipo, sin mezclarlos con la Ejecutiva ni con la asamblea | Entrega del 22/11 | Vital |
| RF-R02 | Grupo Ejecutiva | ofrecer a la Ejecutiva el equipo «CADUS · Ejecutiva», en el que solo están sus miembros, para coordinarse y preparar lo que luego se publica | Entrega del 22/11 | Vital |
| RF-R03 | Grupo Delegaciones | ofrecer a cada delegación de centro (27) un subgrupo, que es un canal privado del equipo «CADUS · Delegaciones», visible solo para la Ejecutiva y para esa delegación | Entrega del 22/11 | Vital |
| RF-R04 | Grupo Asamblea | ofrecer el equipo «CADUS · Asamblea» para preparar y hacer el seguimiento de las asambleas y de los cursos, con la Ejecutiva como propietaria y las delegaciones como miembros | Entrega del 22/11 | Vital |
| RF-R05 | Canal de avisos | ofrecer un canal de avisos (el canal General del equipo «CADUS · Delegaciones») donde solo publica la Ejecutiva y todas las delegaciones leen | Entrega del 22/11 | Vital |
| RF-R06 | Roles y permisos | aplicar tres roles: propietario (Ejecutiva y administrador del equipo), miembro (delegaciones) e invitado (acceso limitado, sin canales con datos personales). En el piloto, los cuatro integrantes del equipo del proyecto son propietarios de los tres equipos | Entrega del 22/11 | Vital |
| RF-R07 | Archivos enlazados al DMS | ofrecer en los canales una pestaña de archivos que apunte a los sitios de SharePoint del DMS, de modo que los documentos oficiales no se copien a Teams | Entrega del 22/11 | Vital |
| RF-R08 | Calendario compartido | mostrar a todo el equipo un calendario con las asambleas y los cursos, que mantiene la Ejecutiva | Entrega del 22/11 | Vital |
| RF-R09 | Planes de tareas | ofrecer en cada grupo un plan de Planner con cubos y tareas asignadas a una persona o delegación y con fecha límite | Entrega del 22/11 | Vital |
| RF-R10 | Formularios | ofrecer Forms para recoger confirmaciones de asistencia y pequeñas encuestas a las delegaciones | Entrega del 22/11 | Vital |
| RF-R11 | Flujos automáticos | avisar en el canal correspondiente cuando se asigna una tarea o vence su fecha, con flujos de Power Automate | Entrega del 29/11 (Lab 8) | Importante |
| RF-R12 | Aplicación de PowerApps | ofrecer, si el tenant de la Universidad lo permite, una aplicación sencilla de PowerApps sobre los datos del equipo (por ejemplo, la lista de delegaciones y su estado) | Entrega del 29/11 (Lab 8); depende de que el tenant la ofrezca | Importante |

## 8. Casos de uso

### CU-R01 - Publicar un aviso del CADUS

- **Evento disparador:** cuando la Ejecutiva tiene algo que comunicar a todas las delegaciones
- **Precondición:** La Ejecutiva ha iniciado sesión en Teams con la cuenta del CADUS
- **Postcondición:** El aviso está publicado y todas las delegaciones pueden leerlo
- **Pasos:**
  1. Ejecutiva del CADUS abre el canal de avisos del equipo
  2. Ejecutiva del CADUS redacta y publica el aviso, con un archivo adjunto si hace falta
  3. El sistema muestra el aviso en el canal y lo notifica a los miembros
  4. El sistema impide que una delegación publique nuevos avisos en ese canal

### CU-R02 - Preparar una asamblea con tareas

- **Evento disparador:** cuando se convoca una asamblea o un curso
- **Precondición:** El grupo Asamblea existe y las delegaciones son miembros
- **Postcondición:** La asamblea está en el calendario y sus tareas están asignadas con fecha
- **Pasos:**
  1. Ejecutiva del CADUS crea el evento de la asamblea en el calendario compartido
  2. Ejecutiva del CADUS crea en el plan del grupo Asamblea las tareas de preparación y las asigna a personas o delegaciones
  3. El sistema muestra el evento a todo el equipo y las tareas a sus responsables
  4. Ejecutiva del CADUS envía a las delegaciones un formulario de confirmación de asistencia
  5. Delegación de centro responde al formulario de asistencia
  6. Delegación de centro actualiza el estado de sus tareas
  7. El sistema refleja el avance del plan para la Ejecutiva

### CU-R03 - Compartir un documento con una delegación

- **Evento disparador:** cuando la Ejecutiva necesita que una delegación vea o complete un documento
- **Precondición:** El documento está en el DMS y la delegación tiene su canal
- **Postcondición:** La delegación puede abrir el documento desde su canal
- **Pasos:**
  1. Ejecutiva del CADUS abre el canal privado de la delegación
  2. Ejecutiva del CADUS enlaza en la pestaña de archivos el documento del sitio de SharePoint del DMS
  3. El sistema muestra el enlace solo a la Ejecutiva y a esa delegación
  4. Delegación de centro abre el documento desde su canal

### CU-R04 - Consultar avisos, calendario y tareas

- **Evento disparador:** al empezar a trabajar o antes de una asamblea
- **Precondición:** La delegación ha iniciado sesión en Teams con la cuenta de su delegación
- **Postcondición:** La delegación sabe qué se ha avisado, cuándo es la próxima asamblea y qué tiene pendiente
- **Pasos:**
  1. Delegación de centro abre el equipo y lee los avisos nuevos
  2. El sistema muestra los avisos, sin canales de otras delegaciones
  3. Delegación de centro consulta el calendario y sus tareas del plan
  4. El sistema muestra los próximos eventos y las tareas asignadas a esa delegación

### CU-R05 - Dar de alta o de baja una delegación

- **Evento disparador:** cuando una delegación se crea o desaparece
- **Precondición:** El equipo existe y el administrador tiene permisos de propietario
- **Postcondición:** La delegación tiene su canal privado y sus permisos, o su canal queda archivado
- **Pasos:**
  1. Administrador del equipo crea un canal privado para la delegación dentro del grupo Delegaciones
  2. Administrador del equipo añade a ese canal a la cuenta de la delegación y a la Ejecutiva
  3. El sistema aplica el rol de miembro a la delegación y de propietaria a la Ejecutiva
  4. Administrador del equipo al dar de baja una delegación, archiva su canal sin borrar lo publicado

## 9. Requisitos no funcionales

| Código | Nombre | El sistema deberá | Importancia |
|---|---|---|---|
| RNF-R01 | Privacidad | cumplir el RGPD y la LOPDGDD: grupos y canales privados, sin canales abiertos, y sin trasladar a Teams los datos de reclamaciones, mediaciones ni votaciones, que siguen en el DMS con sus permisos | Vital |
| RNF-R02 | Facilidad de uso | una persona sin experiencia en Teams debe poder encontrar su canal, leer los avisos y completar una tarea con una guía corta | Vital |
| RNF-R03 | Mantenibilidad | la estructura del equipo (grupos, canales, roles y permisos) queda documentada para que otra persona pueda mantenerla y traspasarla a la Ejecutiva | Vital |
| RNF-R04 | Disponibilidad | estar disponible desde cualquier navegador o aplicación de Teams con la cuenta de la Universidad, también desde el móvil | Vital |

## 10. Reglas de negocio

| Código | Nombre | Regla |
|---|---|---|
| RN-R01 | Solo la Ejecutiva publica avisos | En el canal de avisos solo publica la Ejecutiva; las delegaciones leen y pueden reaccionar (coherente con RN-01 del portal: todo pasa por la Ejecutiva). |
| RN-R02 | Cada delegación ve solo lo suyo | Una delegación solo ve su propio canal, los avisos y los grupos comunes; no ve los canales de otras delegaciones. |
| RN-R03 | Los documentos oficiales viven en el DMS | Las actas, la normativa, los expedientes y las votaciones se guardan en el DMS; la red social solo los enlaza y no guarda copias. |
| RN-R04 | Una cuenta por delegación | Cada delegación usa una sola cuenta, a nombre de la delegación y no de la persona, que pasa al equipo siguiente cuando cambia el delegado (igual que en el portal, RN-04). |
| RN-R05 | Sin acceso para estudiantes | Los estudiantes no son miembros ni invitados: la red social es solo para la Ejecutiva y las delegaciones. |

## 11. Entorno de trabajo del equipo (restricciones)

| Código | Nombre | Descripción |
|---|---|---|
| RC-R01 | Microsoft Teams de la Universidad de Sevilla | La red social se construye en Microsoft Teams del tenant de la Universidad de Sevilla, con equipos, canales, roles y las herramientas de Microsoft 365 que el tenant ofrezca (archivos, calendario, Planner, Forms y, si están disponibles, Power Automate y PowerApps). |
| RC-R02 | Límites del tenant | Los alumnos no administran el tenant: lo que no permita la configuración de la Universidad (por ejemplo, crear equipos o usar Power Automate y PowerApps) se documenta y no se puede cambiar. |
| RC-R03 | Documentación independiente | La red social tiene su propio REM, análisis, diseño, implementación y seguimiento SCRUM, independientes de los del CMS y del DMS. |

## 12. Trazabilidad entre requisitos

| Origen | Destinos |
|---|---|
| OBJ-R01 | RF-R01, RF-R02, RF-R03, RF-R04, RF-R06, IR-R01, IR-R02, UI-R01, RN-R02, RN-R04 |
| OBJ-R02 | RF-R08, RF-R09, RF-R10, RF-R11, RF-R12, IR-R03, IR-R05, CU-R02 |
| OBJ-R03 | RF-R05, RF-R08, UI-R02, RN-R01, CU-R01, CU-R04 |
| OBJ-R04 | RF-R07, RN-R03, CU-R03 |
| OBJ-R05 | RF-R06, IR-R04, RNF-R01, RN-R02, RN-R05 |
| CU-R01 | RF-R02, RF-R05, RF-R06, RN-R01, IR-R02, ACT-R01 |
| CU-R02 | RF-R04, RF-R08, RF-R09, RF-R10, IR-R05, ACT-R01, ACT-R02 |
| CU-R03 | RF-R03, RF-R07, RN-R02, RN-R03, IR-R02, ACT-R01, ACT-R02 |
| CU-R04 | RF-R05, RF-R08, RF-R09, RN-R02, ACT-R02 |
| CU-R05 | RF-R01, RF-R03, RF-R06, RN-R04, IR-R01, IR-R04, ACT-R03 |
| RF-R01 | IR-R01, IR-R02, RC-R01, RC-R02 |
| RF-R06 | IR-R04, RN-R05 |
| RF-R11 | RC-R02, IR-R03 |
| RF-R12 | RC-R02, IR-R03 |
| RNF-R03 | RF-R01, RF-R06 |
| RNF-R02 | UI-R01, UI-R02 |
| RNF-R04 | RC-R01 |
| RC-R03 | RC-R01 |
