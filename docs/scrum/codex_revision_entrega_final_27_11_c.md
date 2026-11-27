# Tercera revisión de la entrega final (27/11/2026, noche)

Revisión de SOLO LECTURA: no edites ni borres archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni WordPress, no ejecutes `scripts/dms/empaquetar_dms.py`, generadores de documentos, scripts PHP ni de Python que escriban, y no toques `cms-wordpress/.htaccess`. Puedes leer, buscar con grep y comprobar sintaxis; para leer los PDF usa `pdftotext` si está disponible o lee el `.md` equivalente. No muestres hashes, contraseñas ni correos reales. Responde en español, con hallazgos por gravedad (alta, media, baja), cada uno con archivo, el fallo concreto y cómo corregirlo, y termina diciendo si cada entrega se puede enviar y qué falta por hacer y a quién.

Hay **dos entregas distintas**, descomprimidas en `docs/dms/entrega/paquete/`:

- **Entrega A, el zip del 29/11/2026** (CMS + DMS + red social v2): `_revision_zip/Entrega-29-11-CADUS-CMS-DMS-RSI-v2/` (163 archivos).
- **Entrega B, los manuales** (extra, hasta el 14/12/2026, aparte del zip; «no es necesaria para la defensa»): `_revision_manuales/` (15 archivos: seis manuales en `.docx` y `.pdf`, el documento completo que los reúne y un `LEEME.md`).

Las dos revisiones anteriores (`docs/scrum/codex_revision_zip_27_11.md` y `_b.md`) están ya atendidas. Lo que ha cambiado desde la segunda: el volcado se regeneró; la retrospectiva consta como celebrada **según Pablo**; la prueba con NVDA consta como hecha **según Pablo** (sin registro paso a paso); la app de Power Apps consta como publicada **según Álvaro, y Marcos confirma de palabra que la tiene** (sin captura); T1 a T3 los cronometró Pablo (50, 10 y 18 s, límite 60 s) y no una persona externa; la prueba cruzada de HU-22 la repitió Claude en nombre de Pablo (13 comprobaciones, `scripts/pruebas/hu22_relevo.py`) y la de HU-14b y HU-16a la hizo Joaquín; P5 (envío real de correo) quedó OK; E3-04 cuenta ahora 43 casos, todos OK.

## Qué hay que comprobar en la entrega A

1. **Coherencia de los números y los estados** en todo el zip (`LEEME.md`, `CMS/Entrega-final-CMS-CADUS.pdf` secciones 7, 9 y 10, `CMS/seguimiento/E3-04-pruebas-de-aceptacion.md`, `CMS/ACTUALIZACION-22-11-estado-del-cms.md`, `CMS/seguimiento/sprint-03.md`, `CMS/seguimiento/product-backlog.md`, `RSI/Entrega-RSI-CADUS.pdf` y `RSI/seguimiento/`). Busca con grep restos de estados antiguos: «40 OK», «3 parciales», «T1 a T3» como pendiente, «NVDA sin probar» o «NVDA no», «sin publicar», «falta la prueba cruzada», «P5 parcial», «retrospectiva pendiente» o «estado a 26/11». Lo que sea un registro histórico fechado (por ejemplo la tabla del 22/11) no es un fallo; sí lo es una frase que hoy sea falsa o que se contradiga con otra.
2. **Que nada se presente más hecho de lo que está.** Cada afirmación basada en la palabra de una persona («según Pablo», «según Álvaro») debe decirlo; T1 a T3 deben decir que los midió quien conoce el portal; HU-22 no debe figurar como prueba de otra persona; no debe haber capturas citadas que no existan.
3. **Volcado** `CMS/bd_cadus_v1_sprint3.sql` y `CMS/LEEME-volcado.md`: copia saneada con tres cuentas `demo-*`. Busca con grep (sin mostrar valores) hashes de contraseña que no sean los de esas tres cuentas, proveedores de correo personales, `session_tokens`, claves de Wordfence, registros de acceso, rutas locales (`C:\Users`, `OneDrive`), la IP de Tailscale, usuarios reales (`root`, `alvaro`, `joaquin`, `marcos`, `Miguel`), cuentas de prueba (`test-estudiante`, `test-delegado`, `test-ejecutivo`), tickets y datos de visitantes. Es normal que haya correos genéricos `@alum.us.es` en textos del sitio y correos institucionales `@us.es` de delegaciones. Comprueba que el `LEEME-volcado.md` describe con verdad lo que hay en el `.sql` y que el documento final del CMS, el `LEEME.md` y el `LEEME-volcado.md` no se contradicen.
4. **Enlaces relativos de los `.md`**: ninguno roto (resuelve cada `[texto](ruta)` e imagen relativa desde la carpeta de su archivo).
5. **El zip contiene** lo que pide el enunciado del DMS y de la red social (REM, UML de análisis y diseño, casos de uso, capturas, seguimiento SCRUM, caso de negocio) y los `.docx` tienen su `.pdf` actualizado (comprueba que el texto del `.pdf` y el del `.md` o `.docx` de origen no se contradicen en los puntos del apartado 1).
6. **Secretos**: ninguna contraseña, clave de aplicación, token ni la contraseña de demostración en claro en ningún archivo del zip (la de demostración vive solo en el zip dentro de `CMS/LEEME-volcado.md`; si aparece en otro sitio, es un fallo).

## Qué hay que comprobar en la entrega B (manuales)

1. **Que cada manual se corresponde con el sistema y es usable**: usuario y administrador de CMS, DMS y RSI. Pasos numerados, nombres de menús y rutas que existan (compáralos con el código en `cms-wordpress/wp-content/plugins/cadus-portal/` y con `docs/`), capturas que se vean y estén en su sitio, sin texto en inglés suelto ni restos de plantilla.
2. **El documento completo** (`Manuales-CADUS-completo.pdf`): portada, índice con números de página correctos, referencias cruzadas entre manuales que lleven al apartado correcto, anexo de límites conocidos (D) coherente con la entrega A (mismas fechas y mismos «según Pablo» / «según Álvaro»). El PDF debe tener marcadores.
3. **Los seis PDF sueltos y el documento completo dicen lo mismo** en los puntos de estado (NVDA, Power Apps, correo, T1 a T3, cuentas reales, despliegue).
4. **Ninguna credencial** ni dato personal real en los manuales (se permiten correos institucionales genéricos y las cuentas `demo-*` sin contraseña).
5. Que el `LEEME.md` de la entrega B describa con verdad su contenido.

## Lo que SÍ puede seguir como pendiente declarado (no es un fallo si está dicho con claridad)

El despliegue en la Universidad de Sevilla; las pruebas con cuentas reales de delegado y de estudiante; el rol estudiante en CU-Expediente del DMS; T1 a T3 con una persona externa y en móvil; la prueba cruzada de HU-22 por otra persona; NVDA sin registro paso a paso; la app de Power Apps sin captura ni integración en Teams. Lo imprescindible es que no se presenten como hechos más allá de lo que se sabe.

Termina con una lista corta y ordenada: qué corregir antes de enviar la entrega A y qué antes de enviar la entrega B.
