"""Sinh các workflow n8n cấp 1 (ops/../n8n/level1/*.json) từ một chỗ, để cả bộ dùng chung hằng số.

Chạy:  py -I -X utf8 ops/build_level1.py
Sau khi import vào n8n: chọn credential cho các node có ghi "CHỌN CREDENTIAL", đổi các hằng số trong node "Cấu hình".
"""
import json, uuid, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "n8n" / "level1"
OUT.mkdir(parents=True, exist_ok=True)
CONTRACT = json.loads((ROOT / "ops" / "contract.json").read_text(encoding="utf8"))
SHEET = CONTRACT["sheet_id"]
API = "https://sheets.googleapis.com/v4/spreadsheets/" + SHEET

CONFIG_JS = r"""// ===== Cấu hình chung cấp 1 (sửa ở đây) =====
const CFG = {
  SHEET_ID: '%s',
  TOKEN: 'DOI_TOKEN_O_DAY',                 // trùng biến SMOCK_LOG_TOKEN trên máy cấp 3
  PACK_DIR: 'C:/claude remote/anh-dang-bai', // thư mục gói bài cấp 3 đọc
  L2_REPO: 'C:/smock-level2-copilot',        // bản clone repo cấp 2 trên máy này
  OFFICE_START: '08:30', OFFICE_END: '17:00',
  LUNCH_START: '11:45', LUNCH_END: '13:15',
  NICK_GROUP_GAP_MIN: 60,       // 2 bài group của CÙNG 1 nick cách nhau tối thiểu (phút)
  TEAM_GROUP_GAP_MIN: 6,        // 2 bài group bất kỳ của cả đội cách nhau tối thiểu (phút)
  GROUP_REPOST_DAYS: 3,         // 1 nick không đăng lại cùng 1 group trong ngần này ngày; cả đội không trùng group trong ngày
  TASK_GAP: [2, 4], BLOCK_GAP: [6, 12], // phút giữa 2 việc trong cụm / giữa 2 cụm
  LANES: 2,                     // số luồng chạy song song: mỗi luồng = 1 phiên Claude cấp 3 + nhóm trình duyệt riêng
  JG_COL: { SM01: 3, SM02: 4, SM03: 5, SM04: 8, SM05: 9, SM06: 10, SM07: 11, SM08: 12 }, // cột nick trong tab Join Group SM (D,E,F,I..M)
  JG_TIER_COL: 6,               // cột G "Tier" tab Join Group SM — dùng khi tab Group Score chưa chấm
  K_START: 122,                 // mã bài Kxxx lớn nhất đã dùng trước khi có n8n (Smock Radar)
  CONTENT_REUSE_DAYS: 7,        // bộ ảnh được phái sinh caption mới sau ngần này ngày
};
// Kho content dùng tab có sẵn, KHÔNG cần tab riêng:
//  - workbook KE, tab '3. CONTENT GROUP' (A STT, B TEXT, C MEDIA) → mã CG<STT>
//  - tab 'Pool Content SM' (A STT, B Content, C Ảnh/Video, D Phân loại) → mã PC<STT>; Phân loại có "chờ duyệt" thì chưa dùng
//  - content đã dùng / mã bài Kxxx: đọc từ cột F, J tab 'Lịch SM' (vd "đăng group K123 (CG13) → group 5")
const buildPool = (ke, pool) => {
  const out = [];
  // row = số dòng thật trên sheet (KE đọc từ A3, Pool Content SM đọc từ A2)
  ke.forEach((r, i) => { const s = String(r[0] || '').trim(); if (/^\d+$/.test(s) && String(r[1] || '').trim()) out.push({ id: 'CG' + s, caption: r[1], media: r[2] || '', kind: 'any', row: i + 3 }); });
  pool.forEach((r, i) => { const s = String(r[0] || '').trim(); if (/^\d+$/.test(s) && String(r[1] || '').trim() && !/chờ duyệt/i.test(r[3] || ''))
    out.push({ id: 'PC' + s, caption: r[1], media: r[2] || '', kind: /tường|wall/i.test(r[3] || '') ? 'wall' : 'any', note: r[3] || '', row: i + 2 }); });
  return out;
};
const lichText = r => (r[5] || '') + ' ' + (r[9] || '');
const usedContent = lich => { const s = new Set(); for (const r of lich) for (const m of lichText(r).matchAll(/\b(CG|PC)(\d+)\b/g)) s.add(m[1] + m[2]); return s; };
const maxKOf = (lich, start) => { let k = start; for (const r of lich) for (const m of lichText(r).matchAll(/\bK(\d{3,})\b/g)) k = Math.max(k, +m[1]); return k; };
const vnNow = () => new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' }));
const isoOf = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const vnOf = d => `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
const sameDay = (s, d) => { s = String(s || '').trim(); return s.startsWith(isoOf(d)) || s.startsWith(vnOf(d)); };
""" % SHEET
KE_SHEET = "1mY_7HeFFokARzxwS9xCeby46cYGC5QpA_ju4jl5f-UA"
KE_RANGE = "\"'3. CONTENT GROUP'!A3:D2000\""
POOL_RANGE = "\"'Pool Content SM'!A2:F2000\""

def node(name, typ, ver, params, pos, **extra):
    n = {"parameters": params, "id": str(uuid.uuid4()), "name": name, "type": typ, "typeVersion": ver, "position": pos}
    n.update(extra)
    return n

def code(name, js, pos, notes=None, each=False):
    p = {"jsCode": js}
    if each: p["mode"] = "runOnceForEachItem"
    return node(name, "n8n-nodes-base.code", 2, p, pos, **({"notes": notes} if notes else {}))

def gget(name, rng_expr, pos, notes="Credential Google Sheets OAuth2 được gắn tự động bởi ops/cai_dat_n8n.py.", sheet=None):
    api = API if sheet is None else "https://sheets.googleapis.com/v4/spreadsheets/" + sheet
    return node(name, "n8n-nodes-base.httpRequest", 4.2, {
        "url": "=" + api + "/values/{{ encodeURIComponent(" + rng_expr + ") }}",
        "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api",
        "options": {"response": {"response": {"responseFormat": "json"}}}}, pos,
        retryOnFail=True, maxTries=3, waitBetweenTries=3000, notes=notes, alwaysOutputData=True)

def gpost(name, path_expr, body_expr, pos, notes="Credential Google Sheets OAuth2 được gắn tự động bởi ops/cai_dat_n8n.py.", **extra):
    return node(name, "n8n-nodes-base.httpRequest", 4.2, {
        "method": "POST", "url": "=" + API + path_expr,
        "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api",
        "sendBody": True, "specifyBody": "json", "jsonBody": "={{ JSON.stringify(" + body_expr + ") }}",
        "options": {}}, pos, retryOnFail=True, maxTries=3, waitBetweenTries=3000, notes=notes, **extra)

def sched(name, cron, pos, notes=None):
    return node(name, "n8n-nodes-base.scheduleTrigger", 1.2,
                {"rule": {"interval": [{"field": "cronExpression", "expression": cron}]}}, pos,
                **({"notes": notes} if notes else {}))

def iff(name, expr, pos):
    return node(name, "n8n-nodes-base.if", 2, {"conditions": {
        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 1},
        "conditions": [{"id": str(uuid.uuid4()), "leftValue": "=" + expr, "rightValue": True,
                        "operator": {"type": "boolean", "operation": "true", "singleValue": True}}],
        "combinator": "and"}, "options": {}}, pos)

def telegram(name, text_expr, pos):
    return node(name, "n8n-nodes-base.telegram", 1.2, {"chatId": "YOUR_TELEGRAM_GROUP_CHAT_ID", "text": "=" + text_expr,
                "additionalFields": {}}, pos, disabled=True,
                notes="Tuỳ chọn: bật node, CHỌN CREDENTIAL Telegram, điền chat ID NHÓM MKT/Sale (không gửi vào máy chủ tài khoản Claude).")

