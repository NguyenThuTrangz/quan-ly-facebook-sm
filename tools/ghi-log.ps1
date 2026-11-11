# Ghi 1 viec da lam: dong Excel (qua ghi-nhat-ky.ps1) + dat dong TSV "Nhat Ky SM" (A..J) vao clipboard de dan len Google Sheet.
# Cach dung: & "C:\claude remote\tools\ghi-log.ps1" SM01 "Tim story" "Story trang chu" "<noi dung>" "Xong" 2 ["<ket qua>"] ["<che do>"]
#   LoaiViec: Tim story / Luot newfeed / Dang bai / Chap nhan ket ban / Tuong tac newsfeed / Join group / Tuong tac group / Ket ban
#   TrangThai: Xong / Mot phan / Khong lam duoc / Bo qua ; SoLuong: so dem thuc te (0 neu khong lam duoc)
param(
    [Parameter(Mandatory)][string]$Ma,
    [Parameter(Mandatory)][string]$Loai,
    [Parameter(Mandatory)][string]$Noi,
    [Parameter(Mandatory)][string]$NoiDung,
    [Parameter(Mandatory)][string]$TrangThai,
    [Parameter(Mandatory)][int]$SoLuong,
    [string]$KetQua = "",
    [string]$CheDo = ""
)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$ten = @{ SM01 = "Sophie Embroidery"; SM02 = "Benita Ariem"; SM03 = "Rosie Smocking"; SM04 = "Jenny Smocking" }[$Ma]
if (-not $KetQua) { $KetQua = $TrangThai }
& (Join-Path (Split-Path $PSScriptRoot) "ghi-nhat-ky.ps1") $Ma $Loai $Noi $NoiDung $KetQua $CheDo
$ngay = Get-Date -Format "yyyy-MM-dd"
$dong = @($ngay, $Ma, $ten, $Loai, $Noi, $NoiDung, $CheDo, $KetQua, $TrangThai, $SoLuong) -join "`t"
# Gom vao hang doi: dan nhieu dong len sheet 1 lan bang tools\dan-log.ps1
Add-Content -Path (Join-Path $PSScriptRoot "hang-doi-log.tsv") -Value $dong -Encoding UTF8
Set-Clipboard -Value $dong
"Clipboard + hang doi: da them 1 dong Nhat Ky SM"
