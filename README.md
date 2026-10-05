# Proyecto GSI — Implantación Incremental de Sistemas de Información

## 1) Descripción del proyecto
Repositorio base del proyecto universitario grupal de la asignatura **Gestión de Sistemas de Información (GSI)**.

El objetivo es implantar de forma incremental, siguiendo **SCRUM**, tres sistemas para una empresa/cliente real:
- **CMS en WordPress**
- **DMS en SharePoint**
- **Colaboración interna con Microsoft Teams, Planner, Power Automate y PowerApps**

## 2) Cliente / empresa real
- **Organización:** CADUS (Consejo de Alumnos de la Universidad de Sevilla)
- **Sector:** Educación Superior / Representación Estudiantil
- **Persona de contacto (rol):** Delegación General del CADUS (`cadus@us.es`)
- **Ubicación física:** Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla

> [!IMPORTANT]
> No publicar en este repositorio información confidencial del cliente (credenciales, datos personales, contratos, documentación sensible o dumps reales de producción).

## 3) Objetivos y alcance
### Objetivos
- Diseñar y desplegar un **CMS** funcional para contenido corporativo.
- Definir e implantar un **DMS** con estructura documental y control de permisos.
- Configurar un entorno de **trabajo colaborativo** en Microsoft 365.
- Gestionar requisitos y evolución del producto con artefactos SCRUM.

### Alcance inicial
- Estructura documental y técnica del proyecto.
- Backlog priorizado y planificación incremental por sprints.
- Trazabilidad entre requisitos (REM/REMUS), historias de usuario y entregables.

## 4) Sistemas y gestión de requisitos/SCRUM
1. **CMS (WordPress):** exportaciones de BD, temas, plugins, configuración.
2. **DMS (SharePoint):** estructura documental, metadatos, permisos.
3. **Colaboración (Microsoft 365):** Teams, Planner, Power Automate, PowerApps.
4. **Gestión de requisitos y SCRUM:** REM/REMUS, mockups, backlog, sprint backlog y burndown.

## 5) Equipo (5 integrantes)
> Completar y mantener actualizada esta tabla.

| Integrante | Nombre real | Usuario GitHub | Rol SCRUM / Área funcional |
|---|---|---|---|
| Miembro 1 | Pablo Ruiz Vidal | `@usuario1` | Product Owner & Dev Infraestructura (Configuración base, Tema, Git y BD) |
| Miembro 2 | Joaquin Luna Canela | `@usuario2` | Scrum Master & Dev Portada (Home, Comunicados y Banner) |
| Miembro 3 | Miguel Angel Camacho Martin | `@usuario3` | Dev — Sección Institucional y Normativa (Qué es CADUS, Gobierno, Estatutos y Actas) |
| Miembro 4 | Alvaro Martinez Ocaña | `@usuario4` | Dev — Directorio de Delegaciones de Alumnos (Facultades, Escuelas y Fichas) |
| Miembro 5 | Marcos-Paban Delgado Rodriguez | `@usuario5` | Dev — Atención al Estudiante y Buzón de Consultas (Formularios, Reclamaciones y FAQ) |

## 6) Arquitectura de directorios

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.md
│   │   ├── historia_usuario.md
│   │   └── tarea_documentacion.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── arquitectura/
│   ├── cliente/
│   ├── maquetas/
│   ├── requisitos/rem-remus/
│   └── scrum/
│       ├── backlog/
│       ├── burndown/
│       └── sprints/
├── cms-wordpress/
│   ├── backup-db/
│   ├── config/
│   ├── plugins/
│   └── themes/
├── dms-sharepoint/
│   ├── estructura-documental/
│   ├── metadatos/
│   └── permisos/
├── colaboracion-microsoft365/
│   ├── planner/
│   ├── power-automate/
│   ├── powerapps/
│   └── teams/
├── scripts/
└── tests/
```

### ¿Qué guardar en cada área?
- **`docs/cliente/`**: actas, alcance acordado, restricciones, decisiones funcionales (sin datos sensibles).
- **`docs/requisitos/rem-remus/`**: especificaciones REM/REMUS, trazabilidad, versiones.
- **`docs/maquetas/`**: mockups y convenciones de diseño.
- **`docs/arquitectura/`**: diagramas y decisiones técnicas.
- **`docs/scrum/`**: backlog de producto, backlog por sprint y burndown.
- **`cms-wordpress/`**: artefactos del CMS (sin dumps reales ni secretos).
- **`dms-sharepoint/`**: definición documental, metadatos y permisos del DMS.
- **`colaboracion-microsoft365/`**: configuración funcional de Teams/Planner/Automate/PowerApps.
- **`scripts/`**: scripts auxiliares de automatización/documentación.
- **`tests/`**: evidencias o pruebas automatizadas/manuales del proyecto.

## 7) Prerrequisitos
- Git 2.40+
- XAMPP (Apache + MySQL)
- WordPress (versión estable)
- Acceso Microsoft 365 para SharePoint/Teams/Planner/Power Platform
- Editor Markdown (VS Code recomendado)

## 8) Despliegue del CMS (WordPress + servidor local)

### Entorno compartido del equipo
El equipo trabaja sobre **un único servidor** (WampServer en el equipo de un integrante) con WordPress y la base de datos `bd_cadus`. El resto de integrantes accede mediante **Tailscale** (VPN privada) y trabaja a la vez sobre la misma instancia. El resto de archivos (tema, plugins, documentación, SCRUM, REM) se gestionan con **GitHub**. Detalle y pasos de conexión en [`docs/arquitectura/entorno-de-trabajo.md`](docs/arquitectura/entorno-de-trabajo.md).

### Instalación local desde cero (solo para montar un servidor nuevo)
1. Instalar XAMPP o WampServer e iniciar **Apache** y **MySQL**.
2. Crear una base de datos local (por ejemplo: `gsi_cms_local`) desde phpMyAdmin.
3. Copiar WordPress en el directorio web local (`htdocs`).
4. Configurar `wp-config.php` con:
   - nombre de BD,
   - usuario local,
   - contraseña local,
   - host (`localhost`).
5. Importar un dump de desarrollo **sanitizado** (si aplica) en la BD local.
6. Acceder a `http://localhost/<carpeta-wordpress>` y finalizar instalación.
7. Activar tema/plugins necesarios para el sprint.

