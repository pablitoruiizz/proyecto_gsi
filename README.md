# Proyecto GSI — Implantación Incremental de Sistemas de Información

## 1) Descripción del proyecto
Repositorio base del proyecto universitario grupal de la asignatura **Gestión de Sistemas de Información (GSI)**.

El objetivo es implantar de forma incremental, siguiendo **SCRUM**, tres sistemas para una empresa/cliente real:
- **CMS en WordPress**
- **DMS en SharePoint**
- **Colaboración interna con Microsoft Teams, Planner, Power Automate y PowerApps**

## 2) Cliente / empresa real
- **Nombre de la empresa:** `[PENDIENTE_DEFINIR]`
- **Sector:** `[PENDIENTE_DEFINIR]`
- **Persona de contacto (rol):** `[PENDIENTE_DEFINIR]`

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

## 5) Equipo (4 integrantes)
> Completar y mantener actualizada esta tabla.

| Integrante | Usuario GitHub | Rol en el equipo |
|---|---|---|
| `[Nombre Apellido 1]` | `@usuario1` | `[Scrum Master / Dev / Analista ...]` |
| `[Nombre Apellido 2]` | `@usuario2` | `[Product Owner / Dev / QA ...]` |
| `[Nombre Apellido 3]` | `@usuario3` | `[Dev / Analista / Documentación ...]` |
| `[Nombre Apellido 4]` | `@usuario4` | `[DevOps / Dev / QA ...]` |

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

## 8) Despliegue local del CMS (XAMPP + WordPress)
1. Instalar XAMPP e iniciar **Apache** y **MySQL**.
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
- **Estado actual:** `Estructura base creada / pendiente de completar por el equipo`
- **Backlog de producto:** [`docs/scrum/backlog/product-backlog.md`](docs/scrum/backlog/product-backlog.md)
- **Sprints:** [`docs/scrum/sprints/README.md`](docs/scrum/sprints/README.md)
- **Burndown:** [`docs/scrum/burndown/README.md`](docs/scrum/burndown/README.md)
- **Requisitos REM/REMUS:** [`docs/requisitos/rem-remus/README.md`](docs/requisitos/rem-remus/README.md)
- **Maquetas:** [`docs/maquetas/README.md`](docs/maquetas/README.md)

---

## 15) Resumen de organización inicial
Esta base separa claramente producto, documentación, infraestructura funcional y artefactos ágiles para facilitar trabajo paralelo por subequipos, trazabilidad y revisiones por sprint.
