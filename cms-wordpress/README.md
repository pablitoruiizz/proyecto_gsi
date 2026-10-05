# Área CMS WordPress

Esta carpeta agrupa artefactos del CMS:

- `backup-db/`: referencias y plantillas de respaldo de base de datos (sin dumps reales).
- `themes/`: temas personalizados o configuraciones del tema.
- `plugins/`: plugins propios/configurados y documentación de uso.
- `config/`: configuraciones de entorno mediante plantillas seguras.

## Buenas prácticas
- No subir `wp-config.php` real ni credenciales.
- Versionar solo ejemplos sanitizados y documentación técnica.

## Base de datos y entorno compartido

El equipo trabaja sobre **un único servidor** (WordPress + MySQL `bd_cadus` en WampServer) accesible por Tailscale, así que no hace falta importar la BD en cada equipo. Ver [entorno de trabajo](../docs/arquitectura/entorno-de-trabajo.md).

Los volcados `.sql` de `backup-db/` son copias de seguridad y de entrega. Guía de exportación, nombres (`bd_cadus_v<version>_sprint<NN>.sql`) y restauración: [`backup-db/README.md`](backup-db/README.md).
