#!/usr/bin/env python3
"""Record execution of the /goal prompt-cache persistence gate.

Written by the save-prompt-cache harness after it delegates the vault write to
claude-obsidian:save. A receipt is proof the completion gate ran — one is
produced for both a real save and a deliberate skip.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outcome", required=True, choices=("saved", "skipped"))
    parser.add_argument("--title", required=True)
    parser.add_argument("--note", default="")
    parser.add_argument("--cwd", default="")
    args = parser.parse_args()

    override = os.environ.get("CLAUDE_PROMPT_CACHE_RECEIPTS")
    receipt_dir = Path(override) if override else Path.home() / ".claude" / "prompt-cache-receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    payload = {
        "schema_version": 1,
        "recorded_at": now.isoformat(),
        "outcome": args.outcome,
        "title": args.title,
        "note": args.note,
        "cwd": args.cwd or str(Path.cwd()),
    }
    target = receipt_dir / f"{now.strftime('%Y%m%dT%H%M%S.%fZ')}.json"
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
