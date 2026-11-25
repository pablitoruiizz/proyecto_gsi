# Mensajes para enviar (Pablo): CADUS y US

**Decisión de Pablo del 23/11: no se van a enviar.** Solo queda anotado, en E3-09, que está pendiente hablar con la US sobre el despliegue.

Borradores del 23/11/2026 para cerrar E2-01, E2-12 (datos reales de las delegaciones) y E3-09 (despliegue). Los envía Pablo; cada respuesta se anota en `docs/scrum/sprints/sprint-02.md` o `sprint-03.md` con su fecha.

## 1. Al CADUS (E2-01 y E2-12)

**Asunto:** Portal del CADUS: datos que necesitamos para dejarlo listo (antes del 26/11)

Hola:

El portal ya funciona con 27 delegaciones publicadas, pero las fichas llevan datos de ejemplo y las cuentas son del equipo de desarrollo. Para entregarlo a final de curso necesitamos dos cosas de vuestra parte.

**1. Las cuentas.** El modelo que acordamos el 09/11 es **una cuenta por delegación**, con el correo institucional de la delegación. Necesitamos:

- La lista de quién tendrá rol **Ejecutiva** (pueden gestionar todo el portal) y su correo institucional.
- Para cada delegación, el correo institucional con el que se creará su cuenta de **Delegado**.
- Qué cuentas de administrador sobran y se pueden retirar.

**2. Los datos de cada ficha.** Por delegación: nombre del delegado o equipo, correo, teléfono (si se quiere publicar), horario de atención, redes sociales y enlaces. Sirve una hoja de cálculo con una fila por delegación; nosotros la cargamos.

Por privacidad, no hace falta mandar contraseñas: las crea el sistema y se entregan en el relevo de cada cuenta.

¿Podéis mandárnoslo antes del **jueves 26/11**? La entrega final es el domingo 29/11 y necesitamos un par de días para cargarlo y probarlo. Si no llega a tiempo, entregamos con los datos que ya tenemos de vuestra web y lo dejamos indicado.

Gracias,
Pablo (Product Owner)

## 2. A la US (E3-09)

**Asunto:** Alojamiento web para el portal del CADUS: qué ofrece la US

Hola:

Somos el equipo que ha desarrollado el portal del CADUS (WordPress). Queremos saber si la US puede alojarlo y en qué condiciones. Lo que necesita el portal:

- **PHP 8.1 o superior**, con las extensiones `mysqli`, `mbstring` y `zip`. El servidor que nos indicaron ofrece PHP 7.2/7.3 y WordPress 7.1 pide 7.4 como mínimo (y nuestro plugin, 8.0).
- **Base de datos MySQL o MariaDB**, y cómo se accede a ella (phpMyAdmin, usuario propio, importación de un volcado `.sql`).
- **Envío de correo** (SMTP) para los avisos del buzón. Pensamos usar la cuenta del CADUS; ¿hay servidor SMTP o hay que usar otro?
- **Tarea programada** (cron) una vez al día, para la anonimización de tickets a los 2 años (RN-03).
- **Copia de seguridad** periódica de ficheros y base de datos.
- **Certificado HTTPS** y el dominio o ruta donde quedaría.

Preguntas:

1. ¿Es posible con el servicio actual o hay otro servicio de la US que lo cubra?
2. Si no lo es, ¿qué alternativa recomendáis?
3. ¿Quién sería nuestro contacto para el despliegue y con qué plazos?

Nuestra entrega final es el domingo 29/11/2026, así que os agradeceríamos una respuesta antes del jueves 26/11. Sin respuesta, entregaremos el portal funcionando en local con el volcado de la base de datos y las instrucciones de instalación.

Gracias,
Pablo (Product Owner)

## Qué hacer con las respuestas

- **CADUS responde:** crear las cuentas con `scripts/roles`, cargar las fichas y cerrar E2-01 y E2-12 en el GitHub Project (#36 y #47).
- **La US ofrece alojamiento:** reabrir E3-09 (#67) y desplegar, probando el correo real (E3-04, P5).
- **La US no ofrece nada o no responde:** anotarlo en `sprint-03.md` y dejarlo como limitación en el documento final del CMS (E3-06).
