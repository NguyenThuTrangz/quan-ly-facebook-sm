# Smock Lead Hunter (n8n)

Tìm bài **công khai** có người đang tìm xưởng smock (boutique, shop online, brand ở US/EU), chấm ý định mua bằng LLM, rồi đưa vào hàng đợi duyệt. Người duyệt xong mới trả lời, theo skill `.claude/skills/tra-loi-lead`.

Chuyển từ workflow "VN B2B Website Lead Hunter" (tìm khách làm website ở VN) sang thị trường smock. Phần khung giữ nguyên: Serper → chuẩn hoá → lọc từ khoá xấu → bỏ trùng → LLM phân loại → LLM trích chi tiết → lưu Postgres, có chu kỳ xoá dữ liệu.

## Luồng

```
Lịch 6 giờ/lần → 10 truy vấn tiếng Anh (Serper, gl=us, 7 ngày)
  → Chuẩn hoá → Bỏ bài phía người bán / đồ cũ / tuyển dụng → Bỏ bài đã quét trong 14 ngày
  → Giới hạn 20 bài/chu kỳ → LLM phân loại (HIGH / LOW / SPAM)
  → HIGH, confidence ≥ 0.6, buyer_signal → LLM trích: cần gì, loại khách, số lượng/hạn, gợi ý trả lời
  → Postgres (lead_opportunities) + Google Sheets tab "Lead Hunter" (Chờ duyệt) + Telegram (tuỳ chọn)
Người duyệt → bot trả lời bằng tài khoản được chỉ định (tối đa 5/ngày) → ghi Radar
```

## Đã đổi so với bản gốc

| Phần | Bản gốc (website VN) | Bản Smock |
| --- | --- | --- |
| Truy vấn | "cần làm website"…, gl=vn, 24h, 15 phút/lần | "looking for smocked supplier", "ISO wholesale smocked"…, gl=us, 7 ngày, 6 giờ/lần |
| Từ khoá loại | tuyển dụng, pass đồ, sỉ lẻ… | we manufacture, supplier here, preloved, destash, giveaway, hiring… |
| Phân loại | Người thuê làm web | Người mua sỉ smock; phụ huynh mua cho con = LOW |
| Trích xuất | có lấy SĐT | **không lấy SĐT/email**; thêm buyer_type, quantity_or_deadline; gợi ý trả lời tiếng Anh, chỉ dùng thông tin thật của xưởng |
| Đầu ra | Telegram "inbox ngay 10 phút" | Thêm Google Sheets tab Lead Hunter (Chờ duyệt); Telegram tuỳ chọn, ghi rõ "không gửi tự động" |
| Sửa lỗi | Telegram chatId cứng | dùng `{{ $json.telegramSalesChatId }}` từ node Set |

## Cài đặt (một lần)

**Không dùng Postgres (sửa 16/11/2026, `ops/sua_lead_hunter.py`)**: chống trùng bằng link cột B tab **Lead Hunter** có sẵn + danh sách bài đã quét 14 ngày lưu trong chính workflow (chỉ ghi nhớ khi chạy theo lịch).

1. Tạo key Serper (serper.dev) → đặt biến môi trường User `SERPER_API_KEY`.
2. Tạo key OpenRouter (openrouter.ai) → trong n8n tạo credential **OpenAI API**: API Key = key OpenRouter, Base URL = `https://openrouter.ai/api/v1`.
3. Chạy `py -I -X utf8 ops/cai_dat_n8n.py lead` → tự gắn credential Google Sheets + OpenAI API, điền Serper key, import đè đúng workflow.
4. Telegram: 2 node đang tắt sẵn; muốn dùng thì điền chat ID nhóm MKT/Sale ở node **Set Telegram Chat ID**, tạo credential Telegram, bật 2 node.
5. Chạy thử 1 lần bằng tay, xem tab Lead Hunter có dòng mới, rồi mới Active.

## Giới hạn cần biết
- Google chỉ index một phần bài Facebook công khai; **bài trong group kín không bao giờ hiện**. Lead Hunter bổ sung cho bot đọc group, không thay thế.
- Reddit, blog, diễn đàn boutique cũng được quét; tuần đầu xem nguồn nào ra lead thật rồi chỉnh truy vấn.
- Model free trên OpenRouter có thể chậm/lỗi; bài đã gửi LLM được ghi nhớ 14 ngày nên bài lỗi sẽ không được thử lại.
- Lead nằm lại trên tab Lead Hunter (không tự xoá); danh sách bài đã quét tự quên sau 14 ngày.
