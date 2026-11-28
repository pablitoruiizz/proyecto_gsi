# Guion del podcast de repaso de la defensa (estado a 28/11/2026)

Dos voces: A pregunta y B responde. Las líneas `[pausa]` dejan unos segundos para contestar en voz alta. El audio se genera con `scripts/defensa/generar_podcast.py` a partir de este guion. Los datos salen de `docs/defensa/guia-defensa-proyecto.html` (del 25/11), corregidos con el estado de 27/11/2026.

## Apertura

A: Hola. Este es el repaso de la defensa del proyecto del CADUS. Son unos veinte minutos para repasar todo en voz alta mientras paseas. Primero el resumen, luego las decisiones y los números, y al final una ronda de preguntas para que contestes tú.
B: Y una regla que conviene recordar desde el principio: si te preguntan por algo que no está terminado, se dice tal cual y con el motivo. Eso lo hemos escrito así en todos los documentos, y es lo que da credibilidad.

## El proyecto en un minuto

A: Empecemos por lo básico. Cuéntame el proyecto en un minuto.
B: El cliente es el CADUS, el Consejo de Alumnos de la Universidad de Sevilla. Le hemos construido tres sistemas. Un portal web en Güordpres, que llamamos CMS, para informar a los estudiantes y atenderlos. Un gestor de documentos en Sherpoint, el DMS, para los documentos internos. Y una red social interna en Teams para coordinar a la Ejecutiva y a las veintisiete delegaciones.
A: ¿Y cómo lo hicisteis?
B: Con el mismo método en los tres. Primero escribimos lo que necesita el cliente, en un documento de requisitos que llamamos REM. Luego dibujamos qué hay, con el UML de análisis. Después decidimos con qué se construye cada cosa, con el UML de diseño. Luego implementamos, con capturas explicadas, y probamos. Todo gestionado con SCRUM en Guit-jab.
A: ¿Qué es lo que une esos cinco pasos?
B: El código del requisito. Por ejemplo, la regla de negocio RN cero tres, la privacidad de las consultas. Ese código aparece en el REM, en las etiquetas rojas de los UML, en las capturas y en las pruebas. Eso es la trazabilidad, y es lo que más conviene saber explicar.

## El cliente y los requisitos

A: ¿Cómo conseguisteis los requisitos?
B: Con una entrevista al CADUS el veintiséis de octubre y con la guía de la asignatura. Los escribimos en REMUS, cada uno con su código. Cuando el cliente cambió algo, se actualizó el REM. El del portal está en la versión dos coma tres, y los del DMS y la red social, en la uno coma uno.
A: ¿Y qué cambió tras la entrevista?
B: Tres cosas importantes. Las votaciones son presenciales y solo votan los delegados, así que se canceló la papeleta online, la historia veintiuno, y el portal solo anuncia la votación. Se añadió el relevo de la cuenta de la delegación, la historia veintidós, para que el delegado pueda pasar la cuenta a su sucesor. Y se añadió la conservación a dos años de tickets y mediaciones, la historia veintitrés, con borrado o anonimización. Además, la privacidad se amplió a todas las consultas.
A: Dime las reglas de negocio del portal.
B: Son cinco. RN cero uno: todo contenido pasa por la Ejecutiva antes de publicarse; en la implementación hay una excepción decidida, las modificaciones permitidas de la ficha propia de cada delegación quedan publicadas sin nueva aprobación. RN cero dos: solo se aceptan consultas desde un correo de alumno de la Universidad, arroba alum punto us punto es. RN cero tres: tickets, reclamaciones y mediaciones son privados, solo los ven su remitente y la Ejecutiva. RN cero cuatro: cada ficha de delegación la edita solo su cuenta o la Ejecutiva. Y RN cero cinco: toda votación publicada está vinculada a una asamblea.
A: ¿Y los requisitos no funcionales que se comprueban?
B: Rendimiento, con la página en menos de tres segundos. Móvil y tablet. Accesibilidad, nivel AA de las pautas WCAG dos punto uno. Seguridad de los formularios. Privacidad según el RGPD. Mantenibilidad para el relevo entre cursos. Y facilidad de uso: crear un ticket, consultar el calendario o ver una noticia en menos de un minuto.

