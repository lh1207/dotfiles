#!/usr/bin/env bash
# save-at-session-end.sh — claude-obsidian auto-save harness (Stop hook)
#
# Requests the local `obsidian-save` skill once per substantive session as a
# fallback for knowledge persistence. Provider prompt caching is independent;
# this hook neither enables caching nor proves a cache hit. Guards prevent
# repeated fallback prompts and recursion.
#
# Contract (from code.claude.com/docs/en/hooks):
#   - stdin  = Stop event JSON (session_id, stop_hook_active, transcript_path, ...)
#   - to force Claude to act, emit {"decision":"block","reason":"..."} on stdout
#   - plain stdout is debug-log-only for Stop, so JSON is required
#   - hooks cannot call skills directly; the injected `reason` makes Claude do it
#
# Guards:
#   - per-session sentinel file  -> fires at most once per session (loop + spam)
#   - sentinel written BEFORE the block -> the forced turn's next Stop passes through
#   - activity gate (>=2 user turns OR any tool use) -> skips throwaway chats
#   - kill switch + stale-sentinel prune
#
# Fail-open: any error exits 0 so the session is never broken.

INPUT="$(cat)"
SENT_DIR="${CLAUDE_VAULT_SAVE_STATE_DIR:-$HOME/.claude/.save-harness}"
mkdir -p "$SENT_DIR" 2>/dev/null || true

# Kill switch: `touch ~/.claude/.save-harness/disabled` to turn the harness off.
[ -f "$SENT_DIR/disabled" ] && exit 0

# Prune stale sentinels (>1 day). session_ids are unique, so no collisions.
find "$SENT_DIR" -name '*.done' -mtime +1 -delete 2>/dev/null || true

# Parse payload + decide. Prints "FIRE::<session_id>" or "SKIP::<session_id>".
RESULT="$(SAVE_HOOK_INPUT="$INPUT" python3 -c '
import os, json, sys
raw = os.environ.get("SAVE_HOOK_INPUT", "")
try:
    data = json.loads(raw)
except Exception:
    print("SKIP::"); sys.exit(0)

sid = str(data.get("session_id", "")).strip()

# A true flag means this turn is already continuing after a Stop hook.
if data.get("stop_hook_active", False) is True:
    print("SKIP::" + sid); sys.exit(0)

tpath = data.get("transcript_path", "") or ""
user_turns = 0
tool_used = False
try:
    with open(tpath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            t = e.get("type")
            msg = e.get("message", {})
            content = msg.get("content") if isinstance(msg, dict) else None
            if t == "user":
                # Count only real user prompts, not tool_result-only turns.
                if isinstance(content, str) and content.strip():
                    user_turns += 1
                elif isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text" and str(c.get("text", "")).strip():
                            user_turns += 1
                            break
            elif t == "assistant" and isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        tool_used = True
                        break
except Exception:
    # Transcript missing/unreadable (async lag): be lenient and fire.
    print("FIRE::" + sid); sys.exit(0)

if user_turns >= 2 or tool_used:
    print("FIRE::" + sid)
else:
    print("SKIP::" + sid)
' 2>/dev/null)"

# Fail-open: if python produced nothing, do not block.
[ -z "$RESULT" ] && exit 0

MODE="${RESULT%%::*}"
SID="${RESULT#*::}"
[ "$MODE" = "FIRE" ] || exit 0

# Sanitize session id for use as a filename; fall back to a fixed name.
SID_SAFE="$(printf '%s' "$SID" | tr -cd 'A-Za-z0-9._-')"
[ -n "$SID_SAFE" ] || SID_SAFE="nosid"
SENT="$SENT_DIR/${SID_SAFE}.done"

# Already fired this session -> allow the turn to end.
[ -f "$SENT" ] && exit 0

# Consume the one shot BEFORE blocking so the forced turn's next Stop passes through.
: > "$SENT"

REASON='Evaluate durable knowledge from this session using the local obsidian-save skill and /Users/levi/Documents/Development/global-vault/VAULT-WORKFLOW.md. Keep repository-specific knowledge in its repo vault when present; save personal and cross-project knowledge to the global vault. Use global as fallback if no repo vault exists; explicit user destinations win. Update the owner note, index, log, and hot note for a save; record a saved-or-skipped receipt in the selected vault. Skip already-saved material and owner-excluded topics unless explicitly requested. This fallback runs once per session; do not repeat it.'

# Emit the block decision as JSON (reason contains no double quotes/backslashes).
printf '{"decision":"block","reason":"%s"}\n' "$REASON"
exit 0
