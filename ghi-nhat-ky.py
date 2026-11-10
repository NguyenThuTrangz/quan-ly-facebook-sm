# Ghi một dòng vào sheet "Nhật ký" của Quan-ly-Facebook-hang-ngay.xlsx
# Cách dùng: python ghi-nhat-ky.py <Mã TK> <Loại việc> <Nơi thực hiện> <Nội dung> <Kết quả> [Chế độ hiển thị] [Ngày YYYY-MM-DD]
import sys
import datetime
from pathlib import Path
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
FILE = Path(__file__).with_name("Quan-ly-Facebook-hang-ngay.xlsx")

args = sys.argv[1:]
if len(args) < 5:
    sys.exit(__doc__ or "Thiếu tham số: Mã TK, Loại việc, Nơi thực hiện, Nội dung, Kết quả")
ma, loai, noi, nd, kq = args[:5]
che_do = args[5] if len(args) > 5 and args[5] else None
ngay = args[6] if len(args) > 6 else datetime.date.today().isoformat()

wb = openpyxl.load_workbook(FILE)
nk = wb["Nhật ký"]
r = 2
while nk.cell(row=r, column=1).value not in (None, ""):
    r += 1
for col, v in ((1, ngay), (2, ma), (4, loai), (5, noi), (6, nd), (7, che_do), (8, kq)):
    nk.cell(row=r, column=col, value=v)
wb.save(FILE)
print(f"Đã ghi dòng {r}: {ngay} | {ma} | {loai} | {kq}")
