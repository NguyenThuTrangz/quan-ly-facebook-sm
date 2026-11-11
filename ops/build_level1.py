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
  GROUP_POST_GAP_MIN: 60,
};
""" % SHEET

def node(name, typ, ver, params, pos, **extra):
    n = {"parameters": params, "id": str(uuid.uuid4()), "name": name, "type": typ, "typeVersion": ver, "position": pos}
    n.update(extra)
    return n

def code(name, js, pos, notes=None, each=False):
    p = {"jsCode": js}
    if each: p["mode"] = "runOnceForEachItem"
    return node(name, "n8n-nodes-base.code", 2, p, pos, **({"notes": notes} if notes else {}))

def gget(name, rng_expr, pos, notes="CHỌN CREDENTIAL: Google Sheets OAuth2 (tài khoản có quyền sửa sheet chính)."):
    return node(name, "n8n-nodes-base.httpRequest", 4.2, {
        "url": "=" + API + "/values/{{ encodeURIComponent(" + rng_expr + ") }}",
        "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api",
        "options": {"response": {"response": {"responseFormat": "json"}}}}, pos,
        retryOnFail=True, maxTries=3, waitBetweenTries=3000, notes=notes, alwaysOutputData=True)

def gpost(name, path_expr, body_expr, pos, notes="CHỌN CREDENTIAL: Google Sheets OAuth2."):
    return node(name, "n8n-nodes-base.httpRequest", 4.2, {
        "method": "POST", "url": "=" + API + path_expr,
        "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api",
        "sendBody": True, "specifyBody": "json", "jsonBody": "={{ JSON.stringify(" + body_expr + ") }}",
        "options": {}}, pos, retryOnFail=True, maxTries=3, waitBetweenTries=3000, notes=notes)

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
const V = n => ($(n).first().json.values || []);
const acc = V('Đọc Tài khoản'), kpi = V('Đọc Target + Workload'), jg = V('Đọc Join Group SM'),
      af = V('Đọc Add Friend'), lich = V('Đọc Lịch SM'), cq = V('Đọc Content Queue'), gs = V('Đọc Group Score');
// Ngày làm việc kế tiếp (bỏ Chủ nhật)
const now = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' }));
const d = new Date(now); d.setDate(d.getDate() + 1); if (d.getDay() === 0) d.setDate(d.getDate() + 1);
const day = d.toISOString().slice(0, 10);
const dayVN = `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
// Đã có lịch cho ngày đó thì dừng (chạy lại không sinh trùng)
if (lich.some(r => (r[0] || '').includes(dayVN) || (r[0] || '').startsWith(day))) return [{ json: { skip: true, reason: 'Đã có lịch ngày ' + day } }];
// Nick hoạt động + tên
const nicks = acc.filter(r => /^SM0\d$/.test(r[0]) && /Hoạt động/i.test(r[5] || '')).map(r => ({ id: r[0], name: r[1] }));
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
const jgCol = { SM01: 3, SM02: 4, SM03: 5 };
// Kho content chưa dùng + mã bài kế tiếp
const cqRows = cq.map((r, i) => ({ r, row: i + 2 })).filter(x => x.r[5] === 'Chưa dùng');
let maxK = 116; for (const r of cq) { const m = /^K(\d+)$/.exec(r[6] || ''); if (m) maxK = Math.max(maxK, +m[1]); }
const used = new Set(); const reserve = [];
const takeContent = (nick, kind) => {
  const x = cqRows.find(x => !used.has(x.row) && (kind === 'group' ? /group/i.test(x.r[2] || 'group') : true));
  if (!x) return null; used.add(x.row); const code = 'K' + (++maxK);
  reserve.push({ row: x.row, code, nick }); return { code, content: x.r[0] };
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
    const canPost = jg.filter(r => /đã join/i.test(r[col] || '') && okGroup.has(+r[0])).map(r => +r[0]);
    for (let i = 0; i < q.grp && canPost.length; i++) {
      const c = takeContent(n.id, 'group'); if (!c) break;
      list.push(['đăng group', `đăng group ${c.code} (${c.content}) → group ${canPost[i % canPost.length]}`, 'group']);
    }
  }
  for (let i = 0; i < q.wall; i++) { const c = takeContent(n.id, 'wall'); if (!c) break; list.push(['đăng tường', `đăng tường ${c.code} (${c.content})`]); }
  const nf = Math.min(q.fr, frList.length - frIdx);
  if (nf > 0) { const ids = frList.slice(frIdx, frIdx + nf); frIdx += nf; ids.forEach(x => frReserve.push({ row: x.row, nick: n.id }));
    list.push(['kết bạn', `kết bạn ${ids.map(x => x.r[0]).join(', ')}`]); }
  // 2 cụm mỗi nick: sáng và chiều (giảm chọn lại trình duyệt, vẫn rải trong ngày)
  shuffle(list); const half = Math.ceil(list.length / 2);
  tasks.push({ nick: n, block: 'sáng', items: list.slice(0, half) }, { nick: n, block: 'chiều', items: list.slice(half) });
}
// Xếp giờ: cụm cách nhau 20–40 phút, việc trong cụm cách 4–9 phút; bài group cả đội cách ≥ 60 phút
const toMin = s => +s.slice(0, 2) * 60 + +s.slice(3); const hhmm = m => String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
const S = toMin(CFG.OFFICE_START), E = toMin(CFG.OFFICE_END), L1 = toMin(CFG.LUNCH_START), L2 = toMin(CFG.LUNCH_END);
const order = [...shuffle(tasks.filter(t => t.block === 'sáng')), ...shuffle(tasks.filter(t => t.block === 'chiều'))];
let t = S + ri(0, 15), lastGroup = -999; const rows = []; const overflow = [];
for (const b of order) {
  if (b.block === 'chiều' && t < L2) t = L2 + ri(0, 10);
  for (const it of b.items) {
    if (t >= L1 && t < L2) t = L2 + ri(0, 10);
    if (it[2] === 'group' && t - lastGroup < CFG.GROUP_POST_GAP_MIN) t = lastGroup + CFG.GROUP_POST_GAP_MIN + ri(0, 5);
    if (t > E) { overflow.push(`${b.nick.id}: ${it[1]}`); continue; }
    if (it[2] === 'group') lastGroup = t;
    rows.push([dayVN, hhmm(t), b.nick.id, b.nick.name, it[0], it[1], 'Có', 'Chờ', '', 'sinh bởi n8n L1-02']);
    t += ri(4, 9);
  }
  t += ri(20, 40);
}
rows.sort((a, b) => a[1].localeCompare(b[1]));
const data = reserve.map(x => ({ range: `'Content Queue'!F${x.row}:I${x.row}`, values: [['Đã xếp', x.code, dayVN, x.nick]] }))
  .concat(frReserve.map(x => ({ range: `'Add Friend'!C${x.row}`, values: [[`Đã xếp ${x.nick} ${dayVN}`]] })));
return [{ json: { skip: false, day, rows, data, overflow, summary: `${rows.length} việc cho ${nicks.length} nick ngày ${dayVN}` + (overflow.length ? `; ${overflow.length} việc không vừa giờ` : '') + (okGroup.size ? '' : '; chưa có group A/B nên không xếp bài group') } }];
"""
nodes, c = [], {}
reads = [("Đọc Tài khoản", "\"'Tài khoản'!A2:I20\""), ("Đọc Target + Workload", "\"'Target + Workload'!A4:K11\""),
         ("Đọc Join Group SM", "\"'Join Group SM'!A2:F200\""), ("Đọc Add Friend", "\"'Add Friend'!A2:D2000\""),
         ("Đọc Lịch SM", "\"'Lịch SM'!A2:A3000\""), ("Đọc Content Queue", "\"'Content Queue'!A2:K3000\""), ("Đọc Group Score", "\"'Group Score'!A2:R500\"")]
