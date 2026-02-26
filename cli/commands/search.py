"""
Search for modules
"""

import json
import os
import sys


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


def search_modules(args):
    """Search for modules"""
    try:
        modules_json_path = get_modules_json()

        with open(modules_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        modules = data.get("modules", [])
        keyword = args.keyword.lower()

        # Filter by keyword
        results = []
        for module in modules:
            # Search in name, description, tags
            name = module.get("name", "").lower()
            description = module.get("description", "").lower()
            tags = " ".join(module.get("tags", [])).lower()

            if keyword in name or keyword in description or keyword in tags:
                results.append(module)

        # Filter by category if specified
        if args.category:
            results = [m for m in results if m.get("category") == args.category]

        if not results:
            print(f"No modules found matching '{args.keyword}'")
            return 0

        print("=" * 80)
        print(f"Search Results: '{args.keyword}' ({len(results)} found)")
        print("=" * 80)
        print()

        for module in results:
            print(f"Module: {module['name']}")
            print(f"  Description: {module.get('description', 'N/A')}")
            print(f"  Category: {module.get('category', 'N/A')}")
            print(f"  Repository: {module.get('repository', 'N/A')}")
            print(f"  License: {module.get('license', 'N/A')}")
            if module.get("tags"):
                print(f"  Tags: {', '.join(module['tags'])}")
            print()

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error searching modules: {e}", file=sys.stderr)
        return 1
