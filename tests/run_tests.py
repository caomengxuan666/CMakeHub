#!/usr/bin/env python3
"""
CMakeHub Test Runner
Cross-platform test runner for CMakeHub
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ANSI color codes for cross-platform terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 50}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

def run_command(cmd, cwd=None, check=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            shell=isinstance(cmd, str)
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def main():
    """Main test runner function"""
    script_dir = Path(__file__).parent.resolve()
    build_dir = script_dir / "build"

    print_header("CMakeHub Test Runner")

    # Step 1: Clean build directory if it exists
    print_info("Preparing build directory...")
    if build_dir.exists():
        print_info(f"  Removing existing build directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    build_dir.mkdir(parents=True, exist_ok=True)
    print_success("Build directory created")

    # Step 2: Configure CMake
    print_info("Configuring CMake...")
    success, stdout, stderr = run_command(
        ["cmake", "..", "-DCMAKEHUB_BUILD_TESTS=ON"],
        cwd=build_dir
    )
    
    if not success:
        print_error("CMake configuration failed!")
        if stderr:
            print_info("Error output:")
            for line in stderr.split('\n'):
                if line.strip():
                    print_info(f"  {line}")
        return 1
    
    print_success("CMake configuration successful")

    # Step 3: Run tests
    print_info("Running tests...")
    success, stdout, stderr = run_command(
        ["ctest", "--output-on-failure", "--verbose"],
        cwd=build_dir
    )
    
    # Print test output
    if stdout:
        print("\nTest output:")
        for line in stdout.split('\n'):
            if line.strip():
                if "PASSED" in line or "Test Passed" in line:
                    print_success(line)
                elif "FAILED" in line or "Test Failed" in line:
                    print_error(line)
                else:
                    print_info(line)
    
    # Print test summary
    print_header("Test Summary")
    
    if success:
        print_success("All tests passed!")
        return 0
    else:
        print_error("Some tests failed")
        if stderr:
            print_info("\nError output:")
            for line in stderr.split('\n'):
                if line.strip():
                    print_info(f"  {line}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)