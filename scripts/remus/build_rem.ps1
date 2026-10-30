param($src, $dst, $data, $md)
$ErrorActionPreference = 'Stop'
Copy-Item $src $dst -Force
$utf8 = New-Object Text.UTF8Encoding($false)
$d = [IO.File]::ReadAllText($data, $utf8) | ConvertFrom-Json
$date = [datetime]::ParseExact($d.date, 'yyyy-MM-dd', $null)
$vMaj = [int]$d.version[0]; $vMin = [int]$d.version[1]

$conn = New-Object System.Data.OleDb.OleDbConnection ("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=$dst")
$conn.Open()
$tx = $conn.BeginTransaction()

function Txt($s) { if ($null -eq $s) { return $null }; return ([string]$s) -replace "`r?`n", "`r`n" }
function Exec($sql, $vals) {
    $cmd = New-Object System.Data.OleDb.OleDbCommand $sql, $conn, $tx
    foreach ($v in $vals) {
        $p = New-Object System.Data.OleDb.OleDbParameter
        if ($null -eq $v) { $p.OleDbType = 'VarWChar'; $v = [DBNull]::Value }
        elseif ($v -is [string]) { $p.OleDbType = 'LongVarWChar' }
        elseif ($v -is [bool]) { $p.OleDbType = 'Boolean' }
        elseif ($v -is [datetime]) { $p.OleDbType = 'Date' }
        elseif ($v -is [single]) { $p.OleDbType = 'Single' }
        else { $p.OleDbType = 'Integer' }
        $p.Value = $v
        [void]$cmd.Parameters.Add($p)
    }
    try { [void]$cmd.ExecuteNonQuery() } catch { throw ("SQL fallido: " + $sql + " | valores: " + (($vals | ForEach-Object { [string]$_ }) -join " ; ") + " | " + $_.Exception.Message) }
}
function Scalar($sql) { $cmd = New-Object System.Data.OleDb.OleDbCommand $sql, $conn, $tx; return $cmd.ExecuteScalar() }
function Ins($table, $cols, $vals) {
    $sql = "INSERT INTO [$table] (" + (($cols | ForEach-Object { "[$_]" }) -join ',') + ") VALUES (" + ((1..$cols.Count | ForEach-Object { '?' }) -join ',') + ")"
    Exec $sql $vals
}

# --- 1. limpiar el contenido de ejemplo (orden respetando las claves ajenas) ---
foreach ($t in 'IsAuthorOf', 'IsSourceOf', 'Trace', 'Step', 'Action', 'UseCase', 'SpecificData', 'InformationRequirement', 'FunctionalRequirement', 'NonFunctionalRequirement', 'ConstraintRequirement', 'Objective', 'Actor', 'Paragraph', 'Stakeholder', 'Change') { Exec "DELETE FROM [$t]" @() }

# --- 2. proyecto, secciones y organizaciones ---
Exec "UPDATE [C_RequirementsSpecification] SET [name]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=?" @($d.cName, $vMaj, $vMin, $date)
Exec "UPDATE [D_RequirementsSpecification] SET [name]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=?" @($d.dName, $vMaj, $vMin, $date)
Exec "UPDATE [Section] SET [versionMajor]=?, [versionMinor]=?, [versionDate]=?" @($vMaj, $vMin, $date)
Exec "UPDATE [Section] SET [name]=? WHERE oid=47" @('Requisitos No Funcionales')
foreach ($o in $d.organizations) {
    Exec "UPDATE [Organization] SET [name]=?, [address]=?, [telephone]=?, [fax]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=? WHERE oid=?" @($o.name, $o.address, $o.telephone, $o.fax, $vMaj, $vMin, $date, [int]$o.oid)
}

$script:next = 1000
function NewOid { $script:next++; return $script:next }
$ordTables = 'Section', 'Paragraph', 'Organization', 'Stakeholder', 'Actor', 'Objective', 'InformationRequirement', 'FunctionalRequirement', 'NonFunctionalRequirement', 'ConstraintRequirement', 'UseCase'
$ordCache = @{}
function NextOrder($parent) {
    if (-not $ordCache.ContainsKey($parent)) {
        $mx = 0
        foreach ($t in $ordTables) { $v = Scalar "SELECT MAX([order]) FROM [$t] WHERE parent=$parent"; if ($v -isnot [DBNull] -and [int]$v -gt $mx) { $mx = [int]$v } }
        $ordCache[$parent] = $mx
    }
    $ordCache[$parent]++
    return $ordCache[$parent]
}
$numCache = @{}
function NextNum($k) { if (-not $numCache.ContainsKey($k)) { $numCache[$k] = 0 }; $numCache[$k]++; return $numCache[$k] }
$common = 'oid', 'name', 'versionMajor', 'versionMinor', 'versionDate', 'comments', 'number', 'document', 'parent', 'order'
function CommonVals($oid, $name, $comments, $num, $parent) { return @($oid, $name, $vMaj, $vMin, $date, $(if ($comments) { $comments } else { 'Ninguno' }), $num, 1, $parent, (NextOrder $parent)) }
$req = 'importance', 'urgency', 'status', 'stability'
$ids = @{}; $src2 = @{}   # codigo -> oid ; codigo -> 'client'|'team' (fuente)