def link(conns, a, b, out=0):
    conns.setdefault(a, {"main": []})
    while len(conns[a]["main"]) <= out: conns[a]["main"].append([])
    conns[a]["main"][out].append({"node": b, "type": "main", "index": 0})

def save(fname, name, nodes, conns, notes):
    wf = {"name": name, "nodes": nodes, "connections": conns, "active": False, "pinData": {},
          "settings": {"executionOrder": "v1", "timezone": CONTRACT["timezone"], "saveDataErrorExecution": "all",
                       "saveDataSuccessExecution": "all"},
          "meta": {"smockNotes": notes}, "tags": []}
    (OUT / fname).write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf8")
    return wf

LV = json.dumps(CONTRACT["tabs"]["Nhật Ký SM"]["loai_viec"], ensure_ascii=False)
TT = json.dumps(CONTRACT["tabs"]["Nhật Ký SM"]["trang_thai"], ensure_ascii=False)
STATUS = json.dumps({k: v.get("statuses", []) for k, v in CONTRACT["tabs"].items()}, ensure_ascii=False)
HEADERS = json.dumps({k: v["headers"] for k, v in CONTRACT["tabs"].items()}, ensure_ascii=False)
HEADER_ROW = json.dumps({k: v.get("header_row", 1) for k, v in CONTRACT["tabs"].items()}, ensure_ascii=False)
FORBID = json.dumps(CONTRACT["forbidden_fields"])

# ---------------------------------------------------------------- L1-01 webhook ghi log + cập nhật trạng thái
validate_js = CONFIG_JS + r"""
const LOAI = %s, TT = %s, STATUS = %s, FORBID = %s;
const req = $input.first().json;
const body = req.body || {};
const errors = [];
const tok = (req.headers || {})['x-smock-token'];
if (tok !== CFG.TOKEN) errors.push('sai token');
for (const k of Object.keys(body)) if (FORBID.includes(k.toLowerCase())) errors.push('không được gửi trường ' + k);
const type = body.type || 'log';
const today = new Date().toLocaleString('sv-SE', { timeZone: 'Asia/Ho_Chi_Minh' }).slice(0, 10);
let out = { type, errors };
if (type === 'log') {
  if (!/^SM0[1-8]$/.test(body.ma_tk || '')) errors.push('ma_tk phải là SM01..SM08');
  if (!LOAI.includes(body.loai_viec)) errors.push('loai_viec không hợp lệ: ' + body.loai_viec);
  if (!TT.includes(body.trang_thai)) errors.push('trang_thai không hợp lệ: ' + body.trang_thai);
  const sl = Number(body.so_luong ?? 0); if (!Number.isFinite(sl) || sl < 0) errors.push('so_luong phải là số ≥ 0');
  if (body.lich_row != null && !(Number.isInteger(body.lich_row) && body.lich_row >= 2)) errors.push('lich_row phải là số dòng ≥ 2');
  if (body.url && !/^https:\/\/(www\.|web\.|m\.)?facebook\.com\//.test(body.url)) errors.push('url phải là link facebook.com');
  // Mã log chống ghi trùng: bot gửi lại cùng việc thì không ghi thêm dòng
  const raw = [today, body.ma_tk, body.lich_row ?? '', body.loai_viec, body.noi_dung ?? ''].join('|');
  let h = 0; for (let i = 0; i < raw.length; i++) { h = ((h << 5) - h + raw.charCodeAt(i)) | 0; }
  out.ma_log = body.ma_log || ('L' + today.replace(/-/g, '') + '-' + Math.abs(h).toString(36));
  out.row = [today, body.ma_tk, '', body.loai_viec, body.noi || '', String(body.noi_dung || '').slice(0, 500), body.che_do || '',
             body.ket_qua || body.trang_thai, body.trang_thai, sl, out.ma_log];
  out.lich_row = body.lich_row ?? null;
  out.lich_values = body.trang_thai === 'Không làm được' ? ['Lỗi', body.url || ''] : ['Done', body.url || ''];
} else if (type === 'status') {
  const tab = body.tab, st = body.status;
  if (!STATUS[tab] || !STATUS[tab].length) errors.push('tab không có cột trạng thái: ' + tab);
  else if (!STATUS[tab].includes(st)) errors.push('trạng thái không hợp lệ cho ' + tab + ': ' + st);
  if (!(Number.isInteger(body.row) && body.row >= 2)) errors.push('row phải là số dòng ≥ 2');
  out.tab = tab; out.row = body.row; out.status = st; out.note = String(body.note || '').slice(0, 300);
} else errors.push('type phải là log hoặc status');
out.ok = errors.length === 0;
return [{ json: out }];
""" % (LV, TT, STATUS, FORBID)

check_dup_js = r"""const v = $('Kiểm tra dữ liệu').first().json;
const col = ($input.first().json.values || []).map(r => r[0]);
return [{ json: { ...v, duplicate: col.includes(v.ma_log) } }];"""

status_body_js = CONFIG_JS + r"""
const HEADERS = %s;
const v = $('Kiểm tra dữ liệu').first().json;
const h = HEADERS[v.tab];
const col = h.indexOf('Trạng thái');
const letter = i => String.fromCharCode(65 + i);
const data = [{ range: `'${v.tab}'!${letter(col)}${v.row}`, values: [[v.status]] }];
const noteCol = h.indexOf('Ghi chú');
if (v.note && noteCol >= 0) data.push({ range: `'${v.tab}'!${letter(noteCol)}${v.row}`, values: [[v.note]] });
return [{ json: { body: { valueInputOption: 'USER_ENTERED', data } } }];""" % HEADERS

nodes, c = [], {}
nodes += [
  node("Webhook smock-log", "n8n-nodes-base.webhook", 2, {"httpMethod": "POST", "path": "smock-log", "responseMode": "responseNode", "options": {}},
       [-900, 300], webhookId=str(uuid.uuid4()), notes="Chỉ gọi từ máy này: http://localhost:5678/webhook/smock-log. Không mở ra internet."),
  code("Kiểm tra dữ liệu", validate_js, [-680, 300], notes="Kiểm theo ops/contract.json. Sai thì trả 400 kèm lý do để bot sửa và gửi lại."),
  iff("Hợp lệ?", "{{ $json.ok }}", [-460, 300]),
  node("Trả lỗi 400", "n8n-nodes-base.respondToWebhook", 1.1, {"respondWith": "json", "responseBody": "={{ JSON.stringify({ ok: false, errors: $json.errors }) }}", "options": {"responseCode": 400}}, [-240, 480]),
  iff("Là log?", "{{ $json.type === 'log' }}", [-240, 220]),
  gget("Đọc cột Mã log", "\"'Nhật Ký SM'!K:K\"", [-20, 120]),
  code("Đã ghi chưa?", check_dup_js, [200, 120]),
  iff("Mới?", "{{ !$json.duplicate }}", [420, 120]),
  gpost("Ghi Nhật Ký SM", "/values/{{ encodeURIComponent(\"'Nhật Ký SM'!A:K\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS",
        "{ values: [$('Đã ghi chưa?').first().json.row] }", [640, 40]),
  iff("Có dòng lịch?", "{{ $('Đã ghi chưa?').first().json.lich_row !== null }}", [860, 40]),
  gpost("Ghi Done vào Lịch SM", ":batchUpdate" if False else "/values:batchUpdate",
        "{ valueInputOption: 'USER_ENTERED', data: [{ range: \"'Lịch SM'!H\" + $('Đã ghi chưa?').first().json.lich_row + ':I' + $('Đã ghi chưa?').first().json.lich_row, values: [$('Đã ghi chưa?').first().json.lich_values] }] }",
        [1080, -40]),
  node("Trả OK", "n8n-nodes-base.respondToWebhook", 1.1, {"respondWith": "json", "responseBody": "={{ JSON.stringify({ ok: true, ma_log: $('Đã ghi chưa?').first().json.ma_log, duplicate: $('Đã ghi chưa?').first().json.duplicate }) }}", "options": {"responseCode": 200}}, [1300, 120]),
  code("Tạo lệnh cập nhật trạng thái", status_body_js, [-20, 360]),
  gpost("Ghi trạng thái", "/values:batchUpdate", "$json.body", [200, 360]),
  node("Trả OK trạng thái", "n8n-nodes-base.respondToWebhook", 1.1, {"respondWith": "json", "responseBody": "={{ JSON.stringify({ ok: true }) }}", "options": {"responseCode": 200}}, [420, 360]),
]
for a, b, o in [("Webhook smock-log", "Kiểm tra dữ liệu", 0), ("Kiểm tra dữ liệu", "Hợp lệ?", 0), ("Hợp lệ?", "Là log?", 0), ("Hợp lệ?", "Trả lỗi 400", 1),
                ("Là log?", "Đọc cột Mã log", 0), ("Là log?", "Tạo lệnh cập nhật trạng thái", 1), ("Đọc cột Mã log", "Đã ghi chưa?", 0),
                ("Đã ghi chưa?", "Mới?", 0), ("Mới?", "Ghi Nhật Ký SM", 0), ("Mới?", "Trả OK", 1), ("Ghi Nhật Ký SM", "Có dòng lịch?", 0),
                ("Có dòng lịch?", "Ghi Done vào Lịch SM", 0), ("Có dòng lịch?", "Trả OK", 1), ("Ghi Done vào Lịch SM", "Trả OK", 0),
                ("Tạo lệnh cập nhật trạng thái", "Ghi trạng thái", 0), ("Ghi trạng thái", "Trả OK trạng thái", 0)]:
    link(c, a, b, o)
