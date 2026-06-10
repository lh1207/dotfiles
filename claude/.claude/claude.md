# Project Workflow

## Model Roles
| Model | Role |
|---|---|
| **Claude Code** | Orchestrator: planning, writing, refactoring, docs, CLAUDE.md management |
| **Codex** (`!codex`) | Adversarial reviewer: bug hunting, targeted review, second-opinion diagnosis |
| **Gemini** (`!gemini`) | Large-context specialist: full-repo reads, multimodal, context-heavy investigation |

Codex and Gemini run as native CLIs through bash mode (`!codex …`, `!gemini …`).
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

## Default Review Loop
1. Plan with Opus (or Gemini if context demands).
2. Write or fix the code.
3. When a chunk is complete, run `!codex review` for an adversarial pass.
4. Surface and integrate the findings.

Reviews are on-demand — no automatic review gates.

---

## Code Style
Follow environment best practices defined in the project CLAUDE.md.
