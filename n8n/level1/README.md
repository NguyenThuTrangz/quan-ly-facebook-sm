# Cấp 1 — 7 workflow n8n (PC công ty, chạy 24/24)

| File | Giờ chạy | Làm gì | Ai dùng kết quả |
| --- | --- | --- | --- |
| `L1-01-webhook-ghi-log.json` | Luôn nghe (localhost) | Nhận 1 lệnh từ Claude → ghi Nhật Ký SM, ghi Done/URL vào Lịch SM, cập nhật trạng thái tab khác. Chống ghi trùng bằng cột **Mã log** | Cấp 3, báo cáo |
| `L1-02-sinh-lich.json` | 21:30 CN–T6 | Sinh Lịch SM ngày làm việc kế tiếp: 08:30–17:00, 2 luồng song song, bài group chỉ vào group A/B đã join, cùng nick cách ≥ 60 phút, cả đội ≥ 6 phút, không đăng lại group trong 3 ngày, đèn Đỏ/Vàng tự giảm; giữ chỗ content (mã Kxxx) và người kết bạn | Cấp 3 |
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
   N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false
   N8N_LISTEN_ADDRESS=127.0.0.1
   N8N_SECURE_COOKIE=false
   EXECUTIONS_DATA_PRUNE=true
   EXECUTIONS_DATA_MAX_AGE=336
   ```
   `NODES_EXCLUDE=[]` bật lại Execute Command (mặc định tắt từ n8n 2.0). `N8N_LISTEN_ADDRESS=127.0.0.1` để webhook chỉ nghe trong máy.
3. Dịch vụ Windows bằng NSSM: `nssm install n8n "C:\Program Files\nodejs\n8n.cmd"`, đặt AppDirectory `C:\n8n`, AppEnvironmentExtra từ file `.env`, Log on = tài khoản Windows đang chạy Claude, Startup = Automatic, Exit actions = Restart. `nssm start n8n` → mở http://localhost:5678.
4. Máy: tắt Sleep/Hibernate; BIOS "Power on after AC loss" = On; đặt Active hours Windows Update ngoài 21:00–07:00 không được vì giới hạn 18 giờ → đặt **06:00–23:59** và kiểm máy mỗi sáng thứ Hai; nên có UPS.
5. **Không tạo tab mới.** Workflow bám theo tab đang có (mô tả ở `ops/contract.json`, đọc thật ngày 16/11/2026):
   - Content: workbook KE tab `3. CONTENT GROUP` (mã `CGn`) + tab `Pool Content SM` (mã `PCn`). Content đã dùng và mã bài `Kxxx` đọc từ cột F/J tab `Lịch SM` (vd `đăng group K123 (CG13) → group 5`).
   - Tier group: tab `Group Score` nếu đã chấm, chưa chấm thì cột G "Tier" tab `Join Group SM`.
   - Đèn sức khoẻ: tính thẳng từ `Nhật Ký SM` 2 ngày gần nhất. Nick chỉ đăng tường: ghi thêm "hạn chế group" vào cột F tab `Tài khoản` (vd `Hoạt động - hạn chế group`).
   - Gói bài (L1-03) ghi "Gói sẵn n/n ảnh" vào cột J của dòng Lịch SM. Caption phái sinh cấp 2 ghi vào `Pool Content SM` với Phân loại "Phái sinh từ CGn – chờ duyệt" (xoá chữ "chờ duyệt" là được dùng).
   - Cột K "Mã log" của Nhật Ký SM không bắt buộc có tiêu đề (L1-01 tự ghi mã vào cột K).
6. Tạo credential **Google Sheets OAuth2** và **Google Drive OAuth2** trong n8n (ứng dụng Google OAuth để **In production**). Đặt biến môi trường User `SMOCK_LOG_TOKEN`. Rồi chạy **`py -I -X utf8 ops/cai_dat_n8n.py`**: tự gắn credential + token vào mọi node, import đè đúng workflow cũ (không sinh bản trùng), thêm quyền ghi file vào `.env`. **Không cần mở từng node chọn lại credential.** Sửa `ops/build_level1.py` xong thì: `py -I -X utf8 ops/build_level1.py` → `node ops/test_level1.js` → chạy lại `cai_dat_n8n.py`.
7. Sau khi `cai_dat_n8n.py` báo đã thêm `.env`: tắt n8n (Ctrl+C) và gõ lại `n8n`.
8. Thứ tự bật (mỗi bước chạy thử 1 ngày rồi mới sang bước sau): **L1-07 → L1-01 → L1-05 → L1-04 → L1-02 + L1-03 → L1-06 → Lead Hunter**. Trước khi bật L1-02, Claude vẫn tự lên lịch như cũ; trước khi bật L1-01, Claude vẫn ghi log kiểu cũ (skill tự chuyển sang DỰ PHÒNG khi webhook không trả lời).

## Kiểm nhanh sau khi cài
```powershell
$env:SMOCK_LOG_TOKEN='<token>'; & "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "Lướt newfeed" "Trang chủ" "thử webhook" "Bỏ qua" 0
```
Phải in `OK L…`; chạy lại lần 2 phải in `(đã ghi trước đó, không ghi lại)`; Nhật Ký SM chỉ có 1 dòng mới.