save("L1-01-webhook-ghi-log.json", "L1-01 Webhook ghi log + trạng thái", nodes, c,
     "Cấp 3 gọi 1 lệnh sau mỗi việc thay vì gõ vào sheet. Chống ghi trùng bằng cột K 'Mã log'.")

# ---------------------------------------------------------------- L1-02 sinh lịch ngày làm việc kế tiếp
gen_js = CONFIG_JS + r"""
// Đầu vào: 6 lần đọc sheet ở các node trước. Sinh lịch NGÀY LÀM VIỆC KẾ TIẾP, giờ hành chính, gom việc theo cụm từng nick.
const V = n => { try { return (($(n).first().json) || {}).values || []; } catch (e) { return []; } };
const acc = V('Đọc Tài khoản'), kpi = V('Đọc Target + Workload'), jg = V('Đọc Join Group SM'),
      af = V('Đọc Add Friend'), lich = V('Đọc Lịch SM'), gs = V('Đọc Group Score'),
      pool = buildPool(V('Đọc content KE'), V('Đọc Pool Content SM')), nk = V('Đọc Nhật Ký SM');
// Ngày làm việc kế tiếp (bỏ Chủ nhật)
const now = vnNow();
const d = new Date(now); d.setDate(d.getDate() + 1); if (d.getDay() === 0) d.setDate(d.getDate() + 1);
const day = isoOf(d);
const dayVN = day;   // tab Lịch SM đang ghi ngày dạng yyyy-mm-dd
// Đã có lịch cho ngày đó thì dừng (chạy lại không sinh trùng)
if (lich.some(r => sameDay(r[0], d))) return [{ json: { skip: true, reason: 'Đã có lịch ngày ' + day } }];
// Nick hoạt động + tên
// Cột F tab Tài khoản: "Hoạt động" = chạy; thêm chữ "hạn chế group" (vd "Hoạt động - hạn chế group") = chỉ đăng tường + tương tác
const nicks = acc.filter(r => /^SM0\d$/.test(r[0]) && /Hoạt động/i.test(r[5] || '')).map(r => ({ id: r[0], name: r[1], noGroup: /hạn chế group|không group|no group/i.test(r[5] || '') }));
const quota = {}; for (const r of kpi) if (/^SM0\d$/.test(r[0])) quota[r[0]] = { wall: +r[3] || 0, join: +r[4] || 0, fr: +r[5] || 0, grp: +r[6] || 0 };
// Random có hạt giống theo ngày → chạy lại ra cùng kết quả
let seed = [...day].reduce((s, ch) => s * 31 + ch.charCodeAt(0), 7) >>> 0;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const pattern = n => Array.from({ length: n }, () => ri(1, 5)).join('/');
// Group tier A/B theo Group Score (nếu chưa chấm thì KHÔNG xếp bài group)
const gsCol = { stt: 0, tier: 14, st: 16 };
const okGroup = new Set(gs.filter(r => ['A', 'B'].includes((r[gsCol.tier] || '').trim()) && ['Đã chấm', 'Đã duyệt'].includes(r[gsCol.st])).map(r => +r[gsCol.stt]));
// Group Score chưa chấm group nào → dùng cột Tier của Join Group SM (A/B)
if (!okGroup.size) for (const r of jg) if (/^(A|B)$/.test(String(r[CFG.JG_TIER_COL] || '').trim())) okGroup.add(+r[0]);
const jgCol = CFG.JG_COL;
// Lịch sử đăng group N ngày gần nhất (chống đăng lại cùng group) — đọc từ tab Lịch SM (A ngày, C nick, F lệnh)
const parseDay = s => { s = String(s || ''); let m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s); if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s); return m ? new Date(+m[3], +m[2] - 1, +m[1]) : null; };
const dayDate = new Date(d.getFullYear(), d.getMonth(), d.getDate());
const recent = {}; // nick -> Set(group)
for (const r of lich) { const dd = parseDay(r[0]); const g = /đăng group .*→ group (\d+)/.exec(r[5] || '');
  if (!dd || !g || !r[2]) continue; const age = (dayDate - dd) / 864e5;
  if (age > 0 && age <= CFG.GROUP_REPOST_DAYS) (recent[r[2]] = recent[r[2]] || new Set()).add(+g[1]); }
// Đèn sức khoẻ nick, tính thẳng từ Nhật Ký SM 2 ngày gần nhất (không cần tab báo cáo riêng):
// Đỏ = có cảnh báo FB → không đăng group; Vàng = ≥ 2 việc "Không làm được" → tối đa 2 bài group
const light = {}; const nkRecent = nk.filter(r => { const dd = parseDay(r[0]); return dd && (now - dd) / 864e5 <= 2; });
for (const r of nkRecent) { const n = r[1]; if (!/^SM0\d$/.test(n || '')) continue;
  if (/checkpoint|identity|xác minh|can.?t use|bị gỡ|hạn chế/i.test((r[5] || '') + ' ' + (r[7] || ''))) light[n] = 'Đỏ';
  else if (r[8] === 'Không làm được' && light[n] !== 'Đỏ') light[n] = (light[n] === 'Vàng1' || light[n] === 'Vàng') ? 'Vàng' : 'Vàng1'; }
for (const k of Object.keys(light)) if (light[k] === 'Vàng1') delete light[k];
const teamGroupsToday = new Set();
// Kho content chưa dùng (KE + Pool Content SM, bỏ mã đã có trong Lịch SM) + mã bài kế tiếp
const usedIds = usedContent(lich);
const cqRows = pool.filter(x => !usedIds.has(x.id));
let maxK = maxKOf(lich, CFG.K_START);
const used = new Set();
const takeContent = (nick, kind) => {
  const x = cqRows.find(x => !used.has(x.id) && (kind === 'group' ? x.kind !== 'wall' : true));
  if (!x) return null; used.add(x.id); const code = 'K' + (++maxK);
  return { code, content: x.id };
};
// Người kết bạn kế tiếp (cột C = 'Chưa Add')
let frIdx = 0; const frList = af.map((r, i) => ({ r, row: i + 2 })).filter(x => /Chưa Add/i.test(x.r[2] || ''));
const frReserve = [];
// Dựng việc theo nick
const tasks = [];
for (const n of nicks) {
  const q = quota[n.id] || { wall: 1, join: 1, fr: 1, grp: 0 };
  const list = [];
  list.push(['story tim', `story tim ${ri(1, 3)}/${ri(1, 4)}`]);
  list.push(['lướt newfeed', `lướt newfeed ${ri(2, 4)}`]);
  list.push(['chấp nhận All', 'chấp nhận All']);
  list.push(['tương tác', `tương tác ${pattern(ri(3, 5))}`]);
  const col = jgCol[n.id];
  if (col !== undefined) {
    const joined = jg.filter(r => /đã join/i.test(r[col] || '')).map(r => +r[0]);
    if (joined.length) list.push(['tương tác group', `group ${joined[ri(0, joined.length - 1)]} tương tác ${pattern(ri(2, 3))}`]);
    const toJoin = jg.filter(r => /chưa join/i.test(r[col] || '') && (okGroup.size === 0 || okGroup.has(+r[0]))).slice(0, Math.max(0, q.join)).map(r => +r[0]);
    if (toJoin.length) list.push(['join group', `join group ${toJoin.join(', ')}`]);
    const rec = recent[n.id] || new Set();
    const canPost = shuffle(jg.filter(r => /đã join/i.test(r[col] || '') && okGroup.has(+r[0])).map(r => +r[0])
      .filter(g => !rec.has(g) && !teamGroupsToday.has(g)));
    let grp = q.grp; if (light[n.id] === 'Đỏ' || n.noGroup) grp = 0; else if (light[n.id] === 'Vàng') grp = Math.min(grp, 2);
    for (let i = 0; i < Math.min(grp, canPost.length); i++) {
      const c = takeContent(n.id, 'group'); if (!c) break;
      teamGroupsToday.add(canPost[i]);
      list.push(['đăng group', `đăng group ${c.code} (${c.content}) → group ${canPost[i]}`, 'group']);
    }
  }
  for (let i = 0; i < q.wall; i++) { const c = takeContent(n.id, 'wall'); if (!c) break; list.push(['đăng tường', `đăng tường ${c.code} (${c.content})`]); }
  const nf = Math.min(q.fr, frList.length - frIdx);
  if (nf > 0) { const ids = frList.slice(frIdx, frIdx + nf); frIdx += nf; ids.forEach(x => frReserve.push({ row: x.row, nick: n.id }));
    list.push(['kết bạn', `kết bạn ${ids.map(x => x.r[0]).join(', ')}`]); }
  // 2 cụm mỗi nick: sáng và chiều (giảm chọn lại trình duyệt, vẫn rải trong ngày)
  // Chia cụm: mỗi bài group 1 cụm riêng (tối thiểu 2 cụm/nick), việc khác rải đều vào các cụm
  const lane = nicks.indexOf(n) % CFG.LANES; const groups = list.filter(x => x[2] === 'group'); const others = shuffle(list.filter(x => x[2] !== 'group'));
  const k = Math.max(2, groups.length); const blocks = Array.from({ length: k }, (_, i) => (groups[i] ? [groups[i]] : []));
  others.forEach((x, i) => blocks[i % k].push(x)); blocks.forEach((b, i) => { shuffle(b); tasks.push({ nick: n, lane, idx: i, items: b }); });
}
// Xếp giờ: mỗi luồng 1 dòng thời gian riêng (chạy song song); việc trong cụm cách TASK_GAP, giữa cụm BLOCK_GAP;
// bài group: cùng nick cách ≥ NICK_GROUP_GAP_MIN, cả đội cách ≥ TEAM_GROUP_GAP_MIN (tính chung mọi luồng)
const toMin = s => +s.slice(0, 2) * 60 + +s.slice(3); const hhmm = m => String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
const S = toMin(CFG.OFFICE_START), E = toMin(CFG.OFFICE_END), L1 = toMin(CFG.LUNCH_START), L2 = toMin(CFG.LUNCH_END);
const rows = []; const overflow = []; const groupTimes = []; const lastNickGroup = {};
const fixGroup = (t, nick) => { t = Math.max(t, (lastNickGroup[nick] ?? -999) + CFG.NICK_GROUP_GAP_MIN);
  for (let k = 0; k < 500; k++) { if (t >= L1 && t < L2) t = L2; const c = groupTimes.find(g => Math.abs(t - g) < CFG.TEAM_GROUP_GAP_MIN); if (!c) break; t = c + CFG.TEAM_GROUP_GAP_MIN; } return t; };
for (let lane = 0; lane < CFG.LANES; lane++) {
  // Xếp vòng: cụm 1 của mọi nick trong luồng, rồi cụm 2... → 2 cụm liền nhau của cùng nick cách xa nhau
  const mine = tasks.filter(x => x.lane === lane); const ln = shuffle([...new Set(mine.map(x => x.nick.id))]);
  const maxIdx = Math.max(-1, ...mine.map(x => x.idx)); const order = [];
  for (let i = 0; i <= maxIdx; i++) for (const id of ln) { const b = mine.find(x => x.nick.id === id && x.idx === i); if (b) order.push(b); }
  let t = S + ri(0, 10);
  for (const b of order) {
    for (const it of b.items) {
      if (t >= L1 && t < L2) t = L2 + ri(0, 10);
      if (it[2] === 'group') t = fixGroup(t, b.nick.id);
      if (t > E) { overflow.push(`${b.nick.id}: ${it[1]}`); continue; }
      if (it[2] === 'group') { groupTimes.push(t); lastNickGroup[b.nick.id] = t; }
      rows.push([dayVN, hhmm(t), b.nick.id, b.nick.name, it[0], it[1], 'Có', 'Chờ', '', `sinh bởi n8n L1-02 · luồng ${lane + 1}`]);
      t += ri(CFG.TASK_GAP[0], CFG.TASK_GAP[1]);
    }
    t += ri(CFG.BLOCK_GAP[0], CFG.BLOCK_GAP[1]);
  }
}
rows.sort((a, b) => a[1].localeCompare(b[1]));
const data = frReserve.map(x => ({ range: `'Add Friend'!C${x.row}`, values: [[`Đã xếp ${x.nick} ${dayVN}`]] }));
const nPost = rows.filter(r => /^đăng/.test(r[4])).length;
return [{ json: { skip: false, day, rows, data, overflow, summary: `${rows.length} việc cho ${nicks.length} nick ngày ${dayVN}` + (overflow.length ? `; ${overflow.length} việc không vừa giờ` : '') + (okGroup.size ? '' : '; chưa có group A/B nên không xếp bài group') + (cqRows.length < nPost + 5 ? `; kho content sắp hết (còn ${cqRows.length - nPost})` : '') } }];
"""
nodes, c = [], {}
reads = [("Đọc Tài khoản", "\"'Tài khoản'!A2:I20\""), ("Đọc Target + Workload", "\"'Target + Workload'!A4:K11\""),
         ("Đọc Join Group SM", "\"'Join Group SM'!A2:M300\""), ("Đọc Add Friend", "\"'Add Friend'!A2:D2000\""),
         ("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\""), ("Đọc Group Score", "\"'Group Score'!A2:R500\""),
         ("Đọc Pool Content SM", POOL_RANGE), ("Đọc content KE", KE_RANGE, KE_SHEET), ("Đọc Nhật Ký SM", "\"'Nhật Ký SM'!A2:J8000\"")]
