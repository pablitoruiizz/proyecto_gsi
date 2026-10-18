# Requisitos REM/REMUS

Esta carpeta contiene la especificación y trazabilidad de requisitos del proyecto.

## Nomenclatura sugerida
- Requisitos funcionales: `RF-XXX`
- Requisitos no funcionales: `RNF-XXX`
- Historias de usuario: `HU-XXX`
- Casos/artefactos REM/REMUS: `REM-XXX` o `REMUS-XXX`

## Trazabilidad mínima
Cada requisito debe enlazarse con:
- historia(s) de usuario,
- sprint(s) donde se implementa,
- evidencia de validación (prueba, demo, acta).

## Archivos de esta carpeta
- [`REM-CADUS.md`](REM-CADUS.md): especificación de requisitos (actores, RF, RI, RN, RNF y restricciones RC).
- [`carga-remus.md`](carga-remus.md): contenido del `.rem` en forma legible. Se genera desde `scripts/remus/cadus_data.json`; no editar a mano.
- [`docs/remus/REM-CMS.rem`](../../remus/REM-CMS.rem): ejemplo de formato que debe seguir la entrega.
- [`CADUS.rem`](CADUS.rem): proyecto de REMUS generado con [`scripts/remus`](../../../scripts/remus/README.md). Es binario: lo edita una sola persona (Product Owner).

## Estructura recomendada
- `matriz-trazabilidad.md` (la trazabilidad inicial está en `carga-remus.md`, apartado 12)
- anexos por sprint o módulo
