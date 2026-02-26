"""
Update modules - Must call CMake to re-download modules
"""

import os
import shutil
import json
import sys
import subprocess


def get_modules_json():
    """Get the path to modules.json"""
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'modules.json'),
        os.path.join(os.getcwd(), 'modules.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'modules.json'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError("modules.json not found. Are you in a CMakeHub project directory?")


def get_cache_dir():
    """Get the CMakeHub cache directory"""
    if 'CMH_CACHE_DIR' in os.environ:
        return os.environ['CMH_CACHE_DIR']
    
    if os.name == 'nt':  # Windows
        cache_dir = os.path.join(os.environ.get('USERPROFILE', '~'), '.cmakehub', 'cache')
    else:  # Unix-like
        cache_dir = os.path.join(os.environ.get('HOME', '~'), '.cmakehub', 'cache')
    
    return os.path.expanduser(cache_dir)


def get_loader_path():
    """Get the path to loader.cmake"""
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'cmake', 'hub', 'loader.cmake'),
        os.path.join(os.getcwd(), 'cmake', 'hub', 'loader.cmake'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'cmake', 'hub', 'loader.cmake'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError("loader.cmake not found. Are you in a CMakeHub project directory?")


def download_module_now(module_name, version=None):
    """立即下载模块（不等待项目使用）"""
    try:
        loader_path = get_loader_path()
        
        # Create temporary CMake script to download module
        # Normalize path for CMake (use forward slashes)
        loader_path_normalized = loader_path.replace('\\', '/')
        
        cmake_script = f'''cmake_minimum_required(VERSION 3.19)

# Include CMakeHub
include("{loader_path_normalized}")

# Download module now
set(CMAKEHUB_VERBOSE TRUE)
cmakehub_use({module_name})
'''
        
        # Write temporary script
        temp_script = os.path.join(os.path.dirname(__file__), 'temp_download_module.cmake')
        with open(temp_script, 'w') as f:
            f.write(cmake_script)
        
        try:
            # Run CMake to download
            print(f"Downloading {module_name}...")
            result = subprocess.run(
                ['cmake', '-P', temp_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✓ Module '{module_name}' downloaded successfully")
                return True
            else:
                print(f"✗ Failed to download module: {result.stderr}", file=sys.stderr)
                return False
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_script):
                os.remove(temp_script)
                
    except Exception as e:
        print(f"✗ Error downloading module: {e}", file=sys.stderr)
        return False


def update_modules(args):
    """Update modules by clearing cache and optionally downloading"""
    try:
        modules_json_path = get_modules_json()
        cache_dir = get_cache_dir()
        loader_path = get_loader_path()
        
        with open(modules_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modules = data.get('modules', [])
        
        if args.module:
            # Update specific module
            module = None
            for m in modules:
                if m['name'] == args.module:
                    module = m
                    break
            
            if not module:
                print(f"Error: Module '{args.module}' not found", file=sys.stderr)
                return 1
            
            print(f"Updating module: {module['name']}")
            print("-" * 80)
            
            # Step 1: Clear Python cache (file operation - can be done in Python)
            module_cache_dir = os.path.join(cache_dir, module['name'])
            if os.path.exists(module_cache_dir):
                print(f"Clearing cache for {module['name']}...")
                shutil.rmtree(module_cache_dir)
                print(f"  ✓ Cache cleared")
            else:
                print(f"  No existing cache found")
            
            # Step 2: Download now if requested
            if args.download_now:
                print()
                download_module_now(module['name'], module.get('version'))
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
                cached_modules = [d for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))]
                
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