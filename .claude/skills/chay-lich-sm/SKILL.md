---
name: chay-lich-sm
description: Quy trình rút gọn để chạy từng dòng Lịch SM (tim story, lướt, tương tác, chấp nhận, join, kết bạn, đăng tường/group) trên SM01–SM08 và ghi log. Dùng khi hẹn giờ một dòng Lịch SM nổ hoặc người dùng bảo làm một việc trong lịch.
---

# Chạy 1 dòng Lịch SM — làm đúng các bước, hạn chế screenshot

Quy tắc nghiệp vụ nằm ở CLAUDE.md; file này chỉ là cách làm nhanh. Ưu tiên `javascript_tool` / `find` hơn screenshot; chỉ chụp (scale 0.4–0.5 hoặc `zoom`) khi cần xác nhận kết quả.

## 0. Chọn trình duyệt
| Nick | deviceId | Ghi chú |
|---|---|---|
| SM01 | `74dc5da7-2665-421e-b6f4-1ad4614b2045` | Chrome Profile 1 |
| SM02 | `39874c3f-67cd-451f-9fc3-cc9eda87f859` | Chrome Profile 2 |
| SM03 | `9db7ffa4-d6d0-43e1-aa29-09b57b9c7cb8` | Edge — cũng dùng để ghi Google Sheet |
| SM04 | `bf159760-2d98-40bf-b4ba-4e3998bd277a` | Chrome Profile 9 (Jenny Smocking) |
| SM05 | `68b78dc0-f73f-4599-b5a8-ba13b9692cf9` | Chrome Profile 10 (Thanh Chi Lê / Olivia Smocking) — giao diện tiếng Việt |
| SM06 | `3c7316d1-8a96-46ab-95aa-0fae1c5b582a` | Chrome Profile 13 (FB tên **Ella Smocked** từ 23/11; trước là Nguyễn Ngọc Ánh) — giao diện tiếng Việt |
| SM07 | `e5a2bf46-4c18-4041-aa8a-0ce12eab78fa` | Chrome Profile 12 (Phan Thị Ngọc Anh / Maily Smock) |
| SM08 | `f969d375-0948-40ec-9614-67da5609a8b8` | Chrome Profile 4 (FB tên **Sarah Smock** từ 23/11; trước là Nguyễn Thương) — giao diện tiếng Việt |

Nick chưa có trong `list_connected_browsers` → `Start-Process "C:\claude remote\SMxx - Chrome.lnk"` (SM03: `SM03.lnk`), chờ ~45 giây rồi kiểm lại. SM04–SM08 giao diện có thể là tiếng Việt: nút/nhãn tiếng Việt ("Thích", "Bày tỏ cảm xúc", "Xác nhận", "Tham gia nhóm", "Thêm bạn bè", "Bạn đang nghĩ gì?") — `find` theo nghĩa, không cứng tiếng Anh.

**Luôn `select_browser` đúng deviceId ở bảng trên TRƯỚC mọi lệnh tab** (`tabs_context_mcp`, `navigate`, `javascript_tool`…). `select_browser` báo lỗi / nick chưa kết nối → **không gọi thêm lệnh trình duyệt nào** (lệnh tab khi chưa chọn được sẽ rơi vào trình duyệt máy khác, vd `87f823ce…`, và mở tab/nhóm tab ở máy đó — đã xảy ra 18/11), chạy shortcut rồi chờ.

`select_browser` → `navigate` facebook.com (tab mới tự tạo) → kiểm tra nick bằng 1 lệnh JS:
```js
[...document.querySelectorAll('span')].map(s=>s.textContent).find(t=>/What's on your mind|bạn đang nghĩ gì/i.test(t))
```
(SM01 "Sophie", SM02 "Benita"/"Marie", SM03 "Rosie", SM04 "Jenny", SM05 "Chi", SM06 "Ella"/"Ánh", SM07 "Anh"/"Maily", SM08 "Sarah"/"Thương"). Sai nick / checkpoint / "confirm your identity" → dừng, ghi log Không làm được, báo người dùng.

**Screenshot hoặc click bị timeout** = cửa sổ đang thu nhỏ → chạy `& "C:\claude remote\tools\cuaso.ps1" -Mo "<một phần tiêu đề, vd Facebook - Google Chrome>"` (mở lại không chiếm focus) rồi thử lại.

