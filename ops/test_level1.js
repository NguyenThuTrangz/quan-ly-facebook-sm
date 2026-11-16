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
// Kho content = workbook KE '3. CONTENT GROUP' (A STT, B TEXT, C MEDIA) + tab Pool Content SM
const ke = Array.from({ length: 12 }, (_, i) => [String(i + 1), 'cap ' + (i + 1), 'https://drive.google.com/drive/folders/abc' + i]);
const gs = [[1, 'G1', 'u', '', '', '', '', '', '', '', '', '', '', 80, 'A', '', 'Đã chấm'], [2, 'G2', 'u', '', '', '', '', '', '', '', '', '', '', 60, 'B', '', 'Đã duyệt']];
const base = { 'Đọc Tài khoản': { values: acc }, 'Đọc Target + Workload': { values: kpi }, 'Đọc Join Group SM': { values: jg }, 'Đọc Add Friend': { values: af },
  'Đọc Lịch SM': { values: [] }, 'Đọc content KE': { values: ke }, 'Đọc Pool Content SM': { values: [['', '', '', '', '', '', 'link', 'Lấy trong đây']] }, 'Đọc Group Score': { values: gs }, 'Đọc Nhật Ký SM': { values: [] } };
r = run(g, { nodes: base })[0].json;
ok(!r.skip && r.rows.length > 20, `sinh ${r.rows.length} việc cho 3 nick (bỏ nick không Hoạt động)`);
ok(r.rows.every(x => x[1] >= '08:30' && x[1] <= '17:00'), 'mọi việc trong 08:30–17:00');
ok(r.rows.every(x => !(x[1] >= '11:45' && x[1] < '13:15')), 'không có việc giờ nghỉ trưa');
const mins = x => +x[1].slice(0, 2) * 60 + +x[1].slice(3);
const gapOK = (rows, teamGap, nickGap) => { const g = rows.filter(x => x[4] === 'đăng group').sort((a, b) => mins(a) - mins(b));
  const team = g.every((x, i) => i === 0 || mins(x) - mins(g[i - 1]) >= teamGap);
  const nick = g.every((x, i) => g.slice(0, i).filter(y => y[2] === x[2]).every(y => mins(x) - mins(y) >= nickGap)); return team && nick; };
ok(gapOK(r.rows, 6, 60), 'bài group: cả đội cách ≥ 6 phút, cùng nick cách ≥ 60 phút');
ok(r.rows.filter(x => x[4] === 'đăng group').every(x => /group (1|2)$/.test(x[5])), 'bài group chỉ vào group tier A/B đã join');
const codes = r.rows.map(x => (/K\d+/.exec(x[5]) || [])[0]).filter(Boolean);
ok(new Set(codes).size === codes.length, `mã bài không trùng (${codes.join(', ')})`);
const srcs = r.rows.map(x => (/\((CG|PC)\d+\)/.exec(x[5]) || [])[0]).filter(Boolean);
ok(srcs.length === codes.length && new Set(srcs).size === srcs.length, 'mỗi bài dùng đúng 1 content, không trùng');
ok(r.rows.every(x => /^\d{4}-\d{2}-\d{2}$/.test(x[0])), 'ngày ghi dạng yyyy-mm-dd như tab Lịch SM đang dùng');
ok(r.data.every(d => d.range.startsWith("'Add Friend'")), 'chỉ ghi giữ chỗ vào tab có sẵn (Add Friend), không tab mới');
const usedL = [['2026-11-11', '09:00', 'SM01', 'x', 'đăng group', 'đăng group K140 (CG1) → group 1']];
const rU = run(g, { nodes: { ...base, 'Đọc Lịch SM': { values: usedL } } })[0].json;
ok(!rU.rows.some(x => /\(CG1\)/.test(x[5])) && rU.rows.some(x => /K141/.test(x[5])), 'content đã có trong Lịch SM không dùng lại; mã bài nối tiếp K lớn nhất');
const fr = r.rows.filter(x => x[4] === 'kết bạn').flatMap(x => x[5].replace('kết bạn ', '').split(', '));
ok(new Set(fr).size === fr.length, 'không giao cùng người kết bạn cho 2 nick');
const again = run(g, { nodes: base })[0].json;
ok(JSON.stringify(again.rows) === JSON.stringify(r.rows), 'chạy lại cùng ngày → cùng kết quả (random có hạt giống)');
const withLich = { ...base, 'Đọc Lịch SM': { values: r.rows.map(x => [x[0]]) } };
ok(run(g, { nodes: withLich })[0].json.skip === true, 'đã có lịch ngày đó → không sinh trùng');
const noGS = run(g, { nodes: { ...base, 'Đọc Group Score': { values: [] } } })[0].json;
ok(noGS.rows.every(x => x[4] !== 'đăng group') && /chưa có group A\/B/.test(noGS.summary), 'chưa chấm group → không xếp bài group, có báo lý do');
const jgT = jg.map((x, i) => { const y = [...x]; y[6] = i === 2 ? 'A' : i === 3 ? 'Loại (chết)' : ''; return y; });
const rT = run(g, { nodes: { ...base, 'Đọc Group Score': { values: [] }, 'Đọc Join Group SM': { values: jgT } } })[0].json;
ok(rT.rows.some(x => x[4] === 'đăng group') && rT.rows.filter(x => x[4] === 'đăng group').every(x => /group 3$/.test(x[5])), 'Group Score trống → dùng Tier cột G tab Join Group SM');


