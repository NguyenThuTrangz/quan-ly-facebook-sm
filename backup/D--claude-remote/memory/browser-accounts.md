---
name: browser-accounts
description: "Which browser/profile holds which Facebook account, and how to connect Claude in Chrome to each"
metadata:
  node_type: memory
  type: reference
  originSessionId: 28cb4341-5419-40a6-af82-2a8d5f546dff
  modified: 2026-10-14T04:34:04.486Z
---

- **Chrome, `Profile 1`** = profile "Nguyễn Thái" (Facebook account Nguyễn Thái). Shortcut `D:\claude remote\Thái (Nguyễn Thái) - Chrome.lnk`. Launch: `chrome.exe --profile-directory="Profile 1" <url>` (chrome.exe in `C:\Program Files (x86)\Google\Chrome\Application\`).
- **Edge** (Claude extension installed) = Facebook account **Nguyễn Thu Trang**. Profile is *locked*, so posts can't be Public; default audience is "Only show to…" (Lê Huyền Linh, Nguyễn Thái). Another Edge window/profile had account "Luxe", stuck on a Facebook checkpoint (as of 2026-10-14).
- The Claude in Chrome extension connects to only one browser at a time; on 2026-10-14 it was connected to Edge, not Chrome. Before acting, always check which Facebook account is logged in and tell the user.
- If the extension says "not connected": user runs `/chrome` in Claude Code, clicks Connect in the extension, or restarts the browser. Too many open windows caused a disconnect once.

Related: [[facebook-posting-preferences]]
