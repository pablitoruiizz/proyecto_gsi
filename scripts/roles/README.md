# Cuentas y roles del portal (E2-01)

Hoy las cinco cuentas del WordPress de desarrollo (`root`, `alvaro`, `joaquin`, `marcos`, `Miguel`) son administradoras: son las del equipo. Para el portal en producción las cuentas son **institucionales, no personales**: la cuenta representa al órgano (el CADUS o una delegación), no a la persona que lo ocupa este curso. Así, el relevo anual no obliga a crear ni borrar cuentas (decisión del cliente, octubre de 2026, confirmada el 09/11/2026).

| Cuenta | Quién la usa | Correo de acceso | Rol de WordPress | Cómo se da de alta |
|---|---|---|---|---|
| **`cadus`** (única) | **Todos los miembros de la Ejecutiva** | `dcadus@us.es` | Administrador | [`crear_cuenta_cadus.php`](crear_cuenta_cadus.php) |
| **Una por delegación** (hasta 27) | El equipo de la delegación de centro | El **correo institucional de la delegación** (p. ej. `delegacionetsii@us.es`) | Delegado de centro | Desde la cuenta `cadus` (Usuarios › Añadir nuevo) o con [`aplicar_usuarios.php`](aplicar_usuarios.php) |

- La Ejecutiva no tiene cuentas personales: entra siempre con `cadus`, que responde a un único correo (`dcadus@us.es`). WordPress no admite dos cuentas con el mismo correo, así que no hay una cuenta de «Ejecutivo del CADUS» aparte; ese rol existe para quien el CADUS quiera con permisos de contenido sin ser administrador.
- **Es la cuenta `cadus` la que da acceso a las delegaciones**: crea su cuenta y la asigna a su ficha.
- Cada delegación entra con su correo institucional y solo puede editar **su propia ficha** (RN-04).
- Hay **una sola cuenta por delegación**: el script rechaza una segunda cuenta para una ficha que ya tiene la suya.
- No se usan correos de alumno (`@alum.us.es`) para las delegaciones: son personales y cambian con cada delegado. El dominio `@alum.us.es` se sigue exigiendo a los **estudiantes** en el buzón (RN-02).

## Alta de la cuenta del CADUS

```bash
php scripts/roles/crear_cuenta_cadus.php
```

No guarda ni muestra contraseñas y no envía correo. La primera vez se entra con **«¿Has olvidado tu contraseña?»** y el usuario `cadus`: el enlace llega a `dcadus@us.es`.

## Alta de las delegaciones

1. Copiar [`usuarios-ejemplo.csv`](usuarios-ejemplo.csv) a `usuarios-reales.csv` y rellenar **una línea por delegación**: `usuario,nombre,correo,rol,delegacion`. Los correos del ejemplo son ilustrativos: hay que poner los que facilite el CADUS.
   - `usuario`: nombre de acceso sin espacios ni tildes (p. ej. `d-etsii`).
   - `nombre`: nombre visible (p. ej. `Delegación de Alumnos ETSII`).
   - `correo`: el **correo institucional de la delegación**. El script rechaza los correos de alumno (`@alum.us.es`) para este rol.
   - `rol`: vacío equivale a `delegado`.
   - `delegacion`: título exacto de la ficha (p. ej. `Delegación de Facultad de Química`); si se deja vacío, se busca una ficha con el mismo título que `nombre`.

   `usuarios-reales.csv` está en `.gitignore`. Los correos de las delegaciones no son personales, pero la lista real la mantiene el CADUS y no hace falta subirla.
2. Ensayo en seco (no cambia nada, lista los problemas y los títulos de las fichas existentes):
   ```bash
   php scripts/roles/aplicar_usuarios.php
   ```
3. Aplicar los cambios (`--avisar` envía a cada delegación el enlace para elegir su contraseña; necesita correo saliente en el servidor):
   ```bash
   php scripts/roles/aplicar_usuarios.php --aplicar --avisar
   ```
4. Comprobar con una cuenta de delegación el menú y los permisos (HU-19c).

## Relevo (cambio de equipo)

La cuenta **no se borra ni se crea de nuevo**: pasa al equipo entrante con una contraseña nueva. Así la ficha, las entradas y el historial siguen en la misma cuenta.

- **Delegación**: el delegado saliente o cualquier miembro de la Ejecutiva, con efecto inmediato:
  1. El equipo nuevo pulsa **«¿Has olvidado tu contraseña?»** con el usuario de la delegación (el enlace llega al correo de la delegación), o la Ejecutiva pone una contraseña nueva desde **Usuarios › Editar**.
  2. En la misma pantalla, **«Cerrar la sesión en todas partes»**, para que el equipo anterior pierda el acceso al momento.
  3. Si cambia quién gestiona el buzón de la delegación, el CADUS lo tramita con la US; la cuenta de la web no cambia.
- **Ejecutiva**: igual, con el usuario `cadus`; el enlace llega a `dcadus@us.es`, al que ya tiene acceso el equipo nuevo.

La función para que el delegado saliente haga el relevo desde su propio perfil, limitado a su delegación, es la HU-22 (Sprint 3).

## Garantías

- Las contraseñas no se guardan ni se muestran: se genera una aleatoria que nadie ve y cada titular elige la suya con el enlace de «contraseña olvidada».
- El script de delegaciones no toca las cuentas de administrador, rechaza usuarios o correos repetidos, rechaza una segunda cuenta para la misma delegación y no deja actualizar una cuenta distinta de la indicada.
- Una delegación queda como **autora** de su ficha, que es lo que le permite editarla y nada más (RN-04).
