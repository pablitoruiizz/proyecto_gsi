# Caso de negocio · Red Social Interna para el CADUS (MS Teams)

Versión del 22/11/2026 · Autor: Pablo Ruiz Vidal (con Claude) · Revisión: pendiente de otra persona del equipo

> **Estructura:** sigue el índice del caso de negocio que muestra el Lab 5 (diapositiva 11, ejemplo de CEMEX): resumen ejecutivo con misión y visión, situación actual con DAFO, descripción del proyecto, drivers, objetivos de negocio, riesgos y participantes (personas y organizaciones). Los requisitos del sistema software (información, funcionales y reglas de negocio) y el glosario van en los apartados 2 y 3 del documento.
> **Qué es:** un caso de negocio construido para la práctica, que justifica por qué se elige Teams. Lo que sale de la entrevista del 26/10/2026 y de los documentos del proyecto va sin marcar; lo que es una **suposición** va marcado «(por confirmar)». No se inventan datos del CADUS.

## 1.1 Introducción – resumen ejecutivo

El CADUS (Consejo de Alumnos de la Universidad de Sevilla) ya tiene un portal web para el público y un gestor documental (DMS en SharePoint) para sus documentos internos, pero la coordinación diaria entre la Ejecutiva, las 27 delegaciones de centro y las asambleas no tiene un espacio propio y documentado (por confirmar con el CADUS). Se propone una **red social interna en Microsoft Teams**, dentro de la cuenta de la Universidad, con tres equipos privados (Ejecutiva, Delegaciones y Asamblea), canales, roles y permisos, y las herramientas de archivos, calendario, tareas y formularios. Se elige Teams frente a Discord y a la mensajería personal porque no tiene coste de licencias, usa las cuentas institucionales, se integra con SharePoint y controla quién ve qué. Un piloto con datos de ejemplo demuestra la estructura; poner en marcha las 27 delegaciones queda fuera del alcance.

### 1.1.1 Misión y visión del sistema

- **Misión:** ofrecer a la Ejecutiva y a las delegaciones del CADUS un espacio privado y ordenado para comunicarse, repartir tareas, compartir archivos y preparar las asambleas, dentro de la cuenta de la Universidad.
- **Visión:** que la coordinación interna del CADUS viva en un único espacio que dure de un curso al siguiente, con permisos claros y sin duplicar los documentos que ya custodia el DMS.

## 1.2 Descripción de la situación actual

- La **Ejecutiva** usa una cuenta única del CADUS (`dcadus@us.es`) que comparten todos sus miembros, y todo lo que se publica pasa por ella (entrevista del 26/10/2026).
- Hay **27 delegaciones de centro**; cada una usa una cuenta a nombre de la delegación (no de la persona), que pasa al equipo siguiente cuando cambia el delegado (decisión del portal, HU-22).
- Se celebran **asambleas** presenciales, con una votación por delegación, y se organizan cursos.
- El CADUS tiene un **portal web** y un **DMS** (actas, normativa, expedientes y votaciones), pero ninguno de los dos es un espacio de conversación ni de reparto de tareas.
- **No consta** qué herramientas usa hoy el CADUS para coordinarse (por confirmar); se supone correo y mensajería personal, sin espacio común.
- El equipo del proyecto coordina su trabajo en Discord y GitHub, y desde el 16/11/2026 ya no cuenta con un contacto en el CADUS.

### 1.2.1 Análisis DAFO

| | Elementos |
|---|---|
| Debilidades | Una sola cuenta para toda la Ejecutiva, sin trazabilidad personal · cambio de delegados cada curso · no consta un espacio común de coordinación (por confirmar) · sin contacto con el CADUS en el equipo desde el 16/11 |
| Amenazas | Que el CADUS no lo adopte · datos personales de estudiantes y delegados (RGPD) · límites del tenant de la Universidad (crear equipos, Power Automate, PowerApps) · que las cuentas de delegación no tengan Teams habilitado (por confirmar) · seguir con mensajería personal y que la información se disperse |
| Fortalezas | Cuentas institucionales ya existentes para la Ejecutiva y las delegaciones · portal y DMS ya construidos y enlazables · estructura de grupos clara (Ejecutiva, 27 delegaciones, asamblea) · sin coste de licencias |
| Oportunidades | Integración con SharePoint (DMS) · Planner, calendario y Forms en el mismo espacio · automatización con Power Automate y PowerApps · reutilizar la cuenta por delegación que ya se traspasa de un curso al siguiente |

