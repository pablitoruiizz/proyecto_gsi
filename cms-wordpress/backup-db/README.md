# Gestión de la base de datos — `backup-db/`

El portal usa **una única base de datos `bd_cadus`**, alojada en el servidor compartido (WampServer en el equipo anfitrión) y accesible para todo el equipo mediante Tailscale. Ver [entorno de trabajo](../../docs/arquitectura/entorno-de-trabajo.md).

Por eso **no hace falta que cada integrante importe un volcado para trabajar**: todos editan la misma base de datos desde el panel de WordPress. Los archivos `.sql` de esta carpeta sirven como:

- **Copia de seguridad** antes de cambios grandes o de instalar plugins.
- **Punto de entrega** de cada sprint.
- **Recuperación** si el servidor falla o hay que montar uno nuevo.

> [!WARNING]
> Los volcados de esta carpeta se versionan en Git (excepción `!cms-wordpress/backup-db/*.sql` del `.gitignore`). Cada volcado queda para siempre en el historial: subir solo los necesarios y revisar antes que no contengan datos personales reales de estudiantes.

## 1. Exportar la base de datos desde phpMyAdmin

Se hace en el equipo anfitrión (o por quien tenga acceso a su phpMyAdmin):

1. Con Wamp en marcha, abrir `http://localhost/phpmyadmin`.
2. Seleccionar la base de datos `bd_cadus` en el panel izquierdo.
3. Pestaña **Exportar** → método **Rápido**, formato **SQL** → **Continuar**.
4. Guardar el archivo descargado en esta carpeta (`cms-wordpress/backup-db/`).

## 2. Nombrar el volcado con control de versiones

```
bd_cadus_v<version>_sprint<NN>.sql
```

Ejemplos: `bd_cadus_v1_sprint1.sql`, `bd_cadus_v2_sprint1.sql`, `bd_cadus_v1_sprint2.sql`.

- Incrementar `<version>` en cada nuevo volcado del mismo sprint.
- No sobrescribir volcados anteriores hasta cerrar el sprint.
- Subir solo los volcados que se quieran conservar (backup relevante o entrega), no uno por cada cambio.

## 3. Subir un volcado a GitHub

```bash
git pull
git add cms-wordpress/backup-db/bd_cadus_v1_sprint1.sql
git commit -m "chore(cms): backup de bd_cadus v1 sprint1"
git push
```

Hacer `git pull` antes evita que dos personas suban volcados a la vez.

## 4. Restaurar un volcado (recuperación o servidor nuevo)

1. Con Wamp en marcha, abrir phpMyAdmin.
2. Crear la base de datos `bd_cadus` con cotejamiento `utf8mb4_unicode_ci` (o vaciarla si ya existe).
3. Pestaña **Importar** → elegir el `.sql` → **Continuar**.
4. Comprobar que `wp-config.php` apunta a `bd_cadus` y que la web carga.

Para el procedimiento general del entorno, ver [`cms-wordpress/README.md`](../README.md).
