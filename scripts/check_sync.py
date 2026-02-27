#!/usr/bin/env python3
"""
Check if data files are in sync

This script checks if the data files in the repository root match
the data files in the CLI package directory.
"""

import sys
from pathlib import Path


def check_sync(source_path, dest_path, name):
    """Check if two files are in sync"""
    source = Path(source_path)
    dest = Path(dest_path)

    if not source.exists():
        print(f"✗ Source not found: {source}")
        return False

    if not dest.exists():
        print(f"✗ Destination not found: {dest}")
        print(f"  → Run: python scripts/sync_data.py")
        return False

    source_content = source.read_text(encoding='utf-8')
    dest_content = dest.read_text(encoding='utf-8')

    if source_content != dest_content:
        print(f"✗ {name} is out of sync")
        print(f"  → Run: python scripts/sync_data.py")
        return False

    return True


def main():
    """Main check function"""
    repo_root = Path(__file__).parent.parent

    checks = [
        (repo_root / "modules.json",
         repo_root / "cli" / "data" / "modules.json",
         "modules.json"),
        (repo_root / "THIRD_PARTY_LICENSES.md",
         repo_root / "cli" / "data" / "THIRD_PARTY_LICENSES.md",
         "THIRD_PARTY_LICENSES.md"),
        (repo_root / "cmake" / "hub" / "loader.cmake",
         repo_root / "cli" / "data" / "cmake" / "hub" / "loader.cmake",
         "loader.cmake"),
    ]

    results = [check_sync(*check) for check in checks]

    if not all(results):
        print()
        print("❌ Some data files are out of sync")
        print()
        print("To fix this, run:")
        print("  python scripts/sync_data.py")
        return 1

    print("✅ All data files are in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())