console.log('L1-02 công suất 8 nick × 5 bài group/ngày (target 1,75× Sale)');
const acc8 = Array.from({ length: 8 }, (_, i) => ['SM0' + (i + 1), 'Nick ' + (i + 1), 'Chrome', 'SM0' + (i + 1), 'u', 'Hoạt động']);
const kpi8 = acc8.map(a => [a[0], 'u', 2, 2, 2, 1, 5]);
// 45 group A/B, mọi nick đã join (cột D,E,F,I..M)
const jg8 = Array.from({ length: 45 }, (_, i) => { const r = [i + 1, 'G' + (i + 1), 'url', 'đã join', 'đã join', 'đã join', 'A', 88, 'đã join', 'đã join', 'đã join', 'đã join', 'đã join']; return r; });
const gs8 = jg8.map(r => [r[0], r[1], 'u', '', '', '', '', '', '', '', '', '', '', 80, 'A', '', 'Đã duyệt']);
const ke8 = Array.from({ length: 120 }, (_, i) => [String(i + 1), 'cap', 'https://drive.google.com/drive/folders/x' + i]);
const base8 = { 'Đọc Tài khoản': { values: acc8 }, 'Đọc Target + Workload': { values: kpi8 }, 'Đọc Join Group SM': { values: jg8 }, 'Đọc Add Friend': { values: af },
  'Đọc Lịch SM': { values: [] }, 'Đọc content KE': { values: ke8 }, 'Đọc Pool Content SM': { values: [] }, 'Đọc Group Score': { values: gs8 }, 'Đọc Nhật Ký SM': { values: [] } };
const r8 = run(g, { nodes: base8 })[0].json;
const g8 = r8.rows.filter(x => x[4] === 'đăng group');
ok(g8.length === 40 && r8.overflow.length === 0, `8 nick × 5 = ${g8.length} bài group, ${r8.rows.length} việc, không việc nào tràn giờ (2 luồng)`);
ok(gapOK(r8.rows, 6, 60), 'công suất cao vẫn giữ: cả đội cách ≥ 6 phút, cùng nick ≥ 60 phút');
const gIds = g8.map(x => /→ group (\d+)/.exec(x[5])[1]);
ok(new Set(gIds).size === gIds.length, 'cả đội không đăng trùng 1 group trong ngày');
ok(r8.rows.every(x => x[1] >= '08:30' && x[1] <= '17:00' && !(x[1] >= '11:45' && x[1] < '13:15')), 'vẫn trong giờ hành chính, bỏ giờ trưa');
ok(new Set(r8.rows.map(x => x[9])).size === 2, 'chia 2 luồng chạy song song (ghi ở cột Ghi chú)');
// Lịch sử: hôm qua SM01 đã đăng group 1..25 → hôm nay SM01 chỉ được vào group > 25
const d0 = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' })); const yest = `${d0.getDate()}/${d0.getMonth() + 1}/${d0.getFullYear()}`;
const hist = Array.from({ length: 25 }, (_, i) => [yest, '09:00', 'SM01', 'Nick 1', 'đăng group', `đăng group K1 (CG1) → group ${i + 1}`]);
const rH = run(g, { nodes: { ...base8, 'Đọc Lịch SM': { values: hist } } })[0].json;
ok(rH.rows.filter(x => x[2] === 'SM01' && x[4] === 'đăng group').every(x => +/→ group (\d+)/.exec(x[5])[1] > 25), 'không đăng lại group đã đăng trong 3 ngày');
const tIso = `${d0.getFullYear()}-${String(d0.getMonth() + 1).padStart(2, '0')}-${String(d0.getDate()).padStart(2, '0')}`;
const nkL = [[tIso, 'SM02', 'x', 'Đăng bài', 'Group 2', 'FB đòi confirm your identity', '', 'Không làm được', 'Không làm được', 0],
             [tIso, 'SM03', 'x', 'Join group', 'g', 'x', '', 'Không làm được', 'Không làm được', 0], [tIso, 'SM03', 'x', 'Kết bạn', 'g', 'x', '', 'Không làm được', 'Không làm được', 0]];
