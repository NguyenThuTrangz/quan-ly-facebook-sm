# Ảnh bìa nick SM — concept "<TÊN> SMOCKS"

## Concept (giữ nguyên cho mọi nick SM)
- Nền pastel smock: váy smock hồng/trắng, khung thêu, hoa cẩm tú cầu, cuộn chỉ — tông kem/hồng nhạt.
- Trên giữa: logo **K-EMBROIDERY** + "Stitching sustainability into every thread" (nằm sẵn trong nền).
- Trái: avatar tròn, viền xanh navy `#4D6276` (77,98,118) + vòng trắng bên trong.
- Giữa: tên **"<TÊN> SMOCKS"** — Montserrat ExtraBold Italic, IN HOA, màu xanh `#145DA0` (20,93,160).
- Dưới tên: tagline "Custom smocked & embroidered collections" (nằm sẵn trong nền).
- Dòng liên hệ: số WhatsApp (Montserrat Bold, `#145DA0`) + `www.k-embroidery.com`.
- **Số WhatsApp chung mọi nick SM: +84 855 555 490** (người dùng chốt 20/11/2026; đổi số phải hỏi người dùng).

## Hai mẫu nền (`nen/`)
| Mẫu | File | Kích thước | Ghi chú |
|---|---|---|---|
| `hd` (mặc định) | `nen_hd_2659x984.png` | 2659x984 | Từ bìa MARIE (SM02), có icon WhatsApp, icon web, nút CONTACT ME; nét cao |
| `chuan` | `nen_chuan_851x315.png` | 851x315 | Từ bìa ROSIE (SM03), kiểu Sophie/Rosie; độ phân giải thấp |

Nền tạo bằng cách xoá tên + số khỏi ảnh gốc (`goc/`) bằng nội suy màu 2 chiều (vùng sau chữ là nền phẳng nên không lộ vệt). Avatar cũ vẫn nằm trong nền nhưng bị avatar mới phủ kín (dán hình tròn đúng bán kính ảnh).

## Cách tạo ảnh bìa cho nick mới
```
py "thiet-ke\anh-bia\tao_anh_bia.py" --ten "OLIVIA" --avatar <ảnh avatar> --out "thiet-ke\anh-bia\moi\SM05_olivia.png"
```
- Dùng `py` thường (không `-I`, vì Pillow cài ở user site). Font Montserrat có sẵn trong `fonts/`.
- Tuỳ chọn: `--mau chuan` (nền 851x315), `--wa "<số>"` (chỉ khi người dùng duyệt số khác), `--tam-y 0.35` (dịch khung cắt avatar lên/xuống để mặt nằm giữa vòng tròn).
- Ra 2 file: kích thước nền + `_1640x624.png` (chuẩn ảnh bìa FB, dùng file này để tải lên).
- Tên dài tự thu nhỏ cho vừa. Avatar nên là ảnh vuông/dọc, người ở giữa.

## Thư mục
- `goc/` — ảnh bìa gốc SM01 (Sophie, 851x315 JPG), SM02 (Marie, 2659x984), SM03 (Rosie, 851x315), avatar SM01/SM02, tham khảo bìa Jenny (SM04).
- `moi/` — 3 ảnh bìa đã đổi số +84 855 555 490 (giữ nguyên toàn bộ phần còn lại): `SM0x_<tên>_<kích thước gốc>.png` + `_1640x624.png`.
- `mau-thu/` — ảnh mẫu chứng minh script chạy.

## Hạn chế
- Bìa Sophie/Rosie gốc chỉ 851x315 → bản 1640x624 là phóng to, hơi mềm nét. Muốn sắc hơn nên dùng mẫu `hd`.
- Tagline và website cố định trong nền; muốn đổi tagline phải sửa nền.
