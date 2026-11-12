# Đồng bộ PC công ty với kiến trúc 3 cấp (làm theo thứ tự)

Claude trên PC công ty: khi người dùng nói "đồng bộ", "cập nhật repo" hoặc mở phiên đầu tiên sau khi pull, đọc file này và làm từng bước, **báo kết quả mỗi bước 1 dòng**. Bước nào cần người (đăng nhập, mật khẩu, chọn credential) thì dừng và nhờ người dùng.

## Bước 1 — Kéo repo này (ngay)
```powershell
cd "C:\claude remote"; git pull
```
Sau khi pull: skill `chay-lich-sm` đã có mục 2 "ghi log 1 lệnh webhook". **Khi n8n chưa cài, script tự rơi về cách ghi cũ (DỰ PHÒNG)**, nên chạy lịch vẫn bình thường. Chưa cần làm gì thêm để tiếp tục làm việc.

## Bước 2 — Clone repo cấp 2 (nơi n8n ghi việc cho Copilot)
```powershell
git clone https://github.com/viethoang223/smock-level2-copilot.git C:\smock-level2-copilot
```

## Bước 3 — Token webhook (một lần)
Người dùng tự chọn một chuỗi bí mật, rồi:
```powershell
[Environment]::SetEnvironmentVariable('SMOCK_LOG_TOKEN', '<chuỗi bí mật>', 'User')
```
Mở lại terminal / Claude để nhận biến. Cùng chuỗi này sẽ dán vào node "Kiểm tra dữ liệu" của L1-01 ở bước 5.

## Bước 4 — Sheet chính (người dùng làm, Claude kiểm)
- Thêm cột **K "Mã log"** vào tab Nhật Ký SM.
- Tạo 4 tab mới đúng tiêu đề trong `ops/contract.json`: Content Queue, Lead Hunter, Group Score, Báo cáo ngày.
- Claude kiểm bằng gviz: đọc dòng 1 từng tab, so với `ops/contract.json`, báo cột nào lệch.

## Bước 5 — Cài n8n cấp 1
Theo `n8n/level1/README.md` (n8n 2.x npm + NSSM, file `.env`, import 7 workflow, chọn credential Google). Bật dần: L1-07 → L1-01 → L1-05 → L1-04 → L1-02 + L1-03 → L1-06 → Lead Hunter. Sau khi bật L1-01, chạy lệnh kiểm nhanh trong README: phải ra `OK`, chạy lần 2 ra "đã ghi trước đó".

## Bước 6 — Máy cấp 2 (máy khác có VS Code + Copilot)
Theo `README.md` của repo `smock-level2-copilot` (Copilot CLI, Task Scheduler 05:30).

## Trạng thái từng bước
Ghi vào `tien-do.md` mục "Đồng bộ 3 cấp": bước nào xong, ngày nào, ai làm.

## Chưa bật (chờ người dùng quyết)
- Skill `lay-text-group`: có thể trái Điều khoản thu thập dữ liệu tự động của Meta. **Không chạy** cho đến khi người dùng xác nhận trong chat.
- Mọi thao tác cấp 3 trên nick persona: xem mục tuân thủ trong báo cáo "Vận hành 3 cấp theo ca" (Usage Policy của Anthropic cấm persona giả / điều phối nhiều tài khoản để né phát hiện). Người dùng quyết danh sách nick được dùng.