## SCRUM

A: ¿Cómo aplicasteis SCRUM?
B: El backlog y los sprints viven en el proyecto de Guit-jab que se llama CADUS Scrum. Hay product backlog con historias, prioridad y puntos en escala de Fibonacci, sprint backlog con subtareas por persona y burndown. Nuestra definición de hecho es que la historia esté en la rama principal, con captura o resultado anotado y probada por otra persona, aunque no siempre la cumplimos: en el portal cerramos puntos por integración aunque faltaran pruebas cruzadas. Cada sprint tiene review y retrospectiva, pero la de la red social está redactada como borrador.
A: ¿Qué sprints hubo?
B: Del portal, tres. El primero, del veintiocho de septiembre al dieciocho de octubre, setenta puntos: el portal base. El segundo, de una semana, veintinueve puntos: calendario, votaciones, mediación y buzón. El tercero, del veintiséis de octubre al quince de noviembre, treinta y seis puntos, cuarenta y cuatro con la historia veinticuatro: móvil, accesibilidad, filtros, seguridad, rendimiento, relevo y conservación. De la red social, dos: el primero con Teams, Plánner, el caso de negocio, el REM y el UML, y el segundo con Páuer Automeit, Páuer Apps y los patrones de Plánner del laboratorio seis.
A: ¿Qué problema tuvisteis?
B: Que cerramos el trabajo al final de cada sprint. En el primero, el ochenta y seis por ciento de los puntos se cerró el último día. En el segundo, el setenta y nueve por ciento se cerró entre el veintitrés y el veinticuatro de octubre, justo antes de la entrega. Acordamos actualizar el burndown cada día y no lo cumplimos. En la red social ya usamos un script que lo actualiza con un comando.
A: ¿Hicisteis retrospectiva?
B: La del sprint tres del portal se celebró en grupo el veintisiete de noviembre, según Pablo, y las acciones acordadas están en el documento del sprint. No conviene extender esa confirmación a los demás sprints. Si te piden detalles, remite a ese documento.
A: ¿Por qué Guit-jab Projects y no Yira o Trello?
B: Porque ya trabajábamos en Guit-jab, y cada historia se enlaza con sus commits y pull requests. Le falta el burndown nativo, y lo generamos desde el backlog.

## UML: análisis y diseño

A: Si te piden la diferencia entre el análisis y el diseño, en una frase.
B: El análisis dice qué hay, y el diseño dice con qué se hace.
A: Explícalo un poco más.
B: El UML de análisis dice qué conceptos existen en el problema y cómo se relacionan, sin hablar de tecnología. El de diseño dice con qué herramienta se construye cada uno: plugins en el portal, elementos de Sherpoint en el DMS y elementos de Teams en la red social.
A: ¿Qué son las etiquetas rojas de los UML?
B: Son los códigos de los requisitos del REM que justifican cada clase o herramienta. Por ejemplo RF guion R cero nueve, o RN cero tres. Sirven para rastrear qué requisito justifica cada cosa.
A: ¿De dónde salen los conceptos en cada sistema?
B: En el portal, del modelo de información, que se deriva de los requisitos de información tres a nueve. En el DMS, del laboratorio cuatro: documento, carpeta, rol, permiso, búsqueda y metadato. Y en la red social, de los laboratorios cinco y seis: los estereotipos Role, Group, Subgroups, Tool y Permission, y después la clase Plan.
A: Dame el ejemplo del DMS.
B: El análisis tiene Carpeta, Permiso, Rol, Documento, con sus cuatro tipos, y Búsqueda. El diseño lo traduce así: Documento es un documento de una biblioteca con columnas de metadatos. Carpeta es un sitio de grupo y una biblioteca. Rol es un grupo de permisos: propietarios, visitantes e integrantes. Permiso es el permiso del grupo sobre el sitio. Y el metadato es una columna.
A: Y el de la red social.
B: Grupo es un equipo privado de Teams: Ejecutiva, Delegaciones y Asamblea. Subgrupo es un canal privado dentro del equipo de Delegaciones, uno por centro. Rol es propietario, miembro o invitado. Permiso es quién publica y quién ve cada canal. Herramienta son las pestañas del canal: archivos, calendario, Plánner y formularios. Y Plan es un plan de Plánner con un patrón de tablero.
A: ¿Qué diferencia hay entre asociación y especialización?
B: Una asociación relaciona dos clases: un grupo se divide en subgrupos. Una especialización dice que una clase es un tipo de otra: en el DMS, Acta, Normativa, Expediente y Registro de votación son tipos de Documento.
A: ¿Y la multiplicidad?
B: Cuántos objetos de una clase se relacionan con los de otra. Uno es exactamente uno, asterisco es cero o más, y cero punto punto uno es opcional.
A: ¿Cómo aplicasteis el laboratorio seis, los patrones de Plánner?
B: Respondimos las cinco preguntas del método para cada plan. Los planes de la Ejecutiva y de las delegaciones usan el ciclo de vida de tareas, donde las tarjetas pasan de por hacer a en curso y a hecho. El de la asamblea usa el proceso de tareas, con un cubo por etapa: convocatoria, preparación, día de la asamblea y después. Descartamos un cubo por delegación porque son veintisiete y Plánner no tiene permisos por tarea. Añadimos la clase Plan al UML y el requisito RF guion R trece al REM. Los planes están capturados.

