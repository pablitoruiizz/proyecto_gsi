# Eventos reales del calendario (E2-19)

1. Rellena [`eventos-reales.csv`](eventos-reales.csv), con una línea por evento, separando los campos con `;`:

   ```
   titulo;fecha;inicio;fin;lugar;categoria;descripcion
   Pleno ordinario del CADUS;20/11/2026;17:00;20:00;Pabellón de Uruguay;Asamblea;Orden del día en el acta
   ```

   - `fecha`: dd/mm/aaaa.
   - `inicio` y `fin`: hh:mm. Si los dejas vacíos, el evento es de todo el día.
   - `categoria`: `Asamblea` o `Curso` (E3-07). Solo los eventos de «Asambleas» admiten votaciones vinculadas (RN-05).
   - `lugar` y `descripcion` son opcionales. El lugar se crea solo si no existe.

   Solo van eventos públicos del CADUS, validados por la Ejecutiva. Nada de datos personales.
2. Haz un ensayo, que no cambia nada y comprueba fechas, horas y categorías:
   ```bash
   php scripts/eventos/cargar_eventos_reales.php
   ```
3. Guarda los eventos. Con `--retirar-ejemplos` se borran además los eventos y la votación de ejemplo:
   ```bash
   php scripts/eventos/cargar_eventos_reales.php --aplicar --retirar-ejemplos
   ```

Se puede volver a ejecutar: un evento con el mismo título y la misma fecha se actualiza, no se duplica. En un servidor sin terminal (solo SFTP), los eventos se crean a mano en **Eventos › Añadir nuevo**, marcando su categoría.
