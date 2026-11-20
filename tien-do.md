# Tiến độ chạy lịch SM

## 2026-11-20 14:3x — kiểm điều kiện (người dùng đổi account claude.ai lần nữa)
- n8n tắt từ sau 18:00 19/11 tới ~08:35 20/11 (lỡ L1-02 21:30, L1-05, L1-06 22:15); lượt bù sáng mới đã cứu: L1-02 10:20 sinh lịch 20/11 (dòng 292–312, 21 việc, **0 bài đăng** — kho 0), L1-03 OK. n8n bị Ctrl+C 14:15, đã chạy lại 14:23.
- L1-06 lỗi `git pull` từ 11:30 19/11 → 11:30 20/11 do GitHub không truy cập được; 14:2x GitHub thông lại (pull/push OK, commit 1b021fb đã push). Copilot 08:33 OK, inbox 0.
- Trình duyệt: SM01 `74dc5da7` OK (Sophie), SM02 `39874c3f` OK. Có deviceId lạ **`66ee2040-2b73-446a-9ba6-5466555a84c8`** — chưa xác nhận là Edge SM03 máy này → chưa dùng; nếu người dùng xác nhận thì cập nhật CLAUDE.md "Máy này".
- Kho KE: 0 bài mới có ảnh. K146 (CG5), K147 (CG13), K148 (CG14) xếp 19/11 chưa đăng → n8n trả lại kho cho lịch 21/11 (RECLAIM_AFTER_DAYS=2). CG2 dùng lại từ 25/11. CG18/19/22/29 thiếu ảnh, CG30 không link ảnh.
- Lịch 19/11 luồng 1 (dòng 276–291) còn Chờ (không chạy bù; K146–K148 n8n xếp lại 21/11).
- **15:00–15:12 chạy bù lịch 20/11: 18/21 Done** (SM03 đã nối lại đúng `9db7ffa4`). Join: SM03 g20, 25, 32; SM01 g29, 30 (đã join), g43 chờ duyệt → đã ghi Join Group SM (F21, F26, F33, D30, D31, D44). SM02 join 304 Bỏ qua (identity).
- **Lỗi 292, 301, 306 (kết bạn)**: tab Add Friend **STT 21 trở đi chưa có link** nhưng n8n L1-02 vẫn xếp ("Đã xếp SMxx") → cần người dùng thêm link; nên sửa L1-02 bỏ qua dòng Add Friend không có link.
- deviceId lạ `66ee2040…` không dùng.
- **n8n L1-02 sửa (đã cài 15:3x)**: không xếp kết bạn cho dòng Add Friend chưa có link Facebook (test 64/64). Add Friend STT 21+ vẫn cần người dùng thêm link.
- **SM04 Jenny Smocking** (deviceId `bf159760…`, đã ghi CLAUDE.md): sửa **Bio** → "Sales at K-Embroidery | Smocked dresses & sets 🧵 / WhatsApp: +84 855 555 490 | k-embroidery.com" (Công khai; rút gọn vì giới hạn 101 ký tự; dùng số 0855555490 vì ảnh bìa người dùng vừa đổi ghi số này). **Rời 5 group việc làm/HR** (Việc Làm Tiếng Tây Ban Nha; Việc làm Cầu Giấy…; Việc Làm Hành Chính Nhân Sự (Tuyển Dụng, HR…); VIỆC LÀM HÀNH CHÍNH - NHÂN SỰ; Tuyển Dụng HR - Việc Làm Hành Chính Nhân Sự). Trang "nhóm đã tham gia" còn đếm (1) nhưng không hiện group nào. **Chưa sửa** (chờ người dùng): Intro còn "Công ty K-Global / HR Specialist", "Đại học Kinh tế Quốc dân - NEU"; avatar. Không ghi Nhật Ký SM (không có loại việc "sửa profile").