nodes.append(sched("21:30 Chủ nhật–Thứ sáu", "30 21 * * 0-5", [-1200, 300], notes="Sinh lịch cho ngày làm việc kế tiếp (thứ 2–7)."))
prev = "21:30 Chủ nhật–Thứ sáu"
for i, (nm, rng) in enumerate(reads):
    nodes.append(gget(nm, rng, [-980 + i * 200, 300])); link(c, prev, nm); prev = nm
nodes += [code("Sinh lịch", gen_js, [420, 300], notes="Luật: giờ hành chính, 2 cụm/nick, bài group chỉ vào group tier A/B đã join, cách nhau ≥60 phút, mỗi content 1 lần."),
          iff("Có việc mới?", "{{ !$json.skip && $json.rows.length > 0 }}", [640, 300]),
          gpost("Ghi Lịch SM", "/values/{{ encodeURIComponent(\"'Lịch SM'!A:J\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS", "{ values: $json.rows }", [860, 220]),
          gpost("Giữ chỗ content + kết bạn", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $('Sinh lịch').first().json.data }", [1080, 220]),
          telegram("Báo nhóm", "{{ '🗓 ' + $('Sinh lịch').first().json.summary }}", [1300, 220])]
link(c, prev, "Sinh lịch"); link(c, "Sinh lịch", "Có việc mới?"); link(c, "Có việc mới?", "Ghi Lịch SM")
link(c, "Ghi Lịch SM", "Giữ chỗ content + kết bạn"); link(c, "Giữ chỗ content + kết bạn", "Báo nhóm")
save("L1-02-sinh-lich.json", "L1-02 Sinh Lịch SM ngày làm việc kế tiếp", nodes, c,
     "Thay việc 'lên lịch hôm nay' của Claude. Chạy lại không sinh trùng (kiểm ngày đã có lịch). Random có hạt giống theo ngày.")

