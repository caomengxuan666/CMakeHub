"""
Update modules index - Download latest modules.json from GitHub
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime


def get_modules_index_url():
    """Get the GitHub raw URL for modules.json"""
    # Use the default branch (main)
    return "https://raw.githubusercontent.com/caomengxuan666/CMakeHub/main/modules.json"


def update_index(args):
    """Download latest modules.json from GitHub"""
    try:
        print("Updating CMakeHub modules index...")
        print("-" * 80)

        # Get URL
        url = get_modules_index_url()
        print(f"Fetching from: {url}")

        # Download
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            print(f"✗ Failed to download modules.json", file=sys.stderr)
            print(f"  Error: {e}", file=sys.stderr)
            print()
            print("Possible reasons:")
            print("  - No internet connection")
            print("  - GitHub is down")
            print("  - URL is incorrect")
            return 1
        except Exception as e:
            print(f"✗ Unexpected error: {e}", file=sys.stderr)
            return 1

        # Parse and validate
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON format", file=sys.stderr)
            print(f"  Error: {e}", file=sys.stderr)
            return 1

        if "modules" not in data:
            print(f"✗ Invalid modules.json format: missing 'modules' key", file=sys.stderr)
            return 1

        modules = data["modules"]
        print(f"✓ Downloaded {len(modules)} modules")

        # Determine where to save
        if args.local:
            # Save to repository root (for development)
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            output_path = os.path.join(repo_root, "modules.json")
        else:
            # Save to package data directory
            from cli.package_data import get_package_data_path
            output_path = get_package_data_path("modules.json")

        # Backup existing file
        if os.path.exists(output_path):
            backup_path = output_path + ".backup"
            os.rename(output_path, backup_path)
            print(f"✓ Backed up existing file to: {os.path.basename(backup_path)}")

        # Save new file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved to: {output_path}")

        # Show stats
        print()
        print("=" * 80)
        print("Index statistics:")
        print("=" * 80)
        print(f"  Total modules: {len(modules)}")
        print(f"  Categories: {len(set(m.get('category', 'unknown') for m in modules))}")
        print(f"  Total stars: {sum(m.get('stars', 0) for m in modules)}")
        print()
        print("Categories:")
        from collections import Counter
        categories = Counter(m.get('category', 'unknown') for m in modules)
        for cat, count in sorted(categories.items()):
            print(f"  - {cat}: {count}")
        print()
        print("✅ Index updated successfully!")
        print()
        print("Note: If you want to use this index in your CMake project,")
        print("copy it to your project root or use 'cmakehub init' to initialize")

        return 0

    except Exception as e:
        print(f"✗ Error updating index: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1