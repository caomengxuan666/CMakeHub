#!/usr/bin/env python3
"""
CMakeHub Single Test Runner
Run a specific test without configuring the entire test suite
"""

import os
import sys
import subprocess
from pathlib import Path

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 50}{Colors.RESET}\n")

def print_success(text):
    # Use ASCII-compatible characters for Windows
    print(f"{Colors.GREEN}[PASS] {text}{Colors.RESET}")

def print_error(text):
    # Use ASCII-compatible characters for Windows
    print(f"{Colors.RED}[FAIL] {text}{Colors.RESET}")

def print_info(text):
    print(f"  {text}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_single_test.py <test_name>")
        print("\nAvailable tests:")
        print("  - test_loader_basic")
        print("  - test_cache")
        print("  - test_version_check")
        print("  - test_dependencies")
        print("  - test_conflicts")
        sys.exit(1)
    
    test_name = sys.argv[1]
    script_dir = Path(__file__).parent.resolve()
    test_script = script_dir / test_name / "run.cmake"
    
    if not test_script.exists():
        print_error(f"Test script not found: {test_script}")
        sys.exit(1)
    
    print_header(f"Running Test: {test_name}")
    
    # Run the test script
    result = subprocess.run(
        ["cmake", "-P", str(test_script)],
        capture_output=True,
        text=True
    )
    
    # Print output
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print_error("Error output:")
        for line in result.stderr.split('\n'):
            if line.strip():
                print_info(f"  {line}")
    
    # Print result
    print_header("Test Result")
    
    if result.returncode == 0:
        print_success(f"Test '{test_name}' passed!")
        return 0
    else:
        print_error(f"Test '{test_name}' failed!")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
