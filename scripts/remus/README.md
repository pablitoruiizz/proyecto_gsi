# Generador del proyecto REMUS (`CADUS.rem`)

`build_rem.ps1` crea `docs/requisitos/rem-remus/CADUS.rem` a partir de [`carga-remus.md`](../../docs/requisitos/rem-remus/carga-remus.md) y de `cadus_meta.json` (organizaciones, stakeholders y sección de cada requisito no funcional).

Un `.rem` es una base de datos de Access (Jet 4.0). El script la rellena con el proveedor `Microsoft.Jet.OLEDB.4.0`, que solo existe en **PowerShell de 32 bits** de Windows.

## Cuándo usarlo
Mientras el `.rem` se mantenga desde los documentos Markdown. **Regenerar descarta cualquier cambio hecho a mano dentro de REMUS**, porque parte siempre del proyecto de ejemplo. En cuanto el equipo empiece a editar el `.rem` directamente en REMUS, dejar de regenerarlo y usar este script solo como referencia.

## Uso
1. Descargar el proyecto base [`madeja.rem`](https://raw.githubusercontent.com/amador-duran-toro/remus/master/madeja/madeja.rem) del repositorio de REMUS (se usa por su esqueleto de documento de 75 secciones).
2. Ejecutar desde la raíz del repositorio:

```powershell
& "C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File scripts\remus\build_rem.ps1 -src RUTA\madeja.rem -dst docs\requisitos\rem-remus\CADUS.rem -md docs\requisitos\rem-remus\carga-remus.md -meta scripts\remus\cadus_meta.json
```

El script trabaja sobre una copia del origen y no lo modifica. Al terminar imprime cuántos objetos y trazas ha creado.

## Qué hace
- Elimina el contenido de ejemplo de Madeja (párrafos e imágenes del documento C, autores y fuentes).
- Actualiza nombre, versión (0.1) y fecha del proyecto, organizaciones y stakeholders.
- Inserta actores, objetivos, requisitos de información (con sus datos específicos), funcionales, no funcionales y restricciones (reglas de negocio y restricciones técnicas), cada uno en su sección del documento.
- Crea autores, fuentes y trazas según el apartado 9 de `carga-remus.md`.
- Los tiempos de vida y las ocurrencias de los requisitos de información quedan como PD (pendiente de definir).
