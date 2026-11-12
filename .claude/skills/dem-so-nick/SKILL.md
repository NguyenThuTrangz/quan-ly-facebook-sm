---
name: dem-so-nick
description: Đếm số liệu thật của từng nick SM (bạn bè, group đã join, bài 7 ngày, mess mới 7 ngày, QI…) rồi điền vào do-luong/moi-nick.csv và push. Dùng khi người dùng nói "đếm số nick", "điền mỗi nick 1 dòng", "fill moi-nick".
---

# Đếm số nick → `do-luong/moi-nick.csv`

## Mục đích
- Đây là bản MKT của tab "Mỗi nick 1 dòng" trong `do-luong/Hoi-Sale-phase-2-dinh-luong.xlsx`. Sale điền bản của Sale.
- Hai bảng đặt cạnh nhau để so workload với hiệu quả, rồi lấy số thật làm target, thay cho các tỷ lệ giả định.
- Chỉ **đọc và đếm**:
  - Không nhắn, không trả lời, không kết bạn, không bấm gì làm thay đổi tài khoản.
  - Không ghi tên hay link của khách vào CSV. CSV chỉ chứa **số**.

## Làm lần lượt từng nick (SM01 → SM03 trên máy này)

### 1. Mở đúng nick
Mở theo mục "Mở tài khoản" trong CLAUDE.md. Đọc tên trên facebook.com, so với cột "Tên nick FB". Sai tên thì dừng và hỏi người dùng.

### 2. Đếm từng cột

Mọi cột "7 ngày" tính lùi từ hôm nay, gồm cả hôm nay.

| Cột | Đếm ở đâu | Cách đếm |
|---|---|---|
| Nick dùng được bao lâu (tháng) | Tab Tài khoản trên Google Sheet chính (ngày bàn giao) | Số tháng từ ngày bàn giao đến hôm nay, làm tròn 0,5 (SM01–SM03 bàn giao 19/10/2026) |
| Số bạn bè hiện tại | `facebook.com/me/friends` | Đọc số "… friends" ở đầu trang |
| Số group đã join | `facebook.com/groups/joins/` | Cuộn tới hết danh sách, đếm group. Không tính group đang chờ duyệt |
| Group có đăng bài 30 ngày qua | Tab **Nhật Ký SM**: Loại việc = `Đăng bài`, Nơi thực hiện là group, nick này, 30 ngày | Đếm số group **khác nhau** |
| Bài tường 7 ngày qua | Trang cá nhân của nick, cuộn qua mốc 7 ngày | Chỉ đếm bài nick tự đăng (bỏ bài được gắn thẻ, bài chia sẻ lại). Đối chiếu với Nhật Ký SM; lệch thì ghi cả hai số vào Ghi chú |
| Trong đó bài sản phẩm | Cùng danh sách bài ở dòng trên | Bài có ảnh hàng, giá, MOQ hoặc lời mời đặt hàng |
| Bài group 7 ngày qua | Nhật Ký SM (Đăng bài + group, 7 ngày) | Có link bài ở cột URL tab Lịch SM thì mở kiểm bài còn hiển thị không. Bài bị gỡ: vẫn đếm, ghi "n bị gỡ" vào Ghi chú |
| Mess MỚI 7 ngày qua | Messenger `facebook.com/messages/` và **Tin nhắn chờ** `facebook.com/messages/requests` | Chỉ đếm người **nhắn trước, lần đầu tiên**, trong 7 ngày. Không đếm cuộc chat nick mình mở đầu hay chat với người cũ. Chỉ mở cuộc chat có hoạt động trong 7 ngày, cuộn lên đầu để xem tin đầu tiên |
| Trong đó QI | Các cuộc chat đã đếm ở dòng trên | Định nghĩa QI ở CLAUDE.md: hỏi giá, MOQ, catalog, sample, thời gian giao hoặc ship **và** là shop hay doanh nghiệp |
| Trong đó khách lẻ/spam | Các cuộc chat đã đếm | Mua 1–2 cái cho con, quảng cáo, lừa đảo, hỏi linh tinh |
| Chuyển WhatsApp 7 ngày qua | Các cuộc chat đã đếm | Khách đã cho số WhatsApp hoặc đã được chuyển sang hotline |
| Order 30 ngày qua | Không tự đếm | Để trống: số này Sale xác nhận qua CRM |
| Giờ dùng nick mỗi ngày | Tab Lịch SM, 7 ngày gần nhất | Trung bình (giờ việc cuối − giờ việc đầu) của các ngày có làm, 1 số lẻ |
| Ngày đếm | — | dd/mm/yyyy |

**Lưu ý khi đọc Messenger:**
- Mở một cuộc chat chưa đọc sẽ làm nó thành "đã đọc". Trước khi mở, ghi lại những cuộc chưa đọc để báo người dùng; nếu là khách hỏi mua thì đẩy vào Radar theo skill `day-du-lieu-radar` (source inbox).
- Không trả lời, kể cả khi khách đang hỏi. Trả lời là việc của skill `tra-loi-lead`, và người dùng phải duyệt.

### 3. Ghi CSV và push
1. Sửa đúng dòng của nick trong `do-luong/moi-nick.csv`:
   - Giữ UTF-8 BOM và đủ 20 cột.
   - Số thập phân dùng dấu chấm.
   - Ô nào không đếm được thì để trống và ghi lý do vào cột Ghi chú. Không đoán.
2. Kiểm tra: `py -X utf8 -c "import csv;r=list(csv.reader(open('do-luong/moi-nick.csv',encoding='utf-8-sig')));assert {len(x) for x in r}=={20};print('ok',len(r)-1,'nick')"`
3. Commit và push:
   - `git add do-luong/moi-nick.csv`
   - `git commit -m "dem-so-nick: SM01-SM03 <dd/mm>"`
   - `git pull --rebase`
   - `git push`
4. Báo người dùng mỗi nick 1 dòng, ví dụ "SM01: 312 bạn, 14 group, 9 bài tường, 6 mess mới (2 QI)". Kèm danh sách ô bị để trống.

## Đếm lại
Mỗi thứ Hai đếm lại để so tuần với tuần:
- Trước khi ghi đè, chép dòng cũ sang `do-luong/lich-su-moi-nick.csv`, cùng tiêu đề.
- Nếu file lịch sử chưa có thì tạo mới, dùng đúng hàng tiêu đề của `moi-nick.csv`.