## 2026-11-19 (máy treo 24/24)
- **Mất mạng ~16:30 18/11 → sau 08:35 19/11** (n8n lỗi ENOTFOUND): L1-04 18:00, L1-02 21:30/08:20, L1-03, L1-05, L1-06 đều lỗi. 09:2x đã chạy bù tay L1-02 (lịch 19/11 dòng 267–291) + L1-03 (gói K145–K148).
- **Sửa n8n cho ổn định** (đã cài + khởi động lại): thêm trigger "Chạy tay (CLI)" vào L1-02…L1-06 → chạy bù: `$env:N8N_USER_FOLDER='C:\n8n'; $env:N8N_RUNNERS_BROKER_PORT='5690'; n8n execute --id <id>` (id: L1-02 iiViedWvLDx7oqdg, L1-03 FgMqcu9ihNyjNUJD, L1-04 Y4oEcO1omIGMLlXE, L1-05 J7ZIdcaAqS7N4F8Z, L1-06 TG3fdIg80T1uDFAv). Lượt bù sáng L1-02 08:20 → **08:20–11:20 mỗi giờ**, L1-03 08:25 → **08:25–11:25** (đã có lịch/gói thì tự bỏ qua).
- **Kiểm gắt content 19/11**: K146 (CG5), K147 (CG13), K148 (CG14) caption khớp 100% KE (chỉ đổi WA +84 855 555 490), không mã, ảnh không trùng bài nào → đăng được. **K145 (CG2) Bỏ qua**: 5 ảnh trùng K143 (PC5 phái sinh từ CG2) SM01 đăng tường 18/11 — n8n chưa chặn trùng ảnh giữa CG và PC phái sinh của nó; CG2 dùng lại được từ 25/11. Kho KE: còn ~3 bài có ảnh (kho Ít 0,3 ngày).
- **Radar không truy cập được bằng tài khoản claude.ai mới** (ArtifactData 404) → không ghi/đọc Radar cho tới khi người dùng chia sẻ lại hoặc tạo mới.
- Luồng 2 (SM02) xong: 270 (0), 271 (2 story), 273, 274 (STT 19 Lecy K-Embroidery, 20 Joy Babeeni), 276 (4), 278 (2); 279 join Bỏ qua (SM02 còn bị confirm identity).
- Luồng 1 (SM01, SM03) **chưa chạy**: tiện ích Claude chưa kết nối SM01 (Chrome Profile 1) và SM03 (Edge) sau khi đổi account.

## ✅ 2026-11-18 13:1x — ĐÃ CÀI bản sửa caption vào n8n (agent mới)
- Sửa test L1-06 lỗi thời; `py ops/cai_dat_n8n.py L1-02 L1-03 L1-06` OK, khởi động lại n8n (healthz OK). DB n8n xác nhận L1-02/03/06 có WA +84 855 555 490 + `USE_POOL_DERIVED: false`, 7 workflow đều bật → lịch 19/11 (21:30) dùng caption gốc KE, không mã Kxxx.
- Test còn 1 lỗi KHÔNG liên quan: "8 nick × 5" phụ thuộc ngày (hạt giống 19/11 → 3 việc tràn giờ, ra 39/40 bài group) — chỉ kịch bản giả 8 nick, lịch thật 3 nick không ảnh hưởng. Sửa bộ xếp giờ sau khi bật SM04–SM08.
- Tiện ích Claude lúc 12:57: chưa trình duyệt nào kết nối. GitHub 2 repo fetch/push OK (máy không có `gh`).
- **Nguồn caption K123–K144 (tra 18/11):** K123–K138 = caption gốc KE (CG), K139–K144 = PC1–PC6 do Copilot cấp 2 viết theo prompt `caption.prompt.md` (commit 7bb7e5b 11/11, Claude soạn). Câu "DM or WhatsApp us code Kxxx for the catalog" có ở **tất cả**: KE gốc thì do L1-03 tự nối (build_level1.py dòng 286 bản 0ac1ddc 11/11, Claude soạn); PC thì do prompt cấp 2 bắt chèn {{MA_BAI}}. Kho content KE không tự thêm.
- **Đã đổi WA trên sheet SMOCK's Information** (14:0x, qua Chrome SM02, Find & Replace từng tab): SM01/SM02/SM03 mỗi tab 2 ô (Bio dòng 6, Intro dòng 9) → +84 855 555 490; không còn số cũ. Tab SM04+ không đụng. Đã bỏ "(message us with the post code Kxxx)" ở Intro dòng 9 của cả 8 tab SM01–SM08 (người dùng đồng ý). Dòng 18 "Pinned post … CTA: message us with the post code (to be written)" còn nguyên (chưa viết). Bio FB thật chưa đổi.
- 13:32 `trang-thai`: n8n + 7 workflow bật, chạy tốt; Copilot 05:30 OK. Đã xoá 3 việc phái sinh CAP-20261118-001…003 (CG8/9/10) khỏi inbox cấp 2 (commit 93cc660) → inbox 0.
- Sau khi đổi account claude.ai: tiện ích mới kết nối SM02 (`39874c3f…`); SM01, SM03 chưa thấy trong danh sách.
- Vẫn chờ người dùng: bài K123–K143 có mã Kxxx (sửa/gỡ?), đổi WA sheet SMOCK's Information + bio FB SM01–SM03. Đăng bài vẫn DỪNG.