nodes.append(sched("21:30 Chủ nhật–Thứ sáu", "30 21 * * 0-5", [-1200, 300], notes="Sinh lịch cho ngày làm việc kế tiếp (thứ 2–7)."))
prev = "21:30 Chủ nhật–Thứ sáu"
for i, rd in enumerate(reads):
    nodes.append(gget(rd[0], rd[1], [-980 + i * 160, 300], sheet=rd[2] if len(rd) > 2 else None)); link(c, prev, rd[0]); prev = rd[0]
nodes += [code("Sinh lịch", gen_js, [420, 300], notes="Luật: giờ hành chính, 2 luồng song song, bài group chỉ vào group A/B đã join; cùng nick cách ≥60 phút, cả đội cách ≥6 phút; không đăng lại 1 group trong 3 ngày; đèn Đỏ → 0 bài group, Vàng → ≤2; mỗi content 1 lần."),
          iff("Có việc mới?", "{{ !$json.skip && $json.rows.length > 0 }}", [640, 300]),
          gpost("Ghi Lịch SM", "/values/{{ encodeURIComponent(\"'Lịch SM'!A:J\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS", "{ values: $json.rows }", [860, 220]),
          iff("Có người kết bạn?", "{{ $('Sinh lịch').first().json.data.length > 0 }}", [1080, 220]),
          gpost("Giữ chỗ kết bạn", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $('Sinh lịch').first().json.data }", [1300, 160]),
          telegram("Báo nhóm", "{{ '🗓 ' + $('Sinh lịch').first().json.summary }}", [1520, 220])]
