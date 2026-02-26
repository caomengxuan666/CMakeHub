#!/usr/bin/env python3
"""
Add a new module to CMakeHub modules.json

Usage:
    python add_module.py --name <name> --repo <repo> --path <path> [options]

Example:
    python add_module.py --name my_module --repo https://github.com/user/repo.git --path cmake/MyModule.cmake --category utils
"""

import argparse
import json
import sys
from pathlib import Path


def validate_url(url):
    """Validate GitHub repository URL"""
    if not url.startswith('https://github.com/'):
        print(f"Error: Repository must be a GitHub URL (https://github.com/...)")
        return False
    if not url.endswith('.git'):
        print(f"Error: Repository URL must end with .git")
        return False
    return True


def validate_path(path):
    """Validate module path"""
    if not path.endswith('.cmake'):
        print(f"Error: Module path must end with .cmake")
        return False
    return True


def add_module(args):
    """Add a new module to modules.json"""
    # Validate inputs
    if not validate_url(args.repo):
        return 1
    if not validate_path(args.path):
        return 1

    # Read modules.json
    modules_json_path = Path(__file__).parent.parent / 'modules.json'
    with open(modules_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if module already exists
    existing = next((m for m in data['modules'] if m['name'] == args.name), None)
    if existing:
        print(f"Error: Module '{args.name}' already exists!")
        return 1

    # Create new module
    new_module = {
        'name': args.name,
        'description': args.description,
        'category': args.category,
        'author': args.author,
        'repository': args.repo,
        'path': args.path,
        'license': args.license,
        'stars': args.stars,
        'last_updated': args.last_updated,
        'version': args.version,
        'cmake_minimum_required': args.cmake_min,
        'cpp_minimum_required': args.cpp_min,
        'dependencies': args.dependencies.split(',') if args.dependencies else [],
        'conflicts': args.conflicts.split(',') if args.conflicts else [],
        'tags': args.tags.split(',') if args.tags else []
    }

    # Add module
    data['modules'].append(new_module)

    # Sort modules by name
    data['modules'].sort(key=lambda x: x['name'])

    # Write back
    with open(modules_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully added module: {args.name}")
    print(f"Total modules: {len(data['modules'])}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Add a new module to CMakeHub modules.json',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Required arguments
    parser.add_argument('--name', required=True, help='Module name (e.g., sanitizers)')
    parser.add_argument('--repo', required=True, help='GitHub repository URL (e.g., https://github.com/user/repo.git)')
    parser.add_argument('--path', required=True, help='Module path in repository (e.g., cmake/MyModule.cmake)')

    # Optional arguments with defaults
    parser.add_argument('--description', default='CMake module', help='Module description')
    parser.add_argument('--category', default='utils', help='Module category (e.g., code_quality, build_optimization)')
    parser.add_argument('--author', default='unknown', help='Module author')
    parser.add_argument('--license', default='MIT', help='Module license (e.g., MIT, Apache-2.0, BSD3)')
    parser.add_argument('--stars', type=int, default=0, help='GitHub stars')
    parser.add_argument('--last-updated', default='2024-01-01', help='Last updated date (YYYY-MM-DD)')
    parser.add_argument('--version', default='master', help='Git version (branch/tag)')
    parser.add_argument('--cmake-min', default='3.14', help='Minimum CMake version')
    parser.add_argument('--cpp-min', default='', help='Minimum C++ version')
    parser.add_argument('--dependencies', default='', help='Comma-separated dependencies')
    parser.add_argument('--conflicts', default='', help='Comma-separated conflicts')
    parser.add_argument('--tags', default='', help='Comma-separated tags')

    args = parser.parse_args()

    # Add module
    return add_module(args)


if __name__ == '__main__':
    sys.exit(main())