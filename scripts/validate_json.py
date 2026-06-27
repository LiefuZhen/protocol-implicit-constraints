from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    root = Path.cwd()
    errors = 0

    for path in sorted(root.rglob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as f:
                json.load(f)
            print(f"[OK] {path.relative_to(root)}")
        except Exception as exc:  # noqa: BLE001 - validator should report any parse/read failure.
            errors += 1
            print(f"[ERROR] {path.relative_to(root)}: {exc}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
