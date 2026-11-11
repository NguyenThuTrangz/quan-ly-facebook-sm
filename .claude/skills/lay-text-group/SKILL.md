---
name: lay-text-group
description: TẠM DỪNG — chỉ chạy khi người dùng đã xác nhận trong chat cho phép. Cấp 3 lấy text nội quy + bài gần nhất của một Facebook group (đã đăng nhập) và lưu thành file cho cấp 2 (Copilot) chấm điểm.
---

# Lấy text group cho cấp 2 chấm

> **TẠM DỪNG (11/11/2026).** Có thể trái Điều khoản thu thập dữ liệu tự động của Meta (cần văn bản cho phép). Không tự chạy khi thấy dòng "Chờ lấy text". Chỉ chạy khi người dùng nói rõ trong chat là cho phép; nếu không, nhờ người dùng chép tay nội quy + vài bài vào file `data/group-text/gNN.txt` rồi mới giao cấp 2.

Claude **không tự chấm** ở đây (tốn token); chỉ lấy text sạch rồi giao cho cấp 2.

1. Đọc tab **Group Score** (gviz CSV trên Edge SM03): các dòng `Trạng thái = Chờ lấy text`, tối đa 8 group mỗi lần.
2. Với mỗi group, mở bằng trình duyệt nick **đã join group đó** (xem tab Join Group SM):
   - `get_page_text` trang `<link>/about` → phần nội quy, mô tả, số thành viên, quyền riêng tư.
   - Mở `<link>` (Most relevant / New activity), cuộn đến khi có khoảng 20 bài; lấy text bằng JS, mỗi bài: ngày tương đối, 300 ký tự đầu, số cảm xúc, số comment.
   - **Bỏ tên và link profile người đăng**, chỉ giữ nội dung bài. Không lấy SĐT/email nếu bài có.
3. Lưu `C:\smock-level2-copilot\data\group-text\gNN.txt` (NN = STT 2 chữ số), dạng:
   ```
   # Group NN · <tên group> · lấy ngày <yyyy-mm-dd>
   ## Nội quy / about
   ...
   ## 20 bài gần nhất
   [1] 2 ngày trước · 5 cảm xúc · 2 comment · <nội dung 300 ký tự>
   ...
   ```
4. Cập nhật trạng thái qua webhook (một lệnh mỗi group):
   `Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/smock-log -Headers @{'X-Smock-Token'=$env:SMOCK_LOG_TOKEN} -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes('{"type":"status","tab":"Group Score","row":<dòng>,"status":"Chờ chấm","note":"data/group-text/gNN.txt"}'))`
   và ghi đường dẫn `data/group-text/gNN.txt` vào cột **File text** (n8n L1-06 sẽ đẩy file sang cấp 2 lúc 22:15).
5. Không vào được group (chờ duyệt, bị chặn) → để nguyên `Chờ lấy text`, ghi chú lý do bằng `"note"`.
6. Báo 1 dòng: "✅ Lấy text 6 group, 2 chưa vào được."