## ⛔ 2026-11-18 ~11:40 — DỪNG ĐĂNG BÀI + BÀN GIAO (người dùng đổi account) — agent mới đọc mục này TRƯỚC
**Trạng thái:** người dùng ra lệnh **dừng toàn bộ hoạt động đăng bài**. Đã huỷ 3 bài SM01 hẹn giờ (K140, K142, K141 → Lịch SM 262/265/266 = Bỏ qua). **Không đăng bài nào cho tới khi người dùng cho chạy lại.**

**Người dùng chỉ ra 2 lỗi nghiêm trọng (Claude gây ra):**
1. Caption bị **lệch tuyến bài, ép điều hướng khách về inquiry**: caption phái sinh PC1–PC6 (Copilot cấp 2 viết theo prompt của Claude: bắt nhắc MOQ/mock-up/giao hàng + "DM for the catalog") thành một khối văn liền, không giống bài gốc KE.
2. **Mã bài Kxxx bị đưa lên caption** ("DM or WhatsApp us code Kxxx for the catalog", do L1-03 tự chèn) → khách hiểu lầm. Mã chỉ được dùng nội bộ (Lịch SM, Radar). Các bài đã đăng 17–18/11 (K123–K143) đang có câu này — **chưa sửa/gỡ, chờ người dùng quyết**.

**Yêu cầu mới của người dùng (18/11, phải áp dụng):**
- **Chỉ dùng caption gốc KE** (workbook `1mY_7HeFFokARzxwS9xCeby46cYGC5QpA_ju4jl5f-UA`, tab "3. CONTENT GROUP"), **giữ nguyên văn**, không phái sinh, không thêm mã Kxxx.
- **WhatsApp mới chung cho SM01, SM02, SM03: 0855555490 (= +84 855 555 490)**. Đổi số WA trong caption gốc sang số này.

**Việc đang làm dở (chưa xong):**
- `ops/build_level1.py` đã sửa (commit kèm bàn giao này, **CHƯA cài vào n8n**): `CFG.USE_POOL_DERIVED=false` (bỏ PC khỏi kho), `CFG.WHATSAPP='+84 855 555 490'` (L1-03 thay mọi số ĐT trong caption), `L2_CAPTION_JOBS` = 0 (tắt phái sinh), L1-03 không chèn mã Kxxx. `ops/test_level1.js` sửa theo: **62 đạt, 1 lỗi** — test "lượt gửi thứ 2 trong ngày…" (L1-06 phái sinh) đã lỗi thời → xoá/sửa test đó, chạy lại cho đạt hết, rồi `py -I -X utf8 ops/cai_dat_n8n.py L1-02 L1-03 L1-06` + khởi động lại n8n (dừng node n8n → `Start-ScheduledTask 'Smock n8n'` → healthz).
- **n8n hiện vẫn chạy code CŨ**: tối 18/11 21:30 L1-02 sẽ sinh lịch 19/11 còn dùng PC + 22:00 L1-03 chèn mã. → Cài bản sửa trước 21:30, hoặc hỏi người dùng có tắt L1-02/L1-03/L1-06 không (đang chờ người dùng trả lời câu này). Lịch/gói 19/11 nếu đã sinh bằng code cũ thì không dùng caption trong `anh-dang-bai\K…\caption.txt`.
- Repo cấp 2 `C:\smock-level2-copilot\.github\prompts\caption.prompt.md` vẫn bắt chèn `{{MA_BAI}}` — phái sinh đã tắt từ cấp 1 nên không chạy; nếu bật lại phải sửa prompt (không mã, không ép chào hàng).
- Chưa đổi số WA trên sheet **SMOCK's Information** (`1Y9xyKErb3sMZvdgPVXCUWyk7GOt6Y7Qp32i5F8jtV8s`, tab SM01–SM03 dòng 6, 9) và chưa đổi bio FB SM01–SM03 → hỏi người dùng trước khi sửa bio (sửa trang cá nhân là thay đổi công khai).

