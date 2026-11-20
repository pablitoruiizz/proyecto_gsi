# Business Case · Red Social Interna del CADUS (MS Teams)

BORRADOR del 16/11/2026 · Autor: Pablo Ruiz Vidal (con Claude) · Revisión: pendiente de otra persona del equipo

> **Estructura:** en clase solo se dio el esquema general (SCRUM review, REM con «Business Case» y «Requisitos de herramienta», UML de análisis y de diseño, implementación). No se dio la estructura del Business Case, así que se usa una estándar de siete apartados. Si el profesor indica otra, se reordena sin perder contenido.
> **Lo que sale de los documentos del proyecto** va sin marcar. Lo que es una **suposición a confirmar** va marcado con «(por confirmar)». No se inventan datos del CADUS: donde no se sabe, se dice.

## 1. Contexto de la organización

El CADUS es el Consejo de Alumnos de la Universidad de Sevilla. Según la entrevista del 26/10/2026 y los documentos del proyecto:

- La **Ejecutiva** lleva el día a día y comparte una única cuenta institucional (`dcadus@us.es`). Todo lo que se publica pasa por ella.
- Hay **27 delegaciones de centro**, cada una con una cuenta propia a nombre de la delegación (no de la persona), que se traspasa al equipo siguiente cuando cambia el delegado.
- Se celebran **asambleas** presenciales, con una votación por delegación, y se organizan **cursos**.
- El CADUS ya tiene un **portal web** (el CMS) para el público y un **gestor documental** (el DMS, en SharePoint) para sus documentos internos: actas, normativa, expedientes y votaciones.

## 2. Problema u oportunidad

El portal y el gestor documental resuelven la publicación y el archivo, pero no la **coordinación diaria entre personas**: quién prepara qué, qué hay que hacer antes de la próxima asamblea, dónde se habla con cada delegación, cómo se comparten borradores y avisos. En los documentos del proyecto no consta qué herramientas usa hoy el CADUS para eso (por confirmar con el CADUS), de modo que el caso se plantea como una **oportunidad**: reunir la comunicación, las tareas y los archivos del CADUS en un único espacio, dentro de la cuenta de la Universidad que ya usan.

## 3. Objetivos de negocio

| ID | Objetivo | Cómo se comprobará |
|---|---|---|
| OBJ-RSI-01 | Que la Ejecutiva y cada delegación tengan un lugar propio y privado donde hablar y compartir archivos | Existe un grupo por cada una, con los permisos previstos |
| OBJ-RSI-02 | Que las tareas de preparación de las asambleas y de los cursos estén a la vista y asignadas | Cada grupo tiene su plan de tareas con responsables |
| OBJ-RSI-03 | Que los avisos y el calendario del CADUS estén en un solo sitio | Un canal de avisos y un calendario compartidos |
| OBJ-RSI-04 | Que los documentos internos sigan en el gestor documental y se enlacen desde la red social, sin duplicarlos | Los archivos del grupo apuntan a los sitios de SharePoint del DMS |
| OBJ-RSI-05 | Que lo interno no se mezcle con lo que ve cualquier estudiante | Los grupos son privados y solo entran las cuentas autorizadas |

## 4. Alcance

**Dentro (piloto):** tres equipos del CADUS, que son los grupos principales (Ejecutiva, Delegaciones, con un canal privado por centro, y Asamblea), con canales, roles y permisos, y las herramientas de archivos, calendario, tareas y formularios. Después, automatizaciones con Power Automate y una aplicación con PowerApps si el tenant las ofrece (Lab 8).

**Fuera:** cambiar el portal o el DMS; migrar las conversaciones o los archivos que el CADUS ya tenga; formación de los usuarios finales; pasar a producción para las 27 delegaciones (se prueba con datos de ejemplo y con el equipo del proyecto).

## 5. Partes interesadas

