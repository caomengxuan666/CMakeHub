"""
Use module - Generate CMake configuration for using modules
"""

import json
import os
import sys
from cli.package_data import load_modules_json, get_loader_path


def use_module(args):
    """Generate CMake configuration for using a module"""
    try:
        data = load_modules_json()
        loader_path = get_loader_path()

        modules = data.get("modules", [])

        # Find the module
        module = None
        for m in modules:
            if m["name"] == args.module:
                module = m
                break

        if not module:
            print(f"Error: Module '{args.module}' not found", file=sys.stderr)
            print("\nUse 'cmakehub list' to see available modules", file=sys.stderr)
            return 1

        # Generate CMake code
        cmake_code = f"""# CMakeHub: {module['name']}
# {module.get('description', 'No description')}

# Include CMakeHub loader
include({{CMAKE_CURRENT_SOURCE_DIR}}/cmake/hub/loader.cmake)

# Use module
cmakehub_use({args.module}"""

        # Add version if specified
        if args.version:
            cmake_code += f'\n    VERSION "{args.version}"'

        # Add options if specified
        if args.options:
            cmake_code += "\n    " + "\n    ".join(args.options)

        cmake_code += ")"

        if args.append:
            # Append to file
            output_file = args.append
            with open(output_file, "a", encoding="utf-8") as f:
                f.write("\n\n" + cmake_code)
            print(f"✅ Configuration appended to {output_file}")

        elif args.output:
            # Write to file
            output_file = args.output
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(cmake_code)
            print(f"✅ Configuration written to {output_file}")

        else:
            # Print to terminal
            print("\n" + "=" * 80)
            print(f"📝 Add this to your CMakeLists.txt:")
            print("=" * 80)
            print()
            print(cmake_code)
            print()
            print("=" * 80)
            print()

            # Show module info
            print(f"Module Information:")
            print(f"  Name: {module['name']}")
            print(f"  Description: {module.get('description', 'N/A')}")
            print(f"  Category: {module.get('category', 'N/A')}")
            print(f"  Repository: {module.get('repository', 'N/A')}")
            print(f"  License: {module.get('license', 'N/A')}")

            if module.get("dependencies"):
                print(f"  Dependencies: {', '.join(module['dependencies'])}")

            if module.get("conflicts"):
                print(f"  Conflicts: {', '.join(module['conflicts'])}")

        # Test download if requested
        if args.test:
            print()
            print("Testing download...")
            from update import download_module_now

            download_module_now(args.module, args.version)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error generating configuration: {e}", file=sys.stderr)
        return 1