**Khác cần biết (18/11):** SM01 bị FB "Can't send request" khi kết bạn (Radar `h-20261118-SM01-friendreq`). K139 lỡ đăng vào group 20 (Radar cat *resale*) — n8n L1-02 chưa lọc group theo cat Radar (resale/hobby không được đăng chào hàng). Sáng 18/11 lỡ tạo 1 nhóm tab trống trên Chrome **máy khác** (`87f823ce…`) khi SM chưa kết nối → đã thêm luật vào skill `chay-lich-sm`: chọn đúng deviceId trước mọi lệnh tab; người dùng yêu cầu **không tác động/thông báo gì sang máy khác**.

## 2026-11-18 — luồng 1 + 2 (bắt đầu 10:55, làm bù xen kẽ)
- Sáng n8n bị dừng 09:21 (mã thoát Ctrl+C) → khởi động lại 10:56, healthz OK. Lượt 08:20/08:25 đã chạy trước đó.
- Lịch 18/11 (dòng 235–266) sinh **sáng 17/11** trước khi đổi trạng thái nick → còn việc SM04 (247, 249, 250, 260, 261) và SM02 đăng/join group (235 K144, 241) → ghi Bỏ qua. K144 (PC6) chưa đăng, còn dùng được.
- Join 238 (SM03) và 257 (SM01) đã join từ 17/11 → Bỏ qua.
- SM01: **K139 → g20** (lên ngay; ⚠️ Radar xếp g20 là *resale*, lẽ ra không đăng — n8n L1-02 chưa lọc theo cat Radar), tường **K143**, chấp nhận 1, story 2, group 39, lướt 4, tương tác 3. **Kết bạn bị FB chặn "Can't send request"** → Radar health `h-20261118-SM01-friendreq`, dừng kết bạn SM01 hôm nay.
- SM01 hẹn giờ (cron trong phiên): 13:19 K140 → g2 (262), 13:47 tường K142 (265), 14:23 K141 → **g27** thay g10 resale (266).
- SM03: xong 236, 240, 243 (Tiana gửi; STT 14 đã có lời mời cũ; lỡ gửi nhầm 1 gợi ý và đã huỷ), 251 (0), 252, 253.
- SM02: xong 237 (0), 239, 242, 254, 255, 256 (2 lời mời).

## 2026-11-17 17:55 — Máy bật 24/24 (phương án A, `ops/BAN-GIAO-CAP-3.md` mục 0c)
- Người dùng để máy treo 24/24 từ 17/11 tối. Đã kiểm `trang-thai`: n8n chạy, L1-01…L1-07 bật, Copilot cấp 2 lần tới 05:30 18/11, Sleep = không bao giờ. Đêm nay: 18:00 L1-04 → 21:30 L1-02 lịch 18/11 → 22:00 L1-03 → 22:15 L1-06 → 05:30 Copilot → 06:30 L1-06 kéo caption. Sáng 18/11 cấp 3 chạy lịch từ 08:30.
- **Nick mới chưa vào n8n/Copilot**: tab Tài khoản cột F của SM04, SM05, SM07 = "Chờ chuẩn hoá profile (chưa chạy lịch, chờ người dùng bảo set)" → L1-02 bỏ qua (chỉ lấy nick có chữ "Hoạt động"). SM06, SM08 để trống.
- **Khi người dùng bảo "set nick mới"** (chỉ lúc đó): (1) người dùng nối tiện ích Claude ở profile Chrome → ghi deviceId vào mục "Máy này" CLAUDE.md; (2) sửa cột F = "Hoạt động - hạn chế group" cho tới khi nick join ≥ 15 group A/B (code n8n chưa có luật ≥ 15, chỉ xếp vào group đã join), đủ thì đổi về "Hoạt động"; (3) có số WA riêng ở sheet SMOCK's Information; (4) kiểm Join Group SM cột I–M, tab Target + Workload có dòng nick; (5) chạy thử `node ops/test_level1.js`. Không cần sửa code n8n (CFG đã có SM04–SM08).

