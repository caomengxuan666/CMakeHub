"""
Cache management
"""

import os
import shutil
import json
import sys


def get_cache_dir():
    """Get the CMakeHub cache directory"""
    # Check environment variable first
    if 'CMH_CACHE_DIR' in os.environ:
        return os.environ['CMH_CACHE_DIR']
    
    # Default locations
    if os.name == 'nt':  # Windows
        cache_dir = os.path.join(os.environ.get('USERPROFILE', '~'), '.cmakehub', 'cache')
    else:  # Unix-like
        cache_dir = os.path.join(os.environ.get('HOME', '~'), '.cmakehub', 'cache')
    
    return os.path.expanduser(cache_dir)


def cache_manager(args):
    """Manage CMakeHub cache"""
    try:
        cache_dir = get_cache_dir()
        
        if not os.path.exists(cache_dir):
            print(f"Cache directory does not exist: {cache_dir}")
            return 0
        
        if args.cache_action == 'info':
            # Show cache information
            print("=" * 80)
            print("Cache Information")
            print("=" * 80)
            print()
            print(f"Cache Directory: {cache_dir}")
            print()
            
            # Count modules in cache
            modules = [d for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))]
            
            if not modules:
                print("Cache is empty")
                return 0
            
            total_size = 0
            total_files = 0
            
            print(f"Cached Modules ({len(modules)}):")
            print("-" * 80)
            
            for module_name in sorted(modules):
                module_dir = os.path.join(cache_dir, module_name)
                module_size = 0
                module_files = 0
                
                for root, dirs, files in os.walk(module_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        module_size += os.path.getsize(file_path)
                        module_files += 1
                
                total_size += module_size
                total_files += module_files
                
                # Format size
                size_mb = module_size / (1024 * 1024)
                print(f"  {module_name}")
                print(f"    Size: {size_mb:.2f} MB ({module_size:,} bytes)")
                print(f"    Files: {module_files}")
                
                # Show versions
                versions = [d for d in os.listdir(module_dir) if os.path.isdir(os.path.join(module_dir, d))]
                if versions:
                    print(f"    Versions: {', '.join(versions)}")
                print()
            
            # Total statistics
            total_size_mb = total_size / (1024 * 1024)
            print(f"Total: {total_size_mb:.2f} MB ({total_size:,} bytes) in {total_files} files")
            
        elif args.cache_action == 'clear':
            # Clear cache
            if args.module:
                # Clear specific module cache
                module_cache_dir = os.path.join(cache_dir, args.module)
                
                if not os.path.exists(module_cache_dir):
                    print(f"Module cache not found: {args.module}")
                    return 0
                
                if not args.force:
                    # Ask for confirmation
                    response = input(f"Are you sure you want to clear cache for '{args.module}'? [y/N]: ")
                    if response.lower() not in ['y', 'yes']:
                        print("Cancelled")
                        return 0
                
                shutil.rmtree(module_cache_dir)
                print(f"Cache cleared for module: {args.module}")
                
            else:
                # Clear all cache
                if not args.force:
                    # Ask for confirmation
                    response = input(f"Are you sure you want to clear ALL cache in {cache_dir}? [y/N]: ")
                    if response.lower() not in ['y', 'yes']:
                        print("Cancelled")
                        return 0
                
                # Remove all module caches
                modules = [d for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))]
                
                for module_name in modules:
                    module_dir = os.path.join(cache_dir, module_name)
                    shutil.rmtree(module_dir)
                    print(f"Cleared cache for: {module_name}")
                
                print(f"\nCache directory cleared: {cache_dir}")
        
        return 0
    
    except Exception as e:
        print(f"Error managing cache: {e}", file=sys.stderr)
        return 1