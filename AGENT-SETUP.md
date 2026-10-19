# Shared agent setup

## Source and discovery

Edit only `codex/.codex/INSTRUCTIONS.md` for cross-agent behavior. Locally it is
linked as `~/.codex/INSTRUCTIONS.md`. Keep project commands and constraints in
each project's own instruction file; do not replace those with global defaults.

| Client | Native global entry point | Connection |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` | Symlink to `INSTRUCTIONS.md`; native discovery loads its contents. |
| Claude Code | `~/.claude/CLAUDE.md` | One-line native import: `@~/.codex/INSTRUCTIONS.md`. |
| Gemini CLI | `~/.gemini/GEMINI.md` | Symlink to the canonical file; no import syntax required. |
| Qwen Code | `~/.qwen/QWEN.md` | Symlink to the canonical file; no import syntax required. |
| Antigravity | `~/.gemini/GEMINI.md` | Uses the same global entry point as Gemini. |
| Cursor | Settings → Rules → User Rules | Global pointer tells Agent to read the canonical file once; requires UI setup below. |
| Roo Code | `~/.roo/rules/00-shared.md` | Symlink directly to the canonical file; native global rule loading reads its contents. |

The repository's `AGENTS.md` points to the checkout-relative canonical file, so
dotfiles maintenance in cloud does not require this Mac's home configuration.
Other cloud repositories need their own supported distribution of personal
instructions; a local symlink cannot configure a remote service. A future agent
needs a supported native adapter, not another copy of the shared workflow.

Use `python3 agent-links.py` to preview, `--apply` to install, and `--check` to
validate filesystem links. Cursor User Rules require separate UI setup; the
installer cannot validate them. Home Cursor `.mdc` links are retained as templates,
not asserted to load globally. The installer touches the other table entry points,
the canonical home link, and the existing Cursor templates. It backs up replaced files and
symlinks under `~/.local/state/agent-instructions/backups/` with a manifest; symlink
targets such as personal vaults are never overwritten. Original repository files
were separately backed up outside Git before this migration. To reverse a home
installation, review that manifest, restore saved entries, and remove only newly
created links after checking for subsequent edits. Revert repository changes
separately. Do not commit backups or live client state.

GNU Stow packages use native directory layouts, including `.cursor/rules/`.
Claude's tracked lowercase `claude.md` is preserved to avoid a case-only Git rename
on macOS; the installer links the native uppercase `~/.claude/CLAUDE.md` to that
one-line import source. Run the installer after raw Stow on case-sensitive Linux;
Stow alone installs the lowercase source. `bootstrap.sh` now runs the installer
after Stow to create the native uppercase entry point. Existing homes can have conflicts;
prefer the targeted installer over `bootstrap.sh`. Do not use Stow `--adopt` to
resolve conflicts automatically. Nondefault `CODEX_HOME` and clients configured
with alternative context filenames need deliberate native configuration; this
installer targets the default locations inspected on this Mac.

## Preserved settings and practical changes

- Codex already uses Sol/Medium with Standard service, plus light/deep profiles.
  Runtime configuration, custom agents, permissions, and MCP settings are preserved.
- Claude keeps Opus, plan-mode permissions, plugins, notifications, and status line.
  Only the automatic vault-save Stop hook is removed. Its script remains dormant;
  do not re-enable it as a quota optimization. Its old cache-savings claims and
  Stop-event logic have not been validated. Requested saves use installed skills.
- Cursor keeps a scoped Obsidian project-rule template for authorized wiki work, without mandatory
  session-start reads, session-end writes, or model routing. Check project-specific
  review-monitor instructions before duplicating an existing review.
- Gemini's former global instruction symlink pointed into the personal global
  vault. Replacing that link preserves the vault's instruction file itself. The
  review removed only the personal vault from local `context.includeDirectories`,
  preventing its instructions from loading globally as additional workspace
  context. Include the vault explicitly for relevant work. This local setting is
  not distributed by Stow; inspect additional context directories on each device.
- Local `qwen-exec` retains the localhost endpoint and existing model default,
  honors an explicit `OPENAI_MODEL`, and reports a missing CLI clearly. It does
  not start LM Studio or load a model; those claims in the old Cursor rule were
  incorrect. Its `lm-studio` API-key placeholder is not a secret.
- Zsh guards optional framework/tool paths, uses `$HOME` for user paths, and
  deduplicates PATH entries. Existing plugins, aliases, and preferences remain.
- Bootstrap uses explicit packages. New docs/tool directories cannot become
  accidental home installations. `--no-folding` keeps real home directories so
  client runtime state cannot enter the checkout through a directory symlink.
  New agent packages also ignore unreviewed runtime files in Git.
  `local/bin` still stows to `~/bin`; the existing
  Mac `~/.local/bin/qwen-exec` link is separate and preserved.

## Subscription-aware operation

Use one agent by default and keep context relevant. Choose model and effort in
the active client's supported controls; a prompt does not switch models. Existing
Codex CLI options: `codex` for general work, `codex --profile light` for narrow
work, and `codex --profile deep` when deeper diagnosis is justified. Those profiles
are local configuration and are not installed by this repository.

Standard service remains selected. Fast mode consumes subscription allowance at
a higher rate; see [official speed guidance](https://learn.chatgpt.com/docs/agent-configuration/speed).
Do not launch second-agent reviews or force vault saves on routine completion.
Shorter instructions reduce recurring context, but no quota increase or measured
task-throughput gain is claimed. Claude, Gemini, and other providers have their
own billing; ChatGPT Plus is not assumed to cover them.

## Verification and limits

`bash cloud-verify.sh` checks shell syntax, tracked and new nonignored JSON,
Python syntax, Stow simulation, and disposable Stow installation plus home-link install/check/reinstall.
`python3 agent-links.py --check` checks real home links without running clients.
Neither proves prompt adherence, model access, hooks, MCP health, or live UI behavior.
Restart sessions to load revised instructions; inspect the client's context/rules
view (Claude `/context`, Gemini `/memory show`, Qwen `/memory`) to confirm loading.
Cursor pointer reads depend on the agent following the User Rule
and having access to the file; do not widen permissions merely to force a read.

Inspected configuration boundaries: Codex maintained files only; Claude tracked
settings/hooks; Gemini context settings; Qwen's documented global memory entry;
Cursor native rules and settings format; Roo installed extension, empty custom modes, and empty MCP settings. Antigravity's MCP config was empty. No credentials, transcripts,
runtime memories, personal hot notes, or plugin caches were read. Cursor's settings
use JSON with comments and remain untouched. Desktop-dependent MCP servers and the
legacy Codex local-provider profile remain unchanged and require separate runtime
verification. Cagent has initialization state but no discovered maintained agent
configuration; no adapter is invented for it.

Native discovery references checked 2026-10-18:

- [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude memory/imports](https://code.claude.com/docs/en/memory)
- [Gemini context files](https://geminicli.com/docs/cli/gemini-md/)
- [Qwen memory](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/)
- [Cursor user rules](https://cursor.com/docs/rules)
- [Roo global rules](https://roocodeinc.github.io/Roo-Code/features/custom-instructions/)
- [Antigravity rules](https://www.antigravity.google/docs/rules/)

## Cursor global setup

Cursor documents `.cursor/rules` as project rules, not a global home-directory
loader. In Cursor Settings → Rules (Customize → Rules in newer clients), add this
User Rule, keeping any unrelated user preferences:

```text
Before working, read ~/.codex/INSTRUCTIONS.md unless already loaded this session.
Resolve ~ to the current user's home directory on this operating system.
If the file is unavailable, report that before proceeding; do not invent its contents.
```

This is a pointer, not a second workflow source. Verify it in the User Rules UI
and verify the read in a new Agent session. The installer output explicitly says
that link checks cannot establish Cursor global loading. Cursor Tab and Inline
Edit do not use User Rules. A cloud agent cannot read this workstation's file;
use a checkout-relative adapter such as this repository's `AGENTS.md` there.

## Platform support

- macOS/Linux/WSL: Python 3 installer plus filesystem symlinks. Stow is optional
  for instruction-only installation. The bootstrap/verifier additionally require
  Bash, Zsh, Git and Stow. WSL installs configure WSL clients, not Windows clients.
- Native Windows: use Python (`py -3 agent-links.py --apply`, then `--check`) in
  a checkout whose Git symlinks are materialized (`core.symlinks=true` with the
  required Windows symlink privileges). The installer prepares all symlinks
  before replacing existing files and reports privilege failures without removing
  them. Developer Mode or appropriate OS privileges may be required. Do not
  replace symlinks with workflow copies. Separate drives use absolute targets.
  Set the Cursor User Rule on that client as well. Bash/Stow bootstrap is Unix-only.
- Nondefault client homes/context filenames and remote/container clients require
  their native paths to be configured deliberately; local links do not propagate
  to another machine or a hosted service. Cowork can skip Claude's home symlinks
  and imports outside its workspace; this setup targets Claude Code.

## Two-pass review, 2026-10-18

Pass 1 checked native discovery against vendor documentation and the local entry
points. Findings: unsupported claim of Cursor home rules being global; extra
Gemini vault context; bootstrap missing Claude's uppercase entry on Linux; and
unlink-before-create risking loss on symlink creation failure. Fixes: explicit
Cursor User Rule setup, opt-in vault inclusion, bootstrap installer invocation,
and prepare-all-links then atomic per-file replacement. Roo now directly links
its native global rule to the canonical file.

Pass 2 checks the resulting diff and disposable regressions: native entry points,
paths containing spaces, repeat-install idempotence, external symlink backup and
target preservation, simulated missing symlink privileges, and refusal to write
through symlinked client directories. No paid model calls or personal shell
startup files are needed. macOS checks are local; Linux/Windows execution and
fresh-session prompt loading must be reported separately, not inferred from
filesystem checks.

Local review evidence: Cursor’s native Customize → Rules view displayed the new
shared-file pointer under User Rules (count 1). No model conversation was sent.
Fresh-session adherence remains untested. Docker was unavailable, so Linux and
Windows execution was not claimed. Home-link and disposable regression checks
passed: `bash cloud-verify.sh`, all four installer regression tests,
`python3 agent-links.py --check`, and `git diff --check`. The cloud publication
handoff was also corrected to include the canonical source and installer/test
dependencies. Review backups are under `~/.codex/backups/shared-agent-review-20261018T222426Z/`;
Roo home-link backups are under `~/.local/state/agent-instructions/backups/20261018T222444Z-wcwenlkj/`.