# ---------------------------------------------------------------- L1-03 chuẩn bị gói bài
pick_js = CONFIG_JS + r"""
const rows = ($input.first().json.values || []).map((r, i) => ({ r, row: i + 2 })).filter(x => x.r[5] === 'Đã xếp');
const out = [];
for (const x of rows) {
  const link = x.r[4] || ''; const m = /folders\/([\w-]+)/.exec(link) || /[?&]id=([\w-]+)/.exec(link);
  // Thay {{MA_BAI}} (caption phái sinh từ cấp 2) bằng mã bài thật; caption gốc chưa có mã thì thêm câu mời nhắn tin
  let cap = (x.r[3] || '').replace(/\{\{MA_BAI\}\}/g, x.r[6]);
  if (!new RegExp('\\b' + x.r[6] + '\\b').test(cap)) cap += `\n\nDM or WhatsApp us code ${x.r[6]} for the catalog.`;
  out.push({ json: { row: x.row, code: x.r[6], caption: cap, folderId: m ? m[1] : null, dir: `${CFG.PACK_DIR}/${x.r[6]}` } });
}
return out.length ? out : [{ json: { empty: true } }];"""
caption_js = r"""const items = [];
for (const it of $input.all()) {
  if (it.json.empty) continue;
  items.push({ json: it.json, binary: { data: { data: Buffer.from(it.json.caption, 'utf8').toString('base64'), mimeType: 'text/plain', fileName: 'caption.txt' } } });
}
return items;"""
explode_js = r"""// Mỗi bài → danh sách file trong folder (từ Drive API) → mỗi ảnh một item để tải bản JPG 2048px
const out = [];
for (const it of $input.all()) {
  const meta = $('Chọn bài cần gói').all().find(x => x.json.folderId && it.json.files !== undefined && x.json.folderId === it.json.folderId) || null;
  const files = (it.json.files || []).filter(f => /^image\//.test(f.mimeType || ''));
  files.forEach((f, i) => out.push({ json: { ...(meta ? meta.json : {}), fileId: f.id, idx: i + 1, total: files.length } }));
}
return out;"""
nodes, c = [], {}
nodes += [sched("22:00 Chủ nhật–Thứ sáu", "0 22 * * 0-5", [-900, 300]),
          gget("Đọc Content Queue", "\"'Content Queue'!A2:K3000\"", [-680, 300]),
          code("Chọn bài cần gói", pick_js, [-460, 300]),
          iff("Có bài?", "{{ !$json.empty && !!$json.folderId }}", [-240, 300]),
          code("Tạo caption.txt", caption_js, [-20, 140]),
          node("Ghi caption.txt", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $json.dir + '/caption.txt' }}", "dataPropertyName": "data", "options": {}}, [200, 140]),
          node("Liệt kê ảnh trong folder Drive", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=https://www.googleapis.com/drive/v3/files?q={{ encodeURIComponent(\"'\" + $json.folderId + \"' in parents and trashed=false\") }}&fields=files(id,name,mimeType)&supportsAllDrives=true&includeItemsFromAllDrives=true",
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleDriveOAuth2Api", "options": {}}, [-20, 380],
              notes="CHỌN CREDENTIAL: Google Drive OAuth2. Folder do người khác sở hữu vẫn liệt kê được nếu tài khoản này mở được link.", retryOnFail=True, maxTries=3),
          code("Tách từng ảnh", explode_js.replace("it.json.files !== undefined && x.json.folderId === it.json.folderId", "true") , [200, 380]),
          node("Tải ảnh JPG 2048px", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=https://drive.google.com/thumbnail?id={{ $json.fileId }}&sz=w2048",
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleDriveOAuth2Api",
              "options": {"response": {"response": {"responseFormat": "file"}}, "batching": {"batch": {"batchSize": 1, "batchInterval": 1500}}}}, [420, 380],
              notes="Luôn tải bản JPG (xử lý được cả HEIC). 1,5 giây/ảnh để không bị Google chặn.", retryOnFail=True, maxTries=3),
          node("Lưu ảnh vào gói", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $json.dir + '/' + String($json.idx).padStart(2, '0') + '.jpg' }}", "dataPropertyName": "data", "options": {}}, [640, 380]),
          code("Gom kết quả theo bài", r"""const by = {};
for (const it of $('Tách từng ảnh').all()) { const k = it.json.row; by[k] = by[k] || { row: k, code: it.json.code, dir: it.json.dir, total: it.json.total, saved: 0 }; }
for (const it of $input.all()) { const k = it.json.row; if (by[k]) by[k].saved++; }
const data = Object.values(by).map(b => ({ range: `'Content Queue'!F${b.row}`, values: [[b.saved > 0 && b.saved === b.total ? 'Gói sẵn' : 'Lỗi gói']] }))
  .concat(Object.values(by).map(b => ({ range: `'Content Queue'!J${b.row}:K${b.row}`, values: [[b.dir, `${b.saved}/${b.total} ảnh`]] })));
return [{ json: { data, n: Object.keys(by).length } }];""", [860, 380]),
          gpost("Ghi trạng thái gói", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $json.data }", [1080, 380])]
