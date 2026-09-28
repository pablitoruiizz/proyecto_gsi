# Maquetas / Mockups

Guardar en esta carpeta maquetas de interfaz y prototipos de baja/alta fidelidad del portal CADUS.

## Pantallas clave a incluir

| Pantalla | Contenido mínimo a maquetar | Historia(s) relacionada(s) |
|---|---|---|
| **Portada / Home** | Banner institucional, listado de comunicados por categoría, acceso al directorio y al buzón. | HU-01, HU-02, HU-18 |
| **Directorio de Delegaciones** | Listado agrupado por Facultad/Escuela y ficha de delegación (contacto, horario). | HU-05, HU-06 |
| **Buzón de Consultas** | Formulario de envío de consulta/reclamación y pantalla de seguimiento por código de ticket. | HU-07, HU-08 |
| **Ficha de Acta/Normativa** | Detalle del documento (tipo, fecha, estado) y descarga en PDF. | HU-03, HU-04 |

## Convenciones
- Nombrar archivos por módulo y pantalla: `modulo-pantalla-version.ext` (p. ej. `portada-home-v1.png`, `directorio-ficha-delegacion-v1.svg`).
- Incluir versión y fecha en el documento asociado.
- Añadir breve contexto en Markdown cuando sea necesario (decisión de UX, alternativa descartada, feedback del cliente).

## Cómo incorporar los bocetos

1. Guardar el archivo de la maqueta dentro de `docs/maquetas/img/` (crear la subcarpeta si no existe).
2. Formatos recomendados: **PNG o SVG** para bocetos y capturas; PDF solo para entregables finales consolidados.
3. Referenciar la imagen desde un documento Markdown de esta carpeta (o desde el `README.md` de la pantalla correspondiente), por ejemplo:
   ```markdown
   ![Portada Home v1](img/portada-home-v1.png)
   ```
4. Indicar junto a la imagen: pantalla que representa, versión, fecha y responsable.

## Formatos recomendados
- `.png`, `.jpg`, `.svg` (ligeros, en `img/`)
- `.pdf` (entregables consolidados)
- `.md` (descripción y decisiones de UX)

> Evitar incluir datos reales del cliente o de estudiantes en capturas.
