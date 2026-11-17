# Tiến độ chạy lịch SM

## 2026-11-17 17:55 — Máy bật 24/24 (phương án A, `ops/BAN-GIAO-CAP-3.md` mục 0c)
- Người dùng để máy treo 24/24 từ 17/11 tối. Đã kiểm `trang-thai`: n8n chạy, L1-01…L1-07 bật, Copilot cấp 2 lần tới 05:30 18/11, Sleep = không bao giờ. Đêm nay: 18:00 L1-04 → 21:30 L1-02 lịch 18/11 → 22:00 L1-03 → 22:15 L1-06 → 05:30 Copilot → 06:30 L1-06 kéo caption. Sáng 18/11 cấp 3 chạy lịch từ 08:30.
- **Nick mới chưa vào n8n/Copilot**: tab Tài khoản cột F của SM04, SM05, SM07 = "Chờ chuẩn hoá profile (chưa chạy lịch, chờ người dùng bảo set)" → L1-02 bỏ qua (chỉ lấy nick có chữ "Hoạt động"). SM06, SM08 để trống.
- **Khi người dùng bảo "set nick mới"** (chỉ lúc đó): (1) người dùng nối tiện ích Claude ở profile Chrome → ghi deviceId vào mục "Máy này" CLAUDE.md; (2) sửa cột F = "Hoạt động - hạn chế group" cho tới khi nick join ≥ 15 group A/B (code n8n chưa có luật ≥ 15, chỉ xếp vào group đã join), đủ thì đổi về "Hoạt động"; (3) có số WA riêng ở sheet SMOCK's Information; (4) kiểm Join Group SM cột I–M, tab Target + Workload có dòng nick; (5) chạy thử `node ops/test_level1.js`. Không cần sửa code n8n (CFG đã có SM04–SM08).

## 2026-11-17 — SM04, SM05, SM07 mới (việc dở cho agent sau)
- **SM07** Chrome profile "SM07", FB đang tên **Phan Thị Ngọc Anh** → đổi tên **Maily Smock** theo sheet (tab SM07 dòng 22–26), cùng cách làm như SM04/SM05.
- **WhatsApp (chốt lại 17/11): mỗi nick 1 số WA riêng, người dùng cấp sau.** Chưa có số riêng thì KHÔNG đưa WA lên bio/intro FB của SM04/05/07 (số 3061 trong sheet chỉ là tạm; ghi chú dòng 27 các tab). SM03 giữ số riêng +84 886 421 089, không sửa.
- Nick nhận từ HR: **SM04** Chrome profile "SM04", FB **Jenny Smocking** `profile.php?id=61595904006414`; **SM05** Chrome profile "SM05", FB đang tên **Thanh Chi Lê** `profile.php?id=61595814087257`.
- Mẫu chuẩn: sheet **SMOCK's Information** `1Y9xyKErb3sMZvdgPVXCUWyk7GOt6Y7Qp32i5F8jtV8s`, tab SM04/SM05 (dòng 1–20 = mẫu, dòng 22–26 = hiện trạng + việc đã chốt).
- Người dùng chốt: Bio/Intro theo mẫu SM, Workplace K-Embroidery, xoá SĐT/Gmail tuyển dụng + trường ĐH + "Công ty K-Global"; **SM05 đổi tên → Olivia Smocking**; avatar/ảnh bìa để sau.
- Việc agent sau: (1) người dùng cài + Connect tiện ích Claude ở 2 profile Chrome; (2) ghi deviceId vào mục "Máy này" CLAUDE.md + shortcut; (3) sửa profile theo sheet; (4) ghi log.

## 2026-11-17 — luồng 1 (SM01, SM03; xong 14:25)
- Bắt đầu 09:45 (trễ) → người dùng duyệt **làm bù xen kẽ**. Lịch luồng 1 dòng 193–234: **xong hết**, log webhook OK.
- Bài: SM03 **K133** g30 (chờ duyệt, 13:38 vẫn pending), **K134** g15 (lên ngay), **K135** g29 (chờ duyệt), **K136** g12 14 ảnh (chờ duyệt), tường **K138** (= CG6 thay CG30 thiếu ảnh). SM01 **K123** g5 (chờ duyệt), **K124** g25 (chờ duyệt), **K125** g1 (đổi từ g32 resale, lên ngay), tường **K129**, **K128**. Tất cả đã đăng ký Radar.
- Bỏ qua (Lỗi gói 0/0 ảnh): K126 (229), K127 (233), K137 (232).
- **SM03 bị hạn chế gửi tin nhắn** ("Confirm your identity to send messages", 11:04) → Radar health `h-20261117-SM03-identity` (Đỏ). Người dùng cho đăng group tiếp, vẫn chạy được. Cần người dùng xác minh trên điện thoại. Inbox David (Trung Quốc, có vẻ xưởng/nhà cung cấp) đã ghi signal, chưa tính QI.
- Join: SM01 g12, 15, 27; SM03 g5, 10, 17 → đã ghi Join Group SM cột D/F + Radar. Kết bạn: SM01 STT1 đã có lời mời cũ, STT2 đã là bạn; SM03 STT6 gửi, STT5 không có nút.
- Content đã dùng ngoài lịch: CG6 (K138), CG4 (K132 luồng 2). CG2 còn chưa đăng (ảnh `anh-dang-bai\CG02`).
- n8n: đã cài cơ chế kiểm tồn kho content (commit 1ba05ef, L1-02/04/06), lịch 18/11 (21:30) là lần đầu áp dụng → kiểm cột J dòng đầu ngày 18/11 có "kho Đầy/Vừa/Ít".
- Người dùng cho Claude tự điều phối n8n + Copilot (memory `feedback-dieu-phoi-n8n-copilot`).

## 2026-11-17 — luồng 2 (SM02, SM04; xong 12:14)
- Done: 197 tương tác, 198 kết bạn (Một phần: STT 4 đã gửi; STT 3 Katherine Connors không có nút), 199 lướt, 201 tương tác group 3, 203 chấp nhận (0), 210 tường **K131** (CG23), 212 tường **K132** (thay CG24 lỗi gói bằng CG4, ảnh `anh-dang-bai\CG04`), 214 tim story. K131, K132 đã đăng ký Radar.
- **SM02 lại bị "confirm your identity"** khi mở composer group (196, K130 → group 2) và khi Join group 10 (211) → Không làm được; Radar health `h-20261117-SM02-identity`. Tường + like/lướt/story/kết bạn vẫn được. SM02 **không đăng group, không join** cho tới khi người dùng xác minh trên điện thoại.
- Content: CG2 vẫn chưa đăng (ảnh `anh-dang-bai\CG02`); CG4 đã dùng (K132).
- SM04: 207, 208, 209, 215, 217 ghi Bỏ qua (không có trình duyệt trên máy ADMIN).
- Group 10, 12, 15 SM02 chưa join.

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
