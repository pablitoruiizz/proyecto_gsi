"""Genera scripts/remus/rsi_data.json, los datos del REM de la Red Social Interna del CADUS (Lab 5, MS Teams).

Es la única fuente de verdad del REM de la red social, como dms_data.json lo es del DMS: se edita aquí y se regenera con
    python scripts/remus/rsi_generar.py
    (PowerShell de 32 bits)  scripts\\remus\\build_rem.ps1 -src docs\\remus\\REM-CMS.rem -dst docs\\redsocial\\rem-remus\\RSI.rem
                              -data scripts\\remus\\rsi_data.json -md docs\\redsocial\\rem-remus\\carga-remus.md
Los códigos llevan R (red social) para no chocar con los del CMS (sin letra) ni los del DMS (D).
El Business Case completo está en docs/redsocial/business-case.md; aquí va resumido en la descripción del sistema.
"""
import json
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = ["Pablo Ruiz Vidal"]

d = {
    "date": "2026-11-16",
    "version": [1, 0],
    "cName": "Red Social Interna del CADUS",
    "dName": "Red Social Interna del CADUS",
    "organizations": [
        {"oid": 13, "name": "CADUS - Consejo de Alumnos de la Universidad de Sevilla", "address": "Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla", "telephone": "PD", "fax": "PD"},
        {"oid": 14, "name": "Equipo de proyecto GSI", "address": "Universidad de Sevilla - Gestión de Sistemas de Información (GSI)", "telephone": "PD", "fax": "PD"},
    ],
    "stakeholders": [
        {"name": "Delegación General del CADUS", "role": "Cliente y usuario (Ejecutiva del CADUS)", "customer": True, "developer": False, "user": True, "org": 13},
        {"name": "Pablo Ruiz Vidal", "role": "Product Owner, Business Case y REM", "customer": False, "developer": True, "user": False, "org": 14},
        {"name": "Joaquin Luna Canela", "role": "Scrum Master y Planner", "customer": False, "developer": True, "user": False, "org": 14},
        {"name": "Alvaro Martinez Ocaña", "role": "Dev UML de análisis y de diseño", "customer": False, "developer": True, "user": False, "org": 14},
        {"name": "Marcos-Paban Delgado Rodriguez", "role": "Dev configuración de Teams y capturas", "customer": False, "developer": True, "user": False, "org": 14},
    ],
    "owner": "Pablo Ruiz Vidal",
    "client": "Delegación General del CADUS",
    "paragraphs": {
        "intro": ("Este documento presenta los requisitos de la red social interna del Consejo de Alumnos de la Universidad de Sevilla (CADUS), "
                  "elaborados por el equipo de la asignatura Gestión de Sistemas de Información (GSI) para el Lab 5. La red social se construye en "
                  "Microsoft Teams, dentro de la cuenta de la Universidad, y reúne la comunicación, las tareas, el calendario y los archivos de la "
                  "Ejecutiva, las delegaciones de centro y las asambleas. Es independiente del portal web (CMS) y del gestor documental (DMS), "
                  "con los que se relaciona: los documentos oficiales siguen en el DMS y la red social los enlaza. Se recogen el Business Case y los "
                  "requisitos de los grupos y de las herramientas."),
        "current": ("BUSINESS CASE. Situación: el CADUS ya tiene un portal web para el público y un gestor documental para sus documentos internos, pero "
                    "su coordinación diaria (quién prepara qué para la asamblea, dónde se habla con cada delegación, cómo se comparten borradores y "
                    "avisos) no tiene un espacio propio. Oportunidad: reunir esa coordinación en un único espacio privado, dentro de la cuenta de la "
                    "Universidad que ya usan la Ejecutiva y las 27 delegaciones. Decisión: se elige Microsoft Teams frente a Discord y a la mensajería "
                    "personal porque no tiene coste de licencias, usa las cuentas institucionales, se integra con SharePoint (ya usado en el DMS), "
                    "controla miembros y permisos por equipo y canal y ofrece tareas, calendario y automatización (Planner, Power Automate y PowerApps). "
                    "Alcance del piloto: tres equipos (Ejecutiva, Delegaciones, con un subgrupo por centro, y Asamblea). Fuera de alcance: cambiar "
                    "el portal o el DMS, migrar conversaciones previas y poner en marcha las 27 delegaciones. Riesgos principales: la Ejecutiva comparte "
                    "una sola cuenta, hay datos personales de estudiantes y delegados, y puede que el CADUS no lo adopte. Costes: sin licencias nuevas; "
                    "el esfuerzo del equipo de cuatro personas. El detalle está en docs/redsocial/business-case.md."),
        "environment": ("El equipo de cuatro integrantes crea y configura la red social en Microsoft Teams con sus cuentas de alumno de la Universidad de "
                        "Sevilla. Los archivos del proyecto y la documentación se gestionan con GitHub y la coordinación diaria del equipo se realiza en "
                        "Discord. Las siguientes restricciones recogen estas decisiones."),
        "glossary": [
            {"name": "Equipo", "text": "En Microsoft Teams, el espacio de trabajo de un grupo de personas, con sus canales, archivos y herramientas."},
            {"name": "Grupo y subgrupo", "text": "Conjunto de personas del CADUS con un mismo papel (Ejecutiva, Delegaciones, Asamblea). Un subgrupo es una parte de un grupo (por ejemplo, la delegación de un centro). En Teams, cada grupo es un equipo y cada subgrupo es un canal privado de ese equipo."},
            {"name": "Canal", "text": "Conversación temática dentro de un equipo. Puede ser estándar (lo ve todo el equipo) o privado (solo las personas invitadas)."},
            {"name": "Herramienta", "text": "Aplicación que se ancla a un canal: Archivos (SharePoint), Calendario, Planner, Forms, y automatizaciones de Power Automate o aplicaciones de PowerApps."},
            {"name": "Rol", "text": "Papel de una persona en el equipo: propietario (administra), miembro (participa) o invitado (acceso limitado)."},
            {"name": "Permiso", "text": "Acción que un rol puede hacer sobre un grupo o un canal: leer, publicar, gestionar canales o administrar miembros."},
            {"name": "Planner", "text": "Herramienta de Microsoft 365 para repartir tareas en planes con cubos, responsables y fechas."},
            {"name": "Power Automate", "text": "Herramienta de Microsoft 365 para crear flujos automáticos, por ejemplo avisos cuando se asigna una tarea."},
            {"name": "PowerApps", "text": "Herramienta de Microsoft 365 para crear aplicaciones sencillas sobre los datos del equipo."},
        ],
    },
    "actors": [
        {"id": "ACT-R01", "name": "Ejecutiva del CADUS", "role": "a los miembros de la Ejecutiva, que usan la cuenta única del CADUS y son propietarios del equipo (administran miembros y canales, publican avisos y reparten tareas)"},
        {"id": "ACT-R02", "name": "Delegación de centro", "role": "a cada una de las 27 delegaciones, que acceden con la cuenta de su delegación (una cuenta por delegación, no por persona) y son miembros: leen los avisos, participan en su canal y gestionan sus tareas"},
        {"id": "ACT-R03", "name": "Administrador del equipo", "role": "a la persona del equipo del proyecto que crea el equipo en Teams y lo configura (Pablo Ruiz Vidal); al terminar el proyecto lo traspasa a la Ejecutiva"},
    ],
    "objectives": [
        {"id": "OBJ-R01", "name": "Espacio propio por grupo", "description": "que la Ejecutiva y cada delegación tengan un lugar propio y privado donde hablar y compartir archivos", "importance": 2, "authors": A},
        {"id": "OBJ-R02", "name": "Tareas a la vista", "description": "que las tareas de preparación de las asambleas y de los cursos estén a la vista y asignadas a quien corresponde", "importance": 2, "authors": A},
        {"id": "OBJ-R03", "name": "Avisos y calendario unificados", "description": "que los avisos y el calendario del CADUS estén en un solo sitio", "importance": 2, "authors": A},
        {"id": "OBJ-R04", "name": "Documentos sin duplicar", "description": "que los documentos internos sigan en el gestor documental (DMS) y se enlacen desde la red social, sin copias", "importance": 2, "authors": A},
        {"id": "OBJ-R05", "name": "Lo interno, solo para quien corresponde", "description": "que lo interno no se mezcle con lo que ve cualquier estudiante: los grupos son privados y solo entran las cuentas autorizadas", "importance": 2, "authors": A},
    ],
    "information": [
        {"id": "IR-R01", "name": "Grupo", "concept": "a cada grupo o subgrupo del equipo, con estos datos:", "importance": 2,
         "data": ["Nombre", "Tipo (Ejecutiva, Delegaciones, subgrupo de centro o Asamblea)", "Descripción", "Propietarios", "Miembros"], "authors": A},
        {"id": "IR-R02", "name": "Canal", "concept": "a cada canal de un grupo, con estos datos:", "importance": 2,
         "data": ["Nombre", "Grupo al que pertenece", "Tipo (estándar o privado)", "Quién puede publicar", "Herramientas ancladas"], "authors": A},
        {"id": "IR-R03", "name": "Herramienta", "concept": "a cada herramienta del equipo, con estos datos:", "importance": 2,
         "data": ["Nombre (Archivos, Calendario, Planner, Forms, Power Automate o PowerApps)", "Para qué se usa", "Grupo o canal donde está", "Quién la gestiona"], "authors": A},
        {"id": "IR-R04", "name": "Rol y permiso", "concept": "a cada rol del equipo, con estos datos:", "importance": 2,
         "data": ["Rol (propietario, miembro o invitado)", "Acciones permitidas (leer, publicar, gestionar canales, administrar miembros)", "Grupo o canal sobre el que se aplica"], "authors": A},
        {"id": "IR-R05", "name": "Plan y tarea", "concept": "a cada plan de tareas y a sus tareas, con estos datos:", "importance": 2,
         "data": ["Plan y grupo al que pertenece", "Cubo", "Tarea", "Responsable", "Fecha límite", "Estado"], "authors": A},
    ],
    "ui": [
        {"id": "UI-R01", "name": "Grupos y canales con nombres claros", "description": "ordenar el equipo por grupos y canales con nombres que se entiendan sin explicación (por ejemplo, «Delegaciones · ETSII»), para que una persona sin experiencia en Teams encuentre su canal", "comments": "RNF-R02", "importance": 2, "urgency": 2, "authors": A},
        {"id": "UI-R02", "name": "Herramientas ancladas en cada canal", "description": "anclar en cada canal, como pestañas, las herramientas que se usan allí (archivos, tareas y calendario)", "comments": "RNF-R02", "importance": 2, "urgency": 2, "authors": A},
    ],
    "functional": [
        {"id": "RF-R01", "name": "Equipos del CADUS", "description": "crear tres equipos privados, que son los grupos principales: «CADUS · Ejecutiva», «CADUS · Delegaciones» y «CADUS · Asamblea». Se usan tres equipos, y no uno con todos los canales, porque Teams limita los canales privados por equipo y las 27 delegaciones más la Ejecutiva casi lo agotarían", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R02", "name": "Grupo Ejecutiva", "description": "ofrecer a la Ejecutiva el equipo «CADUS · Ejecutiva», en el que solo están sus miembros, para coordinarse y preparar lo que luego se publica", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R03", "name": "Grupo Delegaciones", "description": "ofrecer a cada delegación de centro (27) un subgrupo, que es un canal privado del equipo «CADUS · Delegaciones», visible solo para la Ejecutiva y para esa delegación", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R04", "name": "Grupo Asamblea", "description": "ofrecer el equipo «CADUS · Asamblea» para preparar y hacer el seguimiento de las asambleas y de los cursos, con la Ejecutiva como propietaria y las delegaciones como miembros", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R05", "name": "Canal de avisos", "description": "ofrecer un canal de avisos (el canal General del equipo «CADUS · Delegaciones») donde solo publica la Ejecutiva y todas las delegaciones leen", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R06", "name": "Roles y permisos", "description": "aplicar tres roles: propietario (Ejecutiva y administrador del equipo), miembro (delegaciones) e invitado (equipo del proyecto en pruebas, sin acceso a canales con datos personales)", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R07", "name": "Archivos enlazados al DMS", "description": "ofrecer en los canales una pestaña de archivos que apunte a los sitios de SharePoint del DMS, de modo que los documentos oficiales no se copien a Teams", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R08", "name": "Calendario compartido", "description": "mostrar a todo el equipo un calendario con las asambleas y los cursos, que mantiene la Ejecutiva", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R09", "name": "Planes de tareas", "description": "ofrecer en cada grupo un plan de Planner con cubos y tareas asignadas a una persona o delegación y con fecha límite", "comments": "Entrega del 22/11", "importance": 2, "urgency": 2, "authors": A},
        {"id": "RF-R10", "name": "Formularios", "description": "ofrecer Forms para recoger confirmaciones de asistencia y pequeñas encuestas a las delegaciones", "comments": "Entrega del 22/11", "importance": 2, "urgency": 3, "authors": A},
        {"id": "RF-R11", "name": "Flujos automáticos", "description": "avisar en el canal correspondiente cuando se asigna una tarea o vence su fecha, con flujos de Power Automate", "comments": "Entrega del 29/11 (Lab 8)", "importance": 3, "urgency": 3, "authors": A},
        {"id": "RF-R12", "name": "Aplicación de PowerApps", "description": "ofrecer, si el tenant de la Universidad lo permite, una aplicación sencilla de PowerApps sobre los datos del equipo (por ejemplo, la lista de delegaciones y su estado)", "comments": "Entrega del 29/11 (Lab 8); depende de que el tenant la ofrezca", "importance": 3, "urgency": 3, "authors": A},
    ],
    "usecases": [
        {"id": "CU-R01", "name": "Publicar un aviso del CADUS", "trigger": "cuando la Ejecutiva tiene algo que comunicar a todas las delegaciones",
         "pre": "La Ejecutiva ha iniciado sesión en Teams con la cuenta del CADUS", "post": "El aviso está publicado y todas las delegaciones pueden leerlo",
         "steps": [
             {"who": "actor", "text": "abre el canal de avisos del equipo", "actor": "ACT-R01"},
             {"who": "actor", "text": "redacta y publica el aviso, con un archivo adjunto si hace falta", "actor": "ACT-R01"},
             {"who": "system", "text": "muestra el aviso en el canal y lo notifica a los miembros"},
             {"who": "system", "text": "impide que una delegación publique nuevos avisos en ese canal"}],
         "authors": A},
        {"id": "CU-R02", "name": "Preparar una asamblea con tareas", "trigger": "cuando se convoca una asamblea o un curso",
         "pre": "El grupo Asamblea existe y las delegaciones son miembros", "post": "La asamblea está en el calendario y sus tareas están asignadas con fecha",
         "steps": [
             {"who": "actor", "text": "crea el evento de la asamblea en el calendario compartido", "actor": "ACT-R01"},
             {"who": "actor", "text": "crea en el plan del grupo Asamblea las tareas de preparación y las asigna a personas o delegaciones", "actor": "ACT-R01"},
             {"who": "system", "text": "muestra el evento a todo el equipo y las tareas a sus responsables"},
             {"who": "actor", "text": "actualiza el estado de sus tareas", "actor": "ACT-R02"},
             {"who": "system", "text": "refleja el avance del plan para la Ejecutiva"}],
         "authors": A},
        {"id": "CU-R03", "name": "Compartir un documento con una delegación", "trigger": "cuando la Ejecutiva necesita que una delegación vea o complete un documento",
         "pre": "El documento está en el DMS y la delegación tiene su canal", "post": "La delegación puede abrir el documento desde su canal",
         "steps": [
             {"who": "actor", "text": "abre el canal privado de la delegación", "actor": "ACT-R01"},
             {"who": "actor", "text": "enlaza en la pestaña de archivos el documento del sitio de SharePoint del DMS", "actor": "ACT-R01"},
             {"who": "system", "text": "muestra el enlace solo a la Ejecutiva y a esa delegación"},
             {"who": "actor", "text": "abre el documento desde su canal", "actor": "ACT-R02"}],
         "authors": A},
        {"id": "CU-R04", "name": "Consultar avisos, calendario y tareas", "trigger": "al empezar a trabajar o antes de una asamblea",
         "pre": "La delegación ha iniciado sesión en Teams con la cuenta de su delegación", "post": "La delegación sabe qué se ha avisado, cuándo es la próxima asamblea y qué tiene pendiente",
         "steps": [
             {"who": "actor", "text": "abre el equipo y lee los avisos nuevos", "actor": "ACT-R02"},
             {"who": "system", "text": "muestra los avisos, sin canales de otras delegaciones"},
             {"who": "actor", "text": "consulta el calendario y sus tareas del plan", "actor": "ACT-R02"},
             {"who": "system", "text": "muestra los próximos eventos y las tareas asignadas a esa delegación"}],
         "authors": A},
        {"id": "CU-R05", "name": "Dar de alta o de baja una delegación", "trigger": "cuando una delegación se crea o desaparece",
         "pre": "El equipo existe y el administrador tiene permisos de propietario", "post": "La delegación tiene su canal privado y sus permisos, o su canal queda archivado",
         "steps": [
             {"who": "actor", "text": "crea un canal privado para la delegación dentro del grupo Delegaciones", "actor": "ACT-R03"},
             {"who": "actor", "text": "añade a ese canal a la cuenta de la delegación y a la Ejecutiva", "actor": "ACT-R03"},
             {"who": "system", "text": "aplica el rol de miembro a la delegación y de propietaria a la Ejecutiva"},
             {"who": "actor", "text": "al dar de baja una delegación, archiva su canal sin borrar lo publicado", "actor": "ACT-R03"}],
         "authors": A},
    ],
    "nonfunctional": [
        {"id": "RNF-R01", "name": "Privacidad", "description": "cumplir el RGPD y la LOPDGDD: grupos y canales privados, sin canales abiertos, y sin trasladar a Teams los datos de reclamaciones, mediaciones ni votaciones, que siguen en el DMS con sus permisos", "section": 47, "importance": 2, "authors": A},
        {"id": "RNF-R02", "name": "Facilidad de uso", "description": "una persona sin experiencia en Teams debe poder encontrar su canal, leer los avisos y completar una tarea con una guía corta", "section": 47, "importance": 2, "authors": A},
        {"id": "RNF-R03", "name": "Mantenibilidad", "description": "la estructura del equipo (grupos, canales, roles y permisos) queda documentada para que otra persona pueda mantenerla y traspasarla a la Ejecutiva", "section": 47, "importance": 2, "authors": A},
        {"id": "RNF-R04", "name": "Disponibilidad", "description": "estar disponible desde cualquier navegador o aplicación de Teams con la cuenta de la Universidad, también desde el móvil", "section": 47, "importance": 2, "authors": A},
    ],
    "rules": [
        {"id": "RN-R01", "name": "Solo la Ejecutiva publica avisos", "description": "En el canal de avisos solo publica la Ejecutiva; las delegaciones leen y pueden reaccionar (coherente con RN-01 del portal: todo pasa por la Ejecutiva).", "authors": A},
        {"id": "RN-R02", "name": "Cada delegación ve solo lo suyo", "description": "Una delegación solo ve su propio canal, los avisos y los grupos comunes; no ve los canales de otras delegaciones.", "authors": A},
        {"id": "RN-R03", "name": "Los documentos oficiales viven en el DMS", "description": "Las actas, la normativa, los expedientes y las votaciones se guardan en el DMS; la red social solo los enlaza y no guarda copias.", "authors": A},
        {"id": "RN-R04", "name": "Una cuenta por delegación", "description": "Cada delegación usa una sola cuenta, a nombre de la delegación y no de la persona, que pasa al equipo siguiente cuando cambia el delegado (igual que en el portal, RN-04).", "authors": A},
        {"id": "RN-R05", "name": "Sin acceso para estudiantes", "description": "Los estudiantes no son miembros ni invitados: la red social es solo para la Ejecutiva y las delegaciones.", "authors": A},
    ],
    "environment": [
        {"id": "RC-R01", "name": "Microsoft Teams de la Universidad de Sevilla", "description": "La red social se construye en Microsoft Teams del tenant de la Universidad de Sevilla, con equipos, canales, roles y las herramientas de Microsoft 365 que el tenant ofrezca (archivos, calendario, Planner, Forms y, si están disponibles, Power Automate y PowerApps).", "authors": A},
        {"id": "RC-R02", "name": "Límites del tenant", "description": "Los alumnos no administran el tenant: lo que no permita la configuración de la Universidad (por ejemplo, crear equipos o usar Power Automate y PowerApps) se documenta y no se puede cambiar.", "authors": A},
        {"id": "RC-R03", "name": "Documentación independiente", "description": "La red social tiene su propio REM, análisis, diseño, implementación y seguimiento SCRUM, independientes de los del CMS y del DMS.", "authors": A},
    ],
    "traces": [
        ["OBJ-R01", ["RF-R01", "RF-R02", "RF-R03", "RF-R04", "RF-R06", "IR-R01", "IR-R02", "UI-R01", "RN-R02", "RN-R04"]],
        ["OBJ-R02", ["RF-R08", "RF-R09", "RF-R10", "RF-R11", "RF-R12", "IR-R03", "IR-R05", "CU-R02"]],
        ["OBJ-R03", ["RF-R05", "RF-R08", "UI-R02", "RN-R01", "CU-R01", "CU-R04"]],
        ["OBJ-R04", ["RF-R07", "RN-R03", "CU-R03"]],
        ["OBJ-R05", ["RF-R06", "IR-R04", "RNF-R01", "RN-R02", "RN-R05"]],
        ["CU-R01", ["RF-R05", "RF-R06", "RN-R01", "IR-R02", "ACT-R01"]],
        ["CU-R02", ["RF-R04", "RF-R08", "RF-R09", "IR-R05", "ACT-R01", "ACT-R02"]],
        ["CU-R03", ["RF-R03", "RF-R07", "RN-R02", "RN-R03", "IR-R02", "ACT-R01", "ACT-R02"]],
        ["CU-R04", ["RF-R05", "RF-R08", "RF-R09", "RN-R02", "ACT-R02"]],
        ["CU-R05", ["RF-R03", "RF-R06", "RN-R04", "IR-R01", "IR-R04", "ACT-R03"]],
        ["RF-R01", ["IR-R01", "IR-R02", "RC-R01", "RC-R02"]],
        ["RF-R06", ["IR-R04", "RN-R05"]],
        ["RF-R11", ["RC-R02", "IR-R03"]],
        ["RF-R12", ["RC-R02", "IR-R03"]],
        ["RNF-R03", ["RF-R01", "RF-R06"]],
    ],
}

ruta = os.path.join(RAIZ, "scripts", "remus", "rsi_data.json")
json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("generado", os.path.relpath(ruta, RAIZ), "·", len(d["functional"]), "RF,", len(d["usecases"]), "CU,", len(d["rules"]), "RN,", len(d["traces"]), "trazas")
