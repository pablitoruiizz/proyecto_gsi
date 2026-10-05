param($src, $dst, $md, $meta)
$ErrorActionPreference = 'Stop'
Copy-Item $src $dst -Force
$utf8 = New-Object Text.UTF8Encoding($false)
$mdLines = [IO.File]::ReadAllLines($md, $utf8)
$m = [IO.File]::ReadAllText($meta, $utf8) | ConvertFrom-Json
$date = [datetime]::ParseExact($m.date, 'yyyy-MM-dd', $null)

function Parse-Table($prefix) {
    $rows = @(); $on = $false
    foreach ($l in $mdLines) {
        if ($l -match '^## ') { $on = $l.StartsWith($prefix); continue }
        if ($on -and $l.StartsWith('|')) {
            $cells = @($l.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
            if ($cells[0] -match '^:?-+' -or $cells[0] -eq 'ID' -or $cells[0] -eq 'Origen') { continue }
            $rows += , $cells
        }
    }
    return , $rows
}
function Imp($t) { if ($t -like 'Vital*') { 2 } elseif ($t -like 'Importante*') { 3 } else { 4 } }
function Urg($t) { if ($t -like 'Inmed*') { 2 } elseif ($t -like 'Hay*') { 3 } else { 4 } }

$conn = New-Object System.Data.OleDb.OleDbConnection ("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=$dst")
$conn.Open()
$tx = $conn.BeginTransaction()

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
    [void]$cmd.ExecuteNonQuery()
}
function Scalar($sql) { $cmd = New-Object System.Data.OleDb.OleDbCommand $sql, $conn, $tx; return $cmd.ExecuteScalar() }
function Ins($table, $cols, $vals) {
    $sql = "INSERT INTO [$table] (" + (($cols | ForEach-Object { "[$_]" }) -join ',') + ") VALUES (" + ((1..$cols.Count | ForEach-Object { '?' }) -join ',') + ")"
    Exec $sql $vals
}

# --- 1. limpiar contenido de ejemplo de Madeja en el documento C ---
$delOids = @()
foreach ($t in 'Paragraph', 'GraphicFile') {
    $cmd = New-Object System.Data.OleDb.OleDbCommand "SELECT oid FROM [$t] WHERE document=1", $conn, $tx
    $r = $cmd.ExecuteReader(); while ($r.Read()) { $delOids += [int]$r[0] }; $r.Close()
}
Exec "DELETE FROM [Paragraph] WHERE document=1" @()
Exec "DELETE FROM [GraphicFile] WHERE document=1" @()
foreach ($o in $delOids) { Exec "DELETE FROM [Change] WHERE subject=?" @([int]$o) }
Exec "DELETE FROM [IsAuthorOf]" @()
Exec "DELETE FROM [IsSourceOf]" @()
"borrados paragraphs/graficos de ejemplo: " + $delOids.Count

# --- 2. datos del proyecto ---
Exec "UPDATE [C_RequirementsSpecification] SET [name]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=?" @($m.cName, 0, 1, $date)
Exec "UPDATE [D_RequirementsSpecification] SET [name]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=?" @($m.dName, 0, 1, $date)
foreach ($o in $m.organizations) {
    $tel = if ($o.telephone) { $o.telephone } else { 'PD' }; $fax = if ($o.fax) { $o.fax } else { 'PD' }
    Exec "UPDATE [Organization] SET [name]=?, [address]=?, [telephone]=?, [fax]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=? WHERE oid=?" @($o.name, $o.address, $tel, $fax, 0, 1, $date, [int]$o.oid)
}

# --- contadores ---
$script:next = 1000
function NewOid { $script:next++; return $script:next }
$ordTables = 'Section', 'Paragraph', 'GraphicFile', 'Organization', 'Stakeholder', 'Actor', 'Objective', 'InformationRequirement', 'FunctionalRequirement', 'NonFunctionalRequirement', 'ConstraintRequirement', 'UseCase'
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
function NextNum($table) { if (-not $numCache.ContainsKey($table)) { $numCache[$table] = 0 }; $numCache[$table]++; return $numCache[$table] }
$ids = @{}      # codigo -> oid
$kind = @{}     # codigo -> 'actor','obj',...
$common = 'oid', 'name', 'versionMajor', 'versionMinor', 'versionDate', 'comments', 'number', 'document', 'parent', 'order'
function CommonVals($oid, $name, $comments, $num, $parent) { return @($oid, $name, 0, 1, $date, $comments, $num, 1, $parent, (NextOrder $parent)) }

# --- 3. stakeholders (los dos existentes se actualizan, el resto se inserta) ---
$sNum = 2
$stk = @()
foreach ($s in $m.stakeholders) {
    if ($s.oid -gt 0) {
        Exec "UPDATE [Stakeholder] SET [name]=?, [role]=?, [isCustomer]=?, [isDeveloper]=?, [isUser]=?, [organization]=?, [versionMajor]=?, [versionMinor]=?, [versionDate]=? WHERE oid=?" @($s.name, $s.role, [bool]$s.customer, [bool]$s.developer, [bool]$s.user, [int]$s.org, 0, 1, $date, [int]$s.oid)
        $stk += [int]$s.oid
    } else {
        $o = NewOid; $sNum++
        Ins 'Stakeholder' ($common + 'role', 'isCustomer', 'isDeveloper', 'isUser', 'organization') ((CommonVals $o $s.name 'Ninguno' $sNum 123) + @($s.role, [bool]$s.customer, [bool]$s.developer, [bool]$s.user, [int]$s.org))
        $stk += $o
    }
}
$client = 134; $po = $stk[0]; $scrum = $stk[0]; for ($i = 0; $i -lt $m.stakeholders.Count; $i++) { if ($m.stakeholders[$i].role -like "Product Owner*") { $po = $stk[$i] }; if ($m.stakeholders[$i].role -like "Scrum Master*") { $scrum = $stk[$i] } }

