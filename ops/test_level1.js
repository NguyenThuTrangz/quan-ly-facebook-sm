// Chạy thử mã các node Code của cấp 1 với dữ liệu giả, không cần n8n.  node ops/test_level1.js
const fs = require('fs'), path = require('path');
const W = f => JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'n8n', 'level1', f), 'utf8'));
const codeOf = (wf, name) => wf.nodes.find(n => n.name === name).parameters.jsCode;
let pass = 0, fail = 0;
const ok = (cond, msg) => { if (cond) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ ' + msg); } };
function run(js, ctx) {
  const $ = name => ({ first: () => ({ json: ctx.nodes[name] }), all: () => (ctx.all && ctx.all[name]) || [{ json: ctx.nodes[name] }], item: { json: ctx.nodes[name] } });
  const $input = { first: () => ({ json: ctx.input }), all: () => (ctx.inputAll || [{ json: ctx.input }]) };
  return new Function('$', '$input', 'Buffer', js)($, $input, Buffer);
}

console.log('L1-01 webhook: kiểm dữ liệu');
const w1 = W('L1-01-webhook-ghi-log.json'), v1 = codeOf(w1, 'Kiểm tra dữ liệu');
const good = { headers: { 'x-smock-token': 'DOI_TOKEN_O_DAY' }, body: { ma_tk: 'SM01', loai_viec: 'Tim story', noi: 'Story', noi_dung: 'story tim 2/3', trang_thai: 'Xong', so_luong: 2, lich_row: 121 } };
let r = run(v1, { input: good, nodes: {} })[0].json;
ok(r.ok && r.row.length === 11 && r.lich_values[0] === 'Done', 'log hợp lệ → 11 cột, Lịch = Done');
const r2 = run(v1, { input: good, nodes: {} })[0].json;
ok(r.ma_log === r2.ma_log, 'gửi lại cùng việc → cùng Mã log (chống trùng)');
r = run(v1, { input: { ...good, headers: { 'x-smock-token': 'sai' } }, nodes: {} })[0].json;
ok(!r.ok && r.errors.includes('sai token'), 'sai token → từ chối');
r = run(v1, { input: { ...good, body: { ...good.body, loai_viec: 'Đăng story' } }, nodes: {} })[0].json;
ok(!r.ok, 'loại việc ngoài danh sách → từ chối');
r = run(v1, { input: { ...good, body: { ...good.body, phone: '0912' } }, nodes: {} })[0].json;
ok(!r.ok, 'gửi kèm trường phone → từ chối');
r = run(v1, { input: { ...good, body: { ...good.body, trang_thai: 'Không làm được' } }, nodes: {} })[0].json;
ok(r.ok && r.lich_values[0] === 'Lỗi', 'Không làm được → Lịch = Lỗi');
r = run(v1, { input: { headers: good.headers, body: { type: 'status', tab: 'Lead Hunter', row: 5, status: 'Đã trả lời' } }, nodes: {} })[0].json;
ok(r.ok, 'cập nhật trạng thái hợp lệ');
r = run(v1, { input: { headers: good.headers, body: { type: 'status', tab: 'Lead Hunter', row: 5, status: 'Gửi rồi' } }, nodes: {} })[0].json;
ok(!r.ok, 'trạng thái không có trong hợp đồng → từ chối');
const dup = codeOf(w1, 'Đã ghi chưa?');
const v = run(v1, { input: good, nodes: {} })[0].json;
ok(run(dup, { input: { values: [['Mã log'], [v.ma_log]] }, nodes: { 'Kiểm tra dữ liệu': v } })[0].json.duplicate === true, 'Mã log đã có trong sheet → không ghi thêm');

console.log('L1-02 sinh lịch');
const w2 = W('L1-02-sinh-lich.json'), g = codeOf(w2, 'Sinh lịch');
const acc = [['SM01', 'Sophie Embroidery', 'Chrome', 'SM01', 'u', 'Hoạt động'], ['SM02', 'Marie Smocked', 'Chrome', 'SM02', 'u', 'Hoạt động'], ['SM03', 'Rosie Smocking', 'Edge', 'SM03', 'u', 'Hoạt động'], ['SM05', 'Olivia', 'Chrome', 'SM05', 'u', '']];
const kpi = [['SM01', 'u', 2, 2, 3, 2, 2], ['SM02', 'u', 2, 2, 3, 2, 2], ['SM03', 'u', 2, 2, 3, 2, 2]];
const jg = Array.from({ length: 10 }, (_, i) => [i + 1, 'G' + (i + 1), 'url', i < 4 ? 'đã join' : 'Chưa Join', i < 2 ? 'đã join' : 'Chưa Join', 'Chưa Join']);
const af = Array.from({ length: 20 }, (_, i) => [i + 1, 'link', 'Chưa Add']);
const cq = Array.from({ length: 12 }, (_, i) => ['CG' + (i + 1), 'KE', i % 2 ? 'wall' : 'group', 'cap', 'https://drive.google.com/drive/folders/abc' + i, 'Chưa dùng', '', '', '', '', '']);
const gs = [[1, 'G1', 'u', '', '', '', '', '', '', '', '', '', '', 80, 'A', '', 'Đã chấm'], [2, 'G2', 'u', '', '', '', '', '', '', '', '', '', '', 60, 'B', '', 'Đã duyệt']];
const base = { 'Đọc Tài khoản': { values: acc }, 'Đọc Target + Workload': { values: kpi }, 'Đọc Join Group SM': { values: jg }, 'Đọc Add Friend': { values: af },
  'Đọc Lịch SM': { values: [] }, 'Đọc Content Queue': { values: cq }, 'Đọc Group Score': { values: gs } };
r = run(g, { nodes: base })[0].json;
ok(!r.skip && r.rows.length > 20, `sinh ${r.rows.length} việc cho 3 nick (bỏ nick không Hoạt động)`);
ok(r.rows.every(x => x[1] >= '08:30' && x[1] <= '17:00'), 'mọi việc trong 08:30–17:00');
ok(r.rows.every(x => !(x[1] >= '11:45' && x[1] < '13:15')), 'không có việc giờ nghỉ trưa');
const gp = r.rows.filter(x => x[4] === 'đăng group').map(x => +x[1].slice(0, 2) * 60 + +x[1].slice(3)).sort((a, b) => a - b);
ok(gp.every((m, i) => i === 0 || m - gp[i - 1] >= 60), `bài group cả đội cách nhau ≥ 60 phút (${gp.length} bài)`);
ok(r.rows.filter(x => x[4] === 'đăng group').every(x => /group (1|2)$/.test(x[5])), 'bài group chỉ vào group tier A/B đã join');
const codes = r.rows.map(x => (/K\d+/.exec(x[5]) || [])[0]).filter(Boolean);
ok(new Set(codes).size === codes.length, `mã bài không trùng (${codes.join(', ')})`);
ok(r.data.filter(d => d.range.startsWith("'Content Queue'")).length === codes.length, 'mỗi bài giữ chỗ đúng 1 content');
const fr = r.rows.filter(x => x[4] === 'kết bạn').flatMap(x => x[5].replace('kết bạn ', '').split(', '));
ok(new Set(fr).size === fr.length, 'không giao cùng người kết bạn cho 2 nick');
const again = run(g, { nodes: base })[0].json;
ok(JSON.stringify(again.rows) === JSON.stringify(r.rows), 'chạy lại cùng ngày → cùng kết quả (random có hạt giống)');
const withLich = { ...base, 'Đọc Lịch SM': { values: r.rows.map(x => [x[0]]) } };
ok(run(g, { nodes: withLich })[0].json.skip === true, 'đã có lịch ngày đó → không sinh trùng');
const noGS = run(g, { nodes: { ...base, 'Đọc Group Score': { values: [] } } })[0].json;
ok(noGS.rows.every(x => x[4] !== 'đăng group') && /chưa có group A\/B/.test(noGS.summary), 'chưa chấm group → không xếp bài group, có báo lý do');

console.log('L1-03 gói bài: thay mã bài vào caption');
const w3 = W('L1-03-chuan-bi-goi-bai.json'), p3 = codeOf(w3, 'Chọn bài cần gói');
r = run(p3, { input: { values: [['CG1-v1', 'phái sinh', 'group', 'Hello. DM or WhatsApp us code {{MA_BAI}} for the catalog', 'https://drive.google.com/drive/folders/XYZ', 'Đã xếp', 'K130', '', '', '', '']] }, nodes: {} });
ok(r[0].json.caption.includes('K130') && !r[0].json.caption.includes('{{MA_BAI}}') && r[0].json.folderId === 'XYZ', 'caption có K130, lấy đúng folder id');
r = run(p3, { input: { values: [['CG2', 'KE', 'wall', 'Lovely dress', 'https://drive.google.com/drive/folders/Q', 'Đã xếp', 'K131', '', '', '', '']] }, nodes: {} });
ok(/code K131/.test(r[0].json.caption), 'caption gốc chưa có mã → tự thêm lời mời nhắn tin kèm mã');

console.log('L1-06 nhập kết quả cấp 2');
const w6 = W('L1-06-cau-noi-cap-2.json'), imp = codeOf(w6, 'Kiểm + chuyển thành lệnh ghi');
r = run(imp, { inputAll: [
  { json: { data: { task_id: 'CAP-20261111-001', kind: 'caption', sheet_row: 5, source_code: 'CG4', type: 'group', variants: [{ caption: 'a {{MA_BAI}}' }, { caption: 'b {{MA_BAI}}' }, { caption: 'c {{MA_BAI}}' }] } } },
  { json: { data: { task_id: 'GRP-20261111-002', kind: 'group', sheet_row: 3, scores: { gates: false, icp: 25, sell: 20, active: 8, engage: 8, buyer: 5, geo: 10, spam: 5 }, total: 81, tier: 'A', evidence: 'x' } } },
  { json: { data: { task_id: 'BAD', kind: 'caption' } } },
  { json: { data: { task_id: 'GRP-20261111-003', kind: 'group', sheet_row: 4, scores: { icp: 1 }, email: 'a@b.c' } } }] , nodes: {} })[0].json;
ok(r.appends.length === 3 && r.appends.every(a => a[5] === 'Chờ duyệt caption'), '3 caption phái sinh vào "Chờ duyệt caption"');
ok(r.updates.some(u => u.range.includes("'Group Score'!F3:Q3") && u.values[0][11] === 'Đã chấm'), 'điểm group ghi đúng dòng, trạng thái Đã chấm');
ok(r.errors.length === 2, 'từ chối file sai task_id và file có trường email');

console.log(`\n${pass} đạt, ${fail} lỗi`);
process.exit(fail ? 1 : 0);