> [!WARNING]
> No versionar credenciales reales, claves, ni dumps de producción. Solo plantillas, ejemplos anonimizados o documentación.

## 9) Guía general para SharePoint, Teams, Planner, Power Automate y PowerApps
- Documentar en cada subcarpeta:
  - objetivo funcional,
  - configuración aplicada,
  - permisos/roles,
  - evidencias (capturas o exportaciones ligeras sin datos sensibles),
  - dependencias con historias de usuario.
- Mantener trazabilidad con backlog y requisitos REM/REMUS.

## 10) Flujo de ramas Git
- `main`: versión estable y entregable.
- `develop`: integración continua del equipo.
- `feature/*`: nuevas funcionalidades.
- `bugfix/*`: correcciones.
- `docs/*`: cambios de documentación.
- `release/*`: preparación de entrega.

### Pull Requests y revisiones
1. Crear rama desde `develop`.
2. Commit con convención acordada.
3. Abrir PR con plantilla.
4. Revisiones cruzadas del equipo.
5. Merge cuando cumpla DoD y checklist de calidad.

## 11) Flujo SCRUM y Definition of Done (DoD)
### Flujo SCRUM
- Refinamiento del Product Backlog.
- Sprint Planning.
- Ejecución diaria y seguimiento.
- Sprint Review.
- Sprint Retrospective.

### Definition of Done (mínima)
- [ ] Criterios de aceptación cumplidos.
- [ ] Evidencia de prueba/documentación añadida.
- [ ] Trazabilidad actualizada (HU ↔ requisito ↔ artefacto).
- [ ] Revisión por al menos 1 integrante.
- [ ] Sin secretos ni datos sensibles en el repositorio.

## 12) Convenciones de commits
Formato sugerido:
- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
- `test: ...`

Ejemplo: `docs(scrum): actualizar sprint backlog sprint-02`

## 13) Seguridad y protección de datos
- No subir credenciales, tokens, certificados ni información personal real.
- Usar datos anonimizados en capturas y ejemplos.
- Revisar `.gitignore` antes de subir cambios.
- Limitar permisos por rol en SharePoint/Teams/WordPress según principio de mínimo privilegio.

## 14) Estado del proyecto y enlaces rápidos
- **Estado actual:** `Cierre de entrega del Sprint 1 (despliegue base, identidad institucional y portal CADUS V1)`
- **Backlog de producto:** [`docs/scrum/backlog/product-backlog.md`](docs/scrum/backlog/product-backlog.md)
- **Sprint 1:** [`docs/scrum/sprints/sprint-01.md`](docs/scrum/sprints/sprint-01.md)
- **Burndown:** [`docs/scrum/burndown/README.md`](docs/scrum/burndown/README.md)
- **Requisitos REM/REMUS:** [`docs/requisitos/rem-remus/REM-CADUS.md`](docs/requisitos/rem-remus/REM-CADUS.md)
- **Arquitectura / diagrama conceptual:** [`docs/arquitectura/diagrama-conceptual.md`](docs/arquitectura/diagrama-conceptual.md)
- **Maquetas:** [`docs/maquetas/README.md`](docs/maquetas/README.md)
- **Entorno de trabajo (Tailscale + GitHub):** [`docs/arquitectura/entorno-de-trabajo.md`](docs/arquitectura/entorno-de-trabajo.md)
- **Gestión de BD (`bd_cadus`):** [`cms-wordpress/backup-db/README.md`](cms-wordpress/backup-db/README.md)

---

## 15) Resumen de organización inicial
Esta base separa claramente producto, documentación, infraestructura funcional y artefactos ágiles para facilitar trabajo paralelo por subequipos, trazabilidad y revisiones por sprint.
