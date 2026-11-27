# Exporta a PDF los manuales Word de docs/manuales/entrega con Microsoft Word y actualiza antes el índice y los números de página.
# Uso: powershell -File scripts\entrega\exportar_manuales_pdf.ps1
$ErrorActionPreference = 'Stop'
$raiz = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    Get-ChildItem (Join-Path $raiz 'docs\manuales\entrega') -Filter *.docx | ForEach-Object {
        $pdf = [IO.Path]::ChangeExtension($_.FullName, '.pdf')
        $doc = $word.Documents.Open($_.FullName, $false, $false)
        foreach ($t in $doc.TablesOfContents) { $t.Update() }
        $doc.Fields.Update() | Out-Null
        $doc.Save()
        $doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
        $doc.Close($false)
        "pdf: $pdf"
    }
} finally { $word.Quit() }
