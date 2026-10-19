# Cuentas reales y roles (E2-01)

Hoy las cinco cuentas del WordPress (`root`, `alvaro`, `joaquin`, `marcos`, `Miguel`) son administradoras: son las del equipo. Los usuarios del CADUS (Ejecutivo y delegados) todavía no existen. Este script los da de alta con el rol correcto.

## Procedimiento

1. **Miguel Ángel** consigue del CADUS la lista de personas y rellena [`usuarios-reales.csv`](usuarios-reales.csv): `usuario,nombre,correo,rol,delegacion`.
   - `rol`: `ejecutivo`, `delegado` o `estudiante`.
   - `delegacion`: solo para delegados, con el **título exacto** de la delegación (p. ej. `Delegación de Facultad de Derecho`).
2. **Pablo** ejecuta primero el ensayo en seco (no cambia nada, muestra lo que haría y los errores):
   ```bash
   php scripts/roles/aplicar_usuarios.php
   ```
3. Si todo es correcto, aplica los cambios (`--avisar` envía a cada persona el enlace para elegir su contraseña; necesita correo saliente configurado en el servidor):
   ```bash
   php scripts/roles/aplicar_usuarios.php --aplicar --avisar
   ```
4. Comprobar con cada rol el menú y los permisos (HU-19c) y, al cerrar el sprint, decidir qué cuentas de administrador del equipo se conservan.

## Garantías

- Las contraseñas no se guardan ni se muestran: se genera una aleatoria que nadie ve y cada persona la cambia con el enlace de «contraseña olvidada».
- No toca cuentas de administrador.
- Un delegado queda como **autor** de su delegación, que es lo que le permite editarla y nada más (RN-04).
- El CSV con datos personales reales **no debe subirse a Git**: se rellena en local y se borra después (el repositorio solo conserva la cabecera).
