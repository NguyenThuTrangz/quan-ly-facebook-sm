"""Bỏ Postgres khỏi workflow Smock Lead Hunter, dùng tab 'Lead Hunter' có sẵn + bộ nhớ của chính workflow.

Chạy 1 lần (chạy lại không sao):   py -I -X utf8 ops/sua_lead_hunter.py   rồi   py -I -X utf8 ops/cai_dat_n8n.py
- Xoá mọi node Postgres, nhánh tạo bảng (Manual Trigger DDL), nhánh xoá dữ liệu 00:00, nhánh báo cáo n8n API (không có trigger).
- Chống trùng: link đã có ở cột B tab Lead Hunter + danh sách bài đã quét 14 ngày lưu trong workflow static data
  (chỉ lưu khi workflow chạy theo lịch, không lưu khi chạy tay).
- Tắt sẵn 2 node Telegram (bật khi có chat ID nhóm).
- Serper key: cai_dat_n8n.py thay YOUR_SERPER_API_KEY bằng biến môi trường SERPER_API_KEY.
- LLM: tạo credential "OpenAI API" trong n8n, Base URL https://openrouter.ai/api/v1, API key OpenRouter → cai_dat_n8n.py tự gắn.
"""
import json, pathlib, uuid

F = pathlib.Path(__file__).resolve().parent.parent / "n8n" / "smock-lead-hunter.json"
SHEET = "1k7Jl7EzZPI7O0t8Mjfkko4gu_7aWymzfNdjFMXVrnu0"
w = json.loads(F.read_text(encoding="utf8"))
nodes = {n["name"]: n for n in w["nodes"]}
conns = w["connections"]
LIMIT = int(nodes["Limit - Cap Items Per Cycle (Token Guard)"]["parameters"].get("maxItems", 20))
READ = "Đọc link đã có (tab Lead Hunter)"

drop = {n for n, x in nodes.items() if x["type"].endswith(".postgres")}
drop |= {"Manual Trigger - One-Time DB Setup", "Schedule - Daily TTL Purge (00:00 VN)", "Extraction Succeeded?",
         "Set Execution ID", "Get Execution Data", "Build In-Out Report", "Convert Report to JSON File"}
drop &= set(nodes)

if READ not in nodes:
    w["nodes"].append({"parameters": {
        "url": "=https://sheets.googleapis.com/v4/spreadsheets/" + SHEET + "/values/{{ encodeURIComponent(\"'Lead Hunter'!B2:B5000\") }}",
        "authentication": "predefinedCredentialType", "nodeCredentialType": "googleSheetsOAuth2Api",
        "options": {"response": {"response": {"responseFormat": "json"}}}},
        "id": str(uuid.uuid4()), "name": READ, "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
        "position": nodes["Postgres - Get Already Scanned Post IDs"]["position"] if "Postgres - Get Already Scanned Post IDs" in nodes else [900, 560],
        "executeOnce": True, "alwaysOutputData": True, "retryOnFail": True, "maxTries": 3,
        "notes": "Link đã có trong tab Lead Hunter → không đưa lại. Thay cho Postgres."})

# Nối lại: Pre-Filter → [Đọc link, Dedupe] (đọc link chạy trước)
pf = "Pre-Filter Negative Keywords (Defense in Depth)"
conns[pf] = {"main": [[{"node": READ, "type": "main", "index": 0},
                       {"node": "Deduplicate & Clean Content", "type": "main", "index": 0}]]}

nodes["Deduplicate & Clean Content"]["parameters"]["jsCode"] = r"""// Bỏ bài đã có trong tab Lead Hunter (cột B) và bài đã quét trong 14 ngày (bộ nhớ của workflow).
// Chỉ ghi nhớ đúng số bài sẽ gửi LLM ở chu kỳ này (= Limit), bài còn lại để chu kỳ sau.
const norm = u => String(u || '').trim().replace(/[?#].*$/, '').replace(/\/+$/, '').toLowerCase();
let inSheet = [];
try { inSheet = ($('%s').first().json.values || []).map(r => norm(r[0])); } catch (e) { inSheet = []; }
const seenLinks = new Set(inSheet.filter(Boolean));
const mem = $getWorkflowStaticData('global');
const now = Date.now(), TTL = 14 * 864e5;
mem.scanned = Object.fromEntries(Object.entries(mem.scanned || {}).filter(([, t]) => now - t < TTL));
const out = [];
for (const it of $input.all()) {
  const id = it.json.postId, link = norm(it.json.postUrl);
  if ((id && mem.scanned[id]) || (link && seenLinks.has(link))) continue;
  seenLinks.add(link); out.push(it);
}
for (const it of out.slice(0, %d)) if (it.json.postId) mem.scanned[it.json.postId] = now;
return out;""" % (READ, LIMIT)

for n in ("Telegram - Hot Lead Alert", "Set Telegram Chat ID (Static Config)"):
    if n in nodes:
        nodes[n]["disabled"] = True

w["nodes"] = [n for n in w["nodes"] if n["name"] not in drop]
for a in list(conns):
    if a in drop:
        del conns[a]; continue
    conns[a]["main"] = [[o for o in outs if o["node"] not in drop] for outs in conns[a].get("main", [])]
w.setdefault("meta", {})["smockNotes"] = "Không dùng Postgres: chống trùng bằng tab Lead Hunter + static data. Cần SERPER_API_KEY và credential OpenAI API (OpenRouter)."
F.write_text(json.dumps(w, ensure_ascii=False, indent=2), encoding="utf8")
print("đã xoá:", sorted(drop))
print("còn", len(w["nodes"]), "node")
