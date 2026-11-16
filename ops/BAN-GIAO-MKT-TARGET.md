# Bàn giao phần số liệu, target, báo cáo sếp — nhánh Smock (phiên 10–16/11/2026)

Đọc cùng:
- `CLAUDE.md` và `tien-do.md`.
- `ops/BAN-GIAO-CAP-3.md`: phần vận hành hằng ngày (n8n, chạy lịch, ghi log).

File này ghi phần còn lại: **số liệu, target, các sheet, và những gì người dùng đã quyết**. Trả lời người dùng (Việt, TTS MKT) bằng tiếng Việt, ngắn, có số cụ thể. Sếp là anh Quý.

## 1. Bối cảnh
- **Nhánh Smock:** K-Embroidery bán sỉ váy thêu smock cho shop online / boutique ở US/EU. MOQ 15 mẫu, mock-up miễn phí, chuyển khách qua WhatsApp hotline.
- **Người dùng nhận nhánh ngày 10/11.** Sếp từng mắng vì không có số để báo cáo. Mục tiêu: có số thật, target có cơ sở, và chứng minh cách làm của MKT hiệu quả.
- **Trục chính:** Facebook persona, 2 loại bài (bài tường và bài group) → **Mess → Inquiry → Order**. So sánh fanpage với persona: để sau.

## 2. Tài liệu và link
| Thứ | Ở đâu | Ghi chú |
|---|---|---|
| Sheet chính | `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0` | Tab **Target + Workload** (target), **Hòa vốn SM**, Join Group SM (cột I–M = SM04–SM08, thêm 13/11), Lịch SM, Nhật Ký SM… |
| Sheet Sale "lis quiz for sales" | `17LBj_eC0fhRHXjvooRC79A7w7t5ktrnffmLgNnGn7lU` | Tab **Hỏi Sale** (15 câu) + tab **Tỉ lệ convert FB persona** = **nguồn số chính** để build target |
| CRM KE (bản sao) | `16kAT4w4QxcEotA7TIZU9Hl1VGrBgnD5sxjPvdmtwkh8` | Tháng 9–11 là bản ghi chuẩn; cột I = nguồn khách, cột M = sales |
| Doc trình sếp | https://claude.ai/artifact/7tTYrtAxaCeCBLknqnsa3z | "Cơ sở target Smock tháng 12". **Chưa share**: người dùng phải bấm Chia sẻ |
| Smock Radar | https://claude.ai/artifact/4pxRJ5wv1URZUpsooZMjye | Dashboard mã bài, tín hiệu mua, đèn sức khỏe nick |
| Plan ban đầu | https://claude.ai/artifact/3MxPdjrdepAyYEkjmDht4V | North Star = QI/tuần, mã bài làm "pixel" |
| File MKT nội bộ | `1jPj8fNb6AK4tAzNvS_XXVX-d8KfD1oWiPKz9VXBYcrs` | **Đang mất liên kết**: IMPORTRANGE trỏ tới tab "Số đếm FB persona" không còn tồn tại. Chờ người dùng chọn nối lại hay xoá |
| Đề xuất khung Sale–MKT | máy nhà: `E:\HQV\The useful repositories\reports\Smock - phase 2 va khung Sale-MKT.md` | Mới là đề xuất, chưa triển khai |
| Bộ hỏi Sale cũ | `do-luong/Hoi-Sale-phase-2-dinh-luong.xlsx` | Người dùng thấy quá nặng, đã thay bằng tab Tỉ lệ convert |

## 3. Số liệu gốc (Sale tự đếm 30 ngày, lis quiz)
| Sale | Bài tường | Bài group | Mess | Inquiry | Order |
|---|---|---|---|---|---|
| LILY | 25 | 450 | 20 | 5 | 4 |
| EMILY | 25 | 250 | 10 | 9 | 4 |
| GRACIE | 15 | 150 | 15 | 3 | 0 |
| CATHIE | 15 | 150 | 10 | 5 | 1 |
| **Cả team** | **80** | **1.000** | **55** | **22** | **9** |

