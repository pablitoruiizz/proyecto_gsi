# Pruebas de HU-11 · Convocatorias de votación vinculadas a una asamblea

**Requisitos:** RF-12, RN-05 · IR-07 · UI-02 · **Código:** `cms-wordpress/wp-content/plugins/cadus-portal/includes/votaciones.php`
**Quién prueba:** una persona distinta de Joaquín (prueba cruzada). Anotar el resultado real en la última columna y abrir una issue por cada fallo.

## Puesta en marcha

1. Actualizar el repositorio y entrar en el panel de WordPress con un administrador. La primera vez se dan las capacidades del tipo al Ejecutivo y al administrador y se crea la página «Votaciones» (colgando de «Calendario» en el menú si existe).
2. Instalar y activar **YOP Poll** (Plugins › Añadir nuevo) y anotar la versión instalada para la tabla de plugins. Crear una encuesta de prueba y copiar su ID.
3. Con **The Events Calendar** activo (HU-10), crear una asamblea en Eventos. Si el equipo usa una categoría de eventos «asamblea» o «asambleas», ponérsela: entonces solo se ofrecen esas.
4. En **Votaciones › Añadir votación** rellenar título, descripción, asamblea, apertura, cierre e ID de la encuesta.

Se necesita un usuario con rol Ejecutivo, otro Delegado y otro Estudiante, y la caché de WP Fastest Cache activa.

## Casos

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| 1 | Con el Ejecutivo, crear una votación con asamblea y un periodo futuro; publicar. | Se publica y aparece en «Votaciones» como próxima. | |
| 2 | Crear otra **sin asamblea** y pulsar Publicar (RN-05). | Queda en borrador y sale el aviso «Debe vincularse a una asamblea…». | |
| 3 | Elegir asamblea y dejar el cierre vacío; publicar. | Borrador y aviso de apertura y cierre obligatorios. | |
| 4 | Poner un cierre anterior a la apertura; publicar. | Borrador y aviso «El cierre debe ser posterior a la apertura». | |
| 5 | Dejar una votación en borrador sin asamblea y pasarla a «Publicada» con **edición rápida** desde el listado. | Vuelve a borrador (RN-05 no depende del formulario). | |
| 6 | Intentar vincular una asamblea que está en borrador o en la papelera. | No aparece en el selector; si se fuerza, la votación no se publica. | |
| 7 | Votación abierta (apertura pasada, cierre futuro): abrir su página sin iniciar sesión. | Ficha con estado «Abierta», asamblea y papeleta de YOP Poll. | |
| 8 | Votar y volver a votar desde el mismo navegador. | El primer voto se registra; el segundo se impide según la configuración de YOP Poll. | |
| 9 | Votación con apertura futura: abrir su página. | Estado «Próxima», fecha de apertura y **sin papeleta**. | |
| 10 | Votación con cierre pasado: abrir su página. | Estado «Cerrada», aviso de cierre y **sin papeleta**. | |
| 11 | Votación abierta **sin ID de encuesta**. | Aviso de que la papeleta no está disponible; sin errores de PHP. | |
| 12 | Página «Votaciones» con una abierta, una próxima y una cerrada. | Tres grupos con su título; cada tarjeta con asamblea, periodo y botón «Ver votación». | |
| 13 | Con la caché activa, crear una votación que abra en 2–3 minutos y refrescar la ficha y la lista. | La fase cambia de próxima a abierta sin vaciar la caché a mano. | |
| 14 | Portada sin votaciones abiertas ni próximas. | No aparece ningún bloque vacío. | |
| 15 | Portada tras publicar una votación abierta (sin vaciar la caché a mano). | Aparece «Participa en las votaciones» justo después de «¡Últimos eventos!». | |
| 16 | Abrir la ficha de la asamblea en el calendario. | Muestra «Votaciones de esta asamblea» con un enlace a cada votación. | |
| 17 | Con el Delegado y con el Estudiante, abrir `wp-admin/edit.php?post_type=cadus_votacion`. | Sin acceso y sin entrada «Votaciones» en el menú. | |
| 18 | Con el Ejecutivo: menú y barra superior. | Aparecen «Votaciones» y «Nuevo › Votación»; no aparecen menús que no le corresponden (HU-19a). | |
| 19 | Pedir `/wp-json/wp/v2/cadus_votacion`. | La ruta no existe (404). | |
| 20 | Desactivar The Events Calendar y abrir el formulario de una votación nueva; reactivarlo después. | Aparece el modo provisional (título y fecha de la asamblea a mano). | |
| 21 | Mover a la papelera una votación publicada. | Desaparece de la lista, de la portada y de la ficha de la asamblea. | |
| 22 | Página «Votaciones» en móvil (unos 390 px). | Tarjetas en una columna, sin desbordes. | |

## Comprobaciones finales

- Sin avisos de PHP en el registro (`wp-content/debug.log`, si `WP_DEBUG_LOG` está activo) ni en la consola del navegador.
- Sin votaciones ni encuestas de prueba en el volcado final de la base de datos.
- Si PHP está disponible en el equipo: `php -l cms-wordpress/wp-content/plugins/cadus-portal/includes/votaciones.php` sin errores.

## Capturas para la implementación (1920×1080, con pie y códigos RF-12 · RN-05 · HU-11)

A. Formulario de la votación con la asamblea del calendario y el periodo. · B. Intento de publicar sin asamblea: borrador y aviso. · C. Página «Votaciones» con una abierta y una próxima. · D. Votación abierta con la papeleta de YOP Poll. · E. Portada con «Participa en las votaciones». · F. Listado de plugins con YOP Poll activo.