for a, b, o in [("22:00 Chủ nhật–Thứ sáu", "Đọc Content Queue", 0), ("Đọc Content Queue", "Chọn bài cần gói", 0), ("Chọn bài cần gói", "Có bài?", 0),
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
          code("Tính báo cáo + đèn", report_js, [-20, 300], notes="Đèn: Đỏ nếu có cảnh báo FB trong log; Vàng nếu lỗi nhiều hơn xong hoặc thiếu bài so với KPI ngày."),
          gpost("Ghi Báo cáo ngày", "/values/{{ encodeURIComponent(\"'Báo cáo ngày'!A:K\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS", "{ values: $json.rows }", [200, 300]),
          telegram("Gửi nhóm", "{{ $('Tính báo cáo + đèn').first().json.text }}", [420, 300])]
for a, b in [("18:00 Thứ 2–7", "Đọc Nhật Ký SM"), ("Đọc Nhật Ký SM", "Đọc Target + Workload"), ("Đọc Target + Workload", "Đọc Lịch SM"),
             ("Đọc Lịch SM", "Tính báo cáo + đèn"), ("Tính báo cáo + đèn", "Ghi Báo cáo ngày"), ("Ghi Báo cáo ngày", "Gửi nhóm")]:
    link(c, a, b)
save("L1-04-bao-cao-ngay.json", "L1-04 Báo cáo ngày + đèn sức khỏe", nodes, c, "Không cần Claude tổng hợp báo cáo.")

