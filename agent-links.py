#!/usr/bin/env python3
"""Preview, install, or check only the shared instruction links; no client execution."""

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
CANONICAL = ROOT / "codex/.codex/INSTRUCTIONS.md"
SOURCES = {
    ".codex/INSTRUCTIONS.md": CANONICAL,
    ".claude/CLAUDE.md": ROOT / "claude/.claude/claude.md",
    ".cursor/rules/model-workflow.mdc": ROOT / "cursor/.cursor/rules/model-workflow.mdc",
    ".cursor/rules/obsidian-wiki.mdc": ROOT / "cursor/.cursor/rules/obsidian-wiki.mdc",
    ".roo/rules/00-shared.md": CANONICAL,
}
NATIVE_LINKS = {
    ".codex/AGENTS.md": "INSTRUCTIONS.md",
    ".gemini/GEMINI.md": "../.codex/INSTRUCTIONS.md",
    ".qwen/QWEN.md": "../.codex/INSTRUCTIONS.md",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Back up replaced entries and install links")
    mode.add_argument("--check", action="store_true", help="Validate sources and installed links, read-only")
    parser.add_argument("--target", type=Path, default=Path.home(), help="Home or disposable test directory")
    args = parser.parse_args()
    home = args.target.expanduser().resolve()
    links = {}
    for name, source in SOURCES.items():
        try:
            links[name] = os.path.relpath(source, (home / name).parent)
        except ValueError:
            # Windows paths on different drives cannot be relative.
            links[name] = str(source)
    links.update(NATIVE_LINKS)

    # Preflight everything before changing anything. Never replace a directory.
    for name, target in links.items():
        path = home / name
        if path.is_dir():
            parser.error(f"Refusing directory at {path}")
        for parent in path.parents:
            if parent == home:
                break
            if parent.is_symlink():
                parser.error(f"Refusing symlinked parent: {parent}; use real client directories")
            if parent.exists() and not parent.is_dir():
                parser.error(f"Parent is not a directory: {parent}")
        if name in SOURCES and not SOURCES[name].is_file():
            parser.error(f"Missing maintained source: {name}")
    if not CANONICAL.is_file():
        parser.error("Missing canonical instructions")
    for name in ["codex/.codex/AGENTS.md", "gemini/.gemini/GEMINI.md", "qwen/.qwen/QWEN.md", "roo/.roo/rules/00-shared.md"]:
        if (ROOT / name).resolve() != CANONICAL:
            parser.error(f"Incorrect repository pointer: {name}")
    if (ROOT / "claude/.claude/claude.md").read_text(encoding="utf-8").strip() != "@~/.codex/INSTRUCTIONS.md":
        parser.error("Incorrect Claude import")
    for name in ["cursor/.cursor/rules/model-workflow.mdc"]:
        if "~/.codex/INSTRUCTIONS.md" not in (ROOT / name).read_text(encoding="utf-8"):
            parser.error(f"Missing canonical reference: {name}")

    changes = []
    for name, target in links.items():
        path = home / name
        # Compare resolved paths, accepting equivalent Stow-created links.
        expected = (path.parent / target).resolve()
        valid = path.is_symlink() and path.resolve() == expected and path.is_file()
        # Normalize links on installation, including case-only legacy paths on macOS.
        if args.apply and path.is_symlink() and os.readlink(path) != target:
            valid = False
        if valid:
            print(f"PASS {name}")
        else:
            changes.append((name, target))
            print(f"{'FAIL' if args.check else 'LINK'} {name}")
    print("NOTE Cursor global User Rule must be configured/verified in Cursor Settings; home .mdc links are not proof of global loading.")
    if args.check:
        return int(bool(changes))
    if not args.apply or not changes:
        if not args.apply:
            print("Preview only. Use --apply to install these instruction links.")
        return 0

    backup_root = home / ".local/state/agent-instructions/backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-"), dir=backup_root))
    for name, _ in changes:
        path = home / name
        if path.exists() or path.is_symlink():
            saved = backup / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            # Preserve symlinks themselves; never traverse a personal vault.
            shutil.copy2(path, saved, follow_symlinks=False)
    (backup / "MANIFEST.txt").write_text(
        "Target: " + str(home) + "\nChanged entries (missing backup means newly created):\n"
        + "\n".join(name for name, _ in changes) + "\n", encoding="utf-8"
    )
    # Prepare every link before replacing any entry. Missing Windows symlink
    # privileges or a full disk must not remove the original configuration.
    with ExitStack() as stack:
        prepared = []
        try:
            for name, target in changes:
                path = home / name
                path.parent.mkdir(parents=True, exist_ok=True)
                scratch = Path(stack.enter_context(tempfile.TemporaryDirectory(
                    prefix=".agent-link-", dir=path.parent)))
                candidate = scratch / "link"
                candidate.symlink_to(target)
                prepared.append((candidate, path))
        except OSError as exc:
            parser.error(f"Cannot prepare instruction links ({exc.__class__.__name__}); "
                         "existing entries preserved. Windows requires symlink privileges "
                         "(for example Developer Mode).")
        for candidate, path in prepared:
            os.replace(candidate, path)
    print(f"Backups: {backup}")
    print("Installed instruction links. Start fresh client sessions; run --check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