const rL = run(g, { nodes: { ...base8, 'Đọc Nhật Ký SM': { values: nkL } } })[0].json;
const acc8b = acc8.map(a => a[0] === 'SM04' ? [...a.slice(0, 5), 'Hoạt động - hạn chế group'] : a);
const rN = run(g, { nodes: { ...base8, 'Đọc Tài khoản': { values: acc8b } } })[0].json;
ok(rN.rows.filter(x => x[2] === 'SM04' && x[4] === 'đăng group').length === 0 && rN.rows.some(x => x[2] === 'SM04' && x[4] === 'đăng tường'), 'Tài khoản ghi "hạn chế group" → chỉ đăng tường, không đăng group');
ok(rL.rows.filter(x => x[2] === 'SM02' && x[4] === 'đăng group').length === 0 && rL.rows.filter(x => x[2] === 'SM03' && x[4] === 'đăng group').length <= 2, 'đèn Đỏ → 0 bài group, đèn Vàng → tối đa 2');

console.log('L1-03 gói bài: thay mã bài vào caption');
const w3 = W('L1-03-chuan-bi-goi-bai.json'), p3 = codeOf(w3, 'Chọn bài cần gói');
const tmr = new Date(d0); tmr.setDate(tmr.getDate() + 1); const tmrIso = `${tmr.getFullYear()}-${String(tmr.getMonth() + 1).padStart(2, '0')}-${String(tmr.getDate()).padStart(2, '0')}`;
const lich3 = [[tmrIso, '09:00', 'SM01', 'x', 'đăng group', 'đăng group K130 (PC1) → group 2', 'Có', 'Chờ', '', 'sinh bởi n8n L1-02 · luồng 1'],
               [tmrIso, '10:00', 'SM01', 'x', 'đăng tường', 'đăng tường K131 (CG2)', 'Có', 'Chờ', '', ''],
               [tmrIso, '11:00', 'SM02', 'x', 'đăng tường', 'đăng tường K132 (CG3)', 'Có', 'Chờ', '', 'Gói sẵn 3/3 ảnh'],
               ['2026-01-02', '11:00', 'SM02', 'x', 'đăng tường', 'đăng tường K100 (CG4)', 'Có', 'Done', '', '']];
const ctx3 = { nodes: { 'Đọc Lịch SM': { values: lich3 }, 'Đọc content KE': { values: [['2', 'Lovely dress', 'https://drive.google.com/drive/folders/Q'], ['3', 'x', 'y']] },
  'Đọc Pool Content SM': { values: [['1', 'Hello. DM or WhatsApp us code {{MA_BAI}} for the catalog', 'https://drive.google.com/drive/folders/XYZ', 'Phái sinh từ CG1 (v1)']] } } };
r = run(p3, ctx3);
ok(r.length === 2, 'chỉ gói bài chưa "Gói sẵn" và chưa Done, từ hôm nay trở đi');
ok(r[0].json.caption.includes('K130') && !r[0].json.caption.includes('{{MA_BAI}}') && r[0].json.folderId === 'XYZ' && r[0].json.row === 2, 'caption có K130, lấy đúng folder id và dòng Lịch SM');
ok(/code K131/.test(r[1].json.caption), 'caption gốc chưa có mã → tự thêm lời mời nhắn tin kèm mã');

console.log('L1-05 kiểm tiêu đề theo tab đang có');
const w5 = W('L1-05-kiem-hop-dong.json'), k5 = codeOf(w5, 'Kiểm tiêu đề');
const contract = JSON.parse(fs.readFileSync(path.join(__dirname, 'contract.json'), 'utf8'));
// Tiêu đề thật đọc từ sheet ngày 16/11 (Tài khoản cột A là ' ', Lịch SM có thêm cột Random…)
const real = { 'Tài khoản': [' ', 'Tên Facebook', 'Trình duyệt', 'Profile trình duyệt', 'URL profile FB', 'Trạng thái', 'Nhóm'],
  'Target + Workload': ['STT', 'URL', 'Level Nick', 'Bài đăng tường/ngày', 'Join Group/ngày', 'Gửi Kết bạn/ngày', 'Đăng Group/ngày', 'Bài đăng TCN'],
  'Join Group SM': ['STT', 'Tên group', 'Link Group', 'SM01', 'SM02', 'SM03', 'Tier (Smock Radar 11/11)', 'Điểm', 'SM04', 'SM05', 'SM06', 'SM07', 'SM08'],
  'Pool Content SM': ['STT', 'Content', 'Ảnh/Video', 'Phân loại', 'Comment seeding cho bài', 'PIC'],
  'Lịch SM': contract.tabs['Lịch SM'].headers.concat(['Number random', 'Random 2']) };
