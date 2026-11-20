# Exporta a PDF los documentos Word de la red social (docs/redsocial/entrega) con Microsoft Word.
# Uso: powershell -File scripts\redsocial\exportar_pdf.ps1
$ErrorActionPreference = 'Stop'
$raiz = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    Get-ChildItem (Join-Path $raiz 'docs\redsocial\entrega') -Filter *.docx | ForEach-Object {
        $pdf = [IO.Path]::ChangeExtension($_.FullName, '.pdf')
        $doc = $word.Documents.Open($_.FullName, $false, $true)
        $doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
        $doc.Close($false)
        "pdf: $pdf"
    }
} finally { $word.Quit() }
