# Cấp 1 — 7 workflow n8n (PC công ty, chạy 24/24)

| File | Giờ chạy | Làm gì | Ai dùng kết quả |
| --- | --- | --- | --- |
| `L1-01-webhook-ghi-log.json` | Luôn nghe (localhost) | Nhận 1 lệnh từ Claude → ghi Nhật Ký SM, ghi Done/URL vào Lịch SM, cập nhật trạng thái tab khác. Chống ghi trùng bằng cột **Mã log** | Cấp 3, báo cáo |
| `L1-02-sinh-lich.json` | 21:30 CN–T6 | Sinh Lịch SM ngày làm việc kế tiếp: 08:30–17:00, 2 cụm/nick, bài group chỉ vào group A/B đã join, cách ≥ 60 phút; giữ chỗ content (mã Kxxx) và người kết bạn | Cấp 3 |
| `L1-03-chuan-bi-goi-bai.json` | 22:00 CN–T6 | Với mỗi content "Đã xếp": `caption.txt` (đã thay mã bài) + ảnh JPG 2048px vào `anh-dang-bai/Kxxx/` → "Gói sẵn" | Cấp 3 |
| `L1-04-bao-cao-ngay.json` | 18:00 T2–T7 | Tổng hợp Nhật Ký SM hôm nay theo nick + đèn → tab Báo cáo ngày (+ Telegram nhóm, tuỳ chọn) | Mọi người |
| `L1-05-kiem-hop-dong.json` | 06:30, 21:50 | Kiểm tiêu đề cột mọi tab theo `ops/contract.json`, gói bài còn thiếu, lead tồn 48h, lịch hôm qua còn "Chờ"; đánh dấu content "Đã đăng" | Người dùng |
| `L1-06-cau-noi-cap-2.json` | 22:15 / 06:30 | Ghi việc cho cấp 2 vào `smock-level2-copilot/inbox`, sáng kéo `outbox` về, kiểm lại, ghi sheet (caption = "Chờ duyệt caption") | Cấp 2 ↔ sheet |
| `L1-07-heartbeat-sao-luu.json` | 10 phút / 00:15 | Ping healthchecks.io; xuất workflow mỗi đêm, giữ 30 ngày | Người dùng |
| `../smock-lead-hunter.json` | 6 giờ/lần | Tìm lead công khai (xem `../README.md`) | Người duyệt, cấp 3 |

Toàn bộ file được sinh từ `ops/build_level1.py` (sửa ở đó rồi chạy lại, không sửa tay JSON). Kiểm mã các node bằng `node ops/test_level1.js` (25 phép thử cho các chỗ bàn giao).

## Cách cài (đã chỉnh theo nghiên cứu 11/11/2026)

**Vì sao không dùng Docker:** từ n8n 3.0 (27/10/2026) bản tự host chỉ hỗ trợ Docker, nhưng trong Docker node Execute Command chạy trong Linux nên không thấy `git`, PowerShell, ổ `C:\` — L1-06 và L1-07 cần những thứ đó. Bản Docker Desktop cũng chỉ chạy sau khi có người đăng nhập Windows. Vì vậy dùng **n8n 2.x cài bằng npm, chạy như dịch vụ Windows** (cùng tài khoản Windows với Claude Code). Khi n8n 2.x hết hỗ trợ, chuyển sang Docker + một runner nhỏ trên Windows.

1. Cài Node.js 22 LTS. `npm install -g n8n@2` (ghim bản 2.x; kiểm `n8n --version`).
2. Tạo `C:\n8n\.env` (không đưa vào git):
   ```
   N8N_ENCRYPTION_KEY=<chuỗi ngẫu nhiên 32+ ký tự — CẤT BẢN SAO Ở NƠI AN TOÀN>
   GENERIC_TIMEZONE=Asia/Ho_Chi_Minh
   NODES_EXCLUDE=[]
   N8N_LISTEN_ADDRESS=127.0.0.1
   N8N_SECURE_COOKIE=false
   EXECUTIONS_DATA_PRUNE=true
   EXECUTIONS_DATA_MAX_AGE=336
   ```
   `NODES_EXCLUDE=[]` bật lại Execute Command (mặc định tắt từ n8n 2.0). `N8N_LISTEN_ADDRESS=127.0.0.1` để webhook chỉ nghe trong máy.
3. Dịch vụ Windows bằng NSSM: `nssm install n8n "C:\Program Files\nodejs\n8n.cmd"`, đặt AppDirectory `C:\n8n`, AppEnvironmentExtra từ file `.env`, Log on = tài khoản Windows đang chạy Claude, Startup = Automatic, Exit actions = Restart. `nssm start n8n` → mở http://localhost:5678.
4. Máy: tắt Sleep/Hibernate; BIOS "Power on after AC loss" = On; đặt Active hours Windows Update ngoài 21:00–07:00 không được vì giới hạn 18 giờ → đặt **06:00–23:59** và kiểm máy mỗi sáng thứ Hai; nên có UPS.
5. Trên sheet chính: tạo 4 tab mới đúng tiêu đề trong `ops/contract.json` (Content Queue, Lead Hunter, Group Score, Báo cáo ngày) và **thêm cột K "Mã log" vào Nhật Ký SM**. Chạy L1-05 bằng tay: phải ra "không có vấn đề".
6. Import 7 file. Trong mỗi workflow: chọn credential cho node ghi "CHỌN CREDENTIAL" (Google Sheets OAuth2, Google Drive OAuth2; Telegram nếu dùng). Ứng dụng Google OAuth để ở trạng thái **In production** (ở "Testing" token hết hạn sau 7 ngày).
7. Đổi `TOKEN: 'DOI_TOKEN_O_DAY'` trong node "Kiểm tra dữ liệu" (L1-01) và đặt cùng giá trị vào biến môi trường Windows `SMOCK_LOG_TOKEN` của tài khoản chạy Claude.
8. Thứ tự bật (mỗi bước chạy thử 1 ngày rồi mới sang bước sau): **L1-07 → L1-01 → L1-05 → L1-04 → L1-02 + L1-03 → L1-06 → Lead Hunter**. Trước khi bật L1-02, Claude vẫn tự lên lịch như cũ; trước khi bật L1-01, Claude vẫn ghi log kiểu cũ (skill tự chuyển sang DỰ PHÒNG khi webhook không trả lời).

## Kiểm nhanh sau khi cài
```powershell
$env:SMOCK_LOG_TOKEN='<token>'; & "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "Lướt newfeed" "Trang chủ" "thử webhook" "Bỏ qua" 0
```
Phải in `OK L…`; chạy lại lần 2 phải in `(đã ghi trước đó, không ghi lại)`; Nhật Ký SM chỉ có 1 dòng mới.