## Los tres sistemas

A: Vamos con el portal. ¿Por qué un servidor local y no un hosting?
B: La guía de la asignatura exige un servidor local, no cuesta nada, permite instalar cualquier plugin y trabajamos todos sobre la misma instancia. Lo compartimos con Téilskeil sin abrir puertos. Lo malo es la disponibilidad, que mitigamos avisando por Discord y guardando copias de la base de datos.
A: ¿Y el servidor de la Universidad?
B: El servidor que ofreció el CADUS tenía PHP siete punto dos o siete punto tres, y WordPress necesita siete punto cuatro o más. El despliegue en la Universidad no está hecho y queda pendiente de la respuesta de la Universidad.
A: ¿Cómo elegisteis los plugins?
B: Para cada tipo comparamos al menos tres alternativas, con la fecha de la última actualización, las instalaciones activas, la valoración y el encaje con los requisitos. Los cuatro obligatorios de la asignatura son seguridad, con Güordfens, caché, con WP Fastest Cache, analítica, con WP Statistics, y SEO, con Yoast. Y además hay un plugin propio, cadus guion portal.
A: ¿Por qué un plugin propio, y por qué no SupportCandy para los tickets?
B: El plugin propio reúne el buzón, la mediación, las votaciones, el relevo de cuentas, el panel de gestión y las cargas de contenido. Así la lógica específica del CADUS queda versionada en nuestro plugin y evitamos añadir otro gestor de tickets, aunque seguimos dependiendo de Güordpres y de los plugins con los que se integra, como Fluent Forms. Y es fácil de mantener en el relevo entre cursos. SupportCandy lo elegimos al principio, pero guardaba los tickets en sus propias tablas y obligaba a rehacer la integración, el código de seguimiento y la privacidad. El módulo propio ya cumplía RN cero tres.
A: ¿Y el tema visual?
B: Comparamos cinco temas de WordPress y elegimos Bloksi por mantenimiento, valoración, accesibilidad declarada y configuración. Aparte, comparamos tres propuestas visuales y elegimos la identidad del CADUS, con su paleta, logotipo y tipografía oficiales. La etiqueta de accesibilidad del tema no acredita por sí sola el nivel AA.
A: Ahora el DMS. ¿Por qué Sherpoint?
B: Porque está disponible en el Microsoft trescientos sesenta y cinco de la Universidad que usa el equipo para el piloto, y ofrece sitios, bibliotecas con metadatos, permisos por grupo y búsqueda, justo lo que piden los conceptos del análisis. El acceso con las cuentas reales del CADUS y de las delegaciones sigue pendiente de confirmar.
A: ¿Qué reglas tiene el DMS?
B: Un acta solo la ven los delegados cuando la Ejecutiva la aprueba. Los expedientes los ve solo la Ejecutiva. Se conservan hasta dos años y un mes desde la resolución, con una retirada mensual manual. El registro de votación no guarda el DNI. Cuenta un voto por delegación y solo hay una versión vigente de cada norma. El REM tiene seis requisitos de información, dos de interfaz, diez funcionales, cinco no funcionales, siete reglas de negocio, ocho casos de uso y tres actores.
A: ¿Por qué ocho casos de uso en cuatro documentos?
B: Porque el profesor pidió dividirlos por secciones, una por tipo de documento: acta, normativa, expediente y votación, con dos casos en cada uno.
A: Y la red social. ¿Por qué Teams y no Discord?
B: Porque no requiere licencias nuevas para el piloto, usa las cuentas institucionales de la Universidad, se integra con Sherpoint, controla miembros y permisos por equipo y canal, y ofrece tareas, calendario y automatización. Discord lo usamos para el equipo de desarrollo.
A: ¿Por qué tres equipos de Teams y no uno?
B: Porque la Ejecutiva, las delegaciones y la asamblea tienen miembros, permisos y herramientas distintos. Con tres equipos, los canales privados de las delegaciones quedan juntos en uno solo y no se mezclan con los otros dos. Son veintisiete previstos, y el piloto tiene tres de ejemplo.
A: ¿Cómo se relacionan los tres sistemas?
B: El portal y el DMS son independientes, cada uno con su REM, UML, implementación y seguimiento. La red social enlaza a los documentos del DMS desde una pestaña de Archivos, sin copiarlos. Y los tres comparten la misma idea de privacidad: lo interno solo lo ve quien corresponde.
A: ¿Qué automatizáis con Páuer Automeit y Páuer Apps?
B: Hay dos flujos de Páuer Automeit. El primero avisa en el canal cuando se crea una tarea en el plan de la asamblea; si se asigna después una tarea que ya existe, no avisa. El segundo avisa de las tareas que vencen. El segundo se ejecutó programado, por sí solo, el veintiséis y el veintisiete de noviembre a las ocho de la mañana. Y Páuer Apps ofrece una aplicación sencilla con la lista de delegaciones y su estado. Álvaro dice que está publicada, y Marcos confirma de palabra que la tiene, pero no hay captura. No se comprobó que esté integrada en Teams.

