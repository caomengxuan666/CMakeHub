"""
Update modules - Must call CMake to re-download modules
"""

import os
import shutil
import sys
import subprocess
import json
from cli.package_data import load_modules_json, get_loader_path


def get_cache_dir():
    """Get the CMakeHub cache directory"""
    if "CMH_CACHE_DIR" in os.environ:
        return os.environ["CMH_CACHE_DIR"]

    if os.name == "nt":  # Windows
        cache_dir = os.path.join(os.environ.get("USERPROFILE", "~"), ".cmakehub", "cache")
    else:  # Unix-like
        cache_dir = os.path.join(os.environ.get("HOME", "~"), ".cmakehub", "cache")

    return os.path.expanduser(cache_dir)


def download_module_now(module_name, version=None):
    """Download module immediately using Git (without waiting for project use)"""
    try:
        # Get module info
        data = load_modules_json()
        modules = data.get("modules", [])

        module = None
        for m in modules:
            if m["name"] == module_name:
                module = m
                break

        if not module:
            print(f"Error: Module '{module_name}' not found", file=sys.stderr)
            return False

        # Get module details
        repository = module.get("repository", "")
        module_version = version or module.get("version", "master")
        module_path = module.get("path", "")

        if not repository:
            print(f"Error: Module '{module_name}' has no repository URL", file=sys.stderr)
            return False

        # Create cache directory
        cache_dir = get_cache_dir()
        module_cache_dir = os.path.join(cache_dir, module_name, module_version)
        os.makedirs(module_cache_dir, exist_ok=True)

        print(f"Downloading {module_name} from {repository}...")
        print(f"  Version: {module_version}")
        print(f"  Cache: {module_cache_dir}")

        # Check if already downloaded
        meta_file = os.path.join(module_cache_dir, ".cmh_meta.json")
        if os.path.exists(meta_file):
            print(f"  ✓ Module already cached")
            return True

        # Clone repository using Git
        git_clone_cmd = [
            "git", "clone",
            "--depth", "1",
            "--branch", module_version,
            repository,
            module_cache_dir
        ]

        result = subprocess.run(git_clone_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Create metadata file
            from datetime import datetime
            metadata = {
                "module": module_name,
                "repository": repository,
                "version": module_version,
                "path": module_path,
                "downloaded_at": datetime.now().isoformat()
            }

            with open(meta_file, "w") as f:
                json.dump(metadata, f, indent=2)

            print(f"✓ Module '{module_name}' downloaded successfully")
            return True
        else:
            print(f"✗ Failed to download module:", file=sys.stderr)
            print(f"  {result.stderr}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"✗ Error downloading module: {e}", file=sys.stderr)
        return False


def update_modules(args):
    """Update modules by clearing cache and optionally downloading"""
    try:
        data = load_modules_json()
        cache_dir = get_cache_dir()
        loader_path = get_loader_path()

        modules = data.get("modules", [])

        if args.module:
            # Update specific module
            module = None
            for m in modules:
                if m["name"] == args.module:
                    module = m
                    break

            if not module:
                print(f"Error: Module '{args.module}' not found", file=sys.stderr)
                return 1

            print(f"Updating module: {module['name']}")
            print("-" * 80)

            # Step 1: Clear Python cache (file operation - can be done in Python)
            module_cache_dir = os.path.join(cache_dir, module["name"])
            if os.path.exists(module_cache_dir):
                print(f"Clearing cache for {module['name']}...")
                shutil.rmtree(module_cache_dir)
                print(f"  ✓ Cache cleared")
            else:
                print(f"  No existing cache found")

            # Step 2: Download now if requested
            if args.download_now:
                print()
                download_module_now(module["name"], module.get("version"))
            else:
                print()
                print(f"Next time you use 'cmakehub_use({module['name']})' in your project,")
                print(f"CMakeHub will automatically download the latest version.")
                print()
                print(f"To download now, add --download-now flag:")
                print(f"  cmakehub update {module['name']} --download-now")

        else:
            # Update all modules
            print("Updating all modules...")
            print("-" * 80)

            # Step 1: Clear all Python caches (file operation - can be done in Python)
            if os.path.exists(cache_dir):
                cached_modules = [
                    d for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))
                ]

                if not cached_modules:
                    print("No cached modules found")
                    return 0

                print(f"Clearing cache for {len(cached_modules)} modules...")
                for module_name in cached_modules:
                    module_dir = os.path.join(cache_dir, module_name)
                    shutil.rmtree(module_dir)
                    print(f"  ✓ Cleared: {module_name}")
            else:
                print("No cache directory found")

            print()
            print("All caches cleared.")
            print()
            print("Next time you use cmakehub_use() in your project,")
            print("CMakeHub will automatically download the latest versions.")
            print()
            print("To download specific modules now, use:")
            print("  cmakehub update <module_name> --download-now")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error updating modules: {e}", file=sys.stderr)
        return 1