# nueva seccion "Entorno de Trabajo del Equipo" antes del glosario (numero 16, orden 6)
$secEnv = NewOid
Exec "UPDATE [Section] SET [order]=7 WHERE oid=55" @()
Ins 'Section' ($common + 'isOrderedByName', 'isAppendix') @($secEnv, 'Entorno de Trabajo del Equipo', $vMaj, $vMin, $date, 'Ninguno', 16, 1, $null, 6, $false, $false)

# --- 3. stakeholders ---
$sNum = 0; $stkByName = @{}
foreach ($s in $d.stakeholders) {
    $o = NewOid; $sNum++; $stkByName[$s.name] = $o
    Ins 'Stakeholder' ($common + 'role', 'isCustomer', 'isDeveloper', 'isUser', 'organization') ((CommonVals $o $s.name 'Ninguno' $sNum 12) + @($s.role, [bool]$s.customer, [bool]$s.developer, [bool]$s.user, [int]$s.org))
}
$owner = $stkByName[$d.owner]; $client = $stkByName[$d.client]

# --- 4. parrafos ---
function Para($name, $text, $parent, $gloss) { $o = NewOid; Ins 'Paragraph' ($common + 'text', 'isGlossaryItem') ((CommonVals $o $name 'Ninguno' (NextNum 'Paragraph') $parent) + @((Txt $text), [bool]$gloss)) }
Para 'Introducción' $d.paragraphs.intro 7 $false
Para 'Sistema Actual' $d.paragraphs.current 22 $false
Para 'Entorno de trabajo' $d.paragraphs.environment $secEnv $false
foreach ($g in $d.paragraphs.glossary) { Para $g.name $g.text 55 $true }

# --- 5. actores (35) ---
foreach ($a in $d.actors) {
    $o = NewOid; $ids[$a.id] = $o
    Ins 'Actor' ($common + 'role') ((CommonVals $o $a.name 'Ninguno' (NextNum 'Actor') 35) + @($a.role))
}
# --- 6. objetivos (24) ---
foreach ($r in $d.objectives) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'Objective' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) 'Ninguno' (NextNum 'Objective') 24) + @([int]$r.importance, 2, 2, 3, $r.description))
}
# --- 7. requisitos de informacion (28) ---
foreach ($r in $d.information) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'InformationRequirement' ($common + $req + 'relevantConcept', 'avgLifeTimeValue', 'avgLifeTimeTime', 'maxLifeTimeValue', 'maxLifeTimeTime', 'avgOcurrences', 'maxOcurrences') ((CommonVals $o ($r.id + ' - ' + $r.name) 'Ninguno' (NextNum 'InformationRequirement') 28) + @([int]$r.importance, 2, 2, 3, $r.concept, [single]0, 1, [single]0, 1, [single]0, [single]0))
    $i = 0
    foreach ($x in $r.data) { $i++; Ins 'SpecificData' @('oid', 'owner', 'order', 'description', 'comments') @((NewOid), $o, $i, $x, 'Ninguno') }
}
# --- 8. requisitos de interfaz de usuario (36) y funcionales (37) ---
foreach ($r in $d.ui) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'FunctionalRequirement' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) $r.comments (NextNum 'FunctionalRequirement') 36) + @([int]$r.importance, [int]$r.urgency, 2, 3, (Txt $r.description)))
}
foreach ($r in $d.functional) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'FunctionalRequirement' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) $r.comments (NextNum 'FunctionalRequirement') 37) + @([int]$r.importance, [int]$r.urgency, 2, 3, (Txt $r.description)))
}
# --- 9. casos de uso (37) con acciones y pasos ---
$aN = 0
foreach ($u in $d.usecases) {
    $o = NewOid; $ids[$u.id] = $o; $src2[$u.id] = 'client'
    Ins 'UseCase' ($common + $req + 'isAbstract', 'triggeringEvent', 'precondition', 'postcondition', 'frequencyValue', 'frequencyTime') ((CommonVals $o ($u.id + ' - ' + $u.name) 'Ninguno' (NextNum 'UseCase') 37) + @(2, 2, 2, 3, $false, $u.trigger, $u.pre, $u.post, [single]0, 1))
    $k = 0
    foreach ($st in $u.steps) {
        $aN++; $k++
        if ($st.who -eq 'actor') { Ins 'Action' @('oid', 'isUseCaseAction', 'useCase', 'isSystemAction', 'description', 'performanceValue', 'performanceTime', 'isActorAction', 'actor') @($aN, $false, $null, $false, $st.text, [single]0, 1, $true, [int]$ids[$st.actor]) }
        else { Ins 'Action' @('oid', 'isUseCaseAction', 'useCase', 'isSystemAction', 'description', 'performanceValue', 'performanceTime', 'isActorAction', 'actor') @($aN, $false, $null, $true, $st.text, [single]0, 1, $false, $null) }
        Ins 'Step' @('oid', 'owner', 'order', 'isConditional', 'condition', 'action', 'comments') @((NewOid), $o, $k, $false, 'PD', $aN, 'Ninguno')
    }
}
# --- 10. no funcionales (47), reglas de negocio (51) y entorno de trabajo ---
foreach ($r in $d.nonfunctional) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'NonFunctionalRequirement' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) 'Ninguno' (NextNum 'NonFunctionalRequirement') ([int]$r.section)) + @([int]$r.importance, 3, 2, 3, $r.description))
}
foreach ($r in $d.rules) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'client'
    Ins 'ConstraintRequirement' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) 'Ninguno' (NextNum 'ConstraintRequirement') 51) + @(2, 2, 2, 3, $r.description))
}
foreach ($r in $d.environment) {
    $o = NewOid; $ids[$r.id] = $o; $src2[$r.id] = 'team'
    Ins 'ConstraintRequirement' ($common + $req + 'description') ((CommonVals $o ($r.id + ' - ' + $r.name) 'Ninguno' (NextNum 'ConstraintRequirement') $secEnv) + @(2, 2, 2, 3, $r.description))
}

