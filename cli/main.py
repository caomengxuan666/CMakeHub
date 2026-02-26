#!/usr/bin/env python
"""
CMakeHub CLI - Main entry point
"""

import argparse
import sys
import os

# Add parent directory to path to import from commands
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from commands import list as cmd_list
from commands import search as cmd_search
from commands import info as cmd_info
from commands import cache as cmd_cache
from commands import check as cmd_check
from commands import update as cmd_update
from commands import use as cmd_use
from commands import init as cmd_init


def main():
    """Main entry point for cmakehub CLI"""
    parser = argparse.ArgumentParser(
        prog='cmakehub',
        description='CMakeHub - Unified CMake Module Manager CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cmakehub list                    List all available modules
  cmakehub search sanitizer        Search for modules
  cmakehub info sanitizers         Show module details
  cmakehub cache info              Show cache information
  cmakehub cache clear             Clear all cache
  cmakehub cache clear sanitizers  Clear specific module cache
  cmakehub check sanitizers        Check module compatibility
  cmakehub update                  Update all modules
  cmakehub update sanitizers       Update specific module
  cmakehub update sanitizers --download-now  Update and download now
  cmakehub use sanitizers           Generate CMake configuration
  cmakehub use sanitizers --append CMakeLists.txt  Append to file
  cmakehub init myproject          Initialize new project with CMakeHub

For more information, visit: https://github.com/caomengxuan666/CMakeHub
        """
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all available modules')
    list_parser.add_argument('--category', '-c', help='Filter by category')
    list_parser.add_argument('--compact', action='store_true', help='Compact output')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for modules')
    search_parser.add_argument('keyword', help='Search keyword')
    search_parser.add_argument('--category', '-c', help='Filter by category')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show module information')
    info_parser.add_argument('module', help='Module name')
    info_parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose information')
    
    # Cache command
    cache_parser = subparsers.add_parser('cache', help='Cache management')
    cache_subparsers = cache_parser.add_subparsers(dest='cache_action', help='Cache actions')
    
    cache_subparsers.add_parser('info', help='Show cache information')
    
    cache_clear_parser = cache_subparsers.add_parser('clear', help='Clear cache')
    cache_clear_parser.add_argument('module', nargs='?', help='Module name (optional, clear all if not specified)')
    cache_clear_parser.add_argument('--force', '-f', action='store_true', help='Force clear without confirmation')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check module compatibility')
    check_parser.add_argument('module', help='Module name')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update modules')
    update_parser.add_argument('module', nargs='?', help='Module name (optional, update all if not specified)')
    update_parser.add_argument('--download-now', action='store_true', help='Download module immediately')
    
    # Use command
    use_parser = subparsers.add_parser('use', help='Generate CMake configuration for using a module')
    use_parser.add_argument('module', help='Module name')
    use_parser.add_argument('--version', '-v', help='Specify module version')
    use_parser.add_argument('--output', '-o', help='Write configuration to file')
    use_parser.add_argument('--append', '-a', help='Append configuration to file')
    use_parser.add_argument('--test', '-t', action='store_true', help='Test module download')
    use_parser.add_argument('options', nargs='*', help='Module options (e.g., ADDRESS_SANITIZER ON)')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new project with CMakeHub')
    init_parser.add_argument('name', help='Project name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute command
    try:
        if args.command == 'list':
            return cmd_list.list_modules(args)
        elif args.command == 'search':
            return cmd_search.search_modules(args)
        elif args.command == 'info':
            return cmd_info.show_info(args)
        elif args.command == 'cache':
            return cmd_cache.cache_manager(args)
        elif args.command == 'check':
            return cmd_check.check_compatibility(args)
        elif args.command == 'update':
            return cmd_update.update_modules(args)
        elif args.command == 'use':
            return cmd_use.use_module(args)
        elif args.command == 'init':
            return cmd_init.init_project(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())