"""
Setup script for CMakeHub CLI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cmakehub",
    version="0.1.0",
    author="CMakeHub Team",
    author_email="caomengxuan666@github.com",
    description="CMakeHub - Unified CMake Module Manager CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caomengxuan666/CMakeHub",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - pure Python + subprocess calls
    ],
    entry_points={
        "console_scripts": [
            "cmakehub=cli.main:main",
        ],
    },
)