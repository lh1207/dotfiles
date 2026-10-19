# Agent workflow for dotfiles

This is a GNU Stow dotfiles repository, not an application. Read README.md for
layout and CODEX-CLOUD.md for cloud setup and verification limits.

Read `codex/.codex/INSTRUCTIONS.md` for the shared workflow unless its contents
are already loaded. This relative path also works in a cloud checkout.

## Repository constraints

- Do not run bootstrap.sh, source shell startup files, or install these dotfiles
  into the task user's home during cloud setup or verification. bootstrap.sh
  installs an explicit package list into the real home; it is not a verifier.
- Keep Mac paths, Karabiner, LM Studio/Qwen, local vault hooks, and desktop
  integrations out of the cloud runtime. Their files can be edited and checked
  statically; functional verification requires their actual target system.
- Agent instruction entry points share one canonical file. Keep client adapters
  minimal. Personal vaults and desktop tools are not cloud prerequisites.

## Checks and handoff

Run `bash cloud-verify.sh` after relevant edits. It checks shell/JSON syntax and
simulates Stow against an empty temporary target; it never loads configurations.
Use focused checks first and broaden when shared behavior changes. Review the
diff and report checks plus limitations before claiming success.

Do not run `agent-links.py --apply` against the real home during cloud setup or
verification. `cloud-verify.sh` uses a disposable target. Keep durable project
knowledge in repository documentation; no external personal vault is required.