## Calidad

A: Vamos a los números. ¿Cómo protegéis los formularios?
B: Los formularios que guardan datos llevan nonce. En el código que se revisó, las entradas de texto se sanean y las salidas se escapan, salvo las contraseñas, y las consultas directas a la base usan prepare. El buzón y la mediación tienen campo trampa y un límite de diez envíos por IP cada quince minutos. En la prueba de inyección, las etiquetas se eliminan, el texto con SQL se guarda como texto y los envíos con script los bloquea Güordfens antes de llegar al portal.
A: ¿Encontrasteis fallos?
B: Sí. Una revisión encontró un fallo grave: un delegado podía cambiar el título de su ficha por la API REST. Se corrigió y se probó. Güordfens no encontró malware ni vulnerabilidades.
A: Accesibilidad.
B: El objetivo es WCAG dos punto uno, nivel AA. Hay enlace de saltar al contenido, foco visible, formularios con etiquetas y errores enlazados con su campo. Lighthouse de accesibilidad dio noventa y siete, noventa y seis y noventa y seis al principio, y tras los arreglos se repitió con el código actual y dio cien, cien y cien. Se recorrió todo con teclado, se simuló el daltonismo, se leyó el buzón con el Narrador de Windows y también se probó con NVDA el veintisiete de noviembre, según Pablo, sin registro paso a paso.
A: Rendimiento.
B: Con caché, minificación y compresión, la portada pasó de noventa y uno a noventa y nueve en Láithaus, y la respuesta del servidor de quinientos diecisiete milisegundos a ocho. El peso de la portada bajó de quinientos treinta y siete a trescientos once kilobytes, un cuarenta por ciento menos. Con el contenido real, la mediana en móvil fue noventa y ocho. El buzón no se cachea a propósito, por privacidad, y por eso es la página más lenta. Sin caché, las páginas tardan entre tres coma siete y cuatro coma cuatro segundos, así que estas cifras no demuestran por sí solas el requisito de tres segundos.
A: Privacidad.
B: Tickets y mediaciones son privados: no salen por la API REST, ni por la búsqueda, ni por los feeds. Los avisos por correo no llevan el contenido de la consulta. El de la Ejecutiva trae código, tipo, fecha y enlace, y el del estudiante, código, estado y enlace. La búsqueda del panel mira la referencia y el asunto en los tickets, y la referencia y el centro en las mediaciones; nunca nombre, correo ni descripción. Los casos resueltos se anonimizan pasados dos años desde que se cierran, con una tarea diaria; los abiertos no se anonimizan, y esa ejecución programada no se ha comprobado en el servidor del equipo.
A: ¿Y el correo real? Antes decíais que no se había probado.
B: Ya se probó el veintisiete de noviembre con el SMTP de Gmail. Los cuatro avisos llegaron a una dirección de alumno de la Universidad, con entre sesenta y cinco y setenta minutos de retraso. El portal los entregó al servidor de correo al momento, y el retraso apunta al filtro de la Universidad, sin que se haya confirmado la causa. Con eso, la prueba P cinco quedó correcta.
A: ¿Cuántas pruebas hay?
B: Cuarenta y tres casos de aceptación, y los cuarenta y tres constan como correctos. Pero hay matices que hay que decir. Los tiempos de las tareas T uno a T tres los cronometró Pablo, que conoce el portal: cincuenta, diez y dieciocho segundos, con el límite en sesenta. No los midió una persona externa ni se hizo en móvil. La prueba del relevo de cuenta, la historia veintidós, la ejecutó Claude en nombre de Pablo, y no otra persona del equipo. En cambio, Joaquín hizo la prueba cruzada del directorio y de los filtros el veintisiete de noviembre. Y el móvil y la tablet constan como comprobados según Pablo.
A: ¿Por qué decís eso tan claro?
B: Porque cada caso dice quién lo hizo, cuándo y cómo. Es mejor que lo diga el registro a que lo descubra el profesor.