# ---------------------------------------------------------------- L1-05 kiểm hợp đồng (trước & sau ca)
contract_js = CONFIG_JS + r"""
const HEADERS = %s;
const tabs = Object.keys(HEADERS); const res = $input.first().json.valueRanges || [];
const problems = [];
tabs.forEach((t, i) => {
  const got = ((res[i] || {}).values || [[]])[0] || [];
  HEADERS[t].forEach((h, j) => { if ((got[j] || '').trim() !== h) problems.push(`${t}: cột ${String.fromCharCode(65 + j)} phải là "${h}", đang là "${got[j] || ''}"`); });
});
return [{ json: { problems, ok: problems.length === 0, ranges: tabs.map(t => `'${t}'!1:1`) } }];""" % HEADERS
stuck_js = CONFIG_JS + r"""
const cq = ($('Đọc Content Queue').first().json.values || []), lh = ($('Đọc Lead Hunter').first().json.values || []),
      lich = ($('Đọc Lịch SM').first().json.values || []);
const problems = [...$('Kiểm tiêu đề').first().json.problems];
const now = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' }));
const t = new Date(now); t.setDate(t.getDate() + (now.getHours() >= 12 ? 1 : 0)); const dayVN = `${t.getDate()}/${t.getMonth() + 1}/${t.getFullYear()}`;
// 1) Bài có lịch đăng mà gói chưa sẵn
const needPack = lich.filter(r => (r[0] || '').startsWith(dayVN) && /^đăng/.test(r[4] || '')).map(r => (/K\d+/.exec(r[5] || '') || [])[0]).filter(Boolean);
for (const k of needPack) { const row = cq.find(r => r[6] === k); if (!row || row[5] !== 'Gói sẵn') problems.push(`Bài ${k} ngày ${dayVN} chưa có gói (trạng thái: ${row ? row[5] : 'không thấy trong Content Queue'})`); }
// 2) Lead chờ duyệt quá 48 giờ
const old = lh.filter(r => r[11] === 'Chờ duyệt' && (now - new Date((r[0] || '').replace(' ', 'T'))) > 48 * 3600e3).length;
if (old) problems.push(`${old} lead "Chờ duyệt" quá 48 giờ`);
// 3) Lịch hôm qua còn "Chờ" (cấp 3 bỏ sót hoặc webhook không ghi)
const y = new Date(now); y.setDate(y.getDate() - 1); const yVN = `${y.getDate()}/${y.getMonth() + 1}/${y.getFullYear()}`;
const left = lich.filter(r => (r[0] || '').startsWith(yVN) && r[7] === 'Chờ').length;
if (left) problems.push(`${left} việc ngày ${yVN} vẫn "Chờ" — kiểm cấp 3 hoặc webhook`);
// 4) Đối soát: bài đã Done trên Lịch SM → Content Queue "Đã đăng"
const posted = new Set(lich.filter(r => r[7] === 'Done' && /^đăng/.test(r[4] || '')).map(r => (/K\d+/.exec(r[5] || '') || [])[0]).filter(Boolean));
const data = [];
cq.forEach((r, i) => { if (posted.has(r[6]) && r[5] !== 'Đã đăng') data.push({ range: `'Content Queue'!F${i + 2}`, values: [['Đã đăng']] }); });
return [{ json: { problems, data, text: problems.length ? '⚠️ Kiểm hợp đồng Smock\n- ' + problems.join('\n- ') : '✅ Kiểm hợp đồng Smock: không có vấn đề' } }];"""
nodes, c = [], {}
nodes += [sched("06:30 và 21:50", "30 6,21 * * *", [-900, 300], notes="06:30: trước ca (gói bài hôm nay đủ chưa). 21:50: sau khi sinh lịch (gói bài mai sẽ làm lúc 22:00)."),
          node("Đọc dòng tiêu đề mọi tab", "n8n-nodes-base.httpRequest", 4.2, {
              "url": "=" + API + "/values:batchGet?{{ " + json.dumps(list(CONTRACT['tabs'].keys()), ensure_ascii=False) + ".map(t => 'ranges=' + encodeURIComponent(\"'\" + t + \"'!1:1\")).join('&') }}",
              "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api", "options": {}}, [-680, 300], retryOnFail=True, maxTries=3,
              notes="CHỌN CREDENTIAL: Google Sheets OAuth2."),
          code("Kiểm tiêu đề", contract_js, [-460, 300]),
          gget("Đọc Content Queue", "\"'Content Queue'!A2:K3000\"", [-240, 300]),
          gget("Đọc Lead Hunter", "\"'Lead Hunter'!A2:N5000\"", [-20, 300]),
          gget("Đọc Lịch SM", "\"'Lịch SM'!A2:J5000\"", [200, 300]),
          code("Tìm việc kẹt", stuck_js, [420, 300]),
          iff("Có bài cần đánh dấu Đã đăng?", "{{ $json.data.length > 0 }}", [640, 300]),
          gpost("Đánh dấu Đã đăng", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $('Tìm việc kẹt').first().json.data }", [860, 220]),
          telegram("Báo nếu có vấn đề", "{{ $('Tìm việc kẹt').first().json.text }}", [1080, 300])]
