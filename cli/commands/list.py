"""
List all available modules
"""

import sys
from cli.package_data import load_modules_json


def list_modules(args):
    """List all available modules"""
    try:
        data = load_modules_json()

        modules = data.get("modules", [])
        categories = data.get("categories", {})

        # Filter by category if specified
        if args.category:
            modules = [m for m in modules if m.get("category") == args.category]

        if not modules:
            print(f"No modules found")
            return 0

        if args.compact:
            # Compact output
            for module in modules:
                print(f"{module['name']}")
        else:
            # Detailed output
            print("=" * 80)
            print(f"Available Modules ({len(modules)} total)")
            print("=" * 80)
            print()

            # Group by category
            by_category = {}
            for module in modules:
                cat = module.get("category", "uncategorized")
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(module)

            for category, cat_modules in sorted(by_category.items()):
                cat_name = categories.get(category, category)
                print(f"\n{cat_name} ({len(cat_modules)} modules)")
                print("-" * 80)

                for module in sorted(cat_modules, key=lambda x: x["name"]):
                    print(f"  • {module['name']}")
                    if module.get("description"):
                        print(f"    {module['description']}")
                    print()

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading modules: {e}", file=sys.stderr)
        return 1