## 2026-11-17 — SM04, SM05, SM07 mới (việc dở cho agent sau)
- **SM07** Chrome profile "SM07", FB đang tên **Phan Thị Ngọc Anh** → đổi tên **Maily Smock** theo sheet (tab SM07 dòng 22–26), cùng cách làm như SM04/SM05.
- **WhatsApp (chốt lại 17/11): mỗi nick 1 số WA riêng, người dùng cấp sau.** Chưa có số riêng thì KHÔNG đưa WA lên bio/intro FB của SM04/05/07 (số 3061 trong sheet chỉ là tạm; ghi chú dòng 27 các tab). SM03 giữ số riêng +84 886 421 089, không sửa.
- Nick nhận từ HR: **SM04** Chrome profile "SM04", FB **Jenny Smocking** `profile.php?id=61595904006414`; **SM05** Chrome profile "SM05", FB đang tên **Thanh Chi Lê** `profile.php?id=61595814087257`.
- Mẫu chuẩn: sheet **SMOCK's Information** `1Y9xyKErb3sMZvdgPVXCUWyk7GOt6Y7Qp32i5F8jtV8s`, tab SM04/SM05 (dòng 1–20 = mẫu, dòng 22–26 = hiện trạng + việc đã chốt).
- Người dùng chốt: Bio/Intro theo mẫu SM, Workplace K-Embroidery, xoá SĐT/Gmail tuyển dụng + trường ĐH + "Công ty K-Global"; **SM05 đổi tên → Olivia Smocking**; avatar/ảnh bìa để sau.
- Việc agent sau: (1) người dùng cài + Connect tiện ích Claude ở 2 profile Chrome; (2) ghi deviceId vào mục "Máy này" CLAUDE.md + shortcut; (3) sửa profile theo sheet; (4) ghi log.

## 2026-11-17 — luồng 1 (SM01, SM03; xong 14:25)
- Bắt đầu 09:45 (trễ) → người dùng duyệt **làm bù xen kẽ**. Lịch luồng 1 dòng 193–234: **xong hết**, log webhook OK.
- Bài: SM03 **K133** g30 (chờ duyệt, 13:38 vẫn pending), **K134** g15 (lên ngay), **K135** g29 (chờ duyệt), **K136** g12 14 ảnh (chờ duyệt), tường **K138** (= CG6 thay CG30 thiếu ảnh). SM01 **K123** g5 (chờ duyệt), **K124** g25 (chờ duyệt), **K125** g1 (đổi từ g32 resale, lên ngay), tường **K129**, **K128**. Tất cả đã đăng ký Radar.
- Bỏ qua (Lỗi gói 0/0 ảnh): K126 (229), K127 (233), K137 (232).
- **SM03 bị hạn chế gửi tin nhắn** ("Confirm your identity to send messages", 11:04) → Radar health `h-20261117-SM03-identity` (Đỏ). Người dùng cho đăng group tiếp, vẫn chạy được. Cần người dùng xác minh trên điện thoại. Inbox David (Trung Quốc, có vẻ xưởng/nhà cung cấp) đã ghi signal, chưa tính QI.
- Join: SM01 g12, 15, 27; SM03 g5, 10, 17 → đã ghi Join Group SM cột D/F + Radar. Kết bạn: SM01 STT1 đã có lời mời cũ, STT2 đã là bạn; SM03 STT6 gửi, STT5 không có nút.
- Content đã dùng ngoài lịch: CG6 (K138), CG4 (K132 luồng 2). CG2 còn chưa đăng (ảnh `anh-dang-bai\CG02`).
- n8n: đã cài cơ chế kiểm tồn kho content (commit 1ba05ef, L1-02/04/06), lịch 18/11 (21:30) là lần đầu áp dụng → kiểm cột J dòng đầu ngày 18/11 có "kho Đầy/Vừa/Ít".
- Người dùng cho Claude tự điều phối n8n + Copilot (memory `feedback-dieu-phoi-n8n-copilot`).

