# Ban thay the ghi-nhat-ky.py khi may chua co Python (can Microsoft Excel).
# Ghi mot dong vao sheet "Nhat ky" cua Quan-ly-Facebook-hang-ngay.xlsx
# Cach dung: .\ghi-nhat-ky.ps1 <Ma TK> <Loai viec> <Noi thuc hien> <Noi dung> <Ket qua> [Che do hien thi] [Ngay YYYY-MM-DD]
param(
    [Parameter(Mandatory)][string]$Ma,
    [Parameter(Mandatory)][string]$Loai,
    [Parameter(Mandatory)][string]$Noi,
    [Parameter(Mandatory)][string]$NoiDung,
    [Parameter(Mandatory)][string]$KetQua,
    [string]$CheDo = "",
    [string]$Ngay = (Get-Date -Format "yyyy-MM-dd")
)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$file = Join-Path $PSScriptRoot "Quan-ly-Facebook-hang-ngay.xlsx"
$sheetName = "Nh" + [char]0x1EAD + "t k" + [char]0x00FD  # "Nhật ký" (giu file ASCII cho PowerShell 5.1)

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($file)
    if ($wb.ReadOnly) { throw "File dang mo o noi khac (chi doc). Dong file trong Excel roi chay lai." }
    $nk = $wb.Worksheets.Item($sheetName)
    $r = 2
    while ("" + $nk.Cells.Item($r, 1).Value2 -ne "") { $r++ }
    $vals = @{ 1 = $Ngay; 2 = $Ma; 4 = $Loai; 5 = $Noi; 6 = $NoiDung; 7 = $CheDo; 8 = $KetQua }
    foreach ($col in $vals.Keys) {
        if ($vals[$col] -eq "") { continue }
        $cell = $nk.Cells.Item($r, $col)
        $cell.NumberFormat = "@"  # ghi dang chu, giong ban Python
        $cell.Value2 = $vals[$col]
    }
    $wb.Save()
    $wb.Close($false)
    Write-Output "Da ghi dong ${r}: $Ngay | $Ma | $Loai | $KetQua"
}
finally {
    $xl.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
