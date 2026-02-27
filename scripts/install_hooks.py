#!/usr/bin/env python3
"""
Install git hooks from .githooks directory to .git/hooks
"""

import os
import shutil
from pathlib import Path


def main():
    repo_root = Path(__file__).parent.parent
    githooks_dir = repo_root / ".githooks"
    git_hooks_dir = repo_root / ".git" / "hooks"

    print("Installing git hooks...")

    if not githooks_dir.exists():
        print("✗ .githooks directory not found")
        return 1

    git_hooks_dir.mkdir(parents=True, exist_ok=True)

    installed = 0
    for hook_file in githooks_dir.iterdir():
        if hook_file.is_file():
            dest = git_hooks_dir / hook_file.name
            shutil.copy2(hook_file, dest)

            # Make executable on Unix-like systems
            try:
                os.chmod(dest, 0o755)
            except:
                pass

            print(f"✓ Installed: {hook_file.name}")
            installed += 1

    if installed == 0:
        print("No hooks found in .githooks")
        return 0

    print(f"\n✅ Installed {installed} git hook(s)")
    print()
    print("Hooks will run automatically on future git operations.")
    print("To skip a hook, use: git commit --no-verify")
    return 0


if __name__ == "__main__":
    exit(main())