"""
Show module information
"""

import json
import sys
from cli.package_data import load_modules_json


def show_info(args):
    """Show module information"""
    try:
        data = load_modules_json()

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

        # Display module information
        print("=" * 80)
        print(f"Module: {module['name']}")
        print("=" * 80)
        print()

        print(f"Description:")
        print(f"  {module.get('description', 'N/A')}")
        print()

        print(f"Category:")
        print(f"  {module.get('category', 'N/A')}")
        print()

        print(f"Author:")
        print(f"  {module.get('author', 'N/A')}")
        print()

        print(f"Repository:")
        print(f"  {module.get('repository', 'N/A')}")
        print()

        print(f"Path:")
        print(f"  {module.get('path', 'N/A')}")
        print()

        print(f"License:")
        print(f"  {module.get('license', 'N/A')}")
        print()

        print(f"Version:")
        print(f"  {module.get('version', 'N/A')}")
        print()

        if module.get("stars"):
            print(f"Stars:")
            print(f"  {module['stars']}")
            print()

        if module.get("last_updated"):
            print(f"Last Updated:")
            print(f"  {module['last_updated']}")
            print()

        if module.get("cmake_minimum_required"):
            print(f"CMake Minimum Required:")
            print(f"  {module['cmake_minimum_required']}")
            print()

        if module.get("cpp_minimum_required"):
            print(f"C++ Minimum Required:")
            print(f"  C++{module['cpp_minimum_required']}")
            print()

        if module.get("dependencies"):
            print(f"Dependencies:")
            for dep in module["dependencies"]:
                print(f"  - {dep}")
            print()

        if module.get("conflicts"):
            print(f"Conflicts:")
            for conflict in module["conflicts"]:
                print(f"  - {conflict}")
            print()

        if module.get("tags"):
            print(f"Tags:")
            print(f"  {', '.join(module['tags'])}")
            print()

        if module.get("platform"):
            print(f"Platforms:")
            print(f"  {', '.join(module['platform'])}")
            print()

        if args.verbose:
            print(f"Raw JSON:")
            print(json.dumps(module, indent=2))

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading module info: {e}", file=sys.stderr)
        return 1