const vr = Object.keys(contract.tabs).map(t => ({ values: [real[t] || contract.tabs[t].headers.map(h => h === null ? 'x' : h)] }));
r = run(k5, { input: { valueRanges: vr }, nodes: {} })[0].json;
ok(r.ok, 'tiêu đề thật của sheet → không báo lỗi' + (r.ok ? '' : ': ' + r.problems.join('; ')));
const vr2 = vr.map((x, i) => Object.keys(contract.tabs)[i] === 'Add Friend' ? { values: [['STT', 'Link', 'Tình trạng']] } : x);
r = run(k5, { input: { valueRanges: vr2 }, nodes: {} })[0].json;
ok(!r.ok && /Add Friend: cột B/.test(r.problems[0]), 'cột bị đổi tên → báo đúng tab và cột');

console.log('L1-06 nhập kết quả cấp 2');
const w6 = W('L1-06-cau-noi-cap-2.json'), imp = codeOf(w6, 'Kiểm + chuyển thành lệnh ghi');
r = run(imp, { inputAll: [
  { json: { data: { task_id: 'CAP-20261111-001', kind: 'caption', sheet_row: 5, source_code: 'CG4', type: 'group', variants: [{ caption: 'a {{MA_BAI}}' }, { caption: 'b {{MA_BAI}}' }, { caption: 'c {{MA_BAI}}' }] } } },
  { json: { data: { task_id: 'GRP-20261111-002', kind: 'group', sheet_row: 3, scores: { gates: false, icp: 25, sell: 20, active: 8, engage: 8, buyer: 5, geo: 10, spam: 5 }, total: 81, tier: 'A', evidence: 'x' } } },
  { json: { data: { task_id: 'BAD', kind: 'caption' } } },
  { json: { data: { task_id: 'GRP-20261111-003', kind: 'group', sheet_row: 4, scores: { icp: 1 }, email: 'a@b.c' } } }] , nodes: { 'Đọc Pool Content SM (sáng)': { values: [['5', 'x'], ['', '']] },
  'Đọc content KE (sáng)': { values: [['4', 'goc', 'https://drive.google.com/drive/folders/KE4']] } } })[0].json;
ok(r.appends.every(a => a[2] === 'https://drive.google.com/drive/folders/KE4'), 'kết quả cấp 2 thiếu image_link → tự lấy link ảnh của bài gốc CG4');
const exp = codeOf(w6, 'Tạo file việc');
const old = new Date(d0); old.setDate(old.getDate() - 10); const oldIso = `${old.getFullYear()}-${String(old.getMonth() + 1).padStart(2, '0')}-${String(old.getDate()).padStart(2, '0')}`;
const ex = run(exp, { nodes: { 'Đọc Lịch SM': { values: [[oldIso, '09:00', 'SM01', 'x', 'đăng group', 'đăng group K140 (CG2) → group 1', 'Có', 'Done']] },
  'Đọc content KE': { values: [['1', 'a'.repeat(50), 'L1'], ['2', 'b'.repeat(50), 'L2']] }, 'Đọc Pool Content SM': { values: [] }, 'Đọc Group Score': { values: [] } } });
const b = ex.length && ex[0].json.body;
ok(ex.length === 1 && b.source_code === 'CG2' && b.sheet_row === 4 && b.type === 'group' && /^CAP-\d{8}-\d{3}$/.test(b.task_id),
   'việc caption gửi cấp 2 có sheet_row, type, task_id đúng schema repo cấp 2; chỉ bài đã đăng ≥ 7 ngày');
ok(r.appends.length === 3 && r.appends.every(a => a.length === 6 && /Phái sinh từ CG4.*chờ duyệt/.test(a[3])) && r.appends.map(a => a[0]).join() === '6,7,8',
   '3 caption phái sinh ghi vào Pool Content SM (STT 6–8), Phân loại "… chờ duyệt"');
ok(r.updates.some(u => u.range.includes("'Group Score'!F3:Q3") && u.values[0][11] === 'Đã chấm'), 'điểm group ghi đúng dòng, trạng thái Đã chấm');
ok(r.errors.length === 2, 'từ chối file sai task_id và file có trường email');

console.log(`\n${pass} đạt, ${fail} lỗi`);
process.exit(fail ? 1 : 0);
