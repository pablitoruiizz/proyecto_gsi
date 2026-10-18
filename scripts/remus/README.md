# Generador del proyecto REMUS (`CADUS.rem`)

`build_rem.ps1` crea `docs/requisitos/rem-remus/CADUS.rem` a partir de `cadus_data.json`, y genera también la hoja legible [`carga-remus.md`](../../docs/requisitos/rem-remus/carga-remus.md).

Un `.rem` es una base de datos de Access (Jet 4.0). El script la rellena con el proveedor `Microsoft.Jet.OLEDB.4.0`, que solo existe en **PowerShell de 32 bits** de Windows.

## Fuente de los datos
- **`cadus_data.json`**: única fuente de verdad (objetivos, requisitos de información, actores, interfaz, funcionales, casos de uso, no funcionales, reglas de negocio, entorno de trabajo y trazabilidad). Cada requisito lleva un código (`RF-01`, `RNF-03`…) que se escribe al inicio de su nombre en REMUS: es la etiqueta de trazabilidad que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación.
- **`REM-CMS.rem`** (`docs/remus/`): proyecto de ejemplo con el formato exigido. Se usa como base: se conserva su esqueleto de secciones y se sustituye su contenido.

## Cuándo usarlo
Mientras el `.rem` se mantenga desde el JSON. **Regenerar descarta cualquier cambio hecho a mano dentro de REMUS**, porque parte siempre del ejemplo. En cuanto el equipo empiece a editar el `.rem` directamente en REMUS, dejar de regenerarlo.

## Uso
Desde la raíz del repositorio:

```powershell
& "C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File scripts\remus\build_rem.ps1 -src docs\remus\REM-CMS.rem -dst docs\requisitos\rem-remus\CADUS.rem -data scripts\remus\cadus_data.json -md docs\requisitos\rem-remus\carga-remus.md
```

El script trabaja sobre una copia del origen y no lo modifica. Al terminar imprime cuántos objetos y trazas ha creado.

## Qué hace
- Conserva las secciones del ejemplo (Introducción, Participantes, Descripción del sistema actual, Objetivos, Catálogo de requisitos, Glosario) y añade la sección **Entorno de Trabajo del Equipo** (Tailscale, GitHub y Discord).
- Rellena versión, organizaciones, personas, párrafos y glosario.
- Inserta cada requisito en su sección, con importancia y urgencia, casos de uso con sus pasos, autores, fuentes y trazas.
- Los tiempos de vida y las ocurrencias de los requisitos de información quedan como PD (pendiente de definir).
