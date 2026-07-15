# Project Workflow

## Model Roles
| Model | Role |
|---|---|
| **Claude Code** | Orchestrator: planning, writing, refactoring, docs, CLAUDE.md management |
| **Codex** (`!codex`) | Adversarial reviewer: bug hunting, targeted review, second-opinion diagnosis |
| **Gemini** (`!gemini`) | Large-context specialist: full-repo reads, multimodal, context-heavy investigation |
| **Qwen3-Coder** (`!qwen-exec`) | Local executor: implements approved plans, bulk edits, codegen — free, private, offline |

Codex, Gemini, and Qwen3-Coder run as native CLIs through bash mode (`!codex …`, `!gemini …`, `!qwen-exec …`).
No plugins, skills, or slash-commands.

---

## Plan Mode
Always plan before acting on non-trivial tasks. Toggle with `Shift+Tab` or `/plan`.

| Plan with Opus | Plan with Gemini |
|---|---|
| Architecture, design tradeoffs, ambiguous scoping | Context exceeds Claude's window; full-repo or multi-file planning |

---

## Codex — adversarial review (`!codex`)
Run headless via bash mode against the working tree / diff.

| Scenario | Command |
|---|---|
| Review current changes | `!codex review` |
| Diagnosis / fix proposal | `!codex exec "<task>"` |
| One-off review of a diff | `!codex exec "review the diff against main and report bugs"` |
| Pick model | add `-m <model>` (default `gpt-5.4-mini`, medium effort) |

**Use Codex when:** a chunk is complete and you want an adversarial bug pass, or a focused second opinion.
**Skip Codex when:** interactive planning, CLAUDE.md / session-memory awareness needed, or quota is low.

---

## Gemini — large-context analysis (`!gemini`)
Run non-interactive via bash mode.

| Scenario | Command |
|---|---|
| Headless analysis | `!gemini -p "<prompt>"` |
| Read-only investigation | `!gemini -p "<prompt>" --approval-mode plan` |
| Pick model | add `-m <model>` (default `gemini-2.5-pro`, 1M context) |
| Add context dirs | `--include-directories <dirs>` |

**Use Gemini when:** the repo/file tree exceeds Claude's window, multimodal analysis, or a second opinion without spending Codex quota.
**Skip Gemini when:** session-memory or CLAUDE.md awareness is needed.

---

## Qwen3-Coder — local executor (`!qwen-exec`)
Runs Qwen3-Coder via LM Studio (OpenAI-compatible endpoint on `localhost:1234`).
`!qwen-exec` is a wrapper at `~/.local/bin/qwen-exec` that sets the endpoint/model env
and calls the `qwen` CLI (Qwen Code, a Gemini-CLI fork).

| Scenario | Command |
|---|---|
| Headless task (read-only) | `!qwen-exec -p "<task>"` |
| Auto-apply edits | `!qwen-exec -y -p "<scoped task + acceptance criteria>"` (run in the repo dir) |
| Prereqs | LM Studio server running (`lms server start`) + model loaded with ≥32k context |

**Use Qwen when:** an approved plan needs implementing, bulk/mechanical edits, or codegen you
want done locally (free/private/offline). Keep handoffs small and well-specified.
**Skip Qwen when:** the task needs strong reasoning, broad judgment, or CLAUDE.md/session-memory
awareness — Opus owns planning, review, and final correctness.

---

## Default Review Loop
1. Plan with Opus (or Gemini if context demands).
2. Execute: write the code directly, or hand the approved plan to the local executor —
   `!qwen-exec -y -p "<scoped task>"` in the repo dir — then review/integrate its output.
3. When a chunk is complete, run `!codex review` for an adversarial pass.
4. Surface and integrate the findings.

Reviews are on-demand — no automatic review gates.

---

## Second Brain — claude-obsidian Vault

A persistent claude-obsidian "Compound Vault" second brain lives at
`~/.claude/vault/` (owner: Levi). Harness it every session — cheaply.

### Which vault (repo-local wins)
At session start, check the repo root for a local vault in this order:
`./vault/wiki/hot.md` → `./wiki/hot.md` → `./.vault-meta/`.
- Found → that repo-local vault is **primary**; `~/.claude/vault` is the fallback for
  cross-cutting personal context.
- None → use `~/.claude/vault`.

### Warm-up (start of session, silent)
Read **only** `<vault>/wiki/hot.md` (~500 words). That's the whole warm-up — do not
announce it, do not read more yet. If `hot.md` is missing, skip silently.

### Drill deeper — only on demand
When the task actually needs personal/project context you don't already have, escalate
one tier at a time and stop as soon as you have enough:
1. `wiki/hot.md`  → 2. `wiki/index.md`  → 3. the relevant `wiki/<domain>/` page(s).
**Never read the whole vault** (it exceeds a single context window past ~100k tokens /
~200 files). Do **not** consult the vault for general coding questions or anything the
current repo already answers.

### Trust but verify
Vault pages are *claims*, not ground truth — some carry `[!contradiction]` callouts or
may be stale. Prefer live code/files over the wiki when they disagree, and flag the
conflict rather than silently following the wiki.

### Write-back — explicit only
- Mutate the vault only on `/save`, an ingest, or a direct request. General sessions are
  read-only toward the vault.
- At session end, if something worth remembering happened, refresh `<vault>/wiki/hot.md`
  (overwrite, keep <500 words) and append (never edit) a top entry to `wiki/log.md`.
- **Never auto-file** owner-excluded topics — health, finance, cannabis, personal/community.
  Capture those only if Levi explicitly asks.
- Respect vault mechanics: `.raw/` is immutable, `log.md` is append-only (newest on top),
  and honor the plugin's advisory locks / `/wiki` skills for real writes.

---

## Code Style
Follow environment best practices defined in the project CLAUDE.md.
