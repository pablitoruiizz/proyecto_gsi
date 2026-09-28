# Gestión de la base de datos — `backup-db/`

Esta carpeta contiene los volcados (`.sql`) de la base de datos `bd_cadus` usados para sincronizar el entorno local de WordPress entre los 5 integrantes del equipo.

> [!WARNING]
> Los archivos `.sql` están excluidos por `.gitignore` (regla `*.sql` en la raíz). Esto es intencionado: los volcados pueden pesar varios MB y no deben acumularse en el historial de Git. Compartir los volcados por el canal acordado del equipo (Teams) y dejar en el repositorio solo esta guía y, si se acuerda explícitamente, plantillas de ejemplo (`*-template.sql`, `*-example.sql`).

## 1. Exportar la base de datos desde phpMyAdmin

1. Abrir XAMPP e iniciar **Apache** y **MySQL**.
2. Ir a `http://localhost/phpmyadmin`.
3. Seleccionar la base de datos `bd_cadus` en el panel izquierdo.
4. Ir a la pestaña **Exportar**.
5. Método: **Rápido** (o **Personalizado** si se necesita excluir tablas de caché/transients).
6. Formato: **SQL**.
7. Pulsar **Continuar** y guardar el archivo descargado en esta carpeta (`cms-wordpress/backup-db/`).

## 2. Nombrar el volcado con control de versiones

Usar la convención:

```
bd_cadus_v<version>_sprint<NN>.sql
```

Ejemplos:
- `bd_cadus_v1_sprint1.sql` — primer volcado estable del Sprint 1.
- `bd_cadus_v2_sprint1.sql` — segunda versión dentro del mismo sprint (tras corregir contenido).
- `bd_cadus_v1_sprint2.sql` — primer volcado del Sprint 2.

Reglas:
- Incrementar `<version>` cada vez que se comparta un nuevo volcado dentro del mismo sprint.
- No sobrescribir volcados anteriores: mantenerlos hasta el cierre del sprint por si hay que revertir.
- Indicar en el canal del equipo (Teams) qué volcado es el vigente ("volcado activo") para evitar trabajar sobre versiones desactualizadas.

## 3. Importar la base de datos localmente tras `git pull`

Para evitar conflictos, cada integrante mantiene **su propia instancia local** de MySQL; la base de datos nunca se fusiona vía Git, solo se reemplaza por el volcado más reciente:

1. Ejecutar `git pull` (los archivos `.md` de esta carpeta se actualizan; los `.sql` se comparten aparte, según el punto 1).
2. Con Apache y MySQL iniciados, abrir phpMyAdmin.
3. Si es la primera vez, crear la base de datos `bd_cadus` con cotejamiento `utf8mb4_unicode_ci`. Si ya existe, **vaciarla** antes de importar (pestaña *Operaciones* → *Eliminar la base de datos* → volver a crearla, o usar *Vaciar*) para evitar mezclar datos de versiones distintas.
4. Importar el volcado vigente:
   - **Desde phpMyAdmin:** seleccionar `bd_cadus` → pestaña *Importar* → elegir el archivo `.sql` más reciente → *Continuar*.
   - **Desde línea de comandos** (con `C:\xampp\mysql\bin` en el `PATH`):
     ```bash
     mysql -u root -p bd_cadus < cms-wordpress/backup-db/bd_cadus_v1_sprint1.sql
     ```
5. Verificar que `wp-config.php` local (no versionado) apunta a `bd_cadus` con el usuario/contraseña locales.
6. Acceder a `http://localhost/<carpeta-wordpress>/wp-admin` y comprobar que el contenido importado es correcto.

## 4. Antes de subir cambios propios

1. Exportar un volcado nuevo siguiendo la convención de nombres del punto 2.
2. Revisar que no contenga datos personales reales de estudiantes (usar siempre datos de prueba/anonimizados).
3. Compartirlo por el canal del equipo indicando qué volcado sustituye.
4. Avisar para que el resto reimporte antes de seguir trabajando sobre contenido de BD.

Para el procedimiento general de instalación del entorno (XAMPP + WordPress), ver [`cms-wordpress/README.md`](../README.md).
