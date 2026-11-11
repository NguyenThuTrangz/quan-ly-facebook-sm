---
name: tra-loi-lead
description: Xử lý lead do n8n "Smock Lead Hunter" tìm được (tab Lead Hunter trên sheet chính) — đọc lead chờ duyệt, soạn câu trả lời, chờ người dùng duyệt, rồi comment hoặc nhắn tin bằng tài khoản được chỉ định và ghi kết quả. Dùng khi người dùng nói "xử lý lead", "trả lời lead hôm nay", "xem Lead Hunter".
---

# Trả lời lead từ Smock Lead Hunter

Nguồn lead: tab **Lead Hunter** của sheet chính `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0` (n8n ghi vào, mỗi dòng một bài công khai có người đang tìm xưởng smock). Thông tin xưởng để trả lời: mục "Thông tin từ Sale" trong CLAUDE.md (MOQ 15/mẫu, mock-up 2D miễn phí…).

## Nguyên tắc (không đổi được)
- **Không gửi gì khi người dùng chưa duyệt đúng câu đó cho đúng lead đó.** Duyệt một lead không có nghĩa là duyệt lead khác.
- **Tối đa 5 câu trả lời/ngày cho cả đội** trong 2 tuần đầu; tăng chỉ khi người dùng quyết.
- Mỗi lead **một câu viết riêng**, không gửi cùng một nội dung cho nhiều người (chính sách Spam của Meta).
- **Chỉ trả lời người đang công khai tìm nhà cung cấp.** Không nhắn người chỉ khen, hỏi mua lẻ, hay không hỏi gì.
- Ưu tiên trả lời bằng **profile sales thật hoặc Fanpage K-Embroidery**; dùng tài khoản khác chỉ khi người dùng chỉ định.
- Tự giới thiệu đúng là K-Embroidery. Không giả làm khách, không khen hộ, không nhờ nick khác vào comment.
- Group cấm vendor/solicitation trong comment (đọc `/about` trước) → không comment; báo người dùng, chỉ nhắn tin nếu người dùng duyệt.
- Khách không trả lời sau 1 lần nhắc (7 ngày) → dừng, ghi "Không phản hồi". Không nhắc lần 3.
- FB báo hạn chế / "can't use this feature" → dừng ngay, ghi sự cố vào Radar (`day-du-lieu-radar`).
- Không ghi số điện thoại, email của khách lên sheet chung hay Radar; nếu khách đưa, chuyển thẳng cho Sale qua WhatsApp hotline.

## Các bước
1. **Đọc lead chờ duyệt** (Edge SM03, trong tab sheet):
   `fetch('https://docs.google.com/spreadsheets/d/1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0/gviz/tq?tqx=out:csv&sheet=Lead%20Hunter').then(r=>r.text())`
   Lấy các dòng `Trạng thái = Chờ duyệt`, mới nhất trước, tối đa 10.
2. **Mở từng link**, kiểm tra: bài còn không, có phải người mua thật (không phải xưởng khác), đã có ai trong đội trả lời chưa. Không đạt → `Trạng thái = Loại` + lý do ngắn.
3. **Soạn câu trả lời** từ cột "Gợi ý trả lời", sửa theo bài cụ thể (tiếng Anh, tối đa 3 câu, có hỏi khách cần hàng khi nào). Chọn kênh: comment (group cho phép) hoặc tin nhắn.
4. **Trình người dùng một bảng ngắn**: link · khách cần gì · kênh · tài khoản sẽ dùng · nội dung. Chờ người dùng trả lời "Gửi 1, 3" (hoặc sửa). Không có chữ "Gửi" cho lead nào thì không gửi lead đó.
5. **Gửi** bằng tài khoản đã duyệt (mở đúng trình duyệt theo bảng deviceId trong `chay-lich-sm`). Dán nội dung bằng paste event, kiểm tra hiển thị rồi mới bấm.
6. **Ghi kết quả**:
   - Sheet tab Lead Hunter: `Trạng thái = Đã trả lời`, `Người xử lý = <mã tài khoản>`, `Ghi chú = comment|inbox + giờ`.
   - Radar (`day-du-lieu-radar`): một dòng `{"type":"signal","post":"","source":"hunt","author":"<tên hiển thị>","authorUrl":"<link profile nếu công khai>","text":"<trích đoạn bài của khách>"}` để Radar chấm và đếm.
   - Khi khách trả lời lại: ghi `signal` `source:"inbox"` như bình thường; Radar chấm QI thì chuyển Sale (mục 2b của `day-du-lieu-radar`).
7. **Báo 1 dòng**: "✅ Lead: 3 đã trả lời, 2 loại, 5 còn chờ."

## Trạng thái dùng trong cột Trạng thái
`Chờ duyệt` (n8n ghi) → `Loại` | `Đã trả lời` → `Khách phản hồi` → `Chuyển Sale` | `Không phản hồi`.
