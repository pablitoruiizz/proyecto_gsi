# Entorno SharePoint del DMS

Tenant de la Universidad de Sevilla: `https://uses0.sharepoint.com`. Los sitios los creó Pablo el 26/10/2026 con la plantilla «Equipo estándar» (sitio de grupo, privado) y se configuraron el 30/10/2026 por la API REST de SharePoint desde su sesión.

| Sitio | Dirección | Bibliotecas |
|---|---|---|
| CADUS Documentación pública | https://uses0.sharepoint.com/sites/cadus-documentacion-publica | Normativa |
| CADUS Órganos de gobierno | https://uses0.sharepoint.com/sites/cadus-organos-de-gobierno | Actas, Votaciones, Plantillas |
| CADUS Atención al estudiante | https://uses0.sharepoint.com/sites/cadus-atencion-al-estudiante | Expedientes |

## Acceso

Cada sitio tiene 5 miembros: Pablo como propietario y, como miembros (grupo Integrantes, lectura y escritura), Joaquín Luna Canela, Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. Los tres grupos de permisos de cada sitio son los del Lab 4: Propietarios, Integrantes y Visitantes (vacío por ahora).

## Configuración

- **Normativa:** columnas Tipo de documento (obligatoria), Fecha, Curso académico y Estado; vista «Vigente».
- **Actas:** las mismas columnas más Asamblea; aprobación de contenido y borradores visibles solo para autor y aprobadores; vista «Aprobadas».
- **Votaciones:** columnas comunes más Número de votación, Tipo de voto y Resultado; permisos exclusivos (Propietarios e Integrantes; sin Visitantes).
- **Plantillas:** plantilla de acta y plantilla de registro de votación (27 filas).
- **Expedientes:** columnas comunes más Código, Facultad, Estado, Fecha de resolución (obligatoria) y Fecha de caducidad (calculada, resolución + 2 años); vista «Caducados»; permisos exclusivos (sin Visitantes).
- Documentos de ejemplo ficticios en todas las bibliotecas, sin datos personales ni DNI. **Corregido el 12/11/2026:** los de la carga del 30/10 pesaban 2 bytes (el contenido era `{}`, un fallo de la subida por la API) y no se abrían en Word en línea, en la vista previa ni descargados. Se sustituyeron por 8 Word válidos generados con `scripts/dms/generar_ejemplos_docx.py` (Normativa 3, Actas 2, Votaciones 2 y Expedientes 1), con el mismo nombre y metadatos; el acta aprobada conserva su estado y el borrador sigue en borrador. Quedan por sustituir los archivos que otros hayan subido con el mismo fallo (a 12/11, «Votacion 1 de la asamblea de noviembre.docx»).

## Pendiente

- Añadir la cuenta del CADUS (`dcadus@us.es`) como propietaria de los tres sitios.
- Añadir a los delegados y estudiantes como visitantes cuando existan sus cuentas, y probar con ellas que un delegado no ve borradores de actas, votaciones ni expedientes.
- Prueba cruzada de cada caso de uso por otra persona del equipo.
- Los miembros del equipo ven también Votaciones y Expedientes (Integrantes); mientras solo contengan documentos de ejemplo no hay datos personales reales.
