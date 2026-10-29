# Codex Cloud dotfiles pilot

Reviewed 2026-10-19. The original cloud pilot did not change or copy ~/.codex.
Subsequent local instruction consolidation is documented in AGENT-SETUP.md;
its canonical source now travels in this checkout. No secrets are required for
this pilot. Cloud setup remains separate from local home-link installation.

## Pilot: lh1207/dotfiles

The shared-instruction preparation was merged into `main` through
[PR #9](https://github.com/lh1207/dotfiles/pull/9), at
`eb39ccf390bb5ec9d996de6768cfdf76cf238a3c`. Use an up-to-date `main`
checkout containing the verifier and installer. Recheck remote status before
setup; cloud checkouts cannot see uncommitted Mac files.

The pilot is static configuration maintenance, not a full desktop installation.
There is no application build, dependency manifest or lockfile. The existing
Python regression suite tests the instruction-link installer. GNU Stow is the
configuration deployment tool. The added verifier provides
shell parsing, tracked and new nonignored JSON parsing, Python syntax,
disposable installer regressions, and Stow layout simulation. It does not prove
shell startup, hooks, clients, hardware, or external services work.

Required tools: Bash, POSIX sh, Zsh, Python 3 (standard library), Git, GNU Stow.
Use the Linux image's distro tools; this repository currently pins no versions.
Record tested versions in the environment setup report before publishing. No
Node package install, Homebrew, GUI apps, model downloads, or credentials needed.
Optional tmux plugin use requires the public TPM submodule in `.gitmodules`;
static checks do not require downloading it. Initialize only for tmux work with
`git submodule update --init --recursive`, allowing GitHub network access.

## Install and verify

In the environment setup conversation, ask Codex to work from the dotfiles root,
install the required distro packages if missing, and record this tested install
script for an Ubuntu/Debian image (sudo may be needed for a non-root image):

```bash
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  bash dash zsh python3 git stow
bash cloud-verify.sh
```

`dash` supplies the POSIX shell on Debian/Ubuntu; verify `sh` is available.
The apt commands are a proposed setup, not tested on this Mac; use sudo for
both apt-get commands if required and available. Use equivalent packages if
the environment is not Debian/Ubuntu.

Start skill: work in the dotfiles checkout, run `bash cloud-verify.sh`, report
missing tools or failures, and do not run bootstrap.sh or load shell startup files.
There are no application services to start. Restrict network access to the
Package managers preset for installation; disable it afterward for ordinary
static tasks. No environment variables, network secrets, SSH keys, GitHub PAT,
OpenAI API key, or personal vault are required. Connect GitHub through the product.

Do not run bootstrap.sh for setup. It installs into the actual home using an explicit
package list (updated during instruction consolidation). The instruction-link
installer must also not target the real home during cloud setup. New directories
are not automatically packages. Stow simulation uses an empty temporary directory and an explicit
package list; it cannot detect conflicts with an existing user's home. Stow gets
a disposable HOME so personal `.stowrc` options cannot affect verification.
Zsh parsing disables user startup files; shell files are parsed, never sourced.

## What transfers from Codex home

- `AGENTS.md`: outcome-first work, scoped search, preserving user changes/secrets,
  focused checks, one-agent preference, and concise handoffs belong in repository
  instructions. The pilot preserves these. Runtime choices remain client choices.
- `agents/{sol,luna,terra}.toml` and light/deep profiles: reusable role guidance can
  be rewritten as prompts or skills. Local model profiles are not automatically
  installed into cloud tasks; choose an available model/effort in the client.
- `skills/playwright`: potentially reusable with its license/notices, a relative
  wrapper path, Node/npm, Linux browser dependencies, and a fresh browser context.
  Do not copy Mac browser state or cookies. Pin and test dependencies before use.
- `skills/obsidian-save`: its knowledge rules are reusable, but the absolute
  personal vault and recorder path are local dependencies. Adapt to an authorized
  repository-local documentation destination before cloud use. Never clone the
  personal vault just to satisfy a routine coding task.
- `skills/save-prompt-cache`: a compatibility prompt for vault persistence, not a
  cache transfer. Do not make its local receipt gate a cloud prerequisite.
- Keep reviewed skills in a GitHub repo as `.agents/skills/<name>/SKILL.md` plus
  relative supporting files. Repository-local skills travel with the checkout.
  A separate skills repo needs an explicit tested distribution/install step or
  plugin; putting files in GitHub alone does not install them in every task.
- `scripts/check.py` and Codex-home README validate the maintained configuration
  collection; they are not project test commands. Do not run home-wide checks as
  an application build.
- Managed `plugins/`, `vendor_imports/`, and system skills are installation/cache
  content. Use supported cloud connections/plugins afresh; do not vendor caches.

## What does not transfer directly / stays local

- MCP `node_repl` launches a binary inside ChatGPT.app with Mac runtime paths;
  `computer-use` launches a macOS app bundle. Cloud tasks need supported cloud
  tools or separately installed Linux tools, not copies of these commands.
- `model_providers.ollama-launch` and its profile depend on a local provider.
  Replace local inference with the selected hosted model or a separately secured
  service where genuinely needed. No provider credential migration was attempted.
- Keychain/auth credential-store settings, credentials, private keys, OAuth
  sessions, browser cookies, trusted-project paths, local permissions/rules,
  notifications, desktop/TUI preferences, and shell path policy stay local.
  Reconfigure cloud access controls explicitly; never import local allow rules.
- `automations/` contains two PR-monitor definitions. Scheduler-managed tasks
  are not repository configuration; recreate only after confirming cloud support,
  destinations, and notification preferences. Existing automations stay intact.
- Histories, sessions, SQLite state, locks, logs, caches, worktrees, attachments,
  backups, and generated media are local state, not a migration payload. They
  were not read. Never initialize or publish a Git repository over ~/.codex.
- Desktop integrations and enabled plugin entries describe this client; installed
  plugins and their authentication do not automatically follow a Git clone.

Dotfiles-specific limitations: Karabiner requires macOS; fonts/wallpaper and
terminal appearance require a real client; Zsh contains Mac paths; Qwen uses
local LM Studio; Claude vault hooks reference local files. Edit those statically
in cloud and verify on the intended machine. Prefer repository documentation for
cloud handoffs, portable PATH detection for future shell work, and hosted models
for cloud reasoning. Do not run personal hooks or start local-model clients.

## Manual publication and cross-device workflow

1. Before cloud setup, confirm the reviewed changes are committed and merged
   into `main` on GitHub. In the checkout, inspect `git status --short`, fetch
   `origin`, and compare `HEAD` with `origin/main`. Preserve local edits and
   resolve divergence deliberately. For future changes, use a fresh branch and
   reviewed PR rather than reusing the already-merged shared-instructions branch.
   Run `bash cloud-verify.sh` and `git diff --check` before publication. The cloud
   checkout must include `codex/.codex/INSTRUCTIONS.md`, its native adapters,
   `agent-links.py`, `test_agent_links.py`, and `cloud-verify.sh`. Publishing Git
   changes and publishing a cloud environment are separate actions.
2. Sign in to ChatGPT on web or desktop. Choose Work in > Cloud > Select
   environment > Create environment, or Settings > Codex Cloud > Environments >
   Create environment. Connect GitHub if prompted, authorize lh1207/dotfiles,
   select that repository only, and choose Get started. Organization policy or
   repository permissions may require an administrator.
3. Name the setup `dotfiles-pilot`; choose Only me. Confirm the checkout contains
   these files from the reviewed `main` branch before proceeding.
4. Give setup this request: "Prepare lh1207/dotfiles for static configuration
   maintenance. Follow AGENTS.md and CODEX-CLOUD.md. Install Bash, Zsh, Python 3,
   Git and GNU Stow using distro packages. Never run bootstrap.sh, source shell
   configs, install personal hooks or copy credentials. Run bash cloud-verify.sh.
   Record the tested install script and a start skill that checks the checkout.
   No secrets or application services. Keep access private and network restricted
   to package installation. Report tool versions and all check results."
5. Review actual setup files, install script, start skill, permissions and results.
   Resolve failures, save changes, select Publish, and wait for Environment
   published. Environment publication is separate from publishing Git commits.
   This preparation has not created or published a cloud environment for you.
6. Select Start a new task. Example: "Review bootstrap.sh for cross-platform
   portability. Make no changes. Run bash cloud-verify.sh and distinguish static
   findings from checks requiring macOS. Do not commit, push or deploy."
7. On web/desktop choose Work in > Cloud and the published environment. On mobile
   open Codex and choose the environment. Reopen the same task across devices to
   review its diff/checks or ask follow-ups; a new task is separate work. Commit
   or open a PR only when satisfied. The Mac can be asleep for these cloud tasks.
8. For dependency/setup changes, Edit the environment from Settings > Codex Cloud
   > Environments, test, save and Republish. Verify in a new task; existing tasks
   retain their own state. Saved cloud state does not replace Git version control.

Official references (cloud-environments guidance rechecked 2026-10-28):
- https://learn.chatgpt.com/docs/cloud
- https://learn.chatgpt.com/docs/environments/cloud-environments
- https://learn.chatgpt.com/docs/build-skills

These instructions use current published environments (install script/start
skill), not the separately documented legacy setup/maintenance-script workflow.
The current environment UI supports direct Environment variables and proxy-based
Network secrets; network secrets use placeholders and HTTPS domain substitution.
Keep all values in the UI, never in repository files, task text or logs.

## Ready-to-paste environment setup prompt

```text
Prepare only lh1207/dotfiles for static configuration maintenance. Read AGENTS.md,
README.md and CODEX-CLOUD.md, then follow the checkout-relative shared instructions.
Confirm the checkout contains the reviewed preparation merged into main; report
branch and commit. Do not proceed with an older checkout missing the canonical source,
agent-links.py, test_agent_links.py or cloud-verify.sh.
Inspect existing tools first. Install missing Bash, POSIX sh, Zsh, Python 3, Git
and GNU Stow with distro packages. On Debian/Ubuntu use bash dash zsh python3 git
stow. Record versions, the actual tested install script, and exact check results.
Run bash cloud-verify.sh from the repository root. Record a start skill that runs
that static verifier and reports failures; no application services are needed.
Never run bootstrap.sh, source personal shell files, invoke personal hooks,
install dotfiles or instruction links into the real home, start local model
clients, or copy Mac configuration, credentials, histories or vaults.
Keep access Only me. Use Package managers network access only for installation;
request no secrets or application environment variables. Disable task internet
access after setup if available under workspace policy and confirm the verifier
still passes. Distinguish syntax/layout checks from macOS or external-service
functional tests. Do not commit, push, create PRs, publish or change sharing.
Leave the tested configuration ready for my review and manual Publish.
```

## Local verification, 2026-10-19

On macOS 26.6.2 arm64: Bash 3.2.57, Zsh 5.9, Python 3.14.7, Git 2.56.0,
GNU Stow 2.4.1. `bash -n cloud-verify.sh`, `bash cloud-verify.sh` and
`git diff --check` passed. The verifier parsed seven shell files, two JSON
files and two Python files; all four installer regressions, the 13-package Stow
simulation, and disposable install/check/reinstall passed. The read-only
`python3 agent-links.py --check` also passed for the local home. Cloud Linux package
installation, account access, publication and task execution must still be tested
in the environment setup conversation. This repository requires no new files,
package dependencies beyond the tools above, services, secrets or application
variables. The repository AGENTS.md already delegates to the current shared
coding-agent defaults and retains the cloud-specific restrictions; no change
was needed there. Live bootstrap.sh already uses an explicit package list,
so the older claim that every new top-level directory becomes a package is stale.
No new directories were added.


## Follow-up stability review, 2026-10-28

The verifier passed on macOS, including all four installer regressions,
13-package Stow simulation, and disposable install/check/reinstall. A separate
Bash 3.2 isolation check supplied failing `BASH_ENV`, `ENV`, and `ZDOTDIR`
startup files and invalid personal `.stowrc` options; verification still passed
and no startup marker was created. `git diff --check` passed. The publication
steps now account for PR #9 already being merged into `main`. Linux/Windows
execution, cloud publication, and live client behavior remain untested.
