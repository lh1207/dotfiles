---
name: save-prompt-cache
description: Warm-context persistence gate for /goal completion (and the session-Stop fallback). Invoke before declaring a /goal's completion condition met — delegate the Save-vs-Skip decision and vault writes to claude-obsidian:save, then record a receipt. Not a per-turn save; not a substitute for the completion gate.
---

# Save Prompt Cache

The prompt-cache persistence harness. This skill is the **gate and receipt owner**; it is separate
from Obsidian, which is only the transport. Run it while the entire goal remains in active context.

1. Invoke the `claude-obsidian:save` skill with the completed goal's requirements, decisions,
   evidence, deliverables, and final outcome still in context. Let its Save-vs-Skip criteria decide
   whether durable material exists; a deliberate skip (trivial or duplicate goal) is a valid
   persisted outcome. Auto-generate a short descriptive title — do NOT interrupt goal completion to
   ask for one.
2. After the save (or skip) completes, record a receipt with `scripts/record-save.py`:
   - saved: `python3 scripts/record-save.py --outcome saved --title "<title>" --note "<absolute-note-path>"`
   - skipped: `python3 scripts/record-save.py --outcome skipped --title "<short-reason>"`
3. Only after the receipt path exists may you declare the `/goal`'s completion condition met (or, for
   the session-Stop trigger, end the turn).

Do not run this on every turn. Do not substitute local memories or a detached summary process: those
do not guarantee that the active goal context is persisted through the Obsidian workflow. If vault
persistence needs permission, request it; if it cannot run, report the goal incomplete rather than
silently bypassing the gate.
