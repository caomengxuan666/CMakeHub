"""
List all available modules
"""

import json
import os
import sys


def get_modules_json():
    """Get the path to modules.json"""
    # Try multiple possible locations
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'modules.json'),
        os.path.join(os.getcwd(), 'modules.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'modules.json'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError("modules.json not found. Are you in a CMakeHub project directory?")


def list_modules(args):
    """List all available modules"""
    try:
        modules_json_path = get_modules_json()
        
        with open(modules_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modules = data.get('modules', [])
        categories = data.get('categories', {})
        
        # Filter by category if specified
        if args.category:
            modules = [m for m in modules if m.get('category') == args.category]
        
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
                cat = module.get('category', 'uncategorized')
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(module)
            
            for category, cat_modules in sorted(by_category.items()):
                cat_name = categories.get(category, category)
                print(f"\n{cat_name} ({len(cat_modules)} modules)")
                print("-" * 80)
                
                for module in sorted(cat_modules, key=lambda x: x['name']):
                    print(f"  • {module['name']}")
                    if module.get('description'):
                        print(f"    {module['description']}")
                    print()
        
        return 0
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading modules: {e}", file=sys.stderr)
        return 1