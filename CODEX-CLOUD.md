# Codex Cloud pilot and migration plan

Prepared 2026-10-18. The original cloud pilot did not change or copy ~/.codex.
Subsequent local instruction consolidation is documented in AGENT-SETUP.md;
its canonical source now travels in this checkout. No secrets are required for
this pilot. Cloud setup remains separate from local home-link installation.

## Pilot: lh1207/dotfiles

The working tree was clean before preparation. The inspected branch is
`codex/claude-shared-vault`; GitHub advertises it at
`09972d91f7d14d3fe4c47166c7b429327b5cf54a`. GitHub's default branch is `main`.
Make the prepared files available on the branch chosen for cloud tasks; a cloud
checkout cannot see uncommitted Mac files. Remote metadata was checked read-only.

The pilot is static configuration maintenance, not a full desktop installation.
There is no application build, dependency manifest, lockfile, or existing test
suite. GNU Stow is the configuration deployment tool. The added verifier provides
shell parsing, tracked JSON parsing, and Stow layout simulation. It does not prove
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
  bash zsh python3 git stow
bash cloud-verify.sh
```

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
package list; it cannot detect conflicts with an existing user's home.

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

## Project rollout order and readiness conditions

These are inspected local projects, not an exhaustive GitHub account inventory.
Apart from dotfiles, remote freshness and cloud execution remain unverified.
Never reset, stash, pull over, or broadly stage the existing user changes.

| Project | Observed state | Must be true before cloud use |
| --- | --- | --- |
| dotfiles (pilot) | Clean feature branch before these additions; remote branch verified | Publish reviewed preparation to the chosen GitHub branch manually; install distro tools; static verifier passes; keep desktop activation local. |
| ProjectMGT (next app candidate) | Clean `feat/ai` tracking branch; Node >=20, pnpm 9.15.9, pnpm lockfile, Turbo, Nest/React/Prisma/SQLite | Pin a supported Node satisfying >=20; install pnpm 9.15.9; `pnpm install --frozen-lockfile`; generate Prisma client; use a disposable SQLite DATABASE_URL; build shared contracts; run `pnpm typecheck`, `pnpm test`, `pnpm build` and the API e2e suite. Confirm migrations/seed only target disposable data; inspect CLAUDE.md and docs/DEVELOPMENT.md before edits. Lint scripts currently just print a message. |
| levihuff.net | Extensive tracked/untracked changes; main is 26 behind the local origin/main reference; existing AGENTS.md and npm lockfile | First reconcile user work with GitHub deliberately. Confirm Node version from CI/lockfile dependencies; `npm ci`, `npm test`, `npm run build`. Eleventy/Tailwind/Vitest can run in Linux; leave FTP deployment credentials in GitHub Actions. Pushing main triggers deployment. No deploy needed for cloud coding. |
| homelab | Clean main relative to locally recorded origin/main; Compose files, secret guard, gitleaks/KICS/Trivy CI | Start with static Compose validation using dummy inputs and `docker compose config --quiet` (avoid rendering secrets). Confirm Docker availability before integration work. Preserve existing security checks. LAN Ollama, Proxmox, SMB media, host networking and HomeKit/mDNS cannot be assumed in cloud. Use disposable services/mocks; run hardware/LAN integration on its actual host. |
| ad-pxe-lab | main with modified Obsidian graph and untracked .DS_Store | Limit cloud to docs, PowerShell parsing/static review and template checks with PowerShell installed. Hyper-V, Windows roles, ISO/VHD media, PXE and host networking require an isolated Windows lab. Keep credentials and installation media there. Preserve the existing graph change. |
| global-vault | Numerous user changes; no origin URL returned | Exclude from this pilot. Explicitly select any non-sensitive subset and decide private hosting/access before migration; do not upload the whole personal vault. |

ProjectMGT configuration names: DATABASE_URL, PORT, CORS_ORIGIN,
JWT_ACCESS_SECRET, JWT_REFRESH_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL,
AI_ASSIGN_MODEL; optional ANTHROPIC_API_KEY enables AI assignment. Keep AI disabled
for initial tests. For a live preview, supply fresh development JWT secrets through
cloud Environment variables/Personal vault, never production values or prompts.
If AI integration is explicitly tested, use ANTHROPIC_API_KEY as a Network secret
restricted to the provider HTTPS domain, subject to SDK/proxy testing. SQLite
and seeded users must remain disposable; e2e commands reset their test database.

Homelab secret names from templates: POSTGRES_PASSWORD, FTP_USER_PASS,
PGADMIN_DEFAULT_PASSWORD, APP_KEY, BOOKSTACK_DB_PASS, MYSQL_ROOT_PASSWORD,
PIHOLE_WEBPASSWORD. Non-secret configuration names include POSTGRES_USER,
POSTGRES_DB, FTP_USER_NAME, OPTIPLEX_IP, PGADMIN_DEFAULT_EMAIL, PIHOLE_HOST_IP,
DOCKER_LXC_IP, OLLAMA_BASE_URL. No real values were read. Static validation should
use clearly fake inputs. If later needed by local processes in cloud, use cloud
Environment variables/Personal vault with disposable credentials. HTTPS service
credentials can instead use domain-scoped Network secrets. Do not give coding
tasks production infrastructure access just to validate Compose syntax.

## Manual publication and cross-device workflow

1. Review the complete shared-instruction change with Git, including untracked
   files and symlink targets. Re-run `bash cloud-verify.sh`. Publication must
   include the canonical `codex/.codex/INSTRUCTIONS.md`, its native adapters,
   `agent-links.py`, `test_agent_links.py`, the verifier and repository guidance,
   plus reviewed bootstrap/package changes required by those checks. Publishing
   only the original three cloud-pilot files leaves the verifier and shared
   instructions incomplete. Select reviewed paths explicitly; do not broadly
   stage unrelated edits, local settings or backups. No commit/push was performed.
   Publish the complete reviewed change on the intended branch (or through a PR).
   GitHub's default main does not automatically include this feature branch.
2. Sign in to ChatGPT on web or desktop. Choose Work in > Cloud > Select
   environment > Create environment, or Settings > Codex Cloud > Environments >
   Create environment. Connect GitHub if prompted, authorize lh1207/dotfiles,
   select that repository only, and choose Get started. Organization policy or
   repository permissions may require an administrator.
3. Name the setup `dotfiles-pilot`; choose Only me. Confirm the checkout contains
   these files from your published branch. If setup selects main, first merge
   the preparation there or explicitly select the prepared branch where offered.
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

Current official references (checked 2026-10-18):
- https://learn.chatgpt.com/docs/cloud
- https://learn.chatgpt.com/docs/environments/cloud-environments
- https://learn.chatgpt.com/docs/build-skills

These instructions use current published environments (install script/start
skill), not the separately documented legacy setup/maintenance-script workflow.
The current environment UI supports direct Environment variables and proxy-based
Network secrets; network secrets use placeholders and HTTPS domain substitution.
Keep all values in the UI, never in repository files, task text or logs.
