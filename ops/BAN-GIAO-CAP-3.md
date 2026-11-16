# Bàn giao cấp 3 (Claude + trình duyệt) — 16/11/2026

Agent mới đọc file này **sau** `CLAUDE.md` và `tien-do.md`. Trả lời người dùng (Việt TTS) bằng tiếng Việt, cực ngắn, không chụp màn hình trừ khi bắt buộc.

## 1. Hệ thống đang chạy thế nào
```
21:30  n8n L1-02 sinh Lịch SM ngày làm việc kế tiếp (tab Lịch SM, cột J ghi "luồng 1/2")
22:00  n8n L1-03 gói bài: anh-dang-bai\Kxxx\caption.txt + 01.jpg…, ghi "Gói sẵn n/n ảnh" vào cột J dòng lịch
22:15  n8n L1-06 gửi việc caption sang cấp 2 (repo C:\smock-level2-copilot, inbox/)
05:30  Task Scheduler máy này chạy Copilot CLI (cấp 2) xử lý inbox → outbox
06:30  n8n L1-06 kéo outbox về: caption phái sinh vào tab Pool Content SM ("… – chờ duyệt")
06:30 / 21:50  n8n L1-05 kiểm tiêu đề cột + việc kẹt     18:00  L1-04 tóm tắt ngày
08:30–17:00  CẤP 3 (bạn): chạy Lịch SM trên Facebook, ghi log bằng webhook (L1-01)
```
- Đang bật: L1-01, L1-02, L1-03, L1-04, L1-05, L1-06, L1-07. **Tắt**: Smock Lead Hunter (thiếu SERPER_API_KEY + credential OpenAI API/OpenRouter).
- n8n tự mở khi đăng nhập Windows (Task Scheduler "Smock n8n" → `C:\n8n\chay-n8n-mai.cmd`, log `C:\n8n\n8n.log`). Gõ tay: `n8n` trong cmd/PowerShell. Kiểm: `http://localhost:5678/healthz`.
- **Khi L1-02 đang bật: KHÔNG tự "lên lịch hôm nay".** Chỉ chạy lịch n8n đã sinh.

## 2. Việc hằng ngày của cấp 3
1. Người dùng gõ "chạy lịch luồng 1" (phiên 2: "luồng 2"). Đọc Lịch SM ngày hôm nay (gviz), chỉ làm dòng có J chứa đúng luồng của mình, H = "Chờ", G = "Có".
2. Mỗi dòng: skill `chay-lich-sm`. Bài đăng có mã `Kxxx` → mở `anh-dang-bai\Kxxx\` (caption.txt + ảnh). J không có "Gói sẵn" → Bỏ qua, báo 1 dòng.
3. Ghi log **1 lệnh** sau mỗi việc: `& "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "<Loại việc>" "<Nơi>" "<Nội dung>" "<Trạng thái>" <Số lượng> -LichRow <dòng> [-Url <link> -CheDo "Công khai"]`. In `OK L…` là xong (tự ghi Nhật Ký SM + Done/URL vào Lịch SM). In `DỰ PHÒNG` → n8n không chạy, ghi kiểu cũ (mục 2b của skill) và báo người dùng.
4. Đăng bài xong: đăng ký mã Kxxx vào Smock Radar (skill `day-du-lieu-radar`). Cảnh báo FB → ghi Radar trước, báo sau.

## 3. Sửa workflow n8n (chỉ khi người dùng yêu cầu)
- Sửa **`ops/build_level1.py`** (không sửa tay JSON, không sửa trong giao diện n8n) → `py -I -X utf8 ops/build_level1.py` → `node ops/test_level1.js` (42 phép thử, phải 0 lỗi) → `py -I -X utf8 ops/cai_dat_n8n.py [L1-0x]` (tự gắn credential + token, import đè, tự bật lại workflow đang bật) → người dùng khởi động lại n8n.
- Tab dùng: chỉ tab ĐANG CÓ, mô tả ở `ops/contract.json`. Không bắt người dùng tạo tab mới.
- Chạy thử workflow bằng CLI khi n8n đang chạy: đặt `N8N_RUNNERS_BROKER_PORT=5689` và `N8N_PORT=5699`; CLI cần node Manual Trigger (tạo bản sao tạm, chạy xong xoá).
- Bẫy đã gặp: `toLocaleString('sv-SE')` hỏng trong n8n → dùng `isoOf(vnNow())`; lệnh Execute Command chạy qua `cmd` → nối lệnh bằng `&`, không dùng `;`.
- Đồng bộ với Copilot: GitHub là bản gốc. Commit + push ngay sau khi sửa; Copilot `git pull` trước khi làm.

## 4. Tồn đọng (cần người dùng quyết/làm)
| Việc | Ghi chú |
|---|---|
| Add Friend STT 1–15 đã gửi lời mời 26/10 nhưng cột C vẫn "Chưa Add" | n8n đã xếp lại STT 1–8 cho 17/11 (C2:C9 "Đã xếp …"). Người dùng sửa C thành đã gửi rồi xoá các dòng "kết bạn" trùng của 17/11 |
| SM02 có bị hạn chế đăng group không | Nếu có: cột F tab Tài khoản ghi "Hoạt động - hạn chế group" |
| SM04 đang "Hoạt động" nhưng không có trình duyệt trên máy này | Lịch 17/11 có 4 việc SM04 ở luồng 2 |
| Kho content KE gần hết (dùng đến CG30) | Cấp 2 phái sinh tối đa 10 bài/đêm từ bài đã đăng ≥ 7 ngày; người dùng duyệt ở Pool Content SM |
| Tắt Sleep/Hibernate, Windows Update active hours 06:00–23:59 | Người dùng tự làm (cài đặt hệ thống) |
| Task Scheduler cấp 2 (05:30): tick "Run whether user is logged on or not" | Người dùng tự nhập mật khẩu Windows |
| Lead Hunter | SERPER_API_KEY + credential OpenAI API (Base URL https://openrouter.ai/api/v1) → `py -I -X utf8 ops/cai_dat_n8n.py lead` |
| Repo cấp 2 đang public | Nên chuyển private (đã có quyền collaborator) |
| Lịch 10–11/11 còn nhiều dòng "Chờ" (dòng 107–192) | Bản cũ, bỏ qua |

## 5. Không được làm
Nhập mật khẩu/2FA; đọc tab "CRM tài khoản" (có mật khẩu/2FA); đổi cài đặt bảo mật hệ thống; đưa encryption key/token/API key lên git hay chat; seeding chéo nick; chạy skill `lay-text-group` khi người dùng chưa cho phép.