Từ bảng trên:
- **19,6 bài ra 1 mess** (lis quiz ô D17).
- **Mess → Inquiry 40%** (ô B17).
- **Inquiry → Order 41%** (ô C17). Đây là số Sale tự khai.

Đối chiếu CRM tháng 9–11: khách Facebook có 24 người, ra 2 order (~8%); tính mọi nguồn khoảng 10%. Nick MKT (SM01–SM03) đếm ngày 12/11: 0 mess trong 7 ngày.

## 4. Target hiện hành (v3, chốt 13/11) — tab Target + Workload
- **KPI mỗi nick:** cột D = 2 bài tường/ngày, cột G = **5 bài group/ngày**, cột K = G × 30.
- **Tham số:**
  - **O14 = 17,5 bài ra 1 mess**: gõ tay, nằm giữa mức gộp của Sale (19,6) và mức của CATHIE (16,5).
  - **O20** = IMPORTRANGE ô B17 (40%). Cột L của các nick lấy từ ô này.
  - **O15** = IMPORTRANGE ô C17 (41%).
- **Công thức (không làm tròn):** N = (H + K) / O14; O = N × L; P = O × O15.
- **Kết quả:** **96 mess → 38,4 inquiry → 15,7 order/tháng = 1,75 lần team Sale** (ô O18). Hòa vốn ở tỷ lệ chốt ~3% (O16). Lãi ~79 triệu/tháng (O17).
- **Điều kiện để đạt** (ghi ở N21:P26):
  - Tăng dần số bài group theo tuần: 3 → 4 → 5.
  - SM04–SM08 chỉ đăng group khi đã join ≥ 15 group A/B; cả đội cần ≥ 45 group A/B.
  - SM02 phải gỡ xong "confirm identity".
  - 8 trình duyệt trên máy công ty, chạy 2 luồng.
  - Khoảng 40 caption group mới mỗi ngày.
- **Tab Hòa vốn SM:**
  - Chi phí 6,43 triệu/tháng.
  - Lãi gộp mỗi đơn 5,46 triệu (700 USD × **30% biên lãi — GIẢ ĐỊNH** × 26.000).
  - B13 lấy theo O3; A20 lấy theo O15.

## 5. Repo — thay đổi từ phiên này
- `4225759`: bộ sinh lịch L1-02.
  - Giãn cách: cùng nick ≥ 60 phút, cả đội ≥ 6 phút.
  - Một nick không đăng lại 1 group trong 3 ngày; cả đội không trùng group trong ngày.
  - Đèn sức khỏe: Đỏ → 0 bài group, Vàng → tối đa 2.
  - Chạy 2 luồng; mỗi bài group 1 cụm.
  - Test công suất: 8 nick × 5 bài.
- `41225f8`, `be6ae42`: skill `dem-so-nick` và `do-luong/moi-nick.csv`.
- Các commit sau đó (L1-03, L1-06, bàn giao cấp 3) do phiên trên máy công ty làm.

## 6. Người dùng đã quyết (bắt buộc giữ)
- **Sheet Sale chỉ thu số đếm, không bắt Sale tính %.** MKT tự đổi sang %.
- **Không xoá hay cấu trúc lại sheet Sale.**
  - Ngày 12/11 mình xoá mục tính toán bên đó, người dùng phải khôi phục lại bản 08:27.
  - Chỉ sửa đúng ô người dùng chỉ; phần chỉ dành cho MKT thì **chép** sang chỗ khác, không xoá bên Sale.
  - Phần CRM chuyên sâu (khách FB đến từ đâu, công suất từng nick…) người dùng giữ riêng, **không đưa lại vào phần hỏi Sale**.
