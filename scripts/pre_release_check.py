#!/usr/bin/env python3
"""
Pre-release check script for CMakeHub
Verifies that all required files are present and no temporary files remain.
"""

import os
import sys
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Required files and directories
REQUIRED_FILES = [
    'CMakeLists.txt',
    'LICENSE',
    'modules.json',
    'README.md',
    'docs/CONTRIBUTING.md',
    'docs/RELEASE_CHECKLIST.md',
    'tests/run_tests.py',
    'tests/run_single_test.py',
    'tests/verify_modules.cmake',
    '.gitignore',
]

REQUIRED_DIRS = [
    'cmake/hub',
    'examples/basic',
    'tests',
    'scripts',
    'docs',
    '.github/workflows',
]

# Files that should NOT exist
FORBIDDEN_PATTERNS = [
    'temp_verify_*.cmake',
    'test_*.json',
    'cmakehub_test_cache',
    'build',
    '__pycache__',
]

def check_required_files():
    """Check that all required files exist."""
    print(f"{Colors.BLUE}Checking required files...{Colors.RESET}")
    
    missing = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing.append(file)
            print(f"  {Colors.RED}[X]{Colors.RESET} Missing: {file}")
        else:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} Found: {file}")
    
    if missing:
        print(f"\n{Colors.RED}Missing {len(missing)} required files!{Colors.RESET}")
        return False
    else:
        print(f"{Colors.GREEN}[OK] All required files present{Colors.RESET}")
        return True

def check_required_dirs():
    """Check that all required directories exist."""
    print(f"\n{Colors.BLUE}Checking required directories...{Colors.RESET}")
    
    missing = []
    for dir_path in REQUIRED_DIRS:
        if not os.path.exists(dir_path):
            missing.append(dir_path)
            print(f"  {Colors.RED}[X]{Colors.RESET} Missing: {dir_path}/")
        else:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} Found: {dir_path}/")
    
    if missing:
        print(f"\n{Colors.RED}Missing {len(missing)} required directories!{Colors.RESET}")
        return False
    else:
        print(f"{Colors.GREEN}[OK] All required directories present{Colors.RESET}")
        return True

def check_forbidden_files():
    """Check that no forbidden files exist."""
    print(f"\n{Colors.BLUE}Checking for temporary/forbidden files...{Colors.RESET}")
    
    found = []
    root = Path('.')
    
    for pattern in FORBIDDEN_PATTERNS:
        for file in root.glob(pattern):
            if file.is_file() or file.is_dir():
                found.append(str(file))
                print(f"  {Colors.YELLOW}[!]{Colors.RESET} Found: {file}")
    
    if found:
        print(f"\n{Colors.YELLOW}Found {len(found)} files that should be removed:{Colors.RESET}")
        print(f"  {Colors.YELLOW}Run: git clean -fdx{Colors.RESET}")
        return False
    else:
        print(f"{Colors.GREEN}[OK] No forbidden files found{Colors.RESET}")
        return True

def check_file_content():
    """Check that placeholder text has been replaced."""
    print(f"\n{Colors.BLUE}Checking file content...{Colors.RESET}")
    
    issues = []
    
    # Check README.md for placeholders
    readme_path = Path('README.md')
    if readme_path.exists():
        content = readme_path.read_text()
        if 'yourname' in content:
            issues.append("README.md still contains 'yourname' placeholder")
            print(f"  {Colors.RED}[X]{Colors.RESET} README.md contains 'yourname' placeholder")
        else:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} README.md - no placeholders found")
    
    # Check CONTRIBUTING.md for placeholders
    contrib_path = Path('docs/CONTRIBUTING.md')
    if contrib_path.exists():
        content = contrib_path.read_text()
        if 'yourname' in content:
            issues.append("docs/CONTRIBUTING.md still contains 'yourname' placeholder")
            print(f"  {Colors.RED}[X]{Colors.RESET} docs/CONTRIBUTING.md contains 'yourname' placeholder")
        else:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} docs/CONTRIBUTING.md - no placeholders found")
    
    # Check CI workflow for placeholders
    ci_path = Path('.github/workflows/ci.yml')
    if ci_path.exists():
        content = ci_path.read_text()
        if 'yourname' in content:
            issues.append(".github/workflows/ci.yml still contains 'yourname' placeholder")
            print(f"  {Colors.RED}[X]{Colors.RESET} CI workflow contains 'yourname' placeholder")
        else:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} CI workflow - no placeholders found")
    
    if issues:
        print(f"\n{Colors.RED}Found {len(issues)} placeholder issues!{Colors.RESET}")
        for issue in issues:
            print(f"  {Colors.RED}  - {issue}{Colors.RESET}")
        return False
    else:
        print(f"{Colors.GREEN}[OK] All placeholders replaced{Colors.RESET}")
        return True

def main():
    """Run all checks."""
    print(f"{Colors.BOLD}{Colors.BLUE}=== CMakeHub Pre-Release Check ==={Colors.RESET}\n")
    
    results = []
    results.append(check_required_files())
    results.append(check_required_dirs())
    results.append(check_forbidden_files())
    results.append(check_file_content())
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== Summary ==={Colors.RESET}")
    
    if all(results):
        print(f"{Colors.GREEN}{Colors.BOLD}[OK] All checks passed! Ready for release.{Colors.RESET}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.RESET}")
        print(f"  1. Review changes: {Colors.YELLOW}git status{Colors.RESET}")
        print(f"  2. Commit changes: {Colors.YELLOW}git add . && git commit -m 'Prepare for v0.1.0 release'{Colors.RESET}")
        print(f"  3. Tag release: {Colors.YELLOW}git tag -a v0.1.0 -m 'CMakeHub v0.1.0'{Colors.RESET}")
        print(f"  4. Push to GitHub: {Colors.YELLOW}git push origin main --tags{Colors.RESET}")
        print(f"  5. Create Draft Release on GitHub")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}[X] Some checks failed! Please fix the issues above.{Colors.RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
