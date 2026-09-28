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

Cada miembro del equipo trabaja con MySQL local (XAMPP) sobre la base de datos `bd_cadus`, que **no se versiona en Git** (regla `*.sql` del `.gitignore` raíz).

Guía completa de exportación, convención de nombres (`bd_cadus_v<version>_sprint<NN>.sql`) e importación sin conflictos: [`backup-db/README.md`](backup-db/README.md).