## 2026-11-17 — luồng 2 (SM02, SM04; xong 12:14)
- Done: 197 tương tác, 198 kết bạn (Một phần: STT 4 đã gửi; STT 3 Katherine Connors không có nút), 199 lướt, 201 tương tác group 3, 203 chấp nhận (0), 210 tường **K131** (CG23), 212 tường **K132** (thay CG24 lỗi gói bằng CG4, ảnh `anh-dang-bai\CG04`), 214 tim story. K131, K132 đã đăng ký Radar.
- **SM02 lại bị "confirm your identity"** khi mở composer group (196, K130 → group 2) và khi Join group 10 (211) → Không làm được; Radar health `h-20261117-SM02-identity`. Tường + like/lướt/story/kết bạn vẫn được. SM02 **không đăng group, không join** cho tới khi người dùng xác minh trên điện thoại.
- Content: CG2 vẫn chưa đăng (ảnh `anh-dang-bai\CG02`); CG4 đã dùng (K132).
- SM04: 207, 208, 209, 215, 217 ghi Bỏ qua (không có trình duyệt trên máy ADMIN).
- Group 10, 12, 15 SM02 chưa join.

## 2026-11-16 (bàn giao cấp 3 → xem `ops/BAN-GIAO-CAP-3.md`)
- n8n 2.35.7 chạy ở máy này, tự mở khi đăng nhập (Task Scheduler "Smock n8n"). Bật L1-01…L1-07; Lead Hunter tắt (thiếu key).
- **L1-02 đã bật → không tự lên lịch nữa.** Lịch 17/11 (dòng 193–234, 42 việc, 2 luồng) do n8n sinh. Log qua webhook (`ghi-log-webhook.ps1`), đã thử OK (dòng thử ở cuối Nhật Ký SM cần xoá).
- Cầu nối cấp 2 chạy trọn lần đầu: 6 caption phái sinh CG1/CG2 vào Pool Content SM dòng 2–7, người dùng đã duyệt (PC1–PC6).
- Mã bài kế tiếp do n8n tự tính từ Lịch SM (17/11 dùng K123–K138). Content KE đã xếp đến CG30.
- Tồn đọng: Add Friend STT 1–15 đánh dấu đã gửi; SM02 "hạn chế group"?; SM04 không có trình duyệt máy này.
- L1-03 đã gói 10/16 bài ngày 17/11 (48 ảnh). Thiếu ảnh: K126, K127, K130, K132, K137, K138.
- **Dừng tối 16/11, tắt máy.** Sáng 17/11 đọc mục 0 của `ops/BAN-GIAO-CAP-3.md` trước khi chạy lịch.