| Parte | Interés |
|---|---|
| Ejecutiva del CADUS (propietaria) | Coordinar al CADUS, publicar avisos y aprobar |
| Delegaciones de centro | Recibir avisos, preparar asambleas, compartir con la Ejecutiva |
| Estudiantes | No participan: no tienen acceso a la red social |
| Equipo del proyecto (4 personas) | Diseñar, configurar y probar el piloto |
| Profesorado de GSI | Evalúa la entrega |

## 6. Alternativas consideradas

| Criterio | MS Teams (tenant de la US) | Discord (lo usa el equipo del proyecto) | Correo y mensajería personal |
|---|---|---|---|
| Coste | Incluido en la cuenta de la Universidad | Gratuito | Gratuito |
| Cuentas | Las institucionales ya existentes | Cuentas personales de cada uno | Cuentas personales |
| Archivos y gestor documental | Se integra con SharePoint (ya usado en el DMS) | No se integra | No se integra |
| Control de miembros y permisos | Por equipo y canal, con roles de propietario, miembro e invitado | Por servidor y canal | No hay |
| Tareas y calendario | Planner y calendario del equipo | Con bots de terceros | No hay |
| Automatización | Power Automate y PowerApps | Con bots de terceros | No hay |
| Riesgo principal | Hay que conseguir que lo adopten; los límites de creación los fija la US | Cuentas fuera de la Universidad y datos fuera de ella | Dispersión y pérdida de información |

## 7. Solución propuesta, beneficios, costes y riesgos

**Solución:** una red social interna en **MS Teams** con tres equipos («CADUS · Ejecutiva», «CADUS · Delegaciones» y «CADUS · Asamblea»), subgrupos como canales privados y herramientas, como en la sesión del Lab 5: equipos con propietarios, miembros e invitados; canales por tema; herramientas integradas (archivos, calendario, Planner, Forms) y, después, automatizaciones. Se eligen tres equipos y no uno solo porque Teams limita los canales privados por equipo y las 27 delegaciones más la Ejecutiva casi lo agotarían. El diseño detallado va en el análisis y el diseño de clases.

**Beneficios esperados:** un único sitio para hablar, repartir tareas y compartir archivos; menos dispersión entre canales; continuidad cuando cambia un equipo de delegación, porque las cuentas son de la delegación; permisos claros.

**Costes:** sin licencias nuevas (la Universidad ya las ofrece); el esfuerzo del equipo del proyecto (4 personas) y el tiempo de la Ejecutiva para probarlo y adoptarlo.

**Riesgos:**

| Riesgo | Medida |
|---|---|
| La Ejecutiva comparte una sola cuenta, mientras que Teams se apoya en personas con roles distintos | Se diseña para cuentas de grupo (Ejecutiva y cada delegación), como en el portal y el DMS; los roles personales quedan previstos para cuando haya cuentas individuales |
| Datos personales de estudiantes y delegados | Grupos privados, sin canales abiertos; no se pegan datos de reclamaciones; lo sensible sigue en el DMS con sus permisos |
| El CADUS no lo adopta | Piloto pequeño y probado, con guía corta de uso |
| No se puede crear equipos o usar Power Automate y PowerApps en el tenant | Se comprueba antes del Lab 8 y, si no se puede, se documenta y se propone una alternativa dentro de Teams |
| Ya no hay contacto con el cliente en el equipo (Miguel Ángel dejó el trabajo el 16/11) | Las decisiones sobre el CADUS se marcan «por confirmar» |

**Criterios de éxito del piloto:** el equipo existe con los grupos y permisos del diseño; cada grupo tiene su canal, su plan de tareas y su calendario; una persona ajena al diseño puede entrar y comprobar que ve solo lo suyo; todo está documentado con capturas.

## 8. Suposiciones y preguntas abiertas (por confirmar)

1. Qué herramientas usa hoy el CADUS para coordinarse y cuáles quieren sustituir.
2. Si las delegaciones usarían la cuenta de su delegación en Teams.
3. Quién crea y administra el equipo cuando el proyecto termine (por ahora, Pablo).
4. Si el tenant de la US permite a los estudiantes crear equipos y usar Power Automate y PowerApps.