## 1.3 Descripción del proyecto

**Solución:** tres equipos privados de Teams, que son los grupos principales: «CADUS · Ejecutiva» (coordinación y preparación de avisos), «CADUS · Delegaciones» (canal de avisos donde solo publica la Ejecutiva y un canal privado por delegación como subgrupo) y «CADUS · Asamblea» (convocatorias, cursos, calendario y tareas). Cada equipo tiene propietarios y miembros, y sus canales llevan pestañas con las herramientas: archivos enlazados al DMS, calendario, Planner y Forms. Después, flujos de Power Automate y una aplicación de PowerApps si el tenant lo permite (Lab 8). Se usan tres equipos y no uno porque cada grupo tiene miembros, permisos y herramientas distintos, y así los canales privados de las 27 delegaciones quedan en un solo equipo, sin mezclarlos con la Ejecutiva ni con la asamblea.

**Alcance del piloto:** los tres equipos, con tres delegaciones de ejemplo (Biología, Derecho y ETSII), el canal de avisos moderado, un calendario con una asamblea de ejemplo, un plan de Planner por equipo y un formulario de confirmación de asistencia, todo con datos de ejemplo. **Fuera:** cambiar el portal o el DMS, migrar conversaciones o archivos existentes, formar a los usuarios finales y poner en marcha las 27 delegaciones.

**Alternativas consideradas:**

| Criterio | MS Teams (tenant de la US) | Discord (lo usa el equipo del proyecto) | Correo y mensajería personal |
|---|---|---|---|
| Coste | Incluido en la cuenta de la Universidad | Gratuito | Gratuito |
| Cuentas | Las institucionales ya existentes | Cuentas personales de cada uno | Cuentas personales |
| Archivos y gestor documental | Se integra con SharePoint (ya usado en el DMS) | No se integra con SharePoint | No se integra |
| Control de miembros y permisos | Por equipo y canal, con roles de propietario, miembro e invitado | Por servidor y canal | No hay |
| Tareas y calendario | Planner y calendario del equipo | Eventos programados nativos; las tareas necesitan bots de terceros | No hay |
| Automatización | Power Automate y PowerApps | Con bots de terceros | No hay |
| Riesgo principal | Que lo adopten; los límites los fija la Universidad | Cuentas y datos fuera de la Universidad | Dispersión y pérdida de información |

**Costes:** sin licencias nuevas (la Universidad ya las ofrece); el esfuerzo del equipo del proyecto (cuatro personas) y el tiempo de la Ejecutiva para probarlo.

## 1.4 Principales drivers

### 1.4.1 Drivers

| Driver | Por qué importa |
|---|---|
| Cuentas institucionales y permisos | Lo interno no debe verlo cualquier estudiante; RGPD y entrevista del 26/10 («todas las consultas con total privacidad») |
| Integración con SharePoint | Los documentos oficiales ya están en el DMS y no deben duplicarse |
| Coste cero | El CADUS no tiene presupuesto de herramientas (por confirmar) |
| Continuidad entre cursos | Las delegaciones cambian de equipo cada año y la cuenta de la delegación se traspasa |
| Facilidad de uso | La Ejecutiva y las delegaciones no son personal informático; el portal ya se diseñó para que lo use cualquiera |
| Plazos de la asignatura | Estructura de Teams y Planner el 22/11, Power Automate y PowerApps el 29/11, entrega final el 07/12/2026 |

## 1.5 Objetivos de negocio

