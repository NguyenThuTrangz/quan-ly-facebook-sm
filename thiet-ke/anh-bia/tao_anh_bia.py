# Tạo ảnh bìa Facebook cho nick SM theo concept "<TÊN> SMOCKS" (K-Embroidery).
# Cách gọi (cần Pillow; dùng `py` thường, KHÔNG dùng -I vì Pillow cài ở user site):
#   py "thiet-ke\anh-bia\tao_anh_bia.py" --ten "OLIVIA" --avatar <ảnh avatar> --out <file.png>
#   tuỳ chọn: --mau hd|chuan (mặc định hd = nền 2659x984 có icon WhatsApp + CONTACT ME; chuan = nền 851x315 kiểu Sophie/Rosie)
#             --wa "+84 855 555 490"  --tam-y 0.45 (vị trí dọc tâm khuôn mặt trong avatar, 0..1)
# Kết quả: <out> đúng kích thước nền + <out>_1640x624.png (chuẩn ảnh bìa FB).
import argparse, os
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(D, 'fonts', 'Montserrat-VF.ttf')
FONT_I = os.path.join(D, 'fonts', 'Montserrat-Italic-VF.ttf')
XANH = (20, 93, 160)      # màu chữ tên + số WA (lấy mẫu từ ảnh gốc)

# Hình học đo từ ảnh gốc (goc/SM03_rosie_goc.png, goc/SM02_marie_goc.png)
MAU = {
    'chuan': dict(nen='nen_chuan_851x315.png', tam=(161.5, 147), r_anh=96,
                  ten_tam_x=497, ten_tren=87, ten_cao=36, ten_rong_max=470, ten_tracking=0.0,
                  so_xy=(268, 246), so_size=17.5),
    'hd':    dict(nen='nen_hd_2659x984.png', tam=(447, 491.5), r_anh=301,
                  ten_tam_x=1619, ten_tren=333, ten_cao=110, ten_rong_max=1500, ten_tracking=0.12,
                  so_xy=(1105, 642), so_size=41.5),
}

def font(path, size, ten):
    f = ImageFont.truetype(path, size)
    try: f.set_variation_by_name(ten)
    except Exception: pass
    return f

def ve_chu_tracking(d, xy, s, f, fill, tracking):
    """Vẽ chữ có giãn ký tự (tracking = tỉ lệ cỡ chữ)."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking * f.size

def rong_tracking(s, f, tracking):
    return sum(f.getlength(ch) for ch in s) + tracking * f.size * (len(s) - 1)

def dan_avatar(nen, avatar, tam, r, tam_y=0.45):
    a = Image.open(avatar).convert('RGB')
    w, h = a.size; c = min(w, h)
    x0 = (w - c) // 2
    y0 = int(max(0, min(h - c, h * tam_y - c / 2)))
    a = a.crop((x0, y0, x0 + c, y0 + c)).resize((2 * r, 2 * r), Image.LANCZOS)
    ss = 4  # mặt nạ tròn khử răng cưa
    m = Image.new('L', (2 * r * ss, 2 * r * ss), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r * ss - 1, 2 * r * ss - 1), fill=255)
    m = m.resize((2 * r, 2 * r), Image.LANCZOS)
    nen.paste(a, (int(tam[0] - r), int(tam[1] - r)), m)

def tao(ten, avatar, out, mau='hd', wa='+84 855 555 490', tam_y=0.45):
    g = MAU[mau]
    im = Image.open(os.path.join(D, 'nen', g['nen'])).convert('RGB')
    if avatar: dan_avatar(im, avatar, g['tam'], g['r_anh'], tam_y)
    d = ImageDraw.Draw(im)
    chu = f'{ten.strip().upper()} SMOCKS'
    # cỡ chữ tên: chiều cao chữ hoa = ten_cao, thu nhỏ nếu quá rộng
    size = g['ten_cao'] / 0.70
    f = font(FONT_I, size, 'ExtraBold Italic')
    cap = f.getbbox('H')[3] - f.getbbox('H')[1]
    size *= g['ten_cao'] / cap
    f = font(FONT_I, size, 'ExtraBold Italic')
    while rong_tracking(chu, f, g['ten_tracking']) > g['ten_rong_max']:
        size *= 0.97; f = font(FONT_I, size, 'ExtraBold Italic')
    rong = rong_tracking(chu, f, g['ten_tracking'])
    cao = f.getbbox('H')[3] - f.getbbox('H')[1]
    tren = g['ten_tren'] + (g['ten_cao'] - cao) / 2
    ve_chu_tracking(d, (g['ten_tam_x'] - rong / 2, tren - f.getbbox('H')[1]), chu, f, XANH, g['ten_tracking'])
    # số WhatsApp
    fs = font(FONT, g['so_size'], 'Bold')
    bb = fs.getbbox(wa)
    d.text((g['so_xy'][0] - bb[0], g['so_xy'][1] - bb[1]), wa, font=fs, fill=XANH)
    im.save(out)
    # bản chuẩn FB 1640x624 (phủ kín, cắt đều 2 bên)
    W, H = im.size; s = 624 / H; nw = round(W * s)
    fb = im.resize((nw, 624), Image.LANCZOS); x = (nw - 1640) // 2
    out2 = os.path.splitext(out)[0] + '_1640x624.png'
    fb.crop((x, 0, x + 1640, 624)).save(out2)
    return out, out2

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ten', required=True)
    p.add_argument('--avatar')
    p.add_argument('--out', required=True)
    p.add_argument('--mau', default='hd', choices=list(MAU))
    p.add_argument('--wa', default='+84 855 555 490')
    p.add_argument('--tam-y', type=float, default=0.45)
    a = p.parse_args()
    print(*tao(a.ten, a.avatar, a.out, a.mau, a.wa, a.tam_y), sep='\n')
