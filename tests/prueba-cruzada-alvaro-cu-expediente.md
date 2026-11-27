# Prueba cruzada de Álvaro · CU-Expediente del DMS (CU-D04, CU-D05 y rol estudiante)

Reparto: [`docs/dms/reparto-version-definitiva.md`](../docs/dms/reparto-version-definitiva.md), apartado «Pruebas cruzadas (nadie prueba lo suyo)». El caso de uso es de Marcos ([`CU-Expediente.md`](../docs/dms/casos-de-uso/CU-Expediente.md)), así que lo prueba Álvaro. El resultado completo está en el apartado 6 de ese documento; esta hoja lo resume.

> **Ejecución:** 27/11/2026, con la cuenta de la US de Álvaro en Chrome, sobre el sitio CADUS Atención al estudiante (`https://uses0.sharepoint.com/sites/cadus-atencion-al-estudiante`). La ejecutó Claude en nombre de Álvaro y a petición suya, con clics en la interfaz de SharePoint (no por la API).

| ID | Qué hacer | Resultado esperado | Resultado |
|---|---|---|---|
| CU-D04 | En Expedientes, crear el documento de ejemplo «CAD-2026-0002 (ejemplo, prueba cruzada).docx» (sin datos personales) y rellenar Código CAD-2026-0002, Tipo de documento Expediente, Estado Resuelto y Fecha de resolución 20/11/2026 | La Fecha de caducidad se calcula sola (resolución más 2 años) y el expediente no sale en «Caducados» | OK (27/11/2026, Álvaro con Claude): caducidad 20/11/2028 y no aparece en «Caducados». Mientras falta la Fecha de resolución, SharePoint avisa «Falta información obligatoria» y la caducidad sale 30/12/1901; se corrige al rellenarla |
| CU-D05 | En la vista «Caducados», eliminar MED-2024-0003 y quitarlo de la papelera del sitio y de la de segundo nivel | «Caducados» muestra MED-2024-0003; tras borrarlo de los tres sitios, la vista y la papelera de segundo nivel quedan vacías | OK (27/11/2026, Álvaro con Claude): todo como se esperaba. Quedaba en la papelera del sitio otra copia de MED-2024-0003 que Marcos eliminó el 12/11/2026; también se borró de las dos papeleras, que quedan vacías |
| Rol estudiante | Con una cuenta de estudiante, intentar abrir Expedientes, también con el enlace directo | No la ve | Pendiente: no hay cuenta con rol de estudiante; con la de Álvaro, integrante del sitio, no se puede comprobar |
