# Cấp 3 tự chạy luồng (từ 22/11/2026, máy treo 24/24)

Hai tác vụ hẹn giờ của Claude desktop (`smock-luong-1`, `smock-luong-2`) nổ mỗi giờ (phút :05) trong các khung giờ thị trường (từ 27/11 giảm từ 30 phút xuống 1 giờ vì tài khoản Claude chạm giới hạn tuần 25–27/11)
(giờ VN: 06:00–09:59, 14:00–17:59, 19:00–23:59 — phủ cả giờ mùa đông lẫn mùa hè của Mỹ/Anh). Mỗi lần nổ là một phiên Claude mới,
làm các dòng Lịch SM đến hạn của luồng mình rồi thoát. Lịch do n8n L1-02 sinh (21:30 tối hôm trước, bù 05:20–11:20).

Khung giờ thị trường (ops/build_level1.py → `MARKET_WINDOWS`, giờ địa phương, tự quy đổi):
| Khung | Giờ địa phương | Giờ VN mùa đông | Giờ VN mùa hè |
|---|---|---|---|
| US tối | 19:00–21:45 New York | 07:00–09:45 | 06:00–08:45 |
| UK/EU sáng (= tối ở Úc) | 08:00–10:30 London | 15:00–17:30 | 14:00–16:30 |
| US sáng (giờ vàng) | 08:00–11:30 New York | 20:00–23:30 | 19:00–22:30 |

Luồng: nick theo thứ tự tab Tài khoản, xen kẽ → luồng 1 = SM01, SM03, SM05, SM07; luồng 2 = SM02, SM04, SM06, SM08 (cột J Lịch SM ghi "luồng n · <khung>").

## Mỗi lần chạy (phiên cấp 3 làm đúng thứ tự)
1. **Khoá luồng**: file `C:\claude remote\.lock-luong-<n>`. Có file và sửa đổi < 55 phút trước → trả lời 1 dòng "luồng n đang chạy ở phiên khác" rồi dừng. Không thì ghi giờ hiện tại vào file.
2. **Đọc lịch** bằng PowerShell (không cần trình duyệt):
   `(Invoke-WebRequest 'https://docs.google.com/spreadsheets/d/1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0/gviz/tq?tqx=out:csv&sheet=L%E1%BB%8Bch%20SM&range=A1:J5000' -UseBasicParsing).Content | ConvertFrom-Csv`
   Số dòng sheet = chỉ số (0-based) + 2. Lấy dòng: A = hôm nay (yyyy-mm-dd, giờ VN), J chứa `luồng <n>`, G = Có, H = `Chờ`.
3. **Chọn việc**: giờ cột B ≤ bây giờ + 55 phút. Dòng trễ > 90 phút → không làm, ghi webhook `Bỏ qua` J = 0 nội dung "trễ quá 90 phút". Không có việc → xoá khoá, trả lời 1 dòng, dừng.
4. **Làm** theo skill `chay-lich-sm` (đọc `.claude/skills/chay-lich-sm/SKILL.md`), theo giờ tăng dần, gom các việc liền nhau của cùng nick (chọn trình duyệt 1 lần). Chỉ chọn deviceId trong bảng của skill. Ghi log từng việc bằng `tools\ghi-log-webhook.ps1 … -LichRow <dòng>`.
5. **Sự cố**: checkpoint / bị đăng xuất / "confirm your identity" / "can't use this feature" / bài bị gỡ → ghi `Không làm được` (J = 0, nêu rõ cảnh báo trong nội dung), bỏ các việc còn lại của nick đó trong lần chạy này. Không nhập mật khẩu, không bấm xác minh. Trình duyệt không kết nối sau khi chạy shortcut + chờ 45 giây → `Không làm được` "trình duyệt không kết nối".
6. **Giới hạn thời gian**: chạy quá 50 phút → làm xong việc đang dở, dừng (việc còn lại để lần sau).
7. **Kết thúc**: xoá file khoá, đóng tab đã mở, trả lời 1 dòng ("✅ luồng n 20:30: 4 việc xong, 1 bỏ qua").

Quy tắc nghiệp vụ (đăng công khai, nội quy group, WA 490, không seeding…) theo CLAUDE.md. Kho content trống thì lịch không có dòng đăng bài — không tự lấy content khác.

## Giám sát
- Tác vụ Windows `Smock n8n watchdog` (mỗi 10 phút, `tools\n8n-watchdog.ps1`): n8n không trả lời → tự chạy lại; nhật ký `logs\n8n-watchdog.log`.
- Lượt không có việc phải thoát ngay sau khi đọc lịch (không đọc file khác) để tiết kiệm giới hạn sử dụng.

## Bật / tắt
Trong app Claude desktop → Scheduled tasks: `smock-luong-1`, `smock-luong-2` (tạm dừng = tắt enabled). App phải đang mở; app tắt lúc tới giờ thì chạy bù khi mở lại (dòng trễ > 90 phút tự bỏ qua).
