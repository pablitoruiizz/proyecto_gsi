# Cuentas y roles del portal (E2-01)

Hoy las cinco cuentas del WordPress de desarrollo (`root`, `alvaro`, `joaquin`, `marcos`, `Miguel`) son administradoras: son las del equipo. Para el portal en producción el cliente decidió este modelo (octubre de 2026):

| Cuenta | Quién la usa | Correo de acceso | Rol de WordPress | Cómo se da de alta |
|---|---|---|---|---|
| **`cadus`** (única) | **Todos los miembros de la Ejecutiva** | `dcadus@us.es` | Administrador | [`crear_cuenta_cadus.php`](crear_cuenta_cadus.php) |
| **Una por delegado** | Cada delegado de centro | Su **correo de alumno** (`@alum.us.es`) | Delegado de centro | Desde la cuenta `cadus` (Usuarios › Añadir nuevo) o con [`aplicar_usuarios.php`](aplicar_usuarios.php) |

- La Ejecutiva no tiene cuentas personales: entra siempre con `cadus`, que responde a un único correo (`dcadus@us.es`). WordPress no admite dos cuentas con el mismo correo, así que no hay una cuenta de «Ejecutivo del CADUS» aparte; ese rol existe para quien el CADUS quiera con permisos de contenido sin ser administrador.
- **Es la cuenta `cadus` la que da acceso a los delegados**: los da de alta, los asigna a su delegación y los da de baja.
- Cada delegado entra con su correo de alumno y solo puede editar **la ficha de su delegación** (RN-04).

## Alta de la cuenta del CADUS

```bash
php scripts/roles/crear_cuenta_cadus.php
```

No guarda ni muestra contraseñas y no envía correo. La primera vez se entra con **«¿Has olvidado tu contraseña?»** y el usuario `cadus`: el enlace llega a `dcadus@us.es`.

## Alta de los delegados

1. Copiar [`usuarios-ejemplo.csv`](usuarios-ejemplo.csv) a `usuarios-reales.csv` (este fichero **no se sube a GitHub**: lleva correos de alumnos, que son datos personales) y rellenar una línea por delegado: `usuario,nombre,correo,rol,delegacion`.
   - `usuario`: nombre de acceso sin espacios ni tildes (p. ej. `d-etsii`).
   - `nombre`: nombre visible (p. ej. `Delegación de Alumnos ETSII`).
   - `correo`: el **correo de alumno del delegado** (`@alum.us.es`); el script lo exige para los delegados.
   - `rol`: vacío equivale a `delegado`.
   - `delegacion`: título exacto de la ficha (p. ej. `Delegación de Facultad de Química`); si se deja vacío, se busca una ficha con el mismo título que `nombre`.
2. Ensayo en seco (no cambia nada, lista los problemas y los títulos de las fichas existentes):
   ```bash
   php scripts/roles/aplicar_usuarios.php
   ```
3. Aplicar los cambios (`--avisar` envía a cada delegado el enlace para elegir su contraseña; necesita correo saliente en el servidor):
   ```bash
   php scripts/roles/aplicar_usuarios.php --aplicar --avisar
   ```
4. Comprobar con una cuenta de delegado el menú y los permisos (HU-19c).

## Relevo de delegados

Cuando cambia el delegado de un centro, la cuenta `cadus` da de baja la cuenta anterior (Usuarios › Borrar, atribuyendo el contenido a `cadus`) y da de alta la del nuevo delegado, que queda como autor de la ficha de su delegación. Para el relevo de la Ejecutiva no hay que crear cuentas: se usa «¿Has olvidado tu contraseña?» con el usuario `cadus` y el enlace llega a `dcadus@us.es`, al que ya tiene acceso el equipo nuevo.

## Garantías

- Las contraseñas no se guardan ni se muestran: se genera una aleatoria que nadie ve y cada titular elige la suya con el enlace de «contraseña olvidada».
- El script de delegados no toca las cuentas de administrador, rechaza usuarios o correos repetidos y no deja actualizar una cuenta distinta de la indicada.
- Una delegación queda como **autora** de su ficha, que es lo que le permite editarla y nada más (RN-04).
- `usuarios-reales.csv` está en `.gitignore`: los correos de alumnos no deben subirse al repositorio.
