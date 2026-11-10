---
name: chay-lich-sm
description: Quy trình rút gọn để chạy từng dòng Lịch SM (tim story, lướt, tương tác, chấp nhận, join, kết bạn, đăng tường/group) trên SM01–SM03 và ghi log. Dùng khi hẹn giờ một dòng Lịch SM nổ hoặc người dùng bảo làm một việc trong lịch.
---

# Chạy 1 dòng Lịch SM — làm đúng các bước, hạn chế screenshot

Quy tắc nghiệp vụ nằm ở CLAUDE.md; file này chỉ là cách làm nhanh. Ưu tiên `javascript_tool` / `find` hơn screenshot; chỉ chụp (scale 0.4–0.5 hoặc `zoom`) khi cần xác nhận kết quả.

## 0. Chọn trình duyệt
| Nick | deviceId | Ghi chú |
|---|---|---|
| SM01 | `74dc5da7-2665-421e-b6f4-1ad4614b2045` | Chrome Profile 1 |
| SM02 | `39874c3f-67cd-451f-9fc3-cc9eda87f859` | Chrome Profile 2 |
| SM03 | `9db7ffa4-d6d0-43e1-aa29-09b57b9c7cb8` | Edge — cũng dùng để ghi Google Sheet |

`select_browser` → `navigate` facebook.com (tab mới tự tạo) → kiểm tra nick bằng 1 lệnh JS:
```js
[...document.querySelectorAll('span')].map(s=>s.textContent).find(t=>/What's on your mind/.test(t))
```
(SM01 "Sophie", SM02 "Benita", SM03 "Rosie"). Sai nick / checkpoint / "confirm your identity" → dừng, ghi log Không làm được, báo người dùng.

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

**Tương tác a/b/c** (newsfeed) / **group X tương tác a/b**: theo CLAUDE.md (bỏ Sponsored/Reels/gợi ý). Đếm bài bằng JS `[role=article]`, cuộn tới bài đích (`scrollIntoView`), `find` nút Like/Love của bài đó rồi click; xen kẽ Like/Love.

**Chấp nhận All**: mở `facebook.com/friends/requests`, `find` các nút "Confirm", click lần lượt; không có thì J = 0.

**Join group …**: link lấy cột C tab Join Group SM; bấm Join, nội quy → tick đồng ý, câu hỏi → "Oke" rồi Submit. Điền "đã join"/"đang chờ duyệt" vào cột của nick (D=SM01, E=SM02, F=SM03).

**Kết bạn …**: link cột B tab Add Friend; Add friend (không có thì Follow). Báo "can't use this feature" → dừng kết bạn nick đó hôm nay.

**Đăng tường / đăng group CGn**:
1. Lấy caption + folder ảnh: tab "3. CONTENT GROUP" (hoặc tab persona GRACIE/CATHIE/LILY/EMILY) workbook KE `1mY_7HeFFokARzxwS9xCeby46cYGC5QpA_ju4jl5f-UA`, đọc bằng gviz CSV trên Edge. Output JS bị chặn nếu chứa link có query string → chỉ trả id folder (`/folders\/([\w-]+)/`).
2. Mở folder trên Edge, lấy id file: `[...document.querySelectorAll('[data-id]')].map(e=>e.getAttribute('data-id'))` (bỏ trùng).
3. Tải: `Invoke-WebRequest "https://drive.usercontent.google.com/download?id=<id>&export=download" -OutFile "C:\claude remote\anh-dang-bai\CGnn\<i>.jpg"`.
4. Group: đọc `/groups/<id>/about` bằng `get_page_text` **trước** — cấm promotion/business thì bỏ, chọn group khác nick đã join (ghi wholesale/for sale) và báo.
5. Mở composer (`find` "Write something…"/"What's on your mind"), `find` file input ảnh → `file_upload` các file, dán caption bằng sự kiện paste (giữ emoji/xuống dòng), chọn Công khai (tường), bấm Post, lấy link bài.

## 2. Ghi log (3 nơi) — gộp tối đa
1. Một lệnh PowerShell ghi Excel + đưa dòng Nhật Ký SM vào clipboard:
   `& "C:\claude remote\tools\ghi-log.ps1" SM01 "Tim story" "Story trang chủ" "<chi tiết>" "Xong" 2`
   (tham số 7 = Kết quả nếu khác Trạng thái, tham số 8 = Chế độ hiển thị).
2. Trên Edge, giữ 1 tab sheet chính `1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0` (`find` "Name box" lấy ref). Một `browser_batch`:
   Name box → `'Nhật Ký SM'!A<dòng trống kế tiếp>` → Enter → Ctrl+V → Name box → `'Lịch SM'!H<dòng>` → gõ `Done` → Enter (đăng bài: thêm I = link) → JS gviz đọc lại 2 ô để xác nhận.
   Gõ ô: Sheets hay tự điền (vd "kết bạn 16" → "kết bạn 16-20") → bấm `Delete` trước Enter.
3. Không làm được: H để nguyên "Chờ", Nhật Ký SM ghi Không làm được, J = 0.

Dòng Nhật Ký SM trống kế tiếp = dòng cuối + 1 (10/11: đã dùng tới 93).
