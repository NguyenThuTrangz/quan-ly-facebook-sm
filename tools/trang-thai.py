"""Xem nhanh hệ thống Smock đang ở đâu. Gõ:  trang-thai   (trong cmd hoặc PowerShell)
Chỉ đọc: n8n (healthz + database), Task Scheduler, repo cấp 2. Không sửa gì."""
import json, sqlite3, subprocess, urllib.request, pathlib, datetime as dt

DB = r"C:\n8n\.n8n\database.sqlite"
L2 = pathlib.Path(r"C:\smock-level2-copilot")
VN = dt.timedelta(hours=7)
now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + VN
ok = lambda b: "✅" if b else "❌"

print(f"=== Trạng thái Smock lúc {now:%H:%M %d/%m/%Y} ===\n")
try:
    up = urllib.request.urlopen("http://localhost:5678/healthz", timeout=4).status == 200
except Exception:
    up = False
print(f"{ok(up)} n8n {'đang chạy' if up else 'KHÔNG chạy → gõ: n8n   (hoặc đăng xuất/đăng nhập lại Windows)'}")

for task in ("Smock n8n", "Smock Copilot cap 2"):
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
        f"$t=Get-ScheduledTask -TaskName '{task}' -EA SilentlyContinue; if($t){{$i=Get-ScheduledTaskInfo -TaskName '{task}'; "
        f"\"$($t.State)|$($i.LastRunTime.ToString('HH:mm dd/MM'))|$($i.LastTaskResult)|$($i.NextRunTime.ToString('HH:mm dd/MM'))\"}}"],
        capture_output=True, text=True)
    s = r.stdout.strip()
    if not s:
        print(f"❌ Tác vụ '{task}' chưa tạo")
    else:
        st, last, res, nxt = (s.split("|") + ["", "", "", ""])[:4]
        print(f"{ok(res in ('0', '267009') or st == 'Running')} Tác vụ '{task}': {st}, chạy gần nhất {last} (mã {res}), lần tới {nxt or '—'}")

print("\n--- Workflow n8n (lần chạy gần nhất) ---")
NEXT = {"L1-01": "khi Claude ghi log", "L1-02": "21:30 / bù 08:20", "L1-03": "22:00 / bù 08:25", "L1-04": "18:00",
        "L1-05": "06:30, 21:50", "L1-06": "gửi 22:15 / bù 08:35 · kéo 06:30, 9:30, 11:30, 14:30, 16:30",
        "L1-07": "00:15", "Smock": "6 tiếng/lần"}
try:
    c = sqlite3.connect(f"file:{pathlib.Path(DB).as_posix()}?mode=ro", uri=True)
    for wid, name, active in c.execute("select id,name,active from workflow_entity order by name"):
        r = c.execute("select status,mode,startedAt from execution_entity where workflowId=? and mode!='cli' order by id desc limit 1", (wid,)).fetchone()
        last = "chưa chạy"
        if r:
            t = dt.datetime.fromisoformat(r[2][:19]) + VN
            last = f"{'✅' if r[0] == 'success' else '❌ ' + r[0]} {t:%H:%M %d/%m} ({'tự' if r[1] in ('trigger', 'webhook') else 'tay'})"
        key = name.split(" ")[0]
        print(f"{'🟢 BẬT' if active else '⚪ TẮT'}  {name[:42]:<42} {last:<28} lịch: {NEXT.get(key, '')}")
    c.close()
except Exception as e:
    print("❌ không đọc được database n8n:", e)

print("\n--- Cấp 2 (Copilot) ---")
if (L2 / ".git").exists():
    done = {p.name for p in (L2 / "done").glob("*.json")}
    outs = {p.name for p in (L2 / "outbox").rglob("*.json")}
    todo = [p.name for p in (L2 / "inbox").rglob("*.json") if p.name not in done and p.name not in outs]
    print(f"Inbox chờ Copilot: {len(todo)} việc · Outbox chờ n8n kéo về: {len(outs)} · Đã xong: {len(done)}")
    logs = sorted((L2 / "logs").glob("run-*.log"))
    if logs:
        tail = [l for l in logs[-1].read_text(encoding="utf-8-sig", errors="replace").splitlines() if l[:2].isdigit()][-2:]
        print(f"Lần Copilot tự chạy gần nhất ({logs[-1].stem[4:]}): " + " | ".join(tail))
else:
    print("❌ chưa có repo C:\\smock-level2-copilot")

print("\n--- Việc của bạn ---")
h = now.hour
if now.weekday() == 6:
    print("Chủ nhật: nghỉ. n8n tối nay 21:30 sinh lịch thứ Hai.")
elif h < 8 or (h == 8 and now.minute < 30):
    print("Trước giờ làm: không cần làm gì. 08:30 mở agent cấp 3 gõ: chạy lịch luồng 1")
elif h < 17:
    print("Giờ làm: agent cấp 3 đang/nên chạy lịch (gõ: chạy lịch luồng 1). Rảnh thì duyệt caption ở tab Pool Content SM (xoá chữ 'chờ duyệt').")
else:
    print("Hết giờ: để máy bật + vẫn đăng nhập Windows (khoá màn hình Win+L được, không Sign out). Tối n8n tự chuẩn bị cho ngày mai.")