for a, b, o in [("06:30 và 21:50", "Đọc dòng tiêu đề mọi tab", 0), ("Đọc dòng tiêu đề mọi tab", "Kiểm tiêu đề", 0), ("Kiểm tiêu đề", "Đọc Content Queue", 0),
             ("Đọc Content Queue", "Đọc Lead Hunter", 0), ("Đọc Lead Hunter", "Đọc Lịch SM", 0), ("Đọc Lịch SM", "Tìm việc kẹt", 0), ("Tìm việc kẹt", "Có bài cần đánh dấu Đã đăng?", 0),
             ("Có bài cần đánh dấu Đã đăng?", "Đánh dấu Đã đăng", 0), ("Có bài cần đánh dấu Đã đăng?", "Báo nếu có vấn đề", 1), ("Đánh dấu Đã đăng", "Báo nếu có vấn đề", 0)]:
    link(c, a, b, o)
save("L1-05-kiem-hop-dong.json", "L1-05 Kiểm hợp đồng dữ liệu + việc kẹt", nodes, c,
     "Bắt lỗi phối hợp giữa 3 cấp: sai tiêu đề cột, gói bài thiếu, lead tồn, lịch hôm qua còn Chờ.")

# ---------------------------------------------------------------- L1-06 cầu nối cấp 2 (đẩy việc tối, kéo kết quả sáng)
export_js = CONFIG_JS + r"""
const cq = ($('Đọc Content Queue').first().json.values || []), gs = ($('Đọc Group Score').first().json.values || []);
const stamp = new Date().toLocaleString('sv-SE', { timeZone: 'Asia/Ho_Chi_Minh' }).slice(0, 10).replace(/-/g, '');
let n = 0; const files = [];
const id = p => `${p}-${stamp}-${String(++n).padStart(3, '0')}`;
cq.forEach((r, i) => { if (r[5] === 'Cần phái sinh') files.push({ path: `inbox/captions/${id('CAP')}.json`, body: { task_id: null, kind: 'caption', sheet_row: i + 2, source_code: r[0], source_caption: r[3], variants: 3 } }); });
gs.forEach((r, i) => { if (r[16] === 'Chờ chấm' && r[4]) files.push({ path: `inbox/groups/${id('GRP')}.json`, body: { task_id: null, kind: 'group', sheet_row: i + 2, stt: +r[0], name: r[1], url: r[2], text_file: r[4] } }); });
if (new Date().getDay() === 0) files.push({ path: `inbox/reports/${id('RPT')}.json`, body: { task_id: null, kind: 'weekly_report', week_ending: stamp } });
return files.map(f => { f.body.task_id = f.path.split('/').pop().replace('.json', ''); return { json: f, binary: { data: { data: Buffer.from(JSON.stringify(f.body, null, 2)).toString('base64'), mimeType: 'application/json', fileName: f.path.split('/').pop() } } }; });"""
import_js = CONFIG_JS + r"""
const FORBID = %s;
const rows = []; const errors = [];
for (const it of $input.all()) {
  const o = it.json.data || it.json; const fname = it.json.fileName || '';
  if (!/^(CAP|GRP|RPT)-\d{8}-\d{3}$/.test(o.task_id || '')) { errors.push(`${fname}: thiếu/ sai task_id`); continue; }
  if (JSON.stringify(o).match(new RegExp('"(' + FORBID.join('|') + ')"', 'i'))) { errors.push(`${o.task_id}: có trường bị cấm`); continue; }
  if (o.kind === 'caption') {
    if (!Array.isArray(o.variants) || !o.variants.length) { errors.push(`${o.task_id}: không có variants`); continue; }
    o.variants.forEach((v, k) => rows.push({ append: [`${o.source_code}-v${k + 1}`, `phái sinh từ ${o.source_code}`, o.type || 'group', v.caption, o.image_link || '', 'Chờ duyệt caption', '', '', '', '', o.task_id] }));
    rows.push({ update: { range: `'Content Queue'!F${o.sheet_row}`, values: [['Chưa dùng']] } });
  } else if (o.kind === 'group') {
    const s = o.scores || {}; const keys = ['gates', 'icp', 'sell', 'active', 'engage', 'buyer', 'geo', 'spam'];
    if (!keys.every(k => k in s)) { errors.push(`${o.task_id}: thiếu điểm`); continue; }
    rows.push({ update: { range: `'Group Score'!F${o.sheet_row}:Q${o.sheet_row}`, values: [[s.gates, s.icp, s.sell, s.active, s.engage, s.buyer, s.geo, s.spam, o.total, o.tier, String(o.evidence || '').slice(0, 1000), 'Đã chấm']] } });
  }
}
return [{ json: { appends: rows.filter(r => r.append).map(r => r.append), updates: rows.filter(r => r.update).map(r => r.update), errors } }];""" % FORBID
nodes, c = [], {}
nodes += [sched("22:15 đẩy việc sang cấp 2", "15 22 * * *", [-900, 160]),
          gget("Đọc Content Queue", "\"'Content Queue'!A2:K3000\"", [-680, 160]),
          gget("Đọc Group Score", "\"'Group Score'!A2:R500\"", [-460, 160]),
          code("Tạo file việc", export_js, [-240, 160], notes="Mỗi việc một file JSON có task_id duy nhất. File text group do cấp 3 lưu sẵn ở thư mục chung."),
          node("Ghi vào inbox repo cấp 2", "n8n-nodes-base.readWriteFile", 1, {"operation": "write", "fileName": "={{ $('Tạo file việc').item.json.path.startsWith('inbox') ? 'C:/smock-level2-copilot/' + $json.path : '' }}", "dataPropertyName": "data", "options": {}}, [-20, 160]),
          node("git commit + push inbox", "n8n-nodes-base.executeCommand", 1, {"command": "=git -C \"C:/smock-level2-copilot\" pull --rebase && git -C \"C:/smock-level2-copilot\" add inbox && git -C \"C:/smock-level2-copilot\" commit -m \"inbox {{ $now.toFormat('yyyy-MM-dd HH:mm') }}\" ; git -C \"C:/smock-level2-copilot\" push", "executeOnce": True}, [200, 160],
               notes="Cần bật node Execute Command (xem n8n/level1/README.md) và git đã đăng nhập trên máy."),
          sched("06:30 kéo kết quả cấp 2", "30 6 * * *", [-900, 500]),
          node("git pull", "n8n-nodes-base.executeCommand", 1, {"command": "git -C \"C:/smock-level2-copilot\" pull --rebase"}, [-680, 500]),
          node("Đọc file outbox", "n8n-nodes-base.readWriteFile", 1, {"fileSelector": "C:/smock-level2-copilot/outbox/*/*.json", "options": {}}, [-460, 500], alwaysOutputData=True),
          node("Đọc JSON", "n8n-nodes-base.extractFromFile", 1, {"operation": "fromJson", "options": {}}, [-240, 500]),
          code("Kiểm + chuyển thành lệnh ghi", import_js, [-20, 500], notes="Từ chối file sai task_id, thiếu điểm, hoặc có trường bị cấm (SĐT, email, mật khẩu)."),
          gpost("Thêm caption phái sinh (Chờ duyệt)", "/values/{{ encodeURIComponent(\"'Content Queue'!A:K\") }}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS", "{ values: $json.appends }", [200, 440]),
          gpost("Cập nhật điểm group + trạng thái", "/values:batchUpdate", "{ valueInputOption: 'USER_ENTERED', data: $('Kiểm + chuyển thành lệnh ghi').first().json.updates }", [420, 440]),
          node("Chuyển outbox đã xử lý sang done", "n8n-nodes-base.executeCommand", 1, {"command": "powershell -NoProfile -Command \"cd 'C:/smock-level2-copilot'; New-Item -ItemType Directory -Force done | Out-Null; Get-ChildItem outbox -Recurse -Filter *.json | ForEach-Object { git mv $_.FullName ('done/' + $_.Name) }; git commit -m 'done'; git push\""}, [640, 440]),
          telegram("Báo lỗi file cấp 2", "{{ $('Kiểm + chuyển thành lệnh ghi').first().json.errors.length ? '⚠️ Cấp 2: ' + $('Kiểm + chuyển thành lệnh ghi').first().json.errors.join('; ') : '✅ Cấp 2: đã nhập kết quả' }}", [860, 440])]