# --- 4. actores (seccion 24) ---
foreach ($r in (Parse-Table '## 3. Actores')) {
    $o = NewOid; $ids[$r[0]] = $o; $kind[$r[0]] = 'actor'
    Ins 'Actor' ($common + 'role') ((CommonVals $o $r[1] 'Ninguno' (NextNum 'Actor') 24) + @($r[2]))
}
# --- 5. objetivos (seccion 18) ---
$req = 'importance', 'urgency', 'status', 'stability'
foreach ($r in (Parse-Table '## 4. Objetivos')) {
    $o = NewOid; $ids[$r[0]] = $o; $kind[$r[0]] = 'src'
    Ins 'Objective' ($common + $req + 'description') ((CommonVals $o ($r[0] + ' - ' + $r[1]) 'Ninguno' (NextNum 'Objective') 18) + @((Imp $r[3]), 2, 2, 3, $r[2]))
}
# --- 6. requisitos de informacion (seccion 27) ---
foreach ($r in (Parse-Table '## 5. Requisitos de informaci')) {
    $o = NewOid; $ids[$r[0]] = $o; $kind[$r[0]] = 'src'
    Ins 'InformationRequirement' ($common + $req + 'relevantConcept', 'avgLifeTimeValue', 'avgLifeTimeTime', 'maxLifeTimeValue', 'maxLifeTimeTime', 'avgOcurrences', 'maxOcurrences') ((CommonVals $o ($r[0] + ' - ' + $r[1]) 'Tiempos de vida y ocurrencias por estimar (PD).' (NextNum 'InformationRequirement') 27) + @((Imp $r[4]), 2, 2, 3, $r[2], [single]0, 1, [single]0, 1, [single]0, [single]0))
    $i = 0
    foreach ($d in ($r[3] -split ',\s*')) { $i++; Ins 'SpecificData' @('oid', 'owner', 'order', 'description', 'comments') @((NewOid), $o, $i, $d, 'Ninguno') }
}
# --- 7. requisitos funcionales (seccion 29) ---
foreach ($r in (Parse-Table '## 6. Requisitos funcionales')) {
    $o = NewOid; $ids[$r[0]] = $o; $kind[$r[0]] = 'src'
    Ins 'FunctionalRequirement' ($common + $req + 'description') ((CommonVals $o ($r[0] + ' - ' + $r[1]) ('Historias de usuario: ' + $r[3]) (NextNum 'FunctionalRequirement') 29) + @((Imp $r[4]), (Urg $r[5]), 2, 3, $r[2]))
}
# --- 8. requisitos no funcionales (secciones 42-47) ---
foreach ($r in (Parse-Table '## 7. Requisitos no funcionales')) {
    $o = NewOid; $ids[$r[0]] = $o; $kind[$r[0]] = 'src'
    $sec = [int]$m.rnfSection.($r[0])
    Ins 'NonFunctionalRequirement' ($common + $req + 'description') ((CommonVals $o ($r[0] + ' - ' + $r[1]) 'Ninguno' (NextNum 'NonFunctionalRequirement') $sec) + @((Imp $r[3]), 3, 2, 3, $r[2]))
}
# --- 9. restricciones: RN (seccion 28) y RC (seccion 33) ---
foreach ($r in (Parse-Table '## 8. Restricciones')) {
    $o = NewOid; $ids[$r[0]] = $o
    $sec = if ($r[0] -like 'RC-*') { 33 } else { 28 }
    $kind[$r[0]] = if ($r[0] -like 'RC-*') { 'team' } else { 'src' }
    Ins 'ConstraintRequirement' ($common + $req + 'description') ((CommonVals $o ($r[0] + ' - ' + $r[1]) 'Ninguno' (NextNum 'ConstraintRequirement') $sec) + @(2, 2, 2, 3, $r[2]))
}

# --- 10. autoria y fuentes ---
$aN = 0; $sN = 0
foreach ($c in $ids.Keys) {
    if ($kind[$c] -eq 'actor') { continue }
    $aN++; Ins 'IsAuthorOf' @('oid', 'stakeholder', 'specificationObject') @($aN, $po, $ids[$c])
    $sN++; $src = if ($kind[$c] -eq 'team') { $scrum } else { $client }
    Ins 'IsSourceOf' @('oid', 'stakeholder', 'specificationObject') @($sN, $src, $ids[$c])
}

# --- 11. trazabilidad ---
Exec "DELETE FROM [Trace]" @()
$tN = 0; $missing = @()
foreach ($r in (Parse-Table '## 9. Trazabilidad')) {
    $from = $r[0] -split ',\s*'
    $to = $r[1] -split ',\s*'
    foreach ($f in $from) { foreach ($t in $to) {
        if ($ids.ContainsKey($f) -and $ids.ContainsKey($t)) { $tN++; Ins 'Trace' @('oid', 'isChecked', 'source', 'target') @($tN, $false, $ids[$f], $ids[$t]) } else { $missing += "$f->$t" }
    } }
}
$tx.Commit(); $conn.Close()
"objetos creados: " + $ids.Count + " | trazas: $tN | autores: $aN | fuentes: $sN"
if ($missing.Count) { "trazas sin resolver: " + ($missing -join ', ') }