## 1. Các việc
**Tim story a/b** (tim story thứ a, rồi đếm tiếp b → story thứ a+b):
1. Click story đầu trong tray: `[...document.querySelectorAll('a[href*="/stories/"]')].filter(x=>!/create/.test(x.href))[0].click()`
2. Lấy thứ tự: `[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label')).filter(s=>/'s story$/i.test(s))`
3. Mỗi đích: click story đó qua aria-label (xem lướt 1 story trước cho tự nhiên), chờ 2s, **bấm Pause trước** (`[aria-label="Pause"]`) — không pause thì story tự chuyển và tim nhầm người.
4. Tim: `find` "Love reaction button" → click ref. Xác nhận bằng `zoom` vùng đáy story thấy "Sent to <tên>".

**Lướt newfeed N** (N phút, chỉ cuộn): gọi JS này nhiều lần (mỗi lần ≤ 38s, JS timeout 45s) cho đủ N phút:
```js
const sl=ms=>new Promise(r=>setTimeout(r,ms));const end=Date.now()+38000;let n=0;while(Date.now()<end){scrollBy({top:300+Math.random()*500,behavior:'smooth'});n++;await sl(3500+Math.random()*4500)}({n,t:new Date().toTimeString().slice(0,8)})
```
Có thể gửi 2–3 lệnh JS song song trong cùng 1 message (chạy tuần tự).

**Tương tác a/b/c** (newsfeed) / **group X tương tác a/b**: Read `tools\tuong-tac.js`, sửa `ST.targets`/`ST.useLove`, dán vào `javascript_tool` (trên feed/group), rồi gọi `await STEP(38000)` lặp tới khi `left: []`. Nút cảm xúc FB: `aria-label^="React with Like"` (Like), `"React to …"` mở bảng → `aria-label="Love"`. JS click chạy được, không cần screenshot.

**Chấp nhận All**: mở `facebook.com/friends/requests`, `find` các nút "Confirm", click lần lượt; không có thì J = 0.

**Join group …**: link lấy cột C tab Join Group SM; bấm Join, nội quy → tick đồng ý, câu hỏi → "Oke" rồi Submit. Điền "đã join"/"đang chờ duyệt" vào cột của nick (D=SM01, E=SM02, F=SM03, I–M=SM04–SM08).

**Kết bạn …**: link cột B tab Add Friend; Add friend (không có thì Follow). Báo "can't use this feature" → dừng kết bạn nick đó hôm nay.

**Đăng tường / đăng group CGn**:
1. Lấy caption + folder ảnh: tab "3. CONTENT GROUP" (hoặc tab persona GRACIE/CATHIE/LILY/EMILY) workbook KE `1mY_7HeFFokARzxwS9xCeby46cYGC5QpA_ju4jl5f-UA`, đọc bằng gviz CSV trên Edge. Output JS bị chặn nếu chứa link có query string → chỉ trả id folder (`/folders\/([\w-]+)/`).
2. Mở folder trên Edge, lấy id file: `[...document.querySelectorAll('[data-id]')].map(e=>e.getAttribute('data-id'))` (bỏ trùng).
3. Tải: `Invoke-WebRequest "https://drive.usercontent.google.com/download?id=<id>&export=download" -OutFile "C:\claude remote\anh-dang-bai\CGnn\<i>.jpg"`.
4. Group: đọc `/groups/<id>/about` bằng `get_page_text` **trước** — cấm promotion/business thì bỏ, chọn group khác nick đã join (ghi wholesale/for sale) và báo.
   - gviz CSV **làm rơi chữ** ở cột lẫn kiểu (tab persona tưởng trống mà thật có caption) → xem trực tiếp trên sheet hoặc dùng `/export?format=csv&gid=`; link chip ảnh: chọn ô rồi hover chip, đọc `a[href*="drive.google.com"]`.
   - Id Drive trả về bị chặn "Base64" → trả dạng tách 6 ký tự (`x.match(/.{1,6}/g).join(' ')`) rồi ghép lại cẩn thận (phân biệt hoa/thường).
   - File HEIC (đầu file `ftypheic`) → tải bản JPG: `https://drive.google.com/thumbnail?id=<id>&sz=w2048`.
5. Mở composer (`find` "Write something…"/"What's on your mind"), `find` file input ảnh → `file_upload` các file, dán caption bằng sự kiện paste (giữ emoji/xuống dòng), chọn Công khai (tường), bấm Post, lấy link bài.
   - Chọn Công khai: bấm nút "Edit privacy" → **chụp màn hình rồi bấm Public theo tọa độ**, chụp lại xác nhận, rồi bấm Done theo tọa độ (bấm theo ref dễ trúng "Close friends" vì hộp thoại dịch chuyển). Kiểm tra `aria-label` "Sharing with Public." và ô "Set as default audience" **không tick**.
   - Link bài: `find` timestamp của bài → `hover` → lấy `pfbid…` trong `a[href]` của bài (`/pfbid\w+/`).

