# CMakeHub Project Structure

This document describes the directory structure of CMakeHub.

## Root Directory

```
D:\codespace\CMakeHub\
├── .github/              # GitHub Actions CI/CD workflows
│   └── workflows/
│       └── ci.yml        # Automated testing workflow
├── cmake/                # CMakeHub core
│   └── hub/
│       └── loader.cmake  # Main module loader
├── docs/                 # Documentation
│   ├── CONTRIBUTING.md   # Contribution guidelines
│   └── RELEASE_CHECKLIST.md  # Release preparation checklist
├── examples/             # Usage examples
│   ├── basic/            # Basic usage example
│   │   ├── CMakeLists.txt
│   │   ├── main.cpp
│   │   └── README.md
│   └── CMakeLists.txt
├── scripts/              # Utility scripts
│   └── pre_release_check.py  # Pre-release verification script
├── tests/                # Test suite
│   ├── test_cache/       # Cache mechanism tests
│   ├── test_conflicts/   # Conflict detection tests
│   ├── test_dependencies/# Dependency resolution tests
│   ├── test_loader_basic/# Basic loading tests
│   ├── test_version_check/# Version checking tests
│   ├── CMakeLists.txt
│   ├── run_tests.py      # Full test suite runner
│   ├── run_single_test.py  # Single test runner
│   └── verify_modules.cmake  # Module path verification
├── .gitignore            # Git ignore rules
├── CMakeLists.txt        # Root CMake configuration
├── LICENSE               # Apache 2.0 license
├── modules.json          # Module index (20 modules)
├── PROJECT_STRUCTURE.md  # This file
└── README.md             # Main documentation
```

## Key Components

### Core (`cmake/hub/`)
- **loader.cmake**: The main module loader that handles:
  - Module discovery and loading
  - Dependency resolution
  - Conflict detection
  - Version checking
  - Caching

### Documentation (`docs/`)
- **CONTRIBUTING.md**: How to contribute to CMakeHub
- **RELEASE_CHECKLIST.md**: Steps for creating a release

### Examples (`examples/`)
- **basic/**: Simple example showing how to use CMakeHub with sanitizers and coverage

### Scripts (`scripts/`)
- **pre_release_check.py**: Verifies project is ready for release

### Tests (`tests/`)
- Five core test categories:
  - **test_loader_basic**: Basic module loading
  - **test_cache**: Cache mechanism
  - **test_version_check**: Version checking
  - **test_dependencies**: Dependency resolution
  - **test_conflicts**: Conflict detection

## Module Index (`modules.json`)

Contains metadata for 20 curated CMake modules:
- Build optimization (cotire, ccache, unity_build)
- Code quality (sanitizers, coverage, clang_tidy)
- Debugging (memory_leak, launchers, compiler_info)
- Packaging (install_helpers, cpack_extras)
- Dependency management (CPM, vcpkg, conan)
- Platform (android, ios)
- Testing (catch2, benchmark)
- Documentation (doxygen)
- Utilities (auto_version)

## Getting Started

1. Read [README.md](README.md) for quick start
2. Check [examples/basic/](examples/basic/) for usage examples
3. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) to contribute
4. Run tests: `python tests/run_tests.py`