# --- 11. autoria, fuentes y trazabilidad ---
$au = @{}
foreach ($lst in @($d.objectives, $d.information, $d.ui, $d.functional, $d.usecases, $d.nonfunctional, $d.rules, $d.environment)) { foreach ($r in $lst) { if ($r.authors) { $au[$r.id] = @($r.authors) } } }
$aI = 0; $sI = 0
foreach ($c in $src2.Keys) {
    $lista = if ($au.ContainsKey($c)) { $au[$c] } else { @($d.owner) }
    foreach ($n in $lista) { $aI++; Ins 'IsAuthorOf' @('oid', 'stakeholder', 'specificationObject') @($aI, $stkByName[$n], $ids[$c]) }
    $sI++; $who = if ($src2[$c] -eq 'team') { $owner } else { $client }
    Ins 'IsSourceOf' @('oid', 'stakeholder', 'specificationObject') @($sI, $who, $ids[$c])
}
$tN = 0; $missing = @()
foreach ($t in $d.traces) {
    foreach ($to in $t[1]) {
        if ($ids.ContainsKey($t[0]) -and $ids.ContainsKey($to)) { $tN++; Ins 'Trace' @('oid', 'isChecked', 'source', 'target') @($tN, $false, $ids[$t[0]], $ids[$to]) } else { $missing += "$($t[0])->$to" }
    }
}
# --- 12. historial de cambios minimo ---
$cN = 0
foreach ($subj in 1, 2, 3, 4) { $cN++; Ins 'Change' @('oid', 'date', 'type', 'subject', 'subjectType', 'description') @($cN, $date, 'C', $subj, 'D', 'Documento creado'); $cN++; Ins 'Change' @('oid', 'date', 'type', 'subject', 'subjectType', 'description') @($cN, $date, 'S', $subj, 'D', 'Documento guardado') }

$tx.Commit(); $conn.Close()
"objetos creados: " + $ids.Count + " | trazas: $tN | autores: $aI | fuentes: $sI"
if ($missing.Count) { "trazas sin resolver: " + ($missing -join ', ') }

