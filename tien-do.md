# Tiến độ chạy lịch SM

## 2026-11-16 (bàn giao cấp 3 → xem `ops/BAN-GIAO-CAP-3.md`)
- n8n 2.35.7 chạy ở máy này, tự mở khi đăng nhập (Task Scheduler "Smock n8n"). Bật L1-01…L1-07; Lead Hunter tắt (thiếu key).
- **L1-02 đã bật → không tự lên lịch nữa.** Lịch 17/11 (dòng 193–234, 42 việc, 2 luồng) do n8n sinh. Log qua webhook (`ghi-log-webhook.ps1`), đã thử OK (dòng thử ở cuối Nhật Ký SM cần xoá).
- Cầu nối cấp 2 chạy trọn lần đầu: 6 caption phái sinh CG1/CG2 vào Pool Content SM dòng 2–7, người dùng đã duyệt (PC1–PC6).
- Mã bài kế tiếp do n8n tự tính từ Lịch SM (17/11 dùng K123–K138). Content KE đã xếp đến CG30.
- Tồn đọng: Add Friend STT 1–15 đánh dấu đã gửi; SM02 "hạn chế group"?; SM04 không có trình duyệt máy này.
- L1-03 đã gói 10/16 bài ngày 17/11 (48 ảnh). Thiếu ảnh: K126, K127, K130, K132, K137, K138.
- **Dừng tối 16/11, tắt máy.** Sáng 17/11 đọc mục 0 của `ops/BAN-GIAO-CAP-3.md` trước khi chạy lịch.

## 2026-11-11
Toàn bộ việc dở 10/11 (gồm SM02 — người dùng xác nhận SM02 **không** bị checkpoint/shadowban) đã dồn sang Lịch SM dòng **140–162**, 09:25–14:45; CG2 đổi sang group 2 (group 21 cấm quảng cáo). Dòng 110–139 ngày 10/11 còn "Chờ" là bản cũ, bỏ qua.
- 09:12–10:00 chạy dồn: Done 140–142, 144–150, 152–154, 156, 158. Bài: K117 (SM01 group 1 CG1), K118 (SM01 tường CG8), K119 (SM03 tường CG12 — folder ảnh LILY 2 bị từ chối truy cập).
- **SM02: đăng bài group vẫn bị "confirm your identity"** (Account Status vẫn looks good; like/lướt được) → đã ghi health lên Smock Radar; dừng đăng/join/kết bạn SM02. Còn Chờ: 143, 151, 157, 159, 160, 161.
- Còn hẹn giờ: 10:40 SM03 CG6 → group 27 (dòng 155); 11:47 SM01 CG4 → group 5 thay 16 (dòng 162; group 16 cat resale).
- SM02 đăng tường được (chỉ group bị chặn): K120 (CG9, dòng 151), K121 (CG10, dòng 159). SM02 ngâm — chỉ đăng tường + tương tác, chưa vào group. Còn Chờ SM02: 143, 157, 160, 161.
- Nhật Ký SM dòng trống kế tiếp: **118**. Mã Radar kế tiếp: **K122**.
- **10:30 lọc group trên Smock Radar**: chấm 30 group (tier A: 1, 2, 25, 43, 5; B: 10, 20, 32, 49, 27, 17, 50, 54, 15, 29, 30, 53, 12; còn lại Loại), đã ghi Tier/Điểm vào Join Group SM cột G–H. Engage/buyer đang ước lượng.
- Lịch mới dòng 163–175 (join group A/B + tim story + lướt + tương tác group mới, chưa đăng bài vào group mới). Đã làm (Excel đã ghi; **Nhật Ký SM + cột H chưa dán**, hàng đợi ở `tools\hang-doi-log.tsv` → chạy `tools\dan-log.ps1` rồi dán từ A118): 163 SM03 tim story, 164 SM01 join 25+10, 166 SM01 tim story, 172 SM01 tương tác group 25, 169 SM01 lướt (~2 phút, chưa đủ 4).
- 14:05: đã dán log tới Nhật Ký SM dòng 122 (kế tiếp **123**), H163–175 cập nhật, Join Group SM D11/D26 = đã join. Hàng đợi trống. Hẹn giờ 155 (SM03 CG6→g27) và 162 (SM01 CG4→g5) trễ >30 phút, chưa làm.
- Còn lại: 155, 162, 165 SM02 join 43/20/32, 167 SM02 tim story, 168 SM03 join 5, 170 SM03 lướt, 171 SM02 group 43, 173 SM03 group 5, 174–175 chấp nhận All; lọc list bạn bè (chân dung chủ boutique/smock) → Add Friend. Join Group SM chưa cập nhật SM01 cột D cho group 25, 10.

Cập nhật mỗi khi dừng ca. Ngày mới "lên lịch hôm nay" thì **ưu tiên dồn các việc chưa làm dưới đây** trước.

## 2026-11-10 (dừng 17:5x — hết giờ hành chính, người dùng bảo tạm dừng)

**Đã xong (H = Done):** dòng Lịch SM 107–109 (tim story SM03/SM02/SM01), 111 (SM01 lướt), 113 (SM03 lướt), 114–115 (chấp nhận All SM01/SM03: 0 lời mời), 117 (SM03 đăng group CG3 → group 11 Used Clothing Direct Supplier Worldwide), 118 (SM01 đăng tường CG7), 119 (SM03 đăng tường **LILY 1** thay CG11).

**Chưa làm (H còn "Chờ") — dồn sang ngày sau:**
- SM01: tương tác newsfeed (123), đăng group CG1 → group 1 (124), join 6, 8 (125), đăng tường thứ 2 (130, CG8 hoặc bài GRACIE), tương tác group 7 (132), kết bạn #16 (137), đăng group CG4 → group 16 (138).
- SM03: tương tác newsfeed (121), join 1, 2 (127), đăng tường thứ 2 (128, nên dùng LILY 2), đăng group CG6 → group 27 (131), tương tác group 29 (134), kết bạn #19 (135).
- **SM02: dừng cả ngày** — FB yêu cầu "confirm your identity" trên điện thoại (certain actions restricted). Người dùng cần xác minh trước khi chạy lại SM02. Dòng 110, 112, 116, 120, 122, 126, 129, 133, 136, 139 chưa làm.

**Content đã dùng:** CG3, CG7, LILY 1 (CG2 chưa đăng được — còn dùng được). Nhật Ký SM dòng trống kế tiếp: **100**. Ảnh đã tải: `anh-dang-bai\CG02`, `CG03`, `CG07`, `LILY01`.

**Ghi nhớ:**
- Group STT 21/44 "Vintage Kids Clothing & More" cấm quảng cáo → không đăng. STT 2 "SMOCKED DRESS AND ROMPER" ghi Wholesale & Retail → hợp. STT 11 không có nội quy → đã đăng.
- Tab persona (GRACIE/CATHIE/LILY/EMILY) **có caption** — gviz CSV làm rơi dữ liệu, phải xem trực tiếp trên sheet.
- Kết bạn: #1–15 đã gửi (26/10); kế tiếp #16.
