# Entrevista con el CADUS

**Entrevistado:** Miguel Ángel Camacho Martín, miembro del CADUS y contacto con el cliente.
**Entrevistadores:** equipo de desarrollo del portal CADUS (5 integrantes).
**Fecha:** 26/10/2026 (inicio del Sprint 3).
**Contexto:** el portal (CMS) tiene entregados el Sprint 1 y el Sprint 2; quedan móvil, accesibilidad, filtros del panel, protección de formularios y rendimiento. Las respuestas son las que dio Miguel Ángel.

## 1. Votaciones (RF-12, RN-05, HU-21)

**1. Cuando el CADUS convoca una votación, ¿el voto debe ser secreto o nominal?**
Nominal o secreto, según el caso, y **por delegación**.

**2. ¿Quién puede votar y cómo se comprueba?**
Solo los delegados. Cada voto representa a los estudiantes de su delegación, no a la persona. Las votaciones son presenciales, y la identidad se confirma presentando el DNI.

**3. ¿Qué tipos de votación hacéis y qué opciones tienen?**
Las votaciones son sobre asambleas y los votos son sí, no o abstención.

**4. ¿Hace falta publicar el resultado en el portal?**
No. Solo informar de que se va a realizar la votación.

## 2. Cuentas y roles (RF-14, RN-04)

**5. ¿Cuántos delegados y qué pueden hacer?**
Uno por delegación; la cuenta representa a la delegación, no a la persona. Hay **27 delegaciones**. Pueden editar la ficha de su delegación y dar de alta a un nuevo delegado cuando el actual se da de baja.

**6. La Ejecutiva entra con la cuenta única `dcadus@us.es`. ¿Se mantiene?**
Sí, la cuenta se mantiene para todos.

**7. Cuando cambia el delegado, ¿quién da de baja y de alta?**
Cualquier ejecutivo, o el propio delegado que se da de baja, y con acción inmediata a poder ser.

## 3. Atención al estudiante: buzón y mediación (RF-08 a RF-10, RF-13, RN-03)

**8. ¿Quién atiende los tickets y en qué plazo?**
Cualquier ejecutivo. El aviso de ticket debe llegar al correo de `dcadus`. El plazo de respuesta es de al menos 4 días.

**9. ¿Qué consultas recibís más y cuáles son delicadas?**
Becas y conflictos con profesores. Lo de los profesores es más sensible, aunque todas las consultas deberían tratarse con total privacidad.

**10. ¿Cuánto tiempo hay que guardar los tickets?**
2 años desde que el ticket se resuelve, para tenerlo como prueba.

**11. ¿Qué datos del estudiante son necesarios?**
Solo nombre y apellidos, facultad y correo de la US.

**12. ¿Cómo debe avisarse al estudiante?**
Por correo y en el portal, las dos vías.

## 4. Contenido y mantenimiento (RF-01 a RF-07, RN-01)

**13. ¿Quién publicará noticias y actas?**
Cualquier ejecutivo con la cuenta del CADUS.

**14. ¿Qué podemos publicar ya?**
Todo tiene que pasar por la Ejecutiva, así que no publicamos nada: es una web de prueba y ellos subirán el contenido que quieran si es necesario.

**15. ¿Nos pueden pasar los datos de las delegaciones que faltan?**
Sacadlos de la web del CADUS, en `cadus.us.es/delegaciones/`.

**16. ¿Qué debe incluir el calendario?**
Asambleas y cursos. Lo mantienen los ejecutivos.

## 5. Uso, móvil y accesibilidad (RNF-02, RNF-03)

**17. ¿Desde qué dispositivo usará la gente el portal?**
Móvil, tablet y ordenador, así que la vista móvil y tablet es importante.

**18. ¿Qué necesidades de accesibilidad hay que tener en cuenta?**
Estaría muy bien que fuera una página accesible para personas con alguna necesidad (ciegas o daltónicas) y que siga las pautas del **DUA** (Diseño Universal para el Aprendizaje).

