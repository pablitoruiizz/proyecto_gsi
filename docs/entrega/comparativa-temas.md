# Comparativa de temas de WordPress (E2-07)

**Responsable:** Joaquín Luna Canela · **Sprint 2** · **Sección del documento:** 5.3 Tema de WordPress · **Requisitos:** UI-01, RNF-02, RNF-03, RNF-05 · **Historias:** HU-18 (tema base), HU-15 (accesibilidad, Sprint 3)

Texto y tablas listos para pasar a la sección 5.3 del documento de la entrega. Los datos salen de `docs/entrega/datos/themes.json` (API pública de wordpress.org, consulta del 18/10/2026, la misma que las comparativas de plugins); la valoración se expresa sobre 5 (el valor de la API está sobre 100).

## Criterios

Los de la guía del proyecto, igual que en los plugins: fecha de la última actualización, instalaciones activas, valoración de los usuarios y número de valoraciones. Además, dos propios del proyecto: la etiqueta **«Accessibility ready»** de wordpress.org (RNF-03, HU-15) y la **versión mínima de PHP** frente al PHP 8.x del servidor (RNF-05).

## Tabla de temas

| Tema | Versión | Última actualización | Instalaciones activas | Valoración | Nº valoraciones | «Accessibility ready» | PHP mínimo | Decisión |
|---|---|---|---|---|---|---|---|---|
| Blocksy | 2.1.60 | 15/10/2026 | 300 k+ | 5,0/5 | 873 | Sí | PHP 7.0 | **Seleccionado** |
| Astra | 4.14.1 | 15/10/2026 | 1 M+ | 4,9/5 | 6.542 | No | PHP 5.3 | Descartado |
| Kadence | 1.5.2 | 24/07/2026 | 500 k+ | 4,9/5 | 455 | Sí | PHP 7.4 | Descartado |
| Neve | 4.2.16 | 07/10/2026 | 200 k+ | 4,7/5 | 1.283 | Sí | PHP 7.0 | Descartado |
| GeneratePress | 3.6.1 | 01/12/2025 | 500 k+ | 4,9/5 | 1.427 | No | PHP 7.4 | Descartado |

Se descartó Twenty Twenty-Five (tema por defecto de WordPress) como candidato: solo tiene 14 valoraciones (4,0/5), una base de uso demasiado pequeña para compararlo con el resto.

## Justificación

**Tema elegido: Blocksy** (versión 2.1.60, instalado y activo).

- **Valoración y mantenimiento.** Tiene la mejor valoración del grupo (5,0/5 en 873 valoraciones) y se actualizó el 15/10/2026, el mismo día que Astra y poco antes de la consulta. Un tema sin mantenimiento sería un riesgo para un portal que el CADUS debe mantener curso tras curso (RNF-07).
- **Accesibilidad (RNF-03).** Declara la etiqueta «Accessibility ready» (consta también en la cabecera de su `style.css`), igual que Kadence y Neve. Astra y GeneratePress no la incluyen entre las etiquetas que publica wordpress.org. La etiqueta no equivale a cumplir WCAG 2.1 AA: eso se verificará sobre el portal completo en el Sprint 3 (HU-15).
- **Identidad visual sin escribir CSS (UI-01, HU-18).** La paleta del CADUS (granate `#8d0739` y dorado `#faba09`, tomada de cadus.us.es), el logotipo y el menú se configuran desde el personalizador del tema.
- **Compatibilidad (RNF-05).** Requiere PHP 7.0 o superior, por debajo del PHP 8.x del servidor, y está probado hasta WordPress 7.1, la versión instalada.
- **Descartados.** *Astra* es el más instalado (1 M+), pero no declara la etiqueta de accesibilidad. *Kadence* la declara, pero su última actualización es del 24/07/2026, casi tres meses antes de la consulta, mientras que Blocksy y Astra se actualizaron pocos días antes. *Neve* tiene la valoración más baja del grupo (4,7/5). *GeneratePress* está bien valorado (4,9/5), pero no se actualiza desde el 01/12/2025 y tampoco declara la etiqueta de accesibilidad.

## Coste de cambiar de tema

El portal ya está construido sobre Blocksy: `includes/estilo.php` encola la hoja de estilos del CADUS detrás de la de Blocksy (`ct-main-styles`), y `includes/setup.php` aplica la paleta, el logotipo y el menú con los ajustes propios del tema y refresca su caché de CSS. Cambiar de tema obligaría a rehacer esa configuración y a volver a probar toda la portada (HU-01, HU-02, HU-18).

## Limitaciones asumidas

- Blocksy tiene menos instalaciones (300 k+) que Astra (1 M+), Kadence (500 k+) o GeneratePress (500 k+), por lo que hay menos tutoriales de terceros. Se compensa con su valoración, su mantenimiento y que la configuración queda documentada en el README del plugin.
- El aviso del tema sobre su plugin complementario (Blocksy Companion) es opcional y no se ha instalado: el portal no depende de él.
- La identidad visual definitiva (logotipo y colores) se confirmará con el CADUS; se aplicaría desde el personalizador sin cambiar de tema.

## Qué comprobar antes de entregar

- [ ] La versión instalada de Blocksy en el servidor coincide con la de la tabla (Apariencia › Temas).
- [ ] Si Pablo vuelve a consultar la API de wordpress.org antes de entregar, actualizar `themes.json` y esta tabla; en el documento, la fecha de consulta es `FECHA_DATOS` de `scripts/entrega/build_doc.py`.
- [ ] Captura de Apariencia › Temas con Blocksy activo, con pie «UI-01 · RNF-03 · HU-18».