## Equipo y uso de la inteligencia artificial

A: ¿Quién hizo qué?
B: Somos cuatro. Pablo es Product Owner y lleva los REM, los documentos y la infraestructura. Joaquín es Scrum Master y lleva Plánner, los flujos y el seguimiento. Álvaro hizo los UML del DMS, el directorio, los filtros, la conservación a dos años y Páuer Apps. Y Marcos hizo la accesibilidad de los formularios, la búsqueda del panel, el antispam y la configuración de canales y permisos de Teams. Otras partes de accesibilidad, de seguridad y la creación de los equipos se repartieron entre los demás. Fuimos cinco hasta el dieciséis de noviembre, cuando Miguel Ángel, que era el enlace con el cliente, dejó el trabajo.
A: ¿Habéis usado inteligencia artificial?
B: Sí, y lo decimos con claridad. Clod para programar y documentar, y Codex para revisar. En la carpeta docs barra scrum conservamos los encargos de cada revisión de Codex, y los hallazgos y sus correcciones constan en los informes y registros. Y las pruebas que ejecutó Clod en nombre de una persona constan así en el registro.

## Autocrítica

A: ¿Qué haríais distinto?
B: Tres cosas. Repartir el trabajo durante el sprint y actualizar el burndown cada día. Reservar un día de pruebas cruzadas antes de cada entrega, porque muchas las hizo quien implementó. Y conseguir antes la entrevista y el contenido real del cliente, que llegaron tarde.
A: ¿Qué es lo más difícil que os encontrasteis?
B: Combinar tres sistemas con un equipo pequeño, y mantener la privacidad en todos: los tickets son privados en el portal, los expedientes en el DMS y los canales de cada delegación en Teams. Y que el cliente dejara de estar localizable a mitad de camino.

## Lo que no está hecho

A: Ahora lo importante: ¿qué no habéis conseguido? Dilo como lo dirías en la defensa.
B: Cuatro tipos de pendiente, sin mezclarlos. Uno: lo que depende de la Universidad. El despliegue del portal en la Universidad, y probar con cuentas reales de delegado y de estudiante: esperan su respuesta. Las cuentas reales del CADUS dependen del cliente.
A: Siguiente.
B: Dos: lo que está hecho en parte. El piloto de Teams tiene tres canales de ejemplo, y las veintisiete delegaciones quedan previstas en el diseño, no puestas en marcha. Páuer Apps no restringe el alta y la baja por rol, no se probó crear, editar ni borrar delegaciones, y no hay captura de la publicación. Y en el DMS falta comprobar que una cuenta con rol de estudiante no puede entrar en Expedientes. Y el resumen automático del acta, el requisito RF guion D diez, es deseable y no se hizo.
A: Siguiente.
B: Tres: lo que no tiene revisión independiente. No todas las pruebas las repitió otra persona, y los tiempos de las tareas no los midió una persona externa. Y cuatro: faltan datos de las delegaciones que solo puede dar el CADUS, como el horario, siete teléfonos y un correo.
A: ¿Y cómo lo resumes en una frase?
B: Que tenemos una versión preparada para entregar, con las pruebas y las limitaciones registradas, y que no está todo implementado ni verificado: lo que falta consta en cada documento con su motivo.

