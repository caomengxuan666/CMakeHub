#!/usr/bin/env python3
"""
Enhanced module validation script
Checks all modules for validity, accessibility, and completeness
"""

import json
import requests
import sys
from pathlib import Path
from urllib.parse import urljoin


def validate_module(module):
    """Validate a single module"""
    results = {"name": module["name"], "valid": True, "issues": [], "warnings": []}

    # Check required fields
    required_fields = ["name", "description", "category", "repository", "path", "license"]
    for field in required_fields:
        if field not in module or not module[field]:
            results["valid"] = False
            results["issues"].append(f"Missing required field: {field}")

    # Check repository URL format
    repo = module.get("repository", "")
    if not repo.startswith("https://github.com/"):
        results["valid"] = False
        results["issues"].append(f"Invalid repository URL: {repo}")
    if not repo.endswith(".git"):
        results["valid"] = False
        results["issues"].append(f"Repository URL must end with .git: {repo}")

    # Check path format
    path = module.get("path", "")
    if not path.endswith(".cmake"):
        results["warnings"].append(f"Module path should end with .cmake: {path}")

    # Check stars is a number
    stars = module.get("stars")
    if stars is not None and not isinstance(stars, int):
        results["warnings"].append(f"Stars should be an integer: {stars}")

    # Check version
    version = module.get("version", "")
    if not version:
        results["warnings"].append(f"Module has no version specified")

    return results


def check_module_accessibility(module, timeout=10):
    """Check if module file is accessible"""
    results = {"name": module["name"], "accessible": False, "status_code": None, "error": None}

    repo = module["repository"].replace(".git", "")
    path = module["path"]
    raw_url = f"https://raw.githubusercontent.com/{repo.split('/')[-2]}/{repo.split('/')[-1]}/{module.get('version', 'master')}/{path}"

    try:
        response = requests.head(raw_url, timeout=timeout)
        results["status_code"] = response.status_code
        results["accessible"] = response.status_code == 200

        if response.status_code != 200:
            results["error"] = f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        results["error"] = "Timeout"
    except requests.exceptions.RequestException as e:
        results["error"] = str(e)

    return results


def validate_all_modules(modules_json_path):
    """Validate all modules in modules.json"""
    print(f"Reading modules from: {modules_json_path}")

    with open(modules_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modules = data["modules"]
    print(f"Found {len(modules)} modules")

    # Validate module structure
    print("\n=== Module Structure Validation ===")
    validation_results = []
    for module in modules:
        result = validate_module(module)
        validation_results.append(result)

        if result["valid"]:
            print(f"✓ {result['name']}")
        else:
            print(f"✗ {result['name']}")
            for issue in result["issues"]:
                print(f"  - {issue}")

        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"  ⚠ {warning}")

    # Check accessibility
    print("\n=== Module Accessibility Check ===")
    print("Checking module file accessibility (this may take a while)...")
    accessibility_results = []

    for module in modules:
        result = check_module_accessibility(module)
        accessibility_results.append(result)

        if result["accessible"]:
            print(f"✓ {result['name']}")
        else:
            status_info = result["error"] if result["error"] else f"HTTP {result['status_code']}"
            print(f"✗ {result['name']} - {status_info}")

    # Summary
    valid_count = sum(1 for r in validation_results if r["valid"])
    accessible_count = sum(1 for r in accessibility_results if r["accessible"])

    print("\n=== Summary ===")
    print(f"Total modules: {len(modules)}")
    print(f"Valid structure: {valid_count}/{len(modules)}")
    print(f"Accessible: {accessible_count}/{len(modules)}")

    # Check for duplicate modules
    print("\n=== Duplicate Check ===")
    module_names = [m["name"] for m in modules]
    duplicates = [name for name in set(module_names) if module_names.count(name) > 1]
    if duplicates:
        print(f"✗ Found duplicate modules: {', '.join(duplicates)}")
    else:
        print("✓ No duplicate modules found")

    # Check for missing categories
    print("\n=== Category Check ===")
    categories = set(m["category"] for m in modules)
    defined_categories = set(data.get("categories", {}).keys())
    missing_categories = categories - defined_categories
    if missing_categories:
        print(f"⚠ Modules use undefined categories: {', '.join(missing_categories)}")
    else:
        print("✓ All module categories are defined")

    # Overall result
    print("\n=== Overall Result ===")
    all_valid = valid_count == len(modules) and accessible_count == len(modules)

    if all_valid:
        print("✓ All modules are valid and accessible")
        return 0
    else:
        print("✗ Some modules have issues")
        return 1


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    modules_json = project_root / "modules.json"

    if not modules_json.exists():
        print(f"Error: modules.json not found at {modules_json}")
        sys.exit(1)

    result = validate_all_modules(modules_json)
    sys.exit(result)
