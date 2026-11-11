# Kiến trúc vận hành 3 cấp theo ca — nhánh Smock

Mục tiêu: việc lặp lại chạy ở cấp rẻ nhất có thể; Claude (đắt nhất) chỉ làm việc cần trình duyệt đã đăng nhập và phán đoán, trong giờ hành chính.

| Cấp | Chạy ở đâu | Giờ chạy | Làm gì | Không làm gì |
| --- | --- | --- | --- | --- |
| **1 · n8n** | PC công ty (cùng máy với Claude), chạy 24/24 | Cả ngày đêm | Lịch, ghi log, tìm lead, chuẩn bị gói bài, báo cáo, đèn sức khỏe, sao lưu, cầu nối sang cấp 2 | Không thao tác Facebook đăng nhập |
| **1.5 · n8n + LLM rẻ** | Như cấp 1 | Đêm | Phân loại ý định mua (Lead Hunter) | Không ra quyết định gửi gì cho khách |
| **2 · GitHub Copilot** | VS Code trên máy khác, repo `smock-level2-copilot` | Linh hoạt (tối hoặc sáng sớm) | Phái sinh caption, chấm group từ text, báo cáo tuần, sửa workflow/script | Không đăng nhập Facebook, không gửi gì ra ngoài |
| **3 · Claude + Chrome** | PC công ty | Giờ hành chính | Đăng bài, tim/tương tác, join, kết bạn, đọc comment/inbox, kiểm hiển thị chéo, trả lời lead đã duyệt, xử lý sự cố | Không tự soạn lịch, không gõ log vào sheet, không tự tải ảnh |

## Một ngày điển hình

```
22:00  C1  Chuẩn bị gói bài ngày mai (caption + ảnh JPG vào anh-dang-bai/Kxxx)      → tab Content Queue
22:15  C1  Xuất việc cho cấp 2 (bài cần phái sinh, text group cần chấm) → repo cấp 2 inbox/
00:00  C1  Xoá dữ liệu cũ, sao lưu workflow
00:00–06:00 C1.5 Lead Hunter 6 giờ/lần                                                  → tab Lead Hunter "Chờ duyệt"
06:00  C2  (nếu máy cấp 2 bật) Copilot xử lý inbox/ → outbox/, push
06:30  C1  Kéo outbox/ về, ghi caption phái sinh + điểm group lên sheet
07:00  C1  Sinh Lịch SM hôm nay (08:30–17:00, giờ ngẫu nhiên, xoay vòng nick)
08:30–17:00 C3 Claude chạy lịch theo cụm từng nick; mỗi việc xong gọi webhook ghi log (1 lệnh)
12:00, 17:00 C3 Xử lý lead "Chờ duyệt" (người dùng duyệt từng lead)
18:00  C1  Báo cáo ngày + đèn sức khỏe                                                  → tab Báo cáo ngày, Telegram nhóm MKT
mỗi 10 phút C1 Heartbeat (báo nếu n8n chết)
```

## Hợp đồng dữ liệu (Google Sheet chính `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0`)

Mọi cấp chỉ bàn giao qua **trạng thái** trên sheet (hoặc file trong repo cấp 2), không qua tin nhắn.

| Tab | Ai ghi | Ai đọc | Trạng thái |
| --- | --- | --- | --- |
| Lịch SM (có sẵn) | C1 sinh dòng; C1 webhook ghi `Done` + URL | C3 | H: `Chờ` → `Done` / `Bỏ qua` / `Lỗi` |
| Nhật Ký SM (có sẵn) | C1 webhook | C1 báo cáo, Radar | — |
| Content Queue (mới) | C1 (xếp, chuẩn bị), C2 (caption phái sinh) | C3 khi đăng | `Chưa dùng` → `Đã xếp` → `Gói sẵn` → `Đã đăng` |
| Lead Hunter (mới) | C1.5 | Người duyệt, C3 | `Chờ duyệt` → `Loại` / `Đã trả lời` → `Khách phản hồi` → `Chuyển Sale` |
| Group Score (mới) | C3 lấy text, C2 chấm | C1 lịch, C3 trước khi đăng | `Chờ lấy text` → `Chờ chấm` → `Đã chấm` |
| Báo cáo ngày (mới) | C1 | Mọi người | — |

### Cột các tab mới (dòng 1 phải đúng tên)
- **Content Queue:** `Mã content, Nguồn, Loại, Caption, Link ảnh, Trạng thái, Mã bài, Ngày dự kiến, Nick, Thư mục gói, Ghi chú`
- **Lead Hunter:** xem `n8n/README.md`.
- **Group Score:** `STT, Tên group, Link, Ngày lấy text, File text, Cổng loại, ICP, Cho bán, Sôi động, Tương tác, Người mua, Thị trường, Ít rác, Tổng, Tier, Bằng chứng, Trạng thái, Người duyệt`
- **Báo cáo ngày:** `Ngày, Nick, Việc xong, Việc lỗi, Bài tường, Bài group, Join, Kết bạn, Tương tác, Đèn, Ghi chú`

### Webhook ghi log (cấp 1, chỉ nghe trên máy này)
`POST http://localhost:5678/webhook/smock-log` · header `X-Smock-Token: <SMOCK_LOG_TOKEN>`

```json
{"ma_tk":"SM01","loai_viec":"Tim story","noi":"Story trang chủ","noi_dung":"story tim 2/3","ket_qua":"Xong","trang_thai":"Xong","so_luong":2,"che_do":"","lich_row":121,"url":""}
```
`loai_viec` ∈ `Tim story, Lướt newfeed, Đăng bài, Chấp nhận kết bạn, Tương tác newsfeed, Join group, Tương tác group, Kết bạn` · `trang_thai` ∈ `Xong, Một phần, Không làm được, Bỏ qua`. Có `lich_row` thì webhook tự ghi `Done` (hoặc `Lỗi`) và URL vào Lịch SM dòng đó. Trả `{"ok":true,"nhat_ky_row":…}`.

## Quy tắc chung
- Không lưu SĐT/email khách ở bất kỳ tab nào.
- Cấp 1 và 2 không bao giờ thao tác tài khoản Facebook; mọi thao tác Facebook là cấp 3, giờ hành chính, có giới hạn theo CLAUDE.md.
- Token webhook, API key để trong n8n Credentials / biến môi trường, không ghi vào repo.
