# Canh n8n: chạy mỗi 10 phút (tác vụ Windows "Smock n8n watchdog").
# n8n không trả lời /healthz 2 lần liền (cách 20 giây) → tắt tiến trình n8n cũ, chạy lại tác vụ "Smock n8n".
# Lý do (27/11/2026): máy ngủ 25/11 14:02 → n8n chết tới 26/11 11:40, mất lịch 26/11.
$log = 'C:\claude remote\logs\n8n-watchdog.log'
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
function Ok { try { (Invoke-WebRequest http://localhost:5678/healthz -UseBasicParsing -TimeoutSec 8).StatusCode -eq 200 } catch { $false } }
if (Ok) { exit 0 }
Start-Sleep 20
if (Ok) { exit 0 }
"$(Get-Date -Format s) n8n không phản hồi → khởi động lại" | Add-Content $log -Encoding utf8
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'n8n' -and $_.CommandLine -notmatch 'execute' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep 3
Start-ScheduledTask 'Smock n8n'
for ($i = 0; $i -lt 30; $i++) { Start-Sleep 4; if (Ok) { "$(Get-Date -Format s) n8n đã chạy lại" | Add-Content $log -Encoding utf8; exit 0 } }
"$(Get-Date -Format s) n8n vẫn chưa lên sau 2 phút" | Add-Content $log -Encoding utf8
exit 1
