# Pruebas de HU-12 · Solicitud de mediación estudiantil

**Requisitos:** RF-13 · IR-08 · RN-02, RN-03 · RNF-04, RNF-08
**Código probado:** `cms-wordpress/wp-content/plugins/cadus-portal/includes/mediacion.php` (shortcode `[cadus_mediacion]`, formulario de Fluent Forms creado por código y tipo de contenido privado `cadus_mediacion`)
**Quién prueba:** Álvaro Martínez Ocaña · **Fecha:** 24/10/2026 · **Versión probada:** `main`, plugin CADUS Portal 1.0.0, Fluent Forms activo, WordPress 7.1 local (XAMPP, base `bd_cadus`)

## Qué hace HU-12

Una persona rellena un formulario público con su nombre, correo universitario `@alum.us.es`, Facultad o Escuela, descripción del conflicto y consentimiento RGPD. Al enviarlo se crea una solicitud **privada** con una referencia `MED-AAAA-NNNNN-<código>` y estado *Pendiente*. La Ejecutiva la gestiona desde el menú *Mediaciones* del panel y cambia su estado (*Pendiente*, *En proceso*, *Cerrada*).

## Entorno

Para probar el formulario hizo falta instalar y activar **Fluent Forms** en el WordPress local, porque sin él la página muestra «La solicitud de mediación no está disponible temporalmente». El formulario se crea la primera vez que un administrador abre la página de mediación. Las pruebas del formulario se hicieron sin sesión y las del panel con el usuario de prueba de la Ejecutiva.

## Casos del formulario público

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| M1 | Abrir la página de mediación sin sesión. | Aviso de privacidad (RGPD) y formulario con cinco campos. | OK. Aviso y formulario con nombre, correo, centro (6 opciones), descripción y consentimiento. |
| M2 | Enviar el formulario vacío. | No se envía; mensajes de campo obligatorio. | OK. «Este campo es obligatorio» en los cuatro primeros campos y «Debes aceptar el tratamiento de tus datos». |
| M3 | Todo relleno con el correo `prueba@gmail.com`. | No se envía; error de correo `@alum.us.es` (RN-02). | OK. «Utiliza un correo universitario válido terminado en @alum.us.es.» |
| M4 | Correo `@alum.us.es` válido, sin elegir centro. | No se envía; error en el centro. | OK. «Este campo es obligatorio» en Facultad o Escuela (mensaje genérico del formulario). |
| M5 | Todo correcto pero sin marcar el consentimiento. | No se envía; error de consentimiento. | OK. «Debes aceptar el tratamiento de tus datos.» |
| M6 | Todo correcto con `prueba@alum.us.es`. | Confirmación con la referencia. | OK. «Hemos registrado tu solicitud de mediación con la referencia: MED-2026-00061-…» |
| M7 | Recargar la página tras enviar. | Vuelve el formulario vacío; la referencia no se repite. | OK. |
| M8 | Enviar con tildes, `ñ` y comillas. | Se guarda correctamente. | OK. La solicitud MED-2026-00062 conserva `Ñandú Pérez "Prueba"` en el panel. Pendiente de verificar a mano que el HTML del texto de la descripción se muestra escapado. |

## Casos en el panel (Ejecutiva)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| P1 | Abrir *Mediaciones* con la Ejecutiva. | Aparecen las solicitudes enviadas, privadas, con su referencia y estado. | OK. Dos solicitudes (MED-2026-00061 y 00062), en estado *Pendiente* y visibilidad *Privadas*. |
| P2 | Abrir una solicitud. | Datos del solicitante, correo, centro y fecha (IR-08). | OK. Se ven referencia, solicitante, correo, Facultad o Escuela y fecha de la solicitud. |
| P3 | Cambiar el estado a *En proceso* y recargar. | El estado se mantiene. | OK. Se ve en la lista y al reabrir la solicitud. |
| P4 | Cambiar el estado a *Cerrada* y recargar. | El estado se mantiene. | OK. Se ve en la lista. |

## Casos de privacidad (RN-03)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| R1 | Sin sesión, abrir `/wp-json/wp/v2/cadus_mediacion`. | 404: no se expone por la API REST. | OK. `rest_no_route`, estado 404. |
| R2 | Sin sesión, buscar la referencia en el buscador del portal. | Sin resultados. | OK. «Sorry, but nothing matched your search terms.» |
| R3 | Con el Estudiante y el Delegado, abrir `edit.php?post_type=cadus_mediacion`. | Sin permisos. | Pendiente de ejecutar. Hay que anotar que ya se comprobó el caso del Estudiante para tickets en HU-19c (E4) y que el código de roles no concede permisos de mediación al Delegado. |
| R4 | Con un Estudiante con sesión, enviar una solicitud y comprobar que no la ve después. | Solo recibe la referencia. | Pendiente de ejecutar. |

## Fallos y observaciones

| # | Caso | Qué ocurre | Corrección / issue |
|---|---|---|---|
| 1 | Entorno | Sin Fluent Forms instalado, la página muestra «no disponible temporalmente». | Documentar en el README que el entorno local necesita Fluent Forms activo. |
| 2 | M4 | El error de centro vacío es el genérico «Este campo es obligatorio», no el mensaje propio del servidor. | Sin impacto: la solicitud no se envía. |
| 3 | Referencia | El formato real es `MED-2026-NNNNN-<código largo>`, más largo que el documentado inicialmente. | Actualizar la documentación del formato. |
| 4 | Datos de prueba | Quedan dos solicitudes de prueba en la base local. | Borrarlas (papelera y vaciar) antes del volcado final. |

## Comprobaciones finales

- Sin avisos de PHP revisados en `wp-content/debug.log`: no comprobado.
- Solicitudes y usuarios de prueba pendientes de borrar.

## Capturas para la implementación (1920×1080, con pie y códigos RF-13 · IR-08 · RN-02 · RN-03 · HU-12)

- **A.** Formulario de solicitud de mediación en la web pública.
- **B.** Error de correo no universitario (M3).
- **C.** Confirmación con la referencia (M6).
- **D.** Lista de *Mediaciones* en el panel con las solicitudes recibidas (P1).
- **E.** Detalle de la solicitud con el selector de estado (P2).

## Trazabilidad

| Requisito | Casos que lo cubren |
|---|---|
| RF-13 (solicitud de mediación) | M1, M6, P1, P3, P4 |
| IR-08 (datos de la solicitud) | M6, P1, P2 |
| RN-02 (correo `@alum.us.es`) | M3 |
| RN-03 (solicitudes privadas) | R1, R2 (R3 y R4 pendientes) |
