# Área CMS WordPress

Esta carpeta agrupa artefactos del CMS:

- `backup-db/`: referencias y plantillas de respaldo de base de datos (sin dumps reales).
- `themes/`: temas personalizados o configuraciones del tema.
- `plugins/`: plugins propios/configurados y documentación de uso.
- `config/`: configuraciones de entorno mediante plantillas seguras.

## Buenas prácticas
- No subir `wp-config.php` real ni credenciales.
- Versionar solo ejemplos sanitizados y documentación técnica.

## Restaurar la base de datos tras `git pull`

Cada miembro del equipo trabaja con MySQL local (XAMPP), por lo que la base de datos **no se versiona en Git**: solo el volcado `.sql` en `backup-db/` (ver excepción `!**/*-template.sql` / `!**/*-example.sql` del `.gitignore` raíz para plantillas; los dumps reales del equipo se comparten según acuerdo interno, no necesariamente en el repo).

1. Hacer `git pull` para obtener el último volcado disponible en `cms-wordpress/backup-db/`.
2. Abrir XAMPP y arrancar **Apache** y **MySQL** desde el panel de control.
3. Abrir phpMyAdmin en `http://localhost/phpmyadmin`.
4. Si es la primera vez, crear la base de datos local (por ejemplo `gsi_cadus_local`) con cotejamiento `utf8mb4_unicode_ci`.
5. Importar el volcado:
   - **Desde phpMyAdmin:** seleccionar la base de datos → pestaña *Importar* → elegir el archivo `.sql` de `cms-wordpress/backup-db/` → *Continuar*.
   - **Desde línea de comandos** (con XAMPP en el `PATH` o desde `C:\xampp\mysql\bin`):
     ```bash
     mysql -u root -p gsi_cadus_local < cms-wordpress/backup-db/<nombre-del-volcado>.sql
     ```
6. Comprobar/ajustar `wp-config.php` local (no versionado) con el nombre de BD, usuario y contraseña locales.
7. Acceder a `http://localhost/<carpeta-wordpress>/wp-admin` y verificar que el contenido importado se ve correctamente.

> [!IMPORTANT]
> Antes de subir cambios de BD, exportar un volcado actualizado a `backup-db/` (sin datos sensibles de usuarios reales) y avisar al equipo para que reimporten tras el siguiente `git pull`.