link(c, prev, "Sinh lịch"); link(c, "Sinh lịch", "Có việc mới?"); link(c, "Có việc mới?", "Ghi Lịch SM")
link(c, "Ghi Lịch SM", "Có người kết bạn?"); link(c, "Có người kết bạn?", "Giữ chỗ kết bạn", 0); link(c, "Có người kết bạn?", "Báo nhóm", 1)
link(c, "Giữ chỗ kết bạn", "Báo nhóm")
save("L1-02-sinh-lich.json", "L1-02 Sinh Lịch SM ngày làm việc kế tiếp", nodes, c,
     "Thay việc 'lên lịch hôm nay' của Claude. Chạy lại không sinh trùng (kiểm ngày đã có lịch). Random có hạt giống theo ngày.")

# ---------------------------------------------------------------- L1-03 chuẩn bị gói bài
pick_js = CONFIG_JS + r"""
// Bài cần gói = dòng Lịch SM từ hôm nay trở đi, lệnh "đăng … Kxxx (CGn|PCn)", cột J chưa ghi "Gói sẵn"
const V = n => { try { return (($(n).first().json) || {}).values || []; } catch (e) { return []; } };
const lich = V('Đọc Lịch SM'); const pool = buildPool(V('Đọc content KE'), V('Đọc Pool Content SM'));
const byId = Object.fromEntries(pool.map(x => [x.id, x]));
const today = vnNow(); today.setHours(0, 0, 0, 0);
const parseDay = s => { s = String(s || ''); let m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s); if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s); return m ? new Date(+m[3], +m[2] - 1, +m[1]) : null; };
const out = [];
lich.forEach((r, i) => {
  const dd = parseDay(r[0]); if (!dd || dd < today || r[7] === 'Done') return;
  const m = /\b(K\d{3,})\b.*?\b((?:CG|PC)\d+)\b/.exec(r[5] || ''); if (!m || /Gói sẵn/.test(r[9] || '')) return;
  const code = m[1], src = byId[m[2]];
  if (!src) { out.push({ json: { row: i + 2, code, note: r[9] || '', missing: m[2] } }); return; }
  const link = src.media || ''; const f = /folders\/([\w-]+)/.exec(link) || /[?&]id=([\w-]+)/.exec(link) || /\/d\/([\w-]+)/.exec(link);
  // Thay {{MA_BAI}} (caption phái sinh từ cấp 2) bằng mã bài thật; caption gốc chưa có mã thì thêm câu mời nhắn tin
  let cap = String(src.caption).replace(/\{\{MA_BAI\}\}/g, code);
  if (!new RegExp('\\b' + code + '\\b').test(cap)) cap += `\n\nDM or WhatsApp us code ${code} for the catalog.`;
  out.push({ json: { row: i + 2, code, src: m[2], note: r[9] || '', caption: cap, folderId: f ? f[1] : null, dir: `${CFG.PACK_DIR}/${code}` } });
});
return out.length ? out : [{ json: { empty: true } }];"""
caption_js = r"""const items = [];
for (const it of $input.all()) {
  if (it.json.empty) continue;
  items.push({ json: it.json, binary: { data: { data: Buffer.from(it.json.caption, 'utf8').toString('base64'), mimeType: 'text/plain', fileName: 'caption.txt' } } });
}
return items;"""
explode_js = r"""// Mỗi bài → danh sách file trong folder (từ Drive API) → mỗi ảnh một item để tải bản JPG 2048px
// Node Drive trả 1 item cho mỗi bài theo đúng thứ tự đầu vào → ghép với bài cùng vị trí ở nhánh "Có bài?"
const out = []; const metas = $('Có bài?').all();
$input.all().forEach((it, k) => {
  const meta = metas[k] ? metas[k].json : {};
  const files = (it.json.files || []).filter(f => /^image\//.test(f.mimeType || '')).sort((a, b) => String(a.name).localeCompare(String(b.name)));
  files.forEach((f, i) => out.push({ json: { ...meta, fileId: f.id, idx: i + 1, total: files.length } }));
});
return out;"""
nodes, c = [], {}
nodes += [sched("22:00 Chủ nhật–Thứ sáu", "0 22 * * 0-5", [-1340, 300]),
          gget("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\"", [-1120, 300]),
          gget("Đọc Pool Content SM", POOL_RANGE, [-900, 300]),
          gget("Đọc content KE", KE_RANGE, [-680, 300], sheet=KE_SHEET),
          code("Chọn bài cần gói", pick_js, [-460, 300]),
          iff("Có bài?", "{{ !$json.empty && !!$json.folderId }}", [-240, 300]),
          code("Tạo caption.txt", caption_js, [-20, 140]),
          node("Ghi caption.txt", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $json.dir + '/caption.txt' }}", "dataPropertyName": "data", "options": {}}, [200, 140]),
          node("Liệt kê ảnh trong folder Drive", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=https://www.googleapis.com/drive/v3/files?q={{ encodeURIComponent(\"'\" + $json.folderId + \"' in parents and trashed=false\") }}&fields=files(id,name,mimeType)&supportsAllDrives=true&includeItemsFromAllDrives=true",
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleDriveOAuth2Api", "options": {}}, [-20, 380],
              notes="CHỌN CREDENTIAL: Google Drive OAuth2. Folder do người khác sở hữu vẫn liệt kê được nếu tài khoản này mở được link.", retryOnFail=True, maxTries=3),
          code("Tách từng ảnh", explode_js, [200, 380]),
          node("Tải ảnh JPG 2048px", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=https://drive.google.com/thumbnail?id={{ $json.fileId }}&sz=w2048",
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleDriveOAuth2Api",
              "options": {"response": {"response": {"responseFormat": "file"}}, "batching": {"batch": {"batchSize": 1, "batchInterval": 1500}}}}, [420, 380],
              notes="Luôn tải bản JPG (xử lý được cả HEIC). 1,5 giây/ảnh để không bị Google chặn.", retryOnFail=True, maxTries=3),
          node("Lưu ảnh vào gói", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $json.dir + '/' + String($json.idx).padStart(2, '0') + '.jpg' }}", "dataPropertyName": "data", "options": {}}, [640, 380]),
          code("Gom kết quả theo bài", r"""const by = {};
for (const it of $('Tách từng ảnh').all()) { const k = it.json.row; by[k] = by[k] || { row: k, code: it.json.code, note: it.json.note || '', total: it.json.total, saved: 0 }; }
for (const it of $input.all()) { const k = it.json.row; if (by[k]) by[k].saved++; }
// Ghi kết quả vào cột J (Ghi chú) của chính dòng Lịch SM — cấp 3 đọc "Gói sẵn" là có thư mục anh-dang-bai/Kxxx
const tag = b => (b.saved > 0 && b.saved === b.total ? 'Gói sẵn' : 'Lỗi gói') + ` ${b.saved}/${b.total} ảnh`;
const data = Object.values(by).map(b => ({ range: `'Lịch SM'!J${b.row}`, values: [[(b.note ? b.note + ' · ' : '') + tag(b)]] }));
return [{ json: { data, n: Object.keys(by).length } }];""", [860, 380]),
          gpost("Ghi trạng thái gói", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $json.data }", [1080, 380])]