## Qué se entrega

A: ¿Qué se entrega y cuándo?
B: El zip está generado y falta enviarlo, el domingo veintinueve de noviembre. Lleva el portal, el DMS y la red social: documentos, REM, UML, capturas, seguimiento y el volcado saneado de la base de datos con tres cuentas de demostración. Y hasta el catorce de diciembre, aparte, un único PDF con los seis manuales: de usuario y de administrador de cada sistema. Esa entrega extra no es necesaria para la defensa.

## Ronda de preguntas

A: Ahora te toca a ti. Después de cada pregunta hay unos segundos de silencio para que contestes en voz alta, y luego te doy la respuesta corta.
A: Primera pregunta. ¿Qué diferencia hay entre el UML de análisis y el de diseño?
[pausa]
B: El análisis dice qué conceptos hay, sin tecnología. El diseño dice con qué herramienta se construye cada uno.
A: Segunda. ¿Qué dice la regla de negocio RN cero tres?
[pausa]
B: Que tickets, reclamaciones y mediaciones son privados: solo los ven su remitente y la Ejecutiva.
A: Tercera. ¿Qué cambió tras la entrevista del veintiséis de octubre?
[pausa]
B: Votaciones presenciales, así que se canceló la papeleta online. Se añadió el relevo de cuenta, y la conservación a dos años. Y la privacidad se amplió a todas las consultas.
A: Cuarta. ¿Por qué un plugin propio y no SupportCandy?
[pausa]
B: Porque SupportCandy guardaba los tickets en sus tablas y obligaba a rehacer la integración, el código de seguimiento y la privacidad. El módulo propio ya cumplía RN cero tres.
A: Quinta. ¿Por qué Teams y no Discord para la red social?
[pausa]
B: Sin licencias nuevas, con las cuentas de la Universidad, integrado con Sherpoint y con permisos por equipo y canal. Discord es para el equipo de desarrollo.
A: Sexta. ¿Por qué tres equipos de Teams y no uno?
[pausa]
B: Porque Ejecutiva, delegaciones y asamblea tienen miembros, permisos y herramientas distintos, y los canales privados de las delegaciones quedan juntos en un solo equipo.
A: Séptima. ¿Cómo aplicasteis los patrones de Plánner del laboratorio seis?
[pausa]
B: Con las cinco preguntas del método. Ciclo de vida para Ejecutiva y delegaciones, proceso de tareas para la asamblea, y se descartó un cubo por delegación porque son veintisiete.
A: Octava. ¿Qué problema tuvisteis con SCRUM?
[pausa]
B: Cerrábamos el trabajo al final de cada sprint y no actualizábamos el burndown cada día, aunque lo acordamos.
A: Novena. ¿Habéis usado inteligencia artificial?
[pausa]
B: Sí: Clod para programar y documentar, y Codex para revisar. Los encargos de revisión constan en el repositorio, y las pruebas que hizo Clod en nombre de alguien constan así.
A: Décima. ¿Qué no habéis conseguido?
[pausa]
B: Desplegar en la Universidad y probar con cuentas reales, que esperan su respuesta; y que las pruebas las repita siempre otra persona. Lo demás está registrado con sus pruebas y sus limitaciones.

## Cierre

A: Y hasta aquí el repaso. Si solo te acuerdas de tres cosas, que sean estas.
B: Una: el código del requisito une todo, del REM a la prueba. Dos: el análisis dice qué hay y el diseño dice con qué se hace. Y tres: lo que no está hecho se dice tal cual, con su motivo. Mucha suerte en la defensa.
