# Abre el .docx con Microsoft Word, actualiza el indice y los campos, y (opcionalmente) exporta un PDF.
# Uso: powershell -File scripts\entrega\actualizar_indice.ps1 [-Pdf ruta.pdf]
param([string]$Docx = (Join-Path $PSScriptRoot "..\..\docs\entrega\Entrega1-CMS-CADUS.docx"), [string]$Pdf)
$Docx = (Resolve-Path $Docx).Path
$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($Docx)
    $d.Repaginate()
    foreach ($t in $d.TablesOfContents) { $t.Update() }
    $d.Fields.Update() | Out-Null
    "paginas: " + $d.ComputeStatistics(2)
    if ($Pdf) { $d.ExportAsFixedFormat($Pdf, 17) }
    $d.Save(); $d.Close(0)
} finally { $w.Quit() }
