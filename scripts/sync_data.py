#!/usr/bin/env python3
"""
Synchronize data files from repository root to CLI package data directory

This script ensures that:
- modules.json is synced to cli/data/modules.json
- THIRD_PARTY_LICENSES.md is synced to cli/data/THIRD_PARTY_LICENSES.md
- loader.cmake is synced to cli/data/cmake/hub/loader.cmake
"""

import os
import sys
import shutil
from pathlib import Path


def sync_file(source_path, dest_path, description):
    """Sync a single file from source to destination"""
    source = Path(source_path)
    dest = Path(dest_path)

    if not source.exists():
        print(f"✗ Source not found: {source}")
        return False

    # Create destination directory if needed
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Check if files are identical
    if dest.exists():
        if source.read_text(encoding='utf-8') == dest.read_text(encoding='utf-8'):
            print(f"✓ {description}: already in sync")
            return True

    # Copy file
    shutil.copy2(source, dest)
    print(f"✓ {description}: synced")
    return True


def sync_directory(source_dir, dest_dir, description):
    """Sync an entire directory from source to destination"""
    source = Path(source_dir)
    dest = Path(dest_dir)

    if not source.exists():
        print(f"✗ Source directory not found: {source}")
        return False

    # Create destination directory
    dest.mkdir(parents=True, exist_ok=True)

    # Copy all files
    copied = 0
    for item in source.rglob('*'):
        if item.is_file():
            relative = item.relative_to(source)
            dest_item = dest / relative
            dest_item.parent.mkdir(parents=True, exist_ok=True)

            if dest_item.exists():
                if item.read_text(encoding='utf-8') == dest_item.read_text(encoding='utf-8'):
                    continue

            shutil.copy2(item, dest_item)
            copied += 1

    print(f"✓ {description}: synced {copied} files")
    return True


def main():
    """Main sync function"""
    # Get repository root
    repo_root = Path(__file__).parent.parent

    print("=" * 80)
    print("CMakeHub Data Synchronization")
    print("=" * 80)
    print(f"Repository root: {repo_root}")
    print()

    # Sync files
    results = []

    # 1. modules.json
    results.append(sync_file(
        repo_root / "modules.json",
        repo_root / "cli" / "data" / "modules.json",
        "modules.json"
    ))

    # 2. THIRD_PARTY_LICENSES.md
    results.append(sync_file(
        repo_root / "THIRD_PARTY_LICENSES.md",
        repo_root / "cli" / "data" / "THIRD_PARTY_LICENSES.md",
        "THIRD_PARTY_LICENSES.md"
    ))

    # 3. loader.cmake
    results.append(sync_file(
        repo_root / "cmake" / "hub" / "loader.cmake",
        repo_root / "cli" / "data" / "cmake" / "hub" / "loader.cmake",
        "loader.cmake"
    ))

    print()
    print("=" * 80)

    if all(results):
        print("✅ All data files synced successfully!")
        print()
        print("Next steps:")
        print("  1. Test: python -m cli.main list")
        print("  2. Build: python -m build")
        print("  3. Install: pip install dist/*.whl")
        return 0
    else:
        print("❌ Some files failed to sync")
        return 1


if __name__ == "__main__":
    sys.exit(main())