for a, b, o in [("22:00 Chủ nhật–Thứ sáu", "Đọc Lịch SM", 0), ("Đọc Lịch SM", "Đọc Pool Content SM", 0), ("Đọc Pool Content SM", "Đọc content KE", 0),
                ("Đọc content KE", "Chọn bài cần gói", 0), ("Chọn bài cần gói", "Có bài?", 0),
                ("Có bài?", "Tạo caption.txt", 0), ("Có bài?", "Liệt kê ảnh trong folder Drive", 0), ("Tạo caption.txt", "Ghi caption.txt", 0),
                ("Liệt kê ảnh trong folder Drive", "Tách từng ảnh", 0), ("Tách từng ảnh", "Tải ảnh JPG 2048px", 0), ("Tải ảnh JPG 2048px", "Lưu ảnh vào gói", 0),
                ("Lưu ảnh vào gói", "Gom kết quả theo bài", 0), ("Gom kết quả theo bài", "Ghi trạng thái gói", 0)]:
    link(c, a, b, o)
save("L1-03-chuan-bi-goi-bai.json", "L1-03 Chuẩn bị gói bài (caption + ảnh)", nodes, c,
     "Cấp 3 chỉ cần mở thư mục anh-dang-bai/Kxxx: có caption.txt và 01.jpg, 02.jpg…")

# ---------------------------------------------------------------- L1-04 báo cáo ngày + đèn
report_js = CONFIG_JS + r"""
const nk = ($('Đọc Nhật Ký SM').first().json.values || []), kpi = ($('Đọc Target + Workload').first().json.values || []),
      lich = ($('Đọc Lịch SM').first().json.values || []);
const today = new Date().toLocaleString('sv-SE', { timeZone: 'Asia/Ho_Chi_Minh' }).slice(0, 10);
const d = new Date(today); const todayVN = `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
const isToday = s => (s || '').startsWith(today) || (s || '').startsWith(todayVN);
const quota = {}; for (const r of kpi) if (/^SM0\d$/.test(r[0])) quota[r[0]] = { wall: +r[3] || 0, grp: +r[6] || 0 };
const per = {};
for (const r of nk.filter(r => isToday(r[0]))) {
  const n = r[1]; const p = per[n] = per[n] || { xong: 0, loi: 0, wall: 0, grp: 0, join: 0, fr: 0, tt: 0, red: false };
  if (r[8] === 'Xong' || r[8] === 'Một phần') p.xong++; else p.loi++;
  const sl = +r[9] || 0;
  if (r[3] === 'Đăng bài') { if (/group/i.test(r[4] || '')) p.grp += sl; else p.wall += sl; }
  if (r[3] === 'Join group') p.join += sl; if (r[3] === 'Kết bạn') p.fr += sl;
  if (/^Tương tác/.test(r[3] || '') || r[3] === 'Tim story') p.tt += sl;
  if (/checkpoint|identity|xác minh|can.?t use|bị gỡ|hạn chế/i.test((r[5] || '') + ' ' + (r[7] || ''))) p.red = true;
}
const left = lich.filter(r => isToday(r[0]) && r[7] === 'Chờ');
const rows = Object.entries(per).map(([n, p]) => {
  const q = quota[n] || { wall: 0, grp: 0 };
  const den = p.red ? 'Đỏ' : (p.loi > p.xong || p.wall < q.wall || p.grp < q.grp) ? 'Vàng' : 'Xanh';
  return [today, n, p.xong, p.loi, p.wall, p.grp, p.join, p.fr, p.tt, den, left.filter(r => r[2] === n).length + ' việc còn Chờ'];
});
const text = '📊 Smock ' + today + '\n' + rows.map(r => `${r[1]} ${r[9] === 'Đỏ' ? '🔴' : r[9] === 'Vàng' ? '🟡' : '🟢'} xong ${r[2]}, lỗi ${r[3]}, tường ${r[4]}, group ${r[5]}`).join('\n') + (left.length ? `\nCòn ${left.length} việc Chờ` : '');
return [{ json: { rows, text } }];"""
nodes, c = [], {}
nodes += [sched("18:00 Thứ 2–7", "0 18 * * 1-6", [-900, 300]),
          gget("Đọc Nhật Ký SM", "\"'Nhật Ký SM'!A2:K5000\"", [-680, 300]),
          gget("Đọc Target + Workload", "\"'Target + Workload'!A4:K11\"", [-460, 300]),
          gget("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\"", [-240, 300]),
          code("Tính báo cáo + đèn", report_js, [-20, 300], notes="Đèn: Đỏ nếu có cảnh báo FB trong log; Vàng nếu lỗi nhiều hơn xong hoặc thiếu bài so với KPI ngày. Không ghi tab riêng: tab Báo cáo SM đã tự tính từ Nhật Ký SM; L1-02 tự tính đèn từ Nhật Ký SM."),
          telegram("Gửi nhóm", "{{ $('Tính báo cáo + đèn').first().json.text }}", [200, 300])]
for a, b in [("18:00 Thứ 2–7", "Đọc Nhật Ký SM"), ("Đọc Nhật Ký SM", "Đọc Target + Workload"), ("Đọc Target + Workload", "Đọc Lịch SM"),
             ("Đọc Lịch SM", "Tính báo cáo + đèn"), ("Tính báo cáo + đèn", "Gửi nhóm")]:
    link(c, a, b)
save("L1-04-bao-cao-ngay.json", "L1-04 Báo cáo ngày + đèn sức khỏe", nodes, c, "Tóm tắt cuối ngày gửi nhóm (bật node Telegram nếu dùng). Số liệu chi tiết xem tab Báo cáo SM.")

# ---------------------------------------------------------------- L1-05 kiểm hợp đồng (trước & sau ca)
contract_js = CONFIG_JS + r"""
const HEADERS = %s;
// Chỉ báo lệch, KHÔNG đòi tạo tab: tab bị đổi tên/xoá hoặc cột workflow đang dùng bị dời chỗ
const tabs = Object.keys(HEADERS); const res = $input.first().json.valueRanges || [];
const norm = s => String(s || '').trim().replace(/\s+/g, ' ').toLowerCase();
const problems = [];
tabs.forEach((t, i) => {
  const got = ((res[i] || {}).values || [[]])[0] || [];
  if (!res[i]) { problems.push(`Không đọc được tab "${t}" (đổi tên hoặc xoá?)`); return; }
  HEADERS[t].forEach((h, j) => { if (h !== null && !norm(got[j]).startsWith(norm(h))) problems.push(`${t}: cột ${String.fromCharCode(65 + j)} workflow đọc là "${h}", sheet đang là "${got[j] || ''}"`); });
});
return [{ json: { problems, ok: problems.length === 0 } }];""" % HEADERS
stuck_js = CONFIG_JS + r"""
const lh = ($('Đọc Lead Hunter').first().json.values || []), lich = ($('Đọc Lịch SM').first().json.values || []);
const problems = [...$('Kiểm tiêu đề').first().json.problems];
const now = vnNow();
const t = new Date(now); t.setDate(t.getDate() + (now.getHours() >= 12 ? 1 : 0)); if (t.getDay() === 0) t.setDate(t.getDate() + 1);
// 1) Bài có lịch đăng (ngày làm việc tới) mà L1-03 chưa ghi "Gói sẵn" vào cột J
const needPack = lich.filter(r => sameDay(r[0], t) && /^đăng/.test(r[4] || '') && /\bK\d{3,}\b/.test(r[5] || '') && !/Gói sẵn/.test(r[9] || ''));
for (const r of needPack) problems.push(`Bài ${(/K\d{3,}/.exec(r[5]) || [''])[0]} ngày ${isoOf(t)} chưa có gói (${(r[9] || '').slice(-40) || 'cột J trống'})`);
// 2) Lead chờ duyệt quá 48 giờ
const old = lh.filter(r => r[11] === 'Chờ duyệt' && (now - new Date(String(r[0] || '').replace(' ', 'T'))) > 48 * 3600e3).length;
if (old) problems.push(`${old} lead "Chờ duyệt" quá 48 giờ`);
// 3) Lịch hôm qua còn "Chờ" (cấp 3 bỏ sót hoặc webhook không ghi)
const y = new Date(now); y.setDate(y.getDate() - 1);
const left = lich.filter(r => sameDay(r[0], y) && r[7] === 'Chờ').length;
if (left) problems.push(`${left} việc ngày ${isoOf(y)} vẫn "Chờ" — kiểm cấp 3 hoặc webhook`);
return [{ json: { problems, text: problems.length ? '⚠️ Kiểm hợp đồng Smock\n- ' + problems.join('\n- ') : '✅ Kiểm hợp đồng Smock: không có vấn đề' } }];"""
nodes, c = [], {}
nodes += [sched("06:30 và 21:50", "30 6,21 * * *", [-900, 300], notes="06:30: trước ca (gói bài hôm nay đủ chưa). 21:50: sau khi sinh lịch (gói bài mai sẽ làm lúc 22:00)."),
          node("Đọc dòng tiêu đề mọi tab", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=" + API + "/values:batchGet?" + "&".join("ranges=" + __import__("urllib.parse").parse.quote("'%s'!%d:%d" % (t, v.get("header_row", 1), v.get("header_row", 1)), safe="") for t, v in CONTRACT["tabs"].items()),
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api", "options": {}}, [-680, 300], retryOnFail=True, maxTries=3,
              notes="Đọc đúng dòng tiêu đề của từng tab đang có (ops/contract.json)."),
          code("Kiểm tiêu đề", contract_js, [-460, 300]),
          gget("Đọc Lead Hunter", "\"'Lead Hunter'!A2:N5000\"", [-240, 300]),
          gget("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\"", [-20, 300]),
          code("Tìm việc kẹt", stuck_js, [200, 300]),
          telegram("Báo nếu có vấn đề", "{{ $('Tìm việc kẹt').first().json.text }}", [420, 300])]