**19. ¿Qué tres cosas tendría que poder hacer un estudiante en menos de un minuto?**
Crear un ticket, consultar el calendario, y consultar asambleas, eventos y últimas noticias.

## 6. Prioridades y expectativas

**20. ¿Qué es imprescindible el 15/11?**
Todo el WordPress tiene que estar terminado e implementado para el 15.

**21. ¿Qué es lo que más teméis que falle?**
Que se filtre una reclamación, que el portal caiga en plena votación y que alguien publique sin permiso.

**22. ¿Dónde estará alojado el portal y quién lo mantendrá?**
En un servidor SFTP de la US, y lo mantendrá quien ellos crean necesario. Buscan una web con poco mantenimiento, donde se puedan meter datos como noticias o gestionar tickets con facilidad para personas con pocos conocimientos informáticos.

## Qué cambia en el proyecto según las respuestas

| Respuesta | Efecto | Dónde |
|---|---|---|
| Las votaciones son presenciales y no se publican resultados (1-4) | **La papeleta online (HU-21) deja de tener sentido.** El portal solo anuncia la votación (ya cubierto por HU-11). El registro de la votación por delegación pasa al DMS | HU-21, RF-12, RN-05 |
| La cuenta de delegado representa a la delegación y puede dar de alta al nuevo delegado (5, 7) | Nuevo permiso: el delegado crea la cuenta de su sucesor; cualquier ejecutivo también | RF-14, RN-04 (nueva historia) |
| 27 delegaciones, datos de `cadus.us.es/delegaciones/` (5, 15) | Cargar las 27 fichas desde la web del CADUS | E2-12 |
| Aviso de ticket al correo `dcadus` y plazo de respuesta «de al menos 4 días» (8) | El aviso al buzón de la Ejecutiva. **El plazo se publica solo cuando se aclare** si es mínimo o máximo, en días naturales o hábiles y desde cuándo se cuenta | RF-10, E3-08 |
| Conservación de 2 años desde la resolución (10) | Cierra el plazo pendiente de RNF-08; hay que borrar o anonimizar a los 2 años | RNF-08 (nueva tarea) |
| Datos mínimos: nombre y apellidos, facultad y correo (11) | Revisar los campos del buzón y de la mediación | HU-17 |
| Aviso al estudiante por correo y en el portal (12) | Ya cubierto: aviso por correo sin contenido y seguimiento en el portal con código | RF-09 |
| Todas las consultas deben tratarse con total privacidad (9) | RN-03 se amplía de reclamaciones y mediaciones a **todas** las consultas del buzón | RN-03, E3-05 |
| Todo contenido pasa por la Ejecutiva (14) | RN-01 se amplía de actas y normativa a **todo** el contenido publicado | RN-01, E3-05 |
| Tres operaciones de menos de un minuto: crear un ticket, consultar el calendario, ver asambleas, eventos y noticias (19) | Prueba de aceptación de usabilidad | E3-04 |
| Calendario con asambleas y cursos (16) | Añadir la categoría «Cursos» | RF-11 |
| Móvil, tablet y ordenador (17) | HU-14 incluye la tablet en las pruebas | HU-14 |
| Accesibilidad para ciegos y daltónicos y pautas DUA (18) | HU-15 añade criterios de daltonismo, lector de pantalla y DUA | HU-15 |
| Todo el WordPress terminado el 15/11 (20) | Se mantiene el alcance; el ajuste de HU-21 libera 3 SP | Sprint 3 |
| Servidor SFTP de la US y poco mantenimiento (22) | Riesgo: WordPress necesita PHP y MySQL; hay que confirmar qué ofrece el servidor (E3-03) y reservar tiempo para desplegar y probar (E3-09). Simplificar el panel para personas sin conocimientos técnicos | RNF-05, RNF-07 |
| El relevo de delegados exige baja y alta (7) | HU-22 incluye revocar el acceso del anterior, traspasar la ficha y mantener una sola cuenta activa por delegación | RF-14, RN-04 |