| ID | Objetivo | Cómo se comprobará |
|---|---|---|
| OBJ-R01 | Que la Ejecutiva y cada delegación tengan un lugar propio y privado donde hablar y compartir archivos | Existe un equipo o canal por cada una, con los permisos previstos |
| OBJ-R02 | Que las tareas de preparación de las asambleas y de los cursos estén a la vista y asignadas | Cada equipo tiene su plan de tareas con responsables |
| OBJ-R03 | Que los avisos y el calendario del CADUS estén en un solo sitio | Un canal de avisos y un calendario compartidos |
| OBJ-R04 | Que los documentos internos sigan en el DMS y se enlacen desde la red social, sin duplicarlos | Los archivos del equipo apuntan a los sitios de SharePoint del DMS |
| OBJ-R05 | Que lo interno no se mezcle con lo que ve cualquier estudiante | Los equipos son privados y solo entran las cuentas autorizadas |

**Criterios de éxito del piloto:** los equipos existen con los grupos y permisos del diseño; cada equipo tiene su canal, su plan de tareas y su calendario; una persona ajena al diseño comprueba que ve solo lo suyo; todo está documentado con capturas.

## 1.6 Principales riesgos

| Riesgo | Medida |
|---|---|
| La Ejecutiva comparte una sola cuenta, mientras que Teams se apoya en personas con roles distintos | Se diseña para cuentas de grupo (Ejecutiva y una por delegación), como en el portal y el DMS; los roles personales quedan previstos para cuando haya cuentas individuales |
| Datos personales de estudiantes y delegados | Equipos y canales privados, sin canales abiertos; no se pegan datos de reclamaciones; lo sensible sigue en el DMS con sus permisos |
| El CADUS no lo adopta | Piloto pequeño y probado, con guía corta de uso |
| No se pueden crear equipos o usar Power Automate y PowerApps en el tenant | Se comprueba y, si no se puede, se documenta y se propone una alternativa dentro de Teams; los equipos y Planner ya funcionan en el piloto |
| Las cuentas de delegación pueden no tener Teams habilitado ni licencia (por confirmar) | Comprobarlo con la Universidad antes de poner en marcha las 27 delegaciones |
| En el piloto los cuatro integrantes son propietarios de los tres equipos, así que no hay una cuenta «solo miembro» fija con la que probar el aislamiento | El 22/11 se bajó temporalmente a Álvaro a miembro para probarlo y se volvió a subir; con las delegaciones reales habrá cuentas solo miembro |
| No hay contacto con el CADUS en el equipo desde el 16/11/2026 | Las decisiones que dependen del CADUS se marcan «por confirmar» |

## 1.7 Participantes del proyecto

### 1.7.1 Personas

| Persona o grupo | Papel |
|---|---|
| Ejecutiva del CADUS | Cliente y propietaria de los tres equipos; publica avisos y reparte tareas |
| Delegaciones de centro (27) | Miembros: leen los avisos, participan en su canal y gestionan sus tareas |
| Pablo Ruiz Vidal | Product Owner; caso de negocio, REM y creación de los equipos |
| Joaquín Luna Canela | Scrum Master; Planner, Forms y pestaña del DMS |
| Álvaro Martínez Ocaña | Revisión del UML de análisis y de diseño; especificación de PowerApps |
| Marcos-Paban Delgado Rodríguez | Configuración de canales, moderación, calendario y capturas |
| Estudiantes | No participan: no tienen acceso a la red social |

### 1.7.2 Organizaciones

| Organización | Relación |
|---|---|
| CADUS · Consejo de Alumnos de la Universidad de Sevilla | Cliente; usuario final |
| Equipo de proyecto GSI | Diseña, configura y prueba el piloto |
| Universidad de Sevilla | Proporciona el tenant de Microsoft 365 (Teams, SharePoint, Planner, Forms) y fija sus límites |

## Suposiciones y preguntas abiertas (por confirmar)

1. Qué herramientas usa hoy el CADUS para coordinarse y cuáles quieren sustituir.
2. Si las cuentas de delegación tienen Teams habilitado y licencia.
3. Si las delegaciones usarían la cuenta de su delegación en Teams.
4. Quién crea y administra los equipos cuando el proyecto termine (por ahora, Pablo).
5. Si el tenant de la US permite usar Power Automate y PowerApps (Álvaro comprobó que sus páginas de creación cargan; no que se pueda guardar y ejecutar).
