#!/usr/bin/env python3
"""
One-click release script for CMakeHub
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)


def update_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    pyproject_path.write_text(content)
    print(f"Updated version to {new_version}")


def parse_version(version):
    """Parse semantic version"""
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    return tuple(int(p) for p in parts)


def bump_version(version, bump_type):
    """Bump version based on type"""
    major, minor, patch = parse_version(version)
    
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"


def main():
    parser = argparse.ArgumentParser(description="Release CMakeHub to PyPI")
    parser.add_argument(
        "version",
        nargs="?",
        help="Version to release (e.g., 0.1.2). If not specified, will bump patch version."
    )
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        default="patch",
        help="Version bump type (default: patch)"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip local build test"
    )
    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Skip git operations (for testing)"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("CMakeHub Release Script")
    print("=" * 80)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Are you in the CMakeHub root directory?")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    print(f"\nCurrent version: {current_version}")
    
    # Determine new version
    if args.version:
        new_version = args.version
    else:
        new_version = bump_version(current_version, args.bump)
    
    print(f"New version: {new_version}")
    
    # Confirm
    response = input(f"\nRelease version {new_version}? (y/N): ")
    if response.lower() != "y":
        print("Cancelled")
        sys.exit(0)
    
    # Update version in pyproject.toml
    update_version(new_version)
    
    # Build locally to test
    if not args.skip_build:
        print("\n" + "=" * 80)
        print("Building package locally...")
        print("=" * 80)
        
        run_command("python -m build --wheel --sdist --no-isolation")
        
        print("\n" + "=" * 80)
        print("Checking package with twine...")
        print("=" * 80)
        
        run_command("python -m twine check dist/*")
        
        print("\n✅ Build successful!")
    
    # Git operations
    if not args.skip_git:
        print("\n" + "=" * 80)
        print("Git operations...")
        print("=" * 80)
        
        # Commit version bump
        run_command(f"git add pyproject.toml")
        run_command(f'git commit -m "chore: Bump version to {new_version}"')
        
        # Push to remote
        run_command("git push origin main")
        
        # Create tag
        run_command(f'git tag -a v{new_version} -m "Release v{new_version}"')
        
        # Push tag
        run_command(f"git push origin v{new_version}")
        
        print("\n✅ Git operations successful!")
    
    print("\n" + "=" * 80)
    print(f"✅ Release v{new_version} initiated!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Wait for GitHub Actions to complete")
    print("2. Check build status: https://github.com/caomengxuan666/CMakeHub/actions")
    print("3. Verify package on Test PyPI: https://test.pypi.org/project/cmakehub/")
    print("4. Verify package on PyPI: https://pypi.org/project/cmakehub/")
    print()


if __name__ == "__main__":
    main()