- **lis quiz là nguồn chính:** target phải nối thẳng và khớp số bên đó.
- **Target không bao giờ thấp hơn số team Sale đang làm (55 / 22 / 9).** Người dùng muốn 1,5–2,5 lần, nhưng phải khả thi về logic, tài chính, tài nguyên và kỹ thuật.
- Đã gộp mess bài tường và mess bài group thành một cột (không ai phân biệt được khách đến từ đâu). Đã bỏ hai cột "Mess / 100 bài".
- **Tài khoản Copilot:** người dùng tự đổi bằng tay, **không tự động xoay vòng**.
- **Không gửi thông báo đẩy**: tài khoản Claude là của sếp, Remote Control luôn tắt.

## 7. Việc còn mở
1. **Hai số cần xác nhận:** sếp xác nhận biên lãi thật (ô B9 tab Hòa vốn SM). Sale tách đơn mới và khách cũ đặt lại, vì tỷ lệ 41% cao gấp 4 lần CRM.
2. **Doc "Cơ sở target":** người dùng cần share cho sếp.
3. **File MKT nội bộ** (`1jPj8…`): nối lại theo tab hiện tại hay xoá — chưa có câu trả lời.
4. **lis quiz, mục 3:** ô B21/B22 vẫn 480 / 180 bài (KPI cũ). Hỏi trước khi sửa vì đó là file của Sale.
5. **Dọn tab Tỉ lệ convert (lis quiz):**
   - Còn màu thừa ở H5:H8 (vàng), I4, F12:G12, E25.
   - Ghi chú ở C23 trỏ sai ô (B26/D10, đúng phải là B24/D9).
6. **Điều kiện target** (mục 4) chưa đủ: 5 trình duyệt cho SM04–SM08, thêm group A/B (hiện SM01 18, SM02 9, SM03 10), SM02 gỡ xác minh, nguồn content.
7. **Chưa làm:**
   - Thu thập content thành công cùng ngách để ra công thức.
   - Content hybrid (công việc + bản sắc cá nhân), tỷ lệ đề xuất 3 bài sản phẩm : 1 bài hybrid.
   - Khung Sale–MKT dài hạn.

## 8. Mẹo kỹ thuật khi sửa Google Sheet qua trình duyệt
- **Locale tiếng Việt:** công thức dùng `;`, số thập phân dùng dấu phẩy (`27,5`). Dán `20%` thay vì `0,2`.
- **Cách nhập ổn định nhất:**
  1. Bấm Name box, gõ ô đích, Enter. Kiểm `document.getElementById('t-name-box').value` đúng ô và đúng tab.
  2. Dispatch `new ClipboardEvent('paste', {clipboardData: dt})` lên `document.activeElement` với chuỗi TSV.
  3. Gõ phím thẳng vào ô hay mất chữ hoặc lệch ô.
  4. Ô merge (ví dụ A2) thì Name box trả về `A2:I2`.
- **Dán TSV:** tab cuối dòng bị cắt bỏ, nên ô trống ở cuối không bị xoá. Muốn xoá thì chọn vùng rồi bấm Delete.
- **Kiểm kết quả:** `curl` link `export?format=xlsx` (các sheet đang mở link), rồi đọc bằng openpyxl (`data_only=True`). Không tin ảnh chụp màn hình: khung bị ẩn thì ảnh có thể cũ.
- **IMPORTRANGE** giữa các file của người dùng chạy được, không phải bấm cho phép.
- **Trình duyệt trong app** có thể bị đăng xuất, khi đó chỉnh sửa hiện là "ẩn danh". Claude in Chrome thỉnh thoảng mất kết nối.
- **Định dạng số:** chép định dạng bằng `ctrl+alt+v` không ăn. Đổi % bằng nút % trên thanh công cụ; đổi sang số thường bằng menu 123 → Number.

## 9. Lịch sử đầy đủ
Transcript phiên (máy nhà): `C:\Users\anhqa\.claude\projects\E--HQV-The-useful-repositories\2ac43eef-319d-45db-b40d-8689bae57714.jsonl`. Bộ nhớ: `memory/smock-fb-task.md` cùng thư mục project.
