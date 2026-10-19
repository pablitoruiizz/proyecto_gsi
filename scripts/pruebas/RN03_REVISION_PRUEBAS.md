# Revisión de la batería independiente de Claude

Revisada por Codex el 19/10/2026, sin modificar `privacidad_tickets.py` ni `ticket_prueba.php` para conservar su independencia.

Comando ejecutado antes de las correcciones: `python scripts/pruebas/privacidad_tickets.py`. Resultado: **35 correctas y 4 fallos**, ticket ID 55 eliminado por `finally`.

1. **Importante: falsos positivos en búsquedas.** `sin_fugas()` busca en todo el HTML los mismos valores enviados como `s`. WordPress refleja legítimamente la consulta en el título y el campo de búsqueda. Fallaron `?s=TEXTO-SECRETO-RN03`, el mismo con `post_type`, `?s=CAD-2026-99999` y `?s=prueba%40alum.us.es`; ese resultado no prueba una lectura de la BD. Buscar un prefijo y comprobar un marcador distinto del ticket, o limitar la comprobación a los resultados. La batería propia usa `s=RN03-CODEX` y detecta asunto/texto/código completos, no el término reflejado.
2. **Importante: falta el flujo de Fluent Forms.** Crear el post directamente no prueba duplicación en `submissions`, `entry_details`, `submission_meta`, feeds, correos ni confirmación del formulario. La batería propia llama al servicio real de envío y observa las consultas INSERT/UPDATE; una cuenta SQL cero solo pasa si no hay error SQL.
3. **Importante: capacidades no equivalen a acceso HTTP.** Los `WP_User` sintéticos son útiles pero no verifican `edit.php`, `post.php`, REST con nonce/cookie ni el comportamiento público de una Ejecutiva autenticada. La batería propia añade estas rutas, con dos cuentas distintas de Ejecutiva.
4. **Importante: caché.** Una única respuesta con `no-cache` no demuestra ausencia de un fichero que WP Fastest Cache pueda servir después. La prueba real encontró precisamente ese problema. Añadir GET/POST/GET, exigir `no-store` y comprobar que no se crea el HTML de seguimiento.
5. **Menor: estados y casos inconclusos.** `estado != 200` acepta un 500 como éxito; debe exigir 403/404. `SIN CONCLUIR` no altera el código de salida: conviene distinguirlo de un pase completo, especialmente si falta el nonce o se agota el límite. El helper debe propagar su código de salida y la limpieza debe comprobar contadores, no solo imprimir `borrados`.
6. **Menor: datos de prueba y aislamiento.** El código fijo `CAD-2026-99999` y borrar por ese código pueden colisionar con otra ejecución. Añadir una marca de propiedad única, guardia CLI y limpieza de recursos asociados. La batería nueva también es secuencial por diseño: no debe ejecutarse a la vez que otra que exija cero tickets.

Cobertura adicional recomendable: permalink real, adjunto con padre ticket, tipos/metadatos REST, sitemap de Yoast (activo; el sitemap nativo devuelve 404), correo incorrecto frente a código inexistente con respuesta idéntica, undécimo intento, código aleatorio nuevo y código anterior. Se cubren en `rn03_auditoria.php`/`rn03_http.py` salvo ficheros binarios privados, que no forman parte del formulario actual.

Pendiente: revisión de estas correcciones por Claude. No se da por realizada sin su respuesta.