## 2. Ghi log — CÁCH MỚI: 1 lệnh webhook (khi n8n L1-01 đã bật)
Sau mỗi việc chạy **một** lệnh, xong. Webhook tự ghi Nhật Ký SM, ghi `Done`/`Lỗi` + URL vào Lịch SM dòng đó, và chống ghi trùng:
`& "C:\claude remote\tools\ghi-log-webhook.ps1" SM01 "Tim story" "Story trang chủ" "story tim 2/3" "Xong" 2 -LichRow 121`
(đăng bài thêm `-Url "<link bài>" -CheDo "Công khai"`). Kết quả:
- `OK …` → sang việc kế. `(đã ghi trước đó…)` cũng là OK.
- `WEBHOOK TỪ CHỐI: …` → sửa đúng tham số bị báo (sai loại việc, sai trạng thái, sai link) rồi chạy lại. Không ghi kiểu cũ.
- `DỰ PHÒNG: …` → script đã tự ghi Excel kiểu cũ; làm tiếp bước 2–3 ở mục 2b cho dòng này, và báo người dùng "n8n không phản hồi" một lần trong ca.
Không còn mở tab sheet để gõ ô. Số dòng Lịch SM (`-LichRow`) lấy từ lúc đọc lịch đầu ca (gviz, cột A–J, dòng = chỉ số + 2).

**Đăng bài khi có gói sẵn (n8n L1-03):** Hành Động có mã `Kxxx` → mở `C:\claude remote\anh-dang-bai\Kxxx\`: `caption.txt` (đã có mã bài trong lời mời nhắn tin) + `01.jpg, 02.jpg…`. Không đọc workbook KE, không tải ảnh Drive. Cột J của dòng lịch có "Gói sẵn n/n ảnh" là gói đủ. Thư mục thiếu/rỗng hoặc J ghi "Lỗi gói" → `Bỏ qua`, báo người dùng (n8n L1-05 sẽ báo lúc 06:30 nếu gói chưa sẵn). Đăng xong: ghi log bằng webhook kèm `-Url`, rồi đăng ký bài vào Radar (`day-du-lieu-radar`, dùng đúng mã Kxxx).

**Lướt newfeed N phút: một lệnh** thay vì gọi lại mỗi 38 giây — chạy JS không chờ (`setTimeout` lặp trong trang N phút), rồi gọi `computer wait` hoặc làm việc khác của cùng nick; chỉ kiểm lại một lần khi hết N phút.

## 2b. Ghi log (3 nơi) — CÁCH CŨ, chỉ dùng khi webhook DỰ PHÒNG hoặc n8n chưa cài
1. Một lệnh PowerShell ghi Excel + đưa dòng Nhật Ký SM vào clipboard:
   `& "C:\claude remote\tools\ghi-log.ps1" SM01 "Tim story" "Story trang chủ" "<chi tiết>" "Xong" 2`
   (tham số 7 = Kết quả nếu khác Trạng thái, tham số 8 = Chế độ hiển thị).
2. Trên Edge, giữ 1 tab sheet chính `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0` (`find` "Name box" lấy ref). Một `browser_batch`:
   Name box → `'Nhật Ký SM'!A<dòng trống kế tiếp>` → Enter → Ctrl+V → Name box → `'Lịch SM'!H<dòng>` → gõ `Done` → Enter (đăng bài: thêm I = link) → JS gviz đọc lại 2 ô để xác nhận.
   Gõ ô: Sheets hay tự điền (vd "kết bạn 16" → "kết bạn 16-20") → bấm `Delete` trước Enter.
   Gom nhiều việc: `ghi-log.ps1` tự thêm vào hàng đợi → `tools\dan-log.ps1` đưa cả hàng đợi vào clipboard → dán 1 lần; cột H/I nhiều dòng: dựng TSV "H`tI" rồi dán từ H<dòng đầu>.
   **Gõ tiếng Việt bằng `type` bị mất chữ "đ"** → luôn `Set-Clipboard` rồi Ctrl+V cho ô có dấu.
   Đọc tab KE đầy đủ caption: `.../export?format=csv&gid=<gid>` (LILY gid 9663883). Group được đăng chào hàng: `ArtifactData query groups` cat = "potential" (resale/hobby → không đăng).
   **Luôn `navigate` lại tab sheet (URL không có `#`) trước khi ghi** — tab để lâu bị lỗi "Đã xảy ra lỗi", dán/gõ không ăn. Đọc lại thấy rỗng → tải lại, chạy lại `Set-Clipboard` rồi ghi lại.
3. Không làm được: H để nguyên "Chờ", Nhật Ký SM ghi Không làm được, J = 0.

Dòng Nhật Ký SM trống kế tiếp = dòng cuối + 1 (10/11: đã dùng tới 93).