for a, b, o in [("06:30 và 21:50", "Đọc dòng tiêu đề mọi tab", 0), ("Đọc dòng tiêu đề mọi tab", "Kiểm tiêu đề", 0), ("Kiểm tiêu đề", "Đọc Lead Hunter", 0),
             ("Đọc Lead Hunter", "Đọc Lịch SM", 0), ("Đọc Lịch SM", "Tìm việc kẹt", 0), ("Tìm việc kẹt", "Báo nếu có vấn đề", 0)]:
    link(c, a, b, o)
save("L1-05-kiem-hop-dong.json", "L1-05 Kiểm hợp đồng dữ liệu + việc kẹt", nodes, c,
     "Bắt lỗi phối hợp giữa 3 cấp: sai tiêu đề cột, gói bài thiếu, lead tồn, lịch hôm qua còn Chờ.")

# ---------------------------------------------------------------- L1-06 cầu nối cấp 2 (đẩy việc tối, kéo kết quả sáng)
export_js = CONFIG_JS + r"""
const V = n => { try { return (($(n).first().json) || {}).values || []; } catch (e) { return []; } };
const gs = V('Đọc Group Score'), lich = V('Đọc Lịch SM'), poolRaw = V('Đọc Pool Content SM');
const pool = buildPool(V('Đọc content KE'), poolRaw);
const stamp = new Date().toLocaleString('sv-SE', { timeZone: 'Asia/Ho_Chi_Minh' }).slice(0, 10).replace(/-/g, '');
let n = 0; const files = [];
const id = p => `${p}-${stamp}-${String(++n).padStart(3, '0')}`;
// Caption cần phái sinh: content gốc đã đăng ≥ CONTENT_REUSE_DAYS ngày trước, chưa có bản phái sinh trong Pool Content SM; tối đa 10 việc/đêm
const parseDay = s => { s = String(s || ''); let m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s); if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s); return m ? new Date(+m[3], +m[2] - 1, +m[1]) : null; };
const lastUse = {}; for (const r of lich) { const dd = parseDay(r[0]); if (!dd) continue; for (const m of lichText(r).matchAll(/\b((?:CG|PC)\d+)\b/g)) if (!lastUse[m[1]] || lastUse[m[1]] < dd) lastUse[m[1]] = dd; }
const derived = new Set(); for (const r of poolRaw) { const m = /Phái sinh từ ((?:CG|PC)\d+)/i.exec(r[3] || ''); if (m) derived.add(m[1]); }
const now = vnNow();
pool.filter(x => /^CG/.test(x.id) && lastUse[x.id] && (now - lastUse[x.id]) / 864e5 >= CFG.CONTENT_REUSE_DAYS && !derived.has(x.id)).slice(0, 10)
  .forEach(x => files.push({ path: `inbox/captions/${id('CAP')}.json`, body: { task_id: null, kind: 'caption', sheet_row: x.row, source_code: x.id, source_caption: x.caption, type: 'group', image_link: x.media, variants: 3 } }));
gs.forEach((r, i) => { if (r[16] === 'Chờ chấm' && r[4]) files.push({ path: `inbox/groups/${id('GRP')}.json`, body: { task_id: null, kind: 'group', sheet_row: i + 2, stt: +r[0], name: r[1], url: r[2], text_file: r[4] } }); });
if (new Date().getDay() === 0) files.push({ path: `inbox/reports/${id('RPT')}.json`, body: { task_id: null, kind: 'weekly_report', week_ending: stamp } });
return files.map(f => { f.body.task_id = f.path.split('/').pop().replace('.json', ''); return { json: f, binary: { data: { data: Buffer.from(JSON.stringify(f.body, null, 2)).toString('base64'), mimeType: 'application/json', fileName: f.path.split('/').pop() } } }; });"""
import_js = CONFIG_JS + r"""
const FORBID = %s;
const rows = []; const errors = [];
// STT kế tiếp của tab Pool Content SM (caption phái sinh ghi vào đây, Phân loại = "Phái sinh từ CGn – chờ duyệt"; người duyệt xoá chữ "chờ duyệt" là được dùng)
let stt = 0; try { for (const r of ($('Đọc Pool Content SM (sáng)').first().json.values || [])) stt = Math.max(stt, +r[0] || 0); } catch (e) {}
// Kết quả cấp 2 có thể không mang image_link → tra lại theo mã bài gốc (CGn trong KE, PCn trong Pool Content SM)
const media = {}; try {
  for (const x of buildPool(($('Đọc content KE (sáng)').first().json.values || []), ($('Đọc Pool Content SM (sáng)').first().json.values || []))) media[x.id] = x.media;
} catch (e) {}
for (const it of $input.all()) {
  const o = it.json.data || it.json; const fname = it.json.fileName || '';
  if (!/^(CAP|GRP|RPT)-\d{8}-\d{3}$/.test(o.task_id || '')) { errors.push(`${fname}: thiếu/ sai task_id`); continue; }
  if (JSON.stringify(o).match(new RegExp('"(' + FORBID.join('|') + ')"', 'i'))) { errors.push(`${o.task_id}: có trường bị cấm`); continue; }
  if (o.kind === 'caption') {
    if (!Array.isArray(o.variants) || !o.variants.length) { errors.push(`${o.task_id}: không có variants`); continue; }
    o.variants.forEach((v, k) => rows.push({ append: [++stt, v.caption, o.image_link || media[o.source_code] || '', `Phái sinh từ ${o.source_code} (v${k + 1}) – chờ duyệt`, '', `Cấp 2 ${o.task_id}`] }));
  } else if (o.kind === 'group') {
    const s = o.scores || {}; const keys = ['gates', 'icp', 'sell', 'active', 'engage', 'buyer', 'geo', 'spam'];
    if (!keys.every(k => k in s)) { errors.push(`${o.task_id}: thiếu điểm`); continue; }
    rows.push({ update: { range: `'Group Score'!F${o.sheet_row}:Q${o.sheet_row}`, values: [[s.gates, s.icp, s.sell, s.active, s.engage, s.buyer, s.geo, s.spam, o.total, o.tier, String(o.evidence || '').slice(0, 1000), 'Đã chấm']] } });
  }
}
return [{ json: { appends: rows.filter(r => r.append).map(r => r.append), updates: rows.filter(r => r.update).map(r => r.update), errors } }];""" % FORBID
nodes, c = [], {}
nodes += [sched("22:15 đẩy việc sang cấp 2", "15 22 * * *", [-1340, 160]),
          gget("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\"", [-1120, 160]),
          gget("Đọc Pool Content SM", POOL_RANGE, [-900, 160]),
          gget("Đọc content KE", KE_RANGE, [-680, 160], sheet=KE_SHEET),
          gget("Đọc Group Score", "\"'Group Score'!A2:R500\"", [-460, 160]),
          code("Tạo file việc", export_js, [-240, 160], notes="Mỗi việc một file JSON có task_id duy nhất. File text group do cấp 3 lưu sẵn ở thư mục chung."),
          node("Ghi vào inbox repo cấp 2", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $('Tạo file việc').item.json.path.startsWith('inbox') ? 'C:/smock-level2-copilot/' + $json.path : '' }}", "dataPropertyName": "data", "options": {}}, [-20, 160]),
          node("git commit + push inbox", "n8n-nodes-base.executeCommand", 1, {"command": "=git -C \"C:/smock-level2-copilot\" pull --rebase && git -C \"C:/smock-level2-copilot\" add inbox && git -C \"C:/smock-level2-copilot\" commit -m \"inbox {{ $now.toFormat('yyyy-MM-dd HH:mm') }}\" ; git -C \"C:/smock-level2-copilot\" push", "executeOnce": True}, [200, 160],
               notes="Cần bật node Execute Command (xem n8n/level1/README.md) và git đã đăng nhập trên máy."),
          sched("06:30 kéo kết quả cấp 2", "30 6 * * *", [-1120, 500]),
          gget("Đọc Pool Content SM (sáng)", POOL_RANGE, [-1010, 500]),
          gget("Đọc content KE (sáng)", KE_RANGE, [-850, 620], sheet=KE_SHEET),
          node("git pull", "n8n-nodes-base.executeCommand", 1, {"command": "git -C \"C:/smock-level2-copilot\" pull --rebase", "executeOnce": True}, [-680, 500]),
          node("Đọc file outbox", "n8n-nodes-base.readWriteFile", 1, {"fileSelector": "C:/smock-level2-copilot/outbox/*/*.json", "options": {}}, [-460, 500], alwaysOutputData=True),
          node("Đọc JSON", "n8n-nodes-base.extractFromFile", 1, {"operation": "fromJson", "options": {}}, [-240, 500]),
          code("Kiểm + chuyển thành lệnh ghi", import_js, [-20, 500], notes="Từ chối file sai task_id, thiếu điểm, hoặc có trường bị cấm (SĐT, email, mật khẩu)."),
          gpost("Thêm caption phái sinh (Chờ duyệt)", "/values/{{ encodeURIComponent(\"'Pool Content SM'!A:F\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS", "{ values: $json.appends.length ? $json.appends : [] }", [200, 440],
                onError="continueRegularOutput", alwaysOutputData=True),
          gpost("Cập nhật điểm group + trạng thái", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $('Kiểm + chuyển thành lệnh ghi').first().json.updates }", [420, 440],
                onError="continueRegularOutput", alwaysOutputData=True),
          node("Chuyển outbox đã xử lý sang done", "n8n-nodes-base.executeCommand", 1, {"command": "powershell -NoProfile -Command \"cd 'C:/smock-level2-copilot'; New-Item -ItemType Directory -Force done | Out-Null; Get-ChildItem outbox -Recurse -Filter *.json | ForEach-Object { git mv $_.FullName ('done/' + $_.Name) }; git commit -m 'done'; git push\""}, [640, 440]),
          telegram("Báo lỗi file cấp 2", "{{ $('Kiểm + chuyển thành lệnh ghi').first().json.errors.length ? '⚠️ Cấp 2: ' + $('Kiểm + chuyển thành lệnh ghi').first().json.errors.join('; ') : '✅ Cấp 2: đã nhập kết quả' }}", [860, 440])]
