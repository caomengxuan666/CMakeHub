#!/usr/bin/env python3
"""Check which repositories use 'main' instead of 'master' branch"""

import json
import subprocess
import sys

def check_branch(repository):
    """Check if repository has 'main' branch"""
    try:
        # Use git ls-remote to check if 'main' branch exists
        result = subprocess.run(
            ['git', 'ls-remote', '--heads', repository, 'main'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and 'refs/heads/main' in result.stdout
    except Exception as e:
        print(f"Error checking {repository}: {e}")
        return False

def main():
    with open('modules.json') as f:
        data = json.load(f)

    master_modules = [m for m in data['modules'] if m.get('version') == 'master']

    print(f"Checking {len(master_modules)} modules with version='master'...\n")

    main_branch_modules = []
    for module in master_modules:
        name = module['name']
        repo = module['repository']
        print(f"Checking {name}...", end=' ')

        if check_branch(repo):
            print("✓ has 'main' branch")
            main_branch_modules.append(name)
        else:
            print("✗ no 'main' branch")

    print(f"\n{len(main_branch_modules)} modules should use 'main' instead of 'master':")
    for name in sorted(main_branch_modules):
        print(f"  - {name}")

if __name__ == '__main__':
    main()