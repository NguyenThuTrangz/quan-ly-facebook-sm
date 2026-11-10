---
name: facebook-posting-preferences
description: "How the user wants Facebook posts/messages handled (audience, confirmation, language)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 28cb4341-5419-40a6-af82-2a8d5f546dff
  modified: 2026-10-14T04:34:08.141Z
---

User (Vietnamese speaker; reply in Vietnamese) asks Claude to view stories, message friends and post on Facebook via the browser extension.

- Before clicking Post, report the account and the audience and let the user choose. On 2026-10-14 the user picked Public, then Friends once Public turned out to need the profile unlocked.
- Never untick or tick "Set as default audience", and never unlock the profile, without explicit consent.
- When several contacts share a name (e.g. "Vũ Vui Vẻ"), pick the one with existing chat history and tell the user which one.

**Why:** posts go out under the user's real accounts; the wrong account or audience is hard to undo.
**How to apply:** confirm account + audience before any post or group post; ask before admin-approval or anonymous options.

Related: [[browser-accounts]]