for a, b in [("22:15 đẩy việc sang cấp 2", "Đọc Lịch SM"), ("Đọc Lịch SM", "Đọc Pool Content SM"), ("Đọc Pool Content SM", "Đọc content KE"),
             ("Đọc content KE", "Đọc Group Score"), ("Đọc Group Score", "Tạo file việc"),
             ("Tạo file việc", "Ghi vào inbox repo cấp 2"), ("Ghi vào inbox repo cấp 2", "git commit + push inbox"),
             ("06:30 kéo kết quả cấp 2", "Đọc Pool Content SM (sáng)"), ("Đọc Pool Content SM (sáng)", "Đọc content KE (sáng)"), ("Đọc content KE (sáng)", "git pull"), ("git pull", "Đọc file outbox"), ("Đọc file outbox", "Đọc JSON"), ("Đọc JSON", "Kiểm + chuyển thành lệnh ghi"),
             ("Kiểm + chuyển thành lệnh ghi", "Thêm caption phái sinh (Chờ duyệt)"), ("Thêm caption phái sinh (Chờ duyệt)", "Cập nhật điểm group + trạng thái"),
             ("Cập nhật điểm group + trạng thái", "Chuyển outbox đã xử lý sang done"), ("Chuyển outbox đã xử lý sang done", "Báo lỗi file cấp 2")]:
    link(c, a, b)
save("L1-06-cau-noi-cap-2.json", "L1-06 Cầu nối cấp 2 (inbox tối, outbox sáng)", nodes, c,
     "Bàn giao cấp 1 ↔ cấp 2 bằng file JSON trong repo smock-level2-copilot. Caption phái sinh luôn vào 'Chờ duyệt caption', người duyệt mới dùng.")

# ---------------------------------------------------------------- L1-07 heartbeat + sao lưu
nodes, c = [], {}
nodes += [sched("Mỗi 10 phút", "*/10 * * * *", [-600, 160]),
          node("Ping healthchecks", "n8n-nodes-base.httpRequest", 4.2, {"url": "https://hc-ping.com/YOUR-UUID", "options": {"timeout": 10000}}, [-380, 160],
               continueOnFail=True, disabled=True, notes="TẮT sẵn. Muốn dùng: tạo check miễn phí ở healthchecks.io (chu kỳ 10 phút, grace 20 phút), dán link thay YOUR-UUID rồi bật node."),
          sched("00:15 hằng ngày", "15 0 * * *", [-600, 420]),
          node("Xuất toàn bộ workflow", "n8n-nodes-base.executeCommand", 1, {"command": "=set N8N_RUNNERS_BROKER_PORT=5689&& set N8N_PORT=5699&& C:\\n8n\\bin\\n8n.cmd export:workflow --all --separate --output=\"C:/n8n-backup/{{ $now.toFormat('yyyy-MM-dd') }}\""}, [-380, 420],
               notes="Đổi cổng tạm để lệnh CLI không đụng cổng 5678/5679 của n8n đang chạy. C:\\n8n\\bin\\n8n.cmd nạp C:\\n8n\\.env."),
          node("Xoá bản sao lưu > 30 ngày", "n8n-nodes-base.executeCommand", 1, {"command": "powershell -NoProfile -Command \"Get-ChildItem 'C:/n8n-backup' -Directory | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Recurse -Force\""}, [-160, 420])]
link(c, "Mỗi 10 phút", "Ping healthchecks"); link(c, "00:15 hằng ngày", "Xuất toàn bộ workflow"); link(c, "Xuất toàn bộ workflow", "Xoá bản sao lưu > 30 ngày")
save("L1-07-heartbeat-sao-luu.json", "L1-07 Heartbeat + sao lưu", nodes, c, "Biết ngay khi n8n/máy chết; có bản sao lưu workflow mỗi đêm.")

print("\n".join(sorted(p.name for p in OUT.glob("*.json"))))
