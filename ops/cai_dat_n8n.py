"""Cài / cập nhật 7 workflow cấp 1 vào n8n trên máy này, KHÔNG phải chọn credential bằng tay.

Chạy (n8n có thể đang chạy):   py -I -X utf8 ops/cai_dat_n8n.py
Làm gì:
  1. Đọc (chỉ đọc) database n8n: credential Google Sheets / Google Drive / Telegram đã tạo, và id các workflow đang có.
  2. Với mỗi file n8n/level1/L1-*.json: gắn credential thật vào mọi node cần (theo nodeCredentialType), thay token
     DOI_TOKEN_O_DAY bằng biến môi trường SMOCK_LOG_TOKEN, giữ nguyên id workflow cũ cùng tên → import đè, không sinh bản trùng.
  3. Import qua CLI bằng cổng tạm (không đụng n8n đang chạy). File tạm chứa token nằm ngoài repo và bị xoá ngay.
  4. Bổ sung C:\\n8n\\.env: N8N_RESTRICT_FILE_ACCESS_TO (cho phép ghi anh-dang-bai, repo cấp 2, thư mục sao lưu).
Lý do: workflow import từ JSON không mang credential → n8n hiện như đã chọn nhưng khi chạy báo "Credentials not found"
cho tới khi mở node chọn lại và lưu. Gắn sẵn id credential thì chạy được ngay.
Workflow import luôn ở trạng thái TẮT; bật thủ công theo thứ tự trong n8n/level1/README.md.
"""
import json, os, pathlib, sqlite3, subprocess, sys, shutil, uuid, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
N8N_DIR = pathlib.Path(os.environ.get("N8N_HOME", r"C:\n8n"))
DB = N8N_DIR / ".n8n" / "database.sqlite"
ENV = N8N_DIR / ".env"
CLI = N8N_DIR / "bin" / "n8n.cmd"
L2_REPO = pathlib.Path(r"C:\smock-level2-copilot")
FILE_ACCESS = r"C:\claude remote\anh-dang-bai;C:\smock-level2-copilot;C:\n8n-backup"
NODE_CRED = {"n8n-nodes-base.googleSheets": "googleSheetsOAuth2Api", "n8n-nodes-base.googleDrive": "googleDriveOAuth2Api",
             "n8n-nodes-base.telegram": "telegramApi"}


def user_env(name):
    """Biến môi trường User của Windows (đặt bằng SetEnvironmentVariable, chưa có trong phiên hiện tại)."""
    if os.name != "nt":
        return ""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, name)[0]
    except OSError:
        return ""


def main():
    if not DB.exists():
        sys.exit(f"Không thấy database n8n ở {DB}. Chạy n8n ít nhất 1 lần trước.")
    db = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    creds = {}
    for cid, name, typ, upd in db.execute("select id,name,type,updatedAt from credentials_entity order by updatedAt"):
        creds[typ] = {"id": cid, "name": name}          # trùng loại → lấy cái sửa gần nhất
    existing, was_active = {}, set()
    for wid, name, upd, act in db.execute("select id,name,updatedAt,active from workflow_entity order by updatedAt"):
        existing[name] = wid                            # trùng tên → lấy bản sửa gần nhất
        if act: was_active.add(wid)
    db.close()
    for need in ("googleSheetsOAuth2Api", "googleDriveOAuth2Api"):
        print(("✓ " if need in creds else "✗ THIẾU ") + f"credential {need}" + (f" = {creds[need]['name']}" if need in creds else " — tạo trong n8n rồi chạy lại"))

    token = os.environ.get("SMOCK_LOG_TOKEN") or user_env("SMOCK_LOG_TOKEN")
    print("✓ token SMOCK_LOG_TOKEN" if token else "✗ chưa có biến SMOCK_LOG_TOKEN — L1-01 sẽ từ chối mọi log")

    tmp = N8N_DIR / ("import-" + uuid.uuid4().hex[:8])
    tmp.mkdir(parents=True)
    try:
        report = []
        serper = os.environ.get("SERPER_API_KEY") or user_env("SERPER_API_KEY")
        files = sorted((ROOT / "n8n" / "level1").glob("L1-*.json")) + [ROOT / "n8n" / "smock-lead-hunter.json"]
        # Tham số: chỉ cài file có tên chứa chuỗi đó (vd: cai_dat_n8n.py lead  |  cai_dat_n8n.py L1-02 L1-03)
        if sys.argv[1:]:
            files = [f for f in files if any(a.lower() in f.name.lower() for a in sys.argv[1:])]
        for f in files:
            wf = json.loads(f.read_text(encoding="utf8"))
            wf["id"] = existing.get(wf["name"]) or hashlib.md5(wf["name"].encode()).hexdigest()[:16]
            missing = set()
            for n in wf["nodes"]:
                typ = n.get("parameters", {}).get("nodeCredentialType") or NODE_CRED.get(n["type"])
                if not typ:
                    continue
                if typ in creds:
                    n["credentials"] = {typ: creds[typ]}
                elif not n.get("disabled"):
                    missing.add(typ)
            s = json.dumps(wf, ensure_ascii=False)
            if token:
                s = s.replace("DOI_TOKEN_O_DAY", token)
            if serper:
                s = s.replace("YOUR_SERPER_API_KEY", serper)
            elif "YOUR_SERPER_API_KEY" in s:
                missing.add("biến SERPER_API_KEY")
            (tmp / f.name).write_text(s, encoding="utf8")
            report.append(f"  {wf['name']}  (id {wf['id']}{', THIẾU ' + ', '.join(sorted(missing)) if missing else ''})")
        env = dict(os.environ, N8N_RUNNERS_BROKER_PORT="5689", N8N_PORT="5699")
        r = subprocess.run(["cmd", "/c", str(CLI), "import:workflow", "--separate", f"--input={tmp}"], env=env,
                           capture_output=True, text=True, encoding="utf8", errors="replace")
        out = [l for l in (r.stdout + r.stderr).splitlines() if "mport" in l or "rror" in l]
        print("\n".join(out[-3:]) or r.stdout[-500:])
        print("\n".join(report))
        # Import luôn để workflow ở trạng thái tắt → bật lại cái nào trước đó đang bật
        again = [json.loads((tmp / f.name).read_text(encoding="utf8"))["id"] for f in files]
        again = [i for i in again if i in was_active]
        for wid in again:
            subprocess.run(["cmd", "/c", str(CLI), "publish:workflow", f"--id={wid}"], env=env, capture_output=True)
        if again:
            print(f"✓ bật lại {len(again)} workflow đang bật trước đó → tắt n8n (Ctrl+C) rồi gõ lại: n8n")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Quyền ghi file cho node Read/Write File (n8n 2.x chặn ngoài thư mục được phép)
    lines = ENV.read_text(encoding="utf8").splitlines() if ENV.exists() else []
    if not any(l.startswith("N8N_RESTRICT_FILE_ACCESS_TO=") for l in lines):
        lines.append("N8N_RESTRICT_FILE_ACCESS_TO=" + FILE_ACCESS)
        ENV.write_text("\n".join(lines) + "\n", encoding="utf8")
        print("✓ đã thêm N8N_RESTRICT_FILE_ACCESS_TO vào .env → tắt n8n (Ctrl+C) rồi gõ lại: n8n")
    for p in FILE_ACCESS.split(";"):
        if "smock-level2" not in p:
            pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    if not (L2_REPO / ".git").exists():
        print(f"✗ chưa có repo cấp 2 ở {L2_REPO} → L1-06 chưa chạy được (git clone repo smock-level2-copilot vào đây)")


if __name__ == "__main__":
    main()
