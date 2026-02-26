"""
Search for modules
"""

import sys
from cli.package_data import load_modules_json


def search_modules(args):
    """Search for modules"""
    try:
        data = load_modules_json()

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
