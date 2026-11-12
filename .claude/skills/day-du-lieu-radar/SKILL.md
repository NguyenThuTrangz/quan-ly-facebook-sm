---
name: day-du-lieu-radar
description: Đẩy dữ liệu từ Facebook (comment, inbox, số đọc bài, kiểm tra hiển thị, sự cố nick, bài mới có mã) vào dashboard Smock Radar. Dùng khi người dùng nói "quét comment bài Kxxx", "đọc số bài", "kiểm tra hiển thị", "đăng ký bài mới", hoặc ngay sau khi đăng bài / gặp cảnh báo FB.
---

# Đẩy dữ liệu vào Smock Radar

Dashboard: **https://claude.ai/artifact/4pxRJ5wv1URZUpsooZMjye** (cùng tài khoản claude.ai với máy này).
Mọi dữ liệu nằm trong kho chung của trang; trang tự phân loại tín hiệu mua và tự tính đèn sức khỏe nick. Bot chỉ chép đúng những gì thấy trên Facebook, **không tự viết comment hay tương tác giả**.

## Cách ghi (chọn 1)

**A. Có công cụ `ArtifactData`** (Claude Code đăng nhập claude.ai): ghi thẳng.
- Tín hiệu: `action:"batch"`, mỗi entry `{op:"set", collection:"signals", doc_id:"<mã bài>-<8 ký tự đầu của tên + giờ>", data:{post, nick, source, author, authorUrl, text, createdAt, by:"bot"}}`.
- Bài mới: `{op:"set", collection:"posts", doc_id:"K117", data:{code, nick, kind:"tuong"|"group", groupStt, content, title, caption, url, date, postedAt}}`.
- Số đọc: `action:"update"`, collection `posts`, doc_id mã bài, data `{"m24":{"r":6,"c":2,"s":0,"at":"<ISO>"},"alive":"yes"}` (đọc doc trước để có `if_version`).
- Sự cố / phép thử: `{op:"set", collection:"health", doc_id:"h-<yyyymmdd>-<nick>-<kind>", data:{nick, kind, date, post, detail, by:"bot"}}`.

**B. Không có ArtifactData**: mở dashboard trong trình duyệt đã đăng nhập claude.ai (Edge SM03 cũng được), vào tab **Kết nối bot** (`#ket-noi`), `find` "Nhập hàng loạt" → `form_input` vào ô textarea các dòng JSON (mỗi dòng một object, xem dưới) → bấm **Nhập** → đọc dòng kết quả "Đã nhập n/n". Lỗi dòng nào thì sửa dòng đó và nhập lại riêng dòng đó.

## Định dạng dòng JSON (cách B; cách A dùng cùng trường)

```
{"type":"signal","post":"K114","source":"comment","author":"Jane Miller","authorUrl":"https://www.facebook.com/…","text":"How much for 50 pcs?"}
{"type":"post","code":"K117","nick":"SM01","kind":"group","groupStt":2,"content":"CG4","title":"…","caption":"<caption đầy đủ>","url":"https://…"}
{"type":"metric","code":"K114","at":"m24","r":6,"c":2,"s":0,"alive":"yes"}
{"type":"health","nick":"SM02","kind":"identity","detail":"Confirm your identity"}
```
`source`: comment | inbox | whatsapp | email. `alive`: yes | pending | removed.
`kind` của health: identity, checkpoint, cant_use, removed, acct_issue (Đỏ) · vis_fail, pending48, accept_low, reach_drop (Vàng) · vis_ok, acct_clean (Xanh).

## Các việc

### 1. Quét comment một bài ("quét comment bài K114")
1. Lấy URL bài: dashboard tab **Bài có mã**, hoặc ArtifactData `get posts/K114`.
2. Mở bài bằng trình duyệt của nick đăng bài. Bấm "View more comments" / "All comments" cho tới khi hết.
3. Lấy comment bằng JS (không screenshot):
```js
[...document.querySelectorAll('div[role=article][aria-label^="Comment by"]')].map(a=>{const n=a.getAttribute('aria-label').replace(/^Comment by /,'').replace(/\s+(\d+|a|an)\s+\w+ ago$/,'');const t=[...a.querySelectorAll('div[dir=auto]')].map(d=>d.innerText).join(' ').trim();const l=a.querySelector('a[href*="facebook.com/"]');return {author:n,text:t.slice(0,1500),authorUrl:l?l.href.split('?')[0]:''}}).filter(c=>c.text)
```
4. Bỏ comment của chính các nick SM (Sophie Embroidery, Marie Smocked/Benita Ariem, Rosie Smocking, Jenny Smocking…) — không ghi tương tác của mình như tín hiệu khách.
5. Ghi mỗi comment một dòng `signal`. Comment đã ghi lần trước (cùng tác giả + cùng nội dung) thì bỏ.
6. Báo 1 dòng: "✅ K114: 5 comment → 1 QI, 2 có ý mua (xem dashboard)". Số nhãn đọc trên dashboard tab Tín hiệu.