# --- 13. espejo legible en Markdown (carga-remus.md) ---
if ($md) {
    $L = New-Object System.Collections.Generic.List[string]
    function Cell($s) { return (([string]$s) -replace "`r?`n", ' ' -replace '\|', '/') }
    function Imp($n) { switch ([int]$n) { 2 { 'Vital' } 3 { 'Importante' } default { 'Quedaría bien' } } }
    $datoNombre = [IO.Path]::GetFileName($data); $remNombre = [IO.Path]::GetFileName($dst)
    $L.Add("# Hoja de carga para REMUS — $($d.cName)"); $L.Add('')
    $L.Add("> Archivo **generado** por [`scripts/remus/build_rem.ps1`](../../../scripts/remus/README.md) a partir de `scripts/remus/$datoNombre`. No editar a mano: modificar el JSON y regenerar."); $L.Add('')
    $L.Add("Contenido del proyecto [$remNombre]($remNombre) (REMUS), versión $vMaj.$vMin, $($d.date). Cada requisito lleva en el nombre su código de trazabilidad, que debe repetirse en el UML de análisis, en el de diseño y en las capturas de implementación."); $L.Add('')
    $L.Add('## 1. Organizaciones'); $L.Add(''); $L.Add('| Nombre | Dirección |'); $L.Add('|---|---|')
    foreach ($o in $d.organizations) { $L.Add("| $(Cell $o.name) | $(Cell $o.address) |") }; $L.Add('')
    $L.Add('## 2. Personas'); $L.Add(''); $L.Add('| Nombre | Rol |'); $L.Add('|---|---|')
    foreach ($s in $d.stakeholders) { $L.Add("| $(Cell $s.name) | $(Cell $s.role) |") }; $L.Add('')
    $L.Add('## 3. Objetivos del sistema'); $L.Add(''); $L.Add('| Código | Nombre | El sistema deberá | Importancia |'); $L.Add('|---|---|---|---|')
    foreach ($r in $d.objectives) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) | $(Imp $r.importance) |") }; $L.Add('')
    $L.Add('## 4. Requisitos de información'); $L.Add(''); $L.Add('| Código | Nombre | Se almacenará información correspondiente a… | Datos específicos |'); $L.Add('|---|---|---|---|')
    foreach ($r in $d.information) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.concept) | $(Cell ($r.data -join '; ')) |") }; $L.Add('')
    $L.Add('## 5. Actores'); $L.Add(''); $L.Add('| Código | Nombre | Representa… |'); $L.Add('|---|---|---|')
    foreach ($r in $d.actors) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.role) |") }; $L.Add('')
    $L.Add('## 6. Requisitos de interfaz de usuario'); $L.Add(''); $L.Add('| Código | Nombre | El sistema deberá | Historias |'); $L.Add('|---|---|---|---|')
    foreach ($r in $d.ui) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) | $(Cell $r.comments) |") }; $L.Add('')
    $L.Add('## 7. Requisitos funcionales'); $L.Add(''); $L.Add('| Código | Nombre | El sistema deberá | Historias | Importancia |'); $L.Add('|---|---|---|---|---|')
    foreach ($r in $d.functional) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) | $(Cell $r.comments) | $(Imp $r.importance) |") }; $L.Add('')
    $L.Add('## 8. Casos de uso'); $L.Add('')
    foreach ($u in $d.usecases) {
        $L.Add("### $($u.id) - $($u.name)"); $L.Add('')
        $L.Add("- **Evento disparador:** $($u.trigger)"); $L.Add("- **Precondición:** $($u.pre)"); $L.Add("- **Postcondición:** $($u.post)"); $L.Add('- **Pasos:**')
        $i = 0; foreach ($st in $u.steps) { $i++; $who = if ($st.who -eq 'actor') { ($d.actors | Where-Object { $_.id -eq $st.actor }).name } else { 'El sistema' }; $L.Add("  $i. $who $($st.text)") }
        $L.Add('')
    }
    $L.Add('## 9. Requisitos no funcionales'); $L.Add(''); $L.Add('| Código | Nombre | El sistema deberá | Importancia |'); $L.Add('|---|---|---|---|')
    foreach ($r in $d.nonfunctional) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) | $(Imp $r.importance) |") }; $L.Add('')
    $L.Add('## 10. Reglas de negocio'); $L.Add(''); $L.Add('| Código | Nombre | Regla |'); $L.Add('|---|---|---|')
    foreach ($r in $d.rules) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) |") }; $L.Add('')
    $L.Add('## 11. Entorno de trabajo del equipo (restricciones)'); $L.Add(''); $L.Add('| Código | Nombre | Descripción |'); $L.Add('|---|---|---|')
    foreach ($r in $d.environment) { $L.Add("| $($r.id) | $(Cell $r.name) | $(Cell $r.description) |") }; $L.Add('')
    $L.Add('## 12. Trazabilidad entre requisitos'); $L.Add(''); $L.Add('| Origen | Destinos |'); $L.Add('|---|---|')
    foreach ($t in $d.traces) { $L.Add("| $($t[0]) | $($t[1] -join ', ') |") }; $L.Add('')
    [IO.File]::WriteAllText($md, ($L -join "`n"), $utf8)
    "markdown generado: $md"
}
