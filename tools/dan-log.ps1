# Dua toan bo hang doi Nhat Ky SM (tools\hang-doi-log.tsv) vao clipboard de dan 1 lan len Google Sheet, roi xoa hang doi.
$f = Join-Path $PSScriptRoot "hang-doi-log.tsv"
if (-not (Test-Path $f)) { "Hang doi trong"; return }
$t = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8).Trim()
Set-Clipboard -Value $t
$n = ($t -split "`n").Count
Remove-Item $f
"Clipboard: $n dong Nhat Ky SM"
