# Project Workflow

## Model Roles
| Model | Use For |
|---|---|
| **Claude Code** | Orchestrator: planning, writing, refactoring, docs, CLAUDE.md management |
| **Codex** | Async reviewer and rescue agent: bug fixes, targeted review, background tasks |
| **Gemini** | Large-context specialist: full-repo reads, multimodal, context-heavy investigation |

---

## Plan Mode
Always plan before acting on non-trivial tasks.
Default plan model: `claude-opus-4-5` — set with `/model plan claude-opus-4-5`
Toggle: `Shift+Tab` or `/plan`

| Use Opus | Use Gemini |
|---|---|
| Architecture, design tradeoffs, ambiguous scoping | Context exceeds Claude's window, full-repo or multi-file planning |

---

## Codex
Default: `gpt-5.4-mini` at medium reasoning effort. Override per-command only.

| Model | When |
|---|---|
| `gpt-5.4-mini` | Default, most review and rescue work |
| `gpt-5.5` | Complex tasks when quota allows |
| `gpt-5.4` | Skip — 5.5 is strictly better |

| Scenario | Command |
|---|---|
| Feature/fix complete | `/codex:review --background` |
| Pre-merge | `/codex:adversarial-review --base main` |
| Targeted bug fix | `/codex:rescue --model gpt-5.4-mini --effort medium <task>` |
| Retrieve results | `/codex:status` → `/codex:result` |

**Skip Codex when:** multi-file reasoning, interactive planning, CLAUDE.md awareness needed, large-context reads, or quota is low (`/status` to check).

---

## Gemini
Plugin: `sakibsadmanshajib/gemini-plugin-cc` via Gemini CLI (Google AI Pro)
Default: `pro` (Gemini 2.5 Pro, 1M context). Override per-command only.

| Alias | Use |
|---|---|
| `pro` | Default, full reasoning |
| `flash` | Speed over depth |
| `flash-lite` | Quick one-off lookups |

Thinking budget: `--thinking low` (simple) / `--thinking high` (deep analysis)

**Use Gemini when:** repo/file tree exceeds Claude's window, multimodal analysis, large-codebase investigation, second opinion without burning Codex quota.
**Skip Gemini when:** session memory or CLAUDE.md awareness needed, structured async review Codex already handles.

---

## Default Review Loop
1. Plan with Opus (or Gemini if context demands)
2. Write or fix the code
3. Offer `/codex:review --background` when a chunk is complete
4. Surface and integrate result when it finishes

Do not enable review gates on Codex or Gemini — creates long loops and drains quota.

---

## Code Style
Follow environment best practices defined in the project CLAUDE.md.
