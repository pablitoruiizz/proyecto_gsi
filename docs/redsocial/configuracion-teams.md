# Configuración de la red social en Teams (piloto) · guía para Marcos

Estado a 16/11/2026. Lo hecho por Pablo (con Claude) en el tenant de la US, con la cuenta de Pablo:

| Equipo | Privacidad | Propietarios (desde el 20/11) |
|---|---|---|
| CADUS · Ejecutiva | privado | Pablo Ruiz Vidal, Marcos (`mardelrod2@alum.us.es`), Joaquín (`joaluncan@alum.us.es`) y Álvaro (`alvmaroca@alum.us.es`) |
| CADUS · Delegaciones | privado | los mismos cuatro |
| CADUS · Asamblea | privado | los mismos cuatro |

Los tres se invitaron el 16/11 como miembros y el 20/11 se pasaron a **propietarios**, para que los cuatro puedan configurar los equipos. Ninguno es ya «solo miembro»: la prueba de que una delegación solo ve su canal (RN-R02) necesita una cuenta que sea solo miembro (por ejemplo, volver a poner a uno como miembro durante la prueba, o una cuenta de ejemplo). El CADUS real no tiene aún cuentas de delegación en Teams. Cada equipo se creó con la plantilla «Equipo básico» (solo el canal General) y no tiene más configuración todavía.

## Qué falta (R-05, Marcos y Pablo) y qué debe verse al final

Cada paso lleva el requisito del REM (`docs/redsocial/rem-remus/carga-remus.md`) y la captura que lo demuestra (R-07).

### CADUS · Ejecutiva (RF-R02)
1. Añadir el canal estándar **«Preparación de avisos»**. *Se ve:* dos canales (General y Preparación de avisos).
2. Comprobar en «Administrar equipo > Miembros» que solo están Pablo y los tres invitados. *Captura:* lista de miembros.

### CADUS · Delegaciones (RF-R03, RF-R05, RN-R01, RN-R02)
3. **Avisos:** en el canal General, «Administrar canal» (`···`) > «Moderación» > activar la moderación y dejar que **solo los propietarios** publiquen y respondan. *Se ve:* un miembro no puede iniciar una conversación en General. *Captura:* ajuste de moderación y la vista de un miembro.
4. Renombrar el canal General a **«Avisos»** si Teams lo permite (si no, anotarlo en el documento: General hace de Avisos).
5. Crear tres **canales privados** de ejemplo, uno por delegación: **«Delegación · ETSII»** (con Álvaro), **«Delegación · Derecho»** (con Marcos) y **«Delegación · Biología»** (con Joaquín). Pablo es propietario de los tres. *Se ve:* cada miembro solo ve su canal privado y el canal General; los otros canales privados no aparecen en su lista. *Captura:* la vista de un miembro (para esta prueba hace falta iniciar sesión con esa cuenta o pedírsela a esa persona).
6. Anotar en el documento que el patrón se repite para las 27 delegaciones (no se crean las 27 en el piloto). Los tres equipos no se justifican por un límite de canales (no comprobado en el tenant) sino por la separación de miembros, permisos y herramientas.

### CADUS · Asamblea (RF-R04, RF-R08, RF-R09)
7. Añadir el canal estándar **«Cursos»**. *Se ve:* General y Cursos.
8. En el canal General, añadir la pestaña **Calendario** (si la ofrece el tenant) y crear un evento de ejemplo, «Asamblea de noviembre (ejemplo)». *Captura:* el calendario con el evento.

### Herramientas (RF-R07 · R-06 Joaquín)
9. En los canales de delegación y en Asamblea, pestaña **Archivos** y, en uno de ellos, enlazar el sitio de SharePoint del DMS que corresponda (por ejemplo, `cadus-organos-de-gobierno`); no subir documentos reales. *Captura:* la pestaña con el enlace al DMS (RN-R03).
10. Pestaña **Planner** en cada equipo, con el plan «Preparación de la asamblea» (cubos: Por hacer, En curso, Hecho) y tres tareas de ejemplo asignadas a distintas personas (Joaquín). *Captura:* el tablero.
11. Pestaña **Forms** con un formulario «Confirmación de asistencia» de ejemplo (RF-R10), solo si el tenant lo permite.

## Reglas para hacerlo
- Solo datos de ejemplo; no se pega nada de reclamaciones, mediaciones ni votaciones (RNF-R01).
- Todo lo que el tenant **no** permita (una pestaña, la moderación, un límite) se anota con su mensaje de error, porque RC-R02 lo prevé y es contenido válido de la entrega.
- Cada captura lleva un pie que diga qué requisito demuestra. Se guardan en `docs/redsocial/capturas/` con nombre `NN-descripcion.jpg`.
- Quien prueba una cuenta distinta (pasos 3 y 5) lo anota en `docs/redsocial/pruebas.md` con fecha, persona y resultado.