for a, b in [("22:15 đẩy việc sang cấp 2", "Đọc Content Queue"), ("Đọc Content Queue", "Đọc Group Score"), ("Đọc Group Score", "Tạo file việc"),
             ("Tạo file việc", "Ghi vào inbox repo cấp 2"), ("Ghi vào inbox repo cấp 2", "git commit + push inbox"),
             ("06:30 kéo kết quả cấp 2", "git pull"), ("git pull", "Đọc file outbox"), ("Đọc file outbox", "Đọc JSON"), ("Đọc JSON", "Kiểm + chuyển thành lệnh ghi"),
             ("Kiểm + chuyển thành lệnh ghi", "Thêm caption phái sinh (Chờ duyệt)"), ("Thêm caption phái sinh (Chờ duyệt)", "Cập nhật điểm group + trạng thái"),
             ("Cập nhật điểm group + trạng thái", "Chuyển outbox đã xử lý sang done"), ("Chuyển outbox đã xử lý sang done", "Báo lỗi file cấp 2")]:
    link(c, a, b)
save("L1-06-cau-noi-cap-2.json", "L1-06 Cầu nối cấp 2 (inbox tối, outbox sáng)", nodes, c,
     "Bàn giao cấp 1 ↔ cấp 2 bằng file JSON trong repo smock-level2-copilot. Caption phái sinh luôn vào 'Chờ duyệt caption', người duyệt mới dùng.")

