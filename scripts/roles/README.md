# Cuentas institucionales y roles (E2-01)

Hoy las cinco cuentas del WordPress (`root`, `alvaro`, `joaquin`, `marcos`, `Miguel`) son administradoras: son las del equipo. Las cuentas del CADUS todavía no existen.

## Cuentas institucionales, no personales

El CADUS se renueva cada año: sus miembros y los de las delegaciones cambian con cada relevo. Por eso las cuentas del portal **no son de personas, sino de órganos**, y cada una va asociada a un correo institucional que pasa de un equipo al siguiente (decisión del cliente, octubre de 2026):

| Cuenta | Correo | Rol de WordPress | Cómo se da de alta |
|---|---|---|---|
| **CADUS** (única cuenta interna) | `dcadus@us.es` | Administrador | A mano, en **Usuarios › Añadir nuevo** (este script no toca administradores) |
| **Una por delegación** | El correo propio de cada delegación | Delegado | Con este script, a partir de [`usuarios-reales.csv`](usuarios-reales.csv) |

- Todo el CADUS trabaja desde la cuenta `cadus`, porque responde a un único correo (`dcadus@us.es`). WordPress no admite dos cuentas con el mismo correo, así que no hay una cuenta de Ejecutivo aparte.
- Cada delegación tiene su cuenta y solo puede editar **su propia ficha** (RN-04).

## Procedimiento

1. **Miguel Ángel** rellena [`usuarios-reales.csv`](usuarios-reales.csv) con una línea por delegación: `usuario,nombre,correo,rol,delegacion`.
   - `usuario`: nombre de acceso sin espacios ni tildes (p. ej. `d-etsii`, `d-quimica`).
   - `nombre`: nombre visible de la delegación (p. ej. `Delegación de Alumnos ETSII`).
   - `correo`: correo propio de la delegación.
   - `rol`: se puede dejar vacío; vacío equivale a `delegado`.
   - `delegacion`: se puede dejar vacío. Entonces el script busca la ficha de la delegación **cuyo título sea igual al `nombre`**. Solo hace falta rellenarla si la ficha tiene otro título.

   Ejemplo:
   ```
   usuario,nombre,correo,rol,delegacion
   d-etsii,Delegación de Alumnos ETSII,delegacionetsii@us.es,delegado,Delegación de Escuela Técnica Superior de Ingeniería Informática
   d-quimica,Delegación de Alumnos de Química,delegacionquimica@us.es,delegado,Delegación de Facultad de Química
   ```

   Las fichas de delegación se titulan «Delegación de» + el nombre oficial del centro (p. ej. `Delegación de Facultad de Química`), con las mismas tildes y mayúsculas. El ensayo en seco lista los títulos que existen. Si una ficha aún no existe (E2-12), la cuenta se crea igualmente y el script avisa con ⚠; al volver a ejecutarlo cuando la ficha exista, se le asigna.
2. **Pablo** ejecuta primero el ensayo en seco (no cambia nada, muestra lo que haría, los errores y la lista de delegaciones existentes con su título exacto):
   ```bash
   php scripts/roles/aplicar_usuarios.php
   ```
3. Si todo es correcto, aplica los cambios (`--avisar` envía a cada delegación el enlace para elegir su contraseña; necesita correo saliente configurado en el servidor):
   ```bash
   php scripts/roles/aplicar_usuarios.php --aplicar --avisar
   ```
4. Crear a mano la cuenta `cadus` (`dcadus@us.es`, rol Administrador).
5. Comprobar con una cuenta de delegación el menú y los permisos (HU-19c) y, al cerrar el proyecto, retirar las cuentas de administrador del equipo.

## Relevo anual

Cuando entra un equipo nuevo en el CADUS o en una delegación, no se crea ninguna cuenta:

1. En la pantalla de acceso, pulsar **«¿Has olvidado tu contraseña?»** e introducir el usuario (`cadus` o el de la delegación).
2. El enlace llega al correo institucional, al que ya tiene acceso el equipo nuevo.
3. Elegir una contraseña nueva. La del equipo anterior deja de funcionar.

## Garantías

- Las contraseñas no se guardan ni se muestran: se genera una aleatoria que nadie ve y cada titular la cambia con el enlace de «contraseña olvidada».
- No toca cuentas de administrador.
- Una delegación queda como **autora** de su ficha, que es lo que le permite editarla y nada más (RN-04).
- El CSV solo contiene correos institucionales, no datos personales. Aun así, no deben añadirse nombres ni correos personales de los miembros.
