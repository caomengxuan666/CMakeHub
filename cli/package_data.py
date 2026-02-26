"""
Package data utilities for CMakeHub CLI
"""

import os
import sys
import json


def get_package_data_path(filename):
    """
    Get the path to a file in the package data directory.
    Falls back to the repository root if running from source.
    """
    # Try to find the file in the package data directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(package_dir, "data")

    # First, try package data directory
    package_path = os.path.join(data_dir, filename)
    if os.path.exists(package_path):
        return package_path

    # Fallback: try repository root (for development)
    repo_root = os.path.dirname(os.path.dirname(package_dir))
    repo_path = os.path.join(repo_root, filename)
    if os.path.exists(repo_path):
        return repo_path

    # For loader.cmake, try cmake/hub/ subdirectory
    if filename == "loader.cmake":
        loader_package_path = os.path.join(data_dir, "cmake", "hub", filename)
        if os.path.exists(loader_package_path):
            return loader_package_path

        loader_repo_path = os.path.join(repo_root, "cmake", "hub", filename)
        if os.path.exists(loader_repo_path):
            return loader_repo_path

    raise FileNotFoundError(f"{filename} not found in package data or repository root")


def load_modules_json():
    """Load modules.json from package data"""
    modules_json_path = get_package_data_path("modules.json")

    with open(modules_json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_loader_path():
    """Get the path to loader.cmake"""
    return get_package_data_path("loader.cmake")


def get_licenses_path():
    """Get the path to THIRD_PARTY_LICENSES.md"""
    return get_package_data_path("THIRD_PARTY_LICENSES.md")