### 2. Inbox / WhatsApp
Khi nick nhận tin nhắn mới từ người lạ: ghi `signal` với `source:"inbox"`, `post` = mã Kxxx khách nhắc trong tin (CTA có mã); không có mã thì để `post:""`. **Chỉ ghi nội dung tin đầu tiên và tên hiển thị; không ghi số điện thoại, email riêng của khách.**

### 2b. Tín hiệu được Radar chấm QI → chuyển Sale
Radar gắn nhãn "QI · đạt chuẩn" thì báo người dùng ngay 1 dòng để chuyển Sale qua **WhatsApp hotline** trong 2 giờ làm việc, kèm: tên khách, tên shop, link trang cá nhân, nội dung hỏi, mã bài. Trả lời khách (nếu người dùng cho phép) theo thông tin Sale trong CLAUDE.md: MOQ 15 chiếc/mẫu, mock-up 2D miễn phí, hỏi khách cần hàng trước ngày nào và ship về đâu để Sale báo phí ship. Nhãn "Có ý mua": hỏi tiếp shop bán ở đâu, mỗi mẫu bao nhiêu chiếc, cần hàng trước ngày nào.

### 3. Đăng ký bài mới (ngay sau khi đăng, trong `chay-lich-sm`)
Mã mới = mã lớn nhất trên dashboard + 1 (dòng "Mã kế tiếp" ở tab Kết nối bot). Ghi `post` với `caption` đầy đủ (để bộ kiểm trùng nội dung hoạt động) và `postedAt` = giờ đăng thật. Ghi mã vào cột Ghi chú dòng Lịch SM.
Trước khi đăng group: dùng ô **Kiểm tra trước khi đăng vào group** (tab Chấm group) và **Kiểm caption** (tab Chống shadowban). Kết quả "Chưa được đăng" / "Không nên đăng" → không đăng, báo người dùng.

### 4. Đọc số bài (T+24h, T+72h)
Mở link bài, đọc tổng cảm xúc, số comment, số share:
```js
(()=>{const t=document.body.innerText;const g=re=>{const m=t.match(re);return m?+m[1].replace(/[.,]/g,''):0};return {c:g(/(\d[\d.,]*)\s+comments?/i),s:g(/(\d[\d.,]*)\s+shares?/i)}})()
```
Cảm xúc: `find` "All reactions" hoặc nút đếm cảm xúc của bài, đọc số. Bài không mở được / "This content isn't available" → `alive:"removed"`; bài group còn "Pending" → `alive:"pending"`.

### 5. Phép thử chống shadowban
- **Hiển thị chéo** (mỗi bài group, khoảng T+2h): mở link bài bằng trình duyệt của **nick khác** (không phải nick đăng). Thấy bài → `health vis_ok` (post = mã bài); không thấy / "isn't available" / chỉ thấy khi vào bằng nick đăng → `health vis_fail`.
- **Account Status** (thứ Hai): mở `https://www.facebook.com/settings?tab=account_status` (hoặc Menu › Help & support › Account Status) từng nick; không có hạn chế → `acct_clean`, có → `acct_issue` + mô tả.
- **Cảnh báo khi đang chạy**: thấy "You can't use this feature" → `cant_use`; "Confirm your identity" → `identity`; checkpoint/đăng xuất → `checkpoint`; bài bị admin gỡ → `removed`; bài group chờ duyệt quá 48h → `pending48`. Ghi ngay rồi dừng tính năng đó của nick (đèn Đỏ = nghỉ tối thiểu 72h).

## Không làm
- Không tạo comment, cảm xúc hay tin nhắn giả để "có số liệu".
- Không nhập mật khẩu, không lưu SĐT/email cá nhân của khách vào dashboard.
- Không đăng bài mà bộ kiểm trước khi đăng báo chặn.