## 2026-11-11
Toàn bộ việc dở 10/11 (gồm SM02 — người dùng xác nhận SM02 **không** bị checkpoint/shadowban) đã dồn sang Lịch SM dòng **140–162**, 09:25–14:45; CG2 đổi sang group 2 (group 21 cấm quảng cáo). Dòng 110–139 ngày 10/11 còn "Chờ" là bản cũ, bỏ qua.
- 09:12–10:00 chạy dồn: Done 140–142, 144–150, 152–154, 156, 158. Bài: K117 (SM01 group 1 CG1), K118 (SM01 tường CG8), K119 (SM03 tường CG12 — folder ảnh LILY 2 bị từ chối truy cập).
- **SM02: đăng bài group vẫn bị "confirm your identity"** (Account Status vẫn looks good; like/lướt được) → đã ghi health lên Smock Radar; dừng đăng/join/kết bạn SM02. Còn Chờ: 143, 151, 157, 159, 160, 161.
- Còn hẹn giờ: 10:40 SM03 CG6 → group 27 (dòng 155); 11:47 SM01 CG4 → group 5 thay 16 (dòng 162; group 16 cat resale).
- SM02 đăng tường được (chỉ group bị chặn): K120 (CG9, dòng 151), K121 (CG10, dòng 159). SM02 ngâm — chỉ đăng tường + tương tác, chưa vào group. Còn Chờ SM02: 143, 157, 160, 161.
- Nhật Ký SM dòng trống kế tiếp: **118**. Mã Radar kế tiếp: **K122**.
- **10:30 lọc group trên Smock Radar**: chấm 30 group (tier A: 1, 2, 25, 43, 5; B: 10, 20, 32, 49, 27, 17, 50, 54, 15, 29, 30, 53, 12; còn lại Loại), đã ghi Tier/Điểm vào Join Group SM cột G–H. Engage/buyer đang ước lượng.
- Lịch mới dòng 163–175 (join group A/B + tim story + lướt + tương tác group mới, chưa đăng bài vào group mới). Đã làm (Excel đã ghi; **Nhật Ký SM + cột H chưa dán**, hàng đợi ở `tools\hang-doi-log.tsv` → chạy `tools\dan-log.ps1` rồi dán từ A118): 163 SM03 tim story, 164 SM01 join 25+10, 166 SM01 tim story, 172 SM01 tương tác group 25, 169 SM01 lướt (~2 phút, chưa đủ 4).
- 14:05: đã dán log tới Nhật Ký SM dòng 122 (kế tiếp **123**), H163–175 cập nhật, Join Group SM D11/D26 = đã join. Hàng đợi trống. Hẹn giờ 155 (SM03 CG6→g27) và 162 (SM01 CG4→g5) trễ >30 phút, chưa làm.
- Còn lại: 155, 162, 165 SM02 join 43/20/32, 167 SM02 tim story, 168 SM03 join 5, 170 SM03 lướt, 171 SM02 group 43, 173 SM03 group 5, 174–175 chấp nhận All; lọc list bạn bè (chân dung chủ boutique/smock) → Add Friend. Join Group SM chưa cập nhật SM01 cột D cho group 25, 10.

Cập nhật mỗi khi dừng ca. Ngày mới "lên lịch hôm nay" thì **ưu tiên dồn các việc chưa làm dưới đây** trước.

## 2026-11-10 (dừng 17:5x — hết giờ hành chính, người dùng bảo tạm dừng)

**Đã xong (H = Done):** dòng Lịch SM 107–109 (tim story SM03/SM02/SM01), 111 (SM01 lướt), 113 (SM03 lướt), 114–115 (chấp nhận All SM01/SM03: 0 lời mời), 117 (SM03 đăng group CG3 → group 11 Used Clothing Direct Supplier Worldwide), 118 (SM01 đăng tường CG7), 119 (SM03 đăng tường **LILY 1** thay CG11).

**Chưa làm (H còn "Chờ") — dồn sang ngày sau:**
- SM01: tương tác newsfeed (123), đăng group CG1 → group 1 (124), join 6, 8 (125), đăng tường thứ 2 (130, CG8 hoặc bài GRACIE), tương tác group 7 (132), kết bạn #16 (137), đăng group CG4 → group 16 (138).
- SM03: tương tác newsfeed (121), join 1, 2 (127), đăng tường thứ 2 (128, nên dùng LILY 2), đăng group CG6 → group 27 (131), tương tác group 29 (134), kết bạn #19 (135).
- **SM02: dừng cả ngày** — FB yêu cầu "confirm your identity" trên điện thoại (certain actions restricted). Người dùng cần xác minh trước khi chạy lại SM02. Dòng 110, 112, 116, 120, 122, 126, 129, 133, 136, 139 chưa làm.

**Content đã dùng:** CG3, CG7, LILY 1 (CG2 chưa đăng được — còn dùng được). Nhật Ký SM dòng trống kế tiếp: **100**. Ảnh đã tải: `anh-dang-bai\CG02`, `CG03`, `CG07`, `LILY01`.

**Ghi nhớ:**
- Group STT 21/44 "Vintage Kids Clothing & More" cấm quảng cáo → không đăng. STT 2 "SMOCKED DRESS AND ROMPER" ghi Wholesale & Retail → hợp. STT 11 không có nội quy → đã đăng.
- Tab persona (GRACIE/CATHIE/LILY/EMILY) **có caption** — gviz CSV làm rơi dữ liệu, phải xem trực tiếp trên sheet.
- Kết bạn: #1–15 đã gửi (26/10); kế tiếp #16.
