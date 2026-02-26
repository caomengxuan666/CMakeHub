"""
Check module compatibility - Must call CMake for version comparison
"""

import json
import os
import sys
import subprocess


def get_modules_json():
    """Get the path to modules.json"""
    possible_paths = [
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "modules.json",
        ),
        os.path.join(os.getcwd(), "modules.json"),
        os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ),
            "modules.json",
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("modules.json not found. Are you in a CMakeHub project directory?")


def get_loader_path():
    """Get the path to loader.cmake"""
    possible_paths = [
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "cmake",
            "hub",
            "loader.cmake",
        ),
        os.path.join(os.getcwd(), "cmake", "hub", "loader.cmake"),
        os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ),
            "cmake",
            "hub",
            "loader.cmake",
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("loader.cmake not found. Are you in a CMakeHub project directory?")


def check_compatibility(args):
    """Check module compatibility using CMake for version comparison"""
    try:
        modules_json_path = get_modules_json()
        loader_path = get_loader_path()

        with open(modules_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        modules = data.get("modules", [])

        # Find the module
        module = None
        for m in modules:
            if m["name"] == args.module:
                module = m
                break

        if not module:
            print(f"Error: Module '{args.module}' not found", file=sys.stderr)
            return 1

        print("=" * 80)
        print(f"Compatibility Check: {module['name']}")
        print("=" * 80)
        print()

        # Check platform (can be done in Python)
        platform = module.get("platform", [])
        print("Platform Support:")
        if os.name == "nt":
            current_platform = "windows"
        elif sys.platform == "darwin":
            current_platform = "macos"
        else:
            current_platform = "linux"

        print(f"  Required: {', '.join(platform) or 'All platforms'}")
        print(f"  Current:  {current_platform}")

        if platform and current_platform in platform:
            print(f"  Status:   ✓ Supported")
        elif platform:
            print(f"  Status:   ✗ Not supported")
            print(f"  Module requires: {', '.join(platform)}")
        else:
            print(f"  Status:   ✓ Platform-independent")
        print()

        # Check dependencies (can be done in Python)
        dependencies = module.get("dependencies", [])
        print("Dependencies:")
        if dependencies:
            for dep in dependencies:
                dep_found = any(m["name"] == dep for m in modules)
                status = "✓ Available" if dep_found else "⚠ Not found in index"
                print(f"  - {dep}: {status}")
        else:
            print("  None")
        print()

        # Check conflicts (can be done in Python)
        conflicts = module.get("conflicts", [])
        print("Conflicts:")
        if conflicts:
            for conflict in conflicts:
                print(f"  - {conflict}")
        else:
            print("  None")
        print()

        # Check CMake and C++ versions using CMake (MUST use CMake for version comparison)
        print("Version Checking (using CMake):")
        print("-" * 80)

        # Create temporary CMake script to check compatibility
        cmake_script = f"""
cmake_minimum_required(VERSION 3.19)

# Get module info
set(MODULE_NAME "{module['name']}")
set(CMAKE_MIN_REQUIRED "{module.get('cmake_minimum_required', '')}")
set(CPP_MIN_REQUIRED "{module.get('cpp_minimum_required', '')}")

# Check CMake version
message(STATUS "CMake Version:")
message(STATUS "  Required: ${{CMAKE_MIN_REQUIRED}}")
message(STATUS "  Current:  ${{CMAKE_VERSION}}")

if(CMAKE_MIN_REQUIRED AND NOT CMAKE_VERSION VERSION_LESS ${{CMAKE_MIN_REQUIRED}})
    message(STATUS "  Status:   ✓ Compatible")
elseif(CMAKE_MIN_REQUIRED)
    message(FATAL_ERROR "  Status:   ✗ Incompatible - CMake ${{CMAKE_VERSION_REQUIRED}} or higher required")
endif()

# Check C++ standard
message(STATUS "")
message(STATUS "C++ Standard:")
message(STATUS "  Required: C++${{CPP_MIN_REQUIRED}}")

if(CPP_MIN_REQUIRED)
    if(DEFINED CMAKE_CXX_STANDARD)
        message(STATUS "  Current:  C++${{CMAKE_CXX_STANDARD}}")
        if(CMAKE_CXX_STANDARD LESS ${{CPP_MIN_REQUIRED}})
            message(FATAL_ERROR "  Status:   ✗ Incompatible - C++${{CPP_MIN_REQUIRED}} or higher required")
        else()
            message(STATUS "  Status:   ✓ Compatible")
        endif()
    else()
        message(STATUS "  Current:  Not set (requires project context)")
        message(STATUS "  Status:   ⚠ Unknown - Set CMAKE_CXX_STANDARD in your project")
    endif()
else()
    message(STATUS "  Status:   ✓ No requirement")
endif()
"""

        # Write temporary script
        temp_script = os.path.join(os.path.dirname(__file__), "temp_check_compatibility.cmake")
        with open(temp_script, "w") as f:
            f.write(cmake_script)

        try:
            # Run CMake to check compatibility
            result = subprocess.run(["cmake", "-P", temp_script], capture_output=True, text=True)

            # Print CMake output
            print(result.stdout)

            if result.returncode != 0:
                print(f"Status: ✗ Compatibility check failed", file=sys.stderr)
                print(f"Error: {result.stderr}", file=sys.stderr)
                return 1
            else:
                print()
                print("Status: ✓ Module is compatible")

        finally:
            # Clean up temporary file
            if os.path.exists(temp_script):
                os.remove(temp_script)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error checking compatibility: {e}", file=sys.stderr)
        return 1
