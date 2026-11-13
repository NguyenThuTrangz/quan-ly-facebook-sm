# Bàn giao cài đặt n8n cấp 1 (cho agent cấp 2 hướng dẫn tạm, 13/11/2026)

## Hiện trạng máy ADMIN
- n8n **2.35.7** (npm, Node 22.23.5), chạy bằng `C:\n8n\start-n8n.cmd` → http://localhost:5678 (healthz ok). **Chưa là dịch vụ Windows**: đóng cửa sổ/tắt máy là dừng.
- Cấu hình `C:\n8n\.env` (có N8N_ENCRYPTION_KEY — không đưa vào git, không dán vào chat).
- Owner account đã tạo.
- Đã import 8 workflow (L1-01…L1-07 + Smock Lead Hunter), **tất cả đang tắt, chưa có credential** → đó là lý do chạy thử không được.
- L1-01: token đã thay vào node "Kiểm tra dữ liệu"; cùng giá trị nằm ở biến môi trường User `SMOCK_LOG_TOKEN` (mở lại terminal/Claude để có hiệu lực).
- Log "Python 3 is missing" của task runner: bỏ qua (workflow L1 dùng JavaScript).

## Cách agent làm việc với người dùng (BẮT BUỘC)
- Agent **tự mở** mọi trang bằng terminal VS Code: `Start-Process "<url>"` (mở trình duyệt mặc định), hoặc Simple Browser của VS Code (`Ctrl+Shift+P` → "Simple Browser: Show") cho trang localhost. Người dùng **chỉ nhập liệu** (đăng nhập, bấm Allow, dán Client ID/Secret).
- Mỗi bước: agent mở trang → nói đúng 1–2 câu "bấm gì / điền gì" → chờ người dùng báo "xong" → sang bước kế.
- Việc agent tự làm được thì tự làm (copy file, chạy lệnh, kiểm `curl http://localhost:5678/healthz`, mở workflow).
- Danh sách link mở sẵn theo bước:
  | Bước | Lệnh agent chạy |
  |---|---|
  | 1.1 tạo project | `Start-Process "https://console.cloud.google.com/projectcreate"` |
  | 1.2 bật API | `Start-Process "https://console.cloud.google.com/apis/library/sheets.googleapis.com"` rồi `Start-Process "https://console.cloud.google.com/apis/library/drive.googleapis.com"` |
  | 1.3 consent | `Start-Process "https://console.cloud.google.com/auth/overview"` (bản cũ: `/apis/credentials/consent`) |
  | 1.4 OAuth client | `Start-Process "https://console.cloud.google.com/apis/credentials/oauthclient"` |
  | 2 credential n8n | `Start-Process "http://localhost:5678/home/credentials"` |
  | 3 workflow | `Start-Process "http://localhost:5678/home/workflows"` |
  | 4 sheet chính | `Start-Process "https://docs.google.com/spreadsheets/d/1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0/edit"` |
  | n8n chưa chạy | `Start-Process "C:\n8n\start-n8n.cmd"` rồi chờ healthz ok |
- Bước 4 (tạo tab/cột): agent đọc `ops/contract.json`, in sẵn **dòng tiêu đề dạng TSV** rồi `Set-Clipboard` → người dùng chỉ bấm ô A1 của tab mới và Ctrl+V.

## Việc cần làm theo thứ tự

### 1. Google Cloud OAuth (người dùng tự đăng nhập, agent chỉ hướng dẫn)
1. https://console.cloud.google.com → tạo project (vd `smock-n8n`).
2. APIs & Services → Library → bật **Google Sheets API** và **Google Drive API**.
3. OAuth consent screen: User type **External**, điền tên app + email hỗ trợ; Scopes để mặc định; **Publish app → In production** (để Testing thì token hết hạn sau 7 ngày). Cảnh báo "unverified app" lúc đăng nhập: bấm Advanced → Go to app.
4. Credentials → Create credentials → **OAuth client ID** → loại **Web application** → Authorized redirect URI: `http://localhost:5678/rest/oauth2-credential/callback` → lưu Client ID + Client Secret.

### 2. Tạo credential trong n8n
1. n8n → Overview → **Create → Credential**.
2. **Google Sheets OAuth2 API**: dán Client ID/Secret → **Sign in with Google** bằng tài khoản Google có quyền sửa sheet chính `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0` → Save.
3. Lặp lại cho **Google Drive OAuth2 API** (cùng Client ID/Secret).
4. (Tuỳ chọn) Telegram API cho L1-04 nếu muốn gửi báo cáo nhóm.

### 3. Gắn credential vào từng workflow
Mở từng workflow → mọi node có chữ **"CHỌN CREDENTIAL"** hoặc biểu tượng cảnh báo đỏ → chọn credential vừa tạo → Save. Kiểm cả node Sheets lẫn Drive (L1-03 cần Drive để tải ảnh).

### 4. Chuẩn bị sheet chính (trước khi chạy L1-05/L1-01)
Theo `ops/contract.json` (tên tab và tiêu đề cột phải khớp từng chữ):
- Tạo 4 tab: **Content Queue**, **Lead Hunter**, **Group Score**, **Báo cáo ngày**, hàng 1 = đúng danh sách cột trong contract.
- Tab **Nhật Ký SM**: thêm cột **K "Mã log"**.
- Chạy **L1-05** bằng tay (Execute workflow) → phải ra "không có vấn đề". Báo lỗi tab/cột nào thì sửa đúng tên đó.

### 5. Bật dần (mỗi bước chạy thử 1 ngày)
**L1-07 → L1-01 → L1-05 → L1-04 → L1-02 + L1-03 → L1-06 → Lead Hunter.** Bật = công tắc Active ở góc trên workflow.
- L1-07: điền URL ping healthchecks.io nếu dùng (không thì bỏ node ping).
- L1-01 kiểm nhanh (PowerShell mới):
  `& "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "Lướt newfeed" "Trang chủ" "thử webhook" "Bỏ qua" 0`
  → phải in `OK L…`; chạy lần 2 → `(đã ghi trước đó, không ghi lại)`; Nhật Ký SM chỉ thêm 1 dòng (xoá dòng thử sau đó).
- L1-06 cần repo `smock-level2-copilot` clone sẵn trên máy và git đăng nhập được.

### 6. Dịch vụ Windows (sau khi mọi thứ chạy ổn)
NSSM: `nssm install n8n "C:\Program Files\nodejs\node.exe" "%APPDATA%\npm\node_modules\n8n\bin\n8n" start`; AppDirectory `C:\n8n`; AppEnvironmentExtra = các dòng trong `.env`; **Log on = tài khoản Windows `admin` (người dùng tự nhập mật khẩu)**; Startup Automatic; Exit action Restart. Tắt cửa sổ `start-n8n.cmd` trước khi `nssm start n8n` (trùng cổng 5678). Máy: tắt Sleep/Hibernate.

## Lỗi hay gặp
- Workflow báo "Credentials not set / Node has no credentials" → chưa làm bước 3.
- `redirect_uri_mismatch` → URI ở bước 1.4 sai (phải đúng `http://localhost:5678/rest/oauth2-credential/callback`).
- `Unable to parse range` / không thấy tab → tên tab sheet lệch contract (bước 4).
- Execute Command bị tắt → kiểm `.env` có `NODES_EXCLUDE=[]` và n8n được khởi động bằng `start-n8n.cmd` (đọc `.env`).
- Workflow lịch (Schedule) không chạy khi đang tắt Active hoặc n8n không chạy lúc đến giờ.

## Giới hạn an toàn
Agent không nhập mật khẩu/2FA Google hay Windows thay người dùng; không đưa encryption key, token, Client Secret lên git/chat.
