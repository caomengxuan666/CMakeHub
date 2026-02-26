"""
Setup script for CMakeHub CLI
Metadata is provided by pyproject.toml
"""

from setuptools import setup, find_packages

# Only keep build-related configurations, metadata is provided by pyproject.toml
setup(
    packages=find_packages(),
    zip_safe=False,
    # Note: Do not write name, version, description, etc. here!
)
