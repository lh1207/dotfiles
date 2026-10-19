"""Disposable installer regression checks; no clients, network, or real-home writes."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


class InstructionLinks(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="agent links ")
        self.addCleanup(self.scratch.cleanup)
        base = Path(self.scratch.name)
        self.repo = base / "checkout with spaces"
        self.home = base / "home with spaces"
        self.repo.mkdir()
        self.home.mkdir()
        for name in ["agent-links.py", "codex/.codex/INSTRUCTIONS.md",
                     "claude/.claude/claude.md", "cursor/.cursor/rules/model-workflow.mdc",
                     "cursor/.cursor/rules/obsidian-wiki.mdc"]:
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dest)
        for name, target in {
            "codex/.codex/AGENTS.md": "INSTRUCTIONS.md",
            "gemini/.gemini/GEMINI.md": "../../codex/.codex/INSTRUCTIONS.md",
            "qwen/.qwen/QWEN.md": "../../codex/.codex/INSTRUCTIONS.md",
            "roo/.roo/rules/00-shared.md": "../../../codex/.codex/INSTRUCTIONS.md",
        }.items():
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(target)
        self.script = self.repo / "agent-links.py"

    def run_installer(self, mode, expected=0):
        result = subprocess.run([sys.executable, str(self.script), "--target", str(self.home), mode],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_native_paths_single_source_and_idempotence(self):
        self.run_installer("--check", 1)
        self.run_installer("--apply")
        self.run_installer("--check")
        for name in [".codex/AGENTS.md", ".gemini/GEMINI.md", ".qwen/QWEN.md", ".roo/rules/00-shared.md"]:
            self.assertEqual((self.home / name).resolve(), (self.repo / "codex/.codex/INSTRUCTIONS.md").resolve())
        canonical = self.repo / "codex/.codex/INSTRUCTIONS.md"
        canonical.write_text("Updated shared instructions — one source\n", encoding="utf-8")
        for name in [".codex/AGENTS.md", ".gemini/GEMINI.md", ".qwen/QWEN.md", ".roo/rules/00-shared.md"]:
            self.assertEqual((self.home / name).read_bytes(), canonical.read_bytes())
        self.assertEqual((self.home / ".claude/CLAUDE.md").read_text(), "@~/.codex/INSTRUCTIONS.md\n")
        backups = list((self.home / ".local/state/agent-instructions/backups").iterdir())
        self.run_installer("--apply")
        self.assertEqual(backups, list(backups[0].parent.iterdir()))

    def test_backups_preserve_symlink_and_its_external_target(self):
        external = self.home.parent / "external.md"
        external.write_text("untouched", encoding="utf-8")
        entry = self.home / ".gemini/GEMINI.md"
        entry.parent.mkdir()
        entry.symlink_to(external)
        self.run_installer("--apply")
        saved = list((self.home / ".local/state/agent-instructions/backups").glob("*/.gemini/GEMINI.md"))
        self.assertEqual(len(saved), 1)
        self.assertTrue(saved[0].is_symlink())
        self.assertEqual(os.readlink(saved[0]), str(external))
        self.assertEqual(external.read_text(), "untouched")

    def test_link_privilege_failure_preserves_all_entries(self):
        original = self.home / ".codex/INSTRUCTIONS.md"
        original.parent.mkdir()
        original.write_text("original", encoding="utf-8")
        with patch.object(sys, "argv", [str(self.script), "--target", str(self.home), "--apply"]), \
             patch("os.symlink", side_effect=PermissionError("test: symlinks unavailable")), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as exc:
                runpy.run_path(str(self.script), run_name="__main__")
        self.assertEqual(exc.exception.code, 2)
        self.assertEqual(original.read_text(), "original")
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())

    def test_symlinked_parent_refused_without_external_writes(self):
        outside = self.home.parent / "outside"
        outside.mkdir()
        (self.home / ".gemini").symlink_to(outside, target_is_directory=True)
        self.run_installer("--apply", 2)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.home / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