# ---------------------------------------------------------------- L1-07 heartbeat + sao lưu
nodes, c = [], {}
nodes += [sched("Mỗi 10 phút", "*/10 * * * *", [-600, 160]),
          node("Ping healthchecks", "n8n-nodes-base.httpRequest", 4.2, {"url": "https://hc-ping.com/YOUR-UUID", "options": {"timeout": 10000}}, [-380, 160],
               continueOnFail=True, notes="Tạo check miễn phí ở healthchecks.io (chu kỳ 10 phút, grace 20 phút), gửi cảnh báo email/Telegram khi n8n hoặc máy chết."),
          sched("00:15 hằng ngày", "15 0 * * *", [-600, 420]),
          node("Xuất toàn bộ workflow", "n8n-nodes-base.executeCommand", 1, {"command": "=n8n export:workflow --all --separate --output=\"C:/n8n-backup/{{ $now.toFormat('yyyy-MM-dd') }}\""}, [-380, 420],
               notes="Bản npm: chạy được trực tiếp. Bản Docker: đổi thành 'docker exec n8n n8n export:workflow --all --separate --output=/backup/...' với /backup là volume ra ổ đĩa."),
          node("Xoá bản sao lưu > 30 ngày", "n8n-nodes-base.executeCommand", 1, {"command": "powershell -NoProfile -Command \"Get-ChildItem 'C:/n8n-backup' -Directory | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Recurse -Force\""}, [-160, 420])]
link(c, "Mỗi 10 phút", "Ping healthchecks"); link(c, "00:15 hằng ngày", "Xuất toàn bộ workflow"); link(c, "Xuất toàn bộ workflow", "Xoá bản sao lưu > 30 ngày")
save("L1-07-heartbeat-sao-luu.json", "L1-07 Heartbeat + sao lưu", nodes, c, "Biết ngay khi n8n/máy chết; có bản sao lưu workflow mỗi đêm.")

print("\n".join(sorted(p.name for p in OUT.glob("*.json"))))
