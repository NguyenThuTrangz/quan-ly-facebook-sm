# Ghi 1 việc vào Nhật Ký SM (+ Done/URL vào Lịch SM) qua webhook n8n L1-01. Một lệnh thay cho gõ sheet.
# Dùng:  & "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "Tim story" "Story trang chủ" "story tim 2/3" "Xong" 2 -LichRow 121 [-Url "https://facebook.com/..."] [-CheDo "Công khai"]
# Webhook lỗi → tự ghi kiểu cũ bằng tools\ghi-log.ps1 (Excel + clipboard) và báo "DỰ PHÒNG".
param(
  [Parameter(Mandatory)][ValidatePattern('^SM0[1-8]$')][string]$MaTk,
  [Parameter(Mandatory)][ValidateSet('Tim story','Lướt newfeed','Đăng bài','Chấp nhận kết bạn','Tương tác newsfeed','Join group','Tương tác group','Kết bạn')][string]$LoaiViec,
  [Parameter(Mandatory)][string]$Noi,
  [Parameter(Mandatory)][string]$NoiDung,
  [Parameter(Mandatory)][ValidateSet('Xong','Một phần','Không làm được','Bỏ qua')][string]$TrangThai,
  [double]$SoLuong = 0,
  [int]$LichRow = 0,
  [string]$Url = '',
  [string]$CheDo = '',
  [string]$KetQua = ''
)
$token = $env:SMOCK_LOG_TOKEN
$body = @{ type = 'log'; ma_tk = $MaTk; loai_viec = $LoaiViec; noi = $Noi; noi_dung = $NoiDung; trang_thai = $TrangThai;
           so_luong = $SoLuong; ket_qua = $(if ($KetQua) { $KetQua } else { $TrangThai }); che_do = $CheDo; url = $Url }
if ($LichRow -ge 2) { $body.lich_row = $LichRow }
try {
  $r = Invoke-RestMethod -Method Post -Uri 'http://localhost:5678/webhook/smock-log' -TimeoutSec 20 `
       -Headers @{ 'X-Smock-Token' = $token } -ContentType 'application/json; charset=utf-8' `
       -Body ([System.Text.Encoding]::UTF8.GetBytes(($body | ConvertTo-Json -Compress)))
  if ($r.ok) { "OK $($r.ma_log)$(if ($r.duplicate) { ' (đã ghi trước đó, không ghi lại)' })" ; exit 0 }
  "WEBHOOK TỪ CHỐI: $($r.errors -join '; ')"; exit 2
} catch {
  $msg = $_.ErrorDetails.Message
  if ($msg -and $msg -match '"errors"') { "WEBHOOK TỪ CHỐI: $msg"; exit 2 }   # dữ liệu sai → sửa rồi gửi lại, KHÔNG ghi dự phòng
  "DỰ PHÒNG: webhook không phản hồi ($($_.Exception.Message)). Ghi kiểu cũ."
  & (Join-Path $PSScriptRoot 'ghi-log.ps1') $MaTk $LoaiViec $Noi $NoiDung $TrangThai $SoLuong
  exit 3
}
