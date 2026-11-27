# E2-12 · Fichas reales de delegaciones y edición restringida (RN-04)

Ejecutado el 25/11/2026 por Claude en nombre de Pablo (no es prueba de otra persona), con `scripts/pruebas/e2_12_edicion_delegado.php` sobre el WordPress local (cuentas `test-delegado` y `test-ejecutivo`).

## Fichas

Las 27 delegaciones están publicadas con los datos que publica www.cadus.us.es. Lo que falta no lo da esa web:

| Dato | Fichas sin él |
|---|---|
| Miembros | 0 |
| Correo | 1 (Escuela Internacional de Doctorado) |
| Teléfono | 7 (Odontología, Química, Escuela Internacional de Doctorado, Escuela Internacional de Posgrado, Escuela Politécnica Superior, Ingeniería de Edificación y Psicología) |
| Horario | 27: la web del CADUS no lo publica |

Las fichas de Química, Física, Biología y ETSI, que figuraban como pendientes, ya tienen correo y miembros (Física, Biología y ETSI también teléfono; a Química le falta el teléfono).

## Edición restringida

| Caso | Resultado esperado | Resultado |
|---|---|---|
| Delegado sin ficha asignada intenta editar | No edita ninguna de las 27 | OK: 0 de 27 |
| Delegado con una ficha asignada | Edita solo esa | OK: solo la 327 |
| Delegado borra su propia ficha | No puede | OK: no puede |
| Ejecutiva edita una ficha ajena | Puede (decisión X7 del 12/11) | OK |

En aquella ejecución el script asignó una ficha al delegado de prueba para el caso positivo y la devolvió a su autor original (se leyó el autor después). La versión actual del script lo verifica, termina con error si alguna expectativa falla y se niega a empezar si el delegado ya es autor de alguna ficha. El mismo día se le asignó la ficha 32 (ETSII) para la prueba de HU-22; hay que devolverla a su autor original (usuario 1) antes del volcado.

## Qué no cubre

El horario y los teléfonos que faltan solo los puede dar el CADUS. La prueba de HU-22 (relevo de la cuenta con dos navegadores) sigue siendo de Álvaro.
