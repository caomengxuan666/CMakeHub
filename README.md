# CMakeHub

<div align="center">

**Unified CMake Module Manager**

[![CI](https://github.com/caomengxuan666/CMakeHub/workflows/CMakeHub%20CI/badge.svg)](https://github.com/caomengxuan666/CMakeHub/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CMake](https://img.shields.io/badge/CMake-3.19+-blue.svg)](https://cmake.org)

*A centralized repository for discovering, selecting, and integrating third-party CMake modules.*

</div>

---

## What is CMakeHub?

CMakeHub is a unified CMake module manager that provides a "central warehouse" for CMake modules. It solves the problem of scattered CMake modules across different GitHub repositories, making it easy to discover, select, and integrate them into your projects.

**Important**: CMakeHub is **not** a package manager like vcpkg or Conan. It's a module manager that helps you find and use CMake modules more easily.

---

## Features

- 🔍 **Unified Discovery**: Browse and search for CMake modules in one place
- 🚀 **Simple Integration**: Load modules with a single command
- 🔄 **Automatic Dependencies**: Modules automatically declare and load their dependencies
- ⚠️ **Conflict Detection**: Prevents loading incompatible modules
- ✅ **Version Checking**: Ensures compatibility with your CMake and C++ versions
- 💾 **Smart Caching**: Download once, use everywhere (shared across projects)
- 📄 **License Management**: Automatically track module licenses for compliance

---

## Quick Start

### Installation

```bash
# Clone CMakeHub
git clone https://github.com/caomengxuan666/CMakeHub.git
cd CMakeHub

# Or add as a submodule
git submodule add https://github.com/caomengxuan666/CMakeHub.git cmake/cmakehub
```

### Basic Usage

```cmake
# In your CMakeLists.txt
cmake_minimum_required(VERSION 3.19)
project(MyProject CXX)

# Include CMakeHub
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmakehub/loader.cmake)

# Load modules
cmakehub_use(sanitizers)
cmakehub_use(coverage)

# Now use the modules' features
enable_testing()
add_executable(myapp main.cpp)
target_link_libraries(myapp PRIVATE mylib)
```

### Configuration Options

```cmake
# Set cache directory (optional)
set(CMH_CACHE_DIR "$ENV{HOME}/.cmakehub/cache")

# Enable verbose output (optional)
set(CMAKEHUB_VERBOSE ON)

# Set version check mode (STRICT, WARNING, SILENT)
set(CMAKEHUB_VERSION_CHECK_MODE "STRICT")
```

---

## Available Modules

CMakeHub includes 20 curated CMake modules organized by category:

### Build Optimization
- **cotire**: Precompiled headers and unity builds
- **ccache**: Compiler cache integration
- **unity_build**: Unity build support

### Code Quality
- **sanitizers**: ASan, UBSan, TSan, MSan integration
- **coverage**: Code coverage with gcov/lcov
- **clang_tidy**: Static analysis integration

### Debugging
- **memory_leak**: MSVC memory leak detection
- **launchers**: Create launcher scripts for IDEs
- **compiler_info**: Get compiler information

### Packaging
- **install_helpers**: Installation helpers
- **cpack_extras**: CPack configuration helpers

### Dependency Management
- **CPM**: Lightweight CMake package manager
- **vcpkg**: vcpkg integration
- **conan**: Conan integration

### Platform
- **android**: Android toolchain helpers
- **ios**: iOS toolchain helpers

### Testing
- **catch2**: Catch2 testing framework
- **benchmark**: Google Benchmark integration

### Documentation
- **doxygen**: Doxygen documentation helpers

### Utilities
- **auto_version**: Automatic version management

---

## API Reference

### cmakehub_use(module_name [VERSION version])

Load a CMake module.

```cmake
cmakehub_use(sanitizers)
cmakehub_use(cotire VERSION 1.0.0)  # Specify version
```

### cmakehub_use_category(category_name)

Load all modules in a category.

```cmake
cmakehub_use_category(code_quality)
```

### cmakehub_show_licenses()

Display licenses of all loaded modules.

```cmake
cmakehub_show_licenses()
```

### cmakehub_list_compatible_modules()

List all modules compatible with current CMake version.

```cmake
cmakehub_list_compatible_modules()
```

### cmakehub_info(module_name)

Display detailed information about a module.

```cmake
cmakehub_info(sanitizers)
```

---

## Examples

See the `examples/` directory for complete examples:

- `examples/basic/`: Basic usage with sanitizers and coverage

Run the example:

```bash
cd examples/basic
mkdir build && cd build
cmake ..
cmake --build .
./myapp
```

---

## Testing

Run the test suite:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test
python tests/run_single_test.py test_loader_basic
python tests/run_single_test.py test_cache
python tests/run_single_test.py test_version_check
python tests/run_single_test.py test_dependencies
python tests/run_single_test.py test_conflicts
```

---

## Requirements

- **CMake**: 3.19 or higher
- **Python**: 3.6 or higher (for tests only)
- **Internet connection**: Required for downloading modules

---

## Cache Mechanism

CMakeHub caches downloaded modules in `~/.cmakehub/cache/` (or `%USERPROFILE%/.cmakehub/cache/` on Windows). Cache is shared across projects, so you only download each module once.

Cache structure:
```
~/.cmakehub/cache/
├── sanitizers/
│   └── master/
│       ├── sanitizers.cmake
│       └── .cmh_meta.json
└── cotire/
    └── master/
        ├── CMake/
        │   └── cotire.cmake
        └── .cmh_meta.json
```

---

## Version Checking

CMakeHub automatically checks module requirements:

- **CMake version**: Ensures your CMake version meets the module's minimum requirement
- **C++ standard**: Warns if the module requires a higher C++ standard

Version check modes:
- **STRICT** (default): Fails on version mismatch
- **WARNING**: Shows a warning but continues
- **SILENT**: Disables version checking

---

## Dependency Management

Modules can declare dependencies:

```json
{
  "name": "module_a",
  "dependencies": ["module_b", "module_c"]
}
```

When you load `module_a`, CMakeHub automatically loads `module_b` and `module_c` first.

---

## Conflict Detection

Modules can declare conflicts:

```json
{
  "name": "cpm",
  "conflicts": ["conan", "vcpkg"]
}
```

If you try to load `cpm` and `conan` together, CMakeHub will show an error.

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

**Note**: Each module has its own license. Use `cmakehub_show_licenses()` to view all licenses and ensure compliance.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## Roadmap

- [ ] v0.2: Add more modules, improve path verification
- [ ] v1.0: Stable API, advanced features
- [ ] v1.1: Web interface, IDE plugins

---

## Acknowledgments

CMakeHub is built on the work of many talented CMake module authors:

- [CLIUtils/cmake](https://github.com/CLIUtils/cmake)
- [sakra/cotire](https://github.com/sakra/cotire)
- [rpavlik/cmake-modules](https://github.com/rpavlik/cmake-modules)
- [cpm-cmake/CPM.cmake](https://github.com/cpm-cmake/CPM.cmake)
- [conan-io/cmake-conan](https://github.com/conan-io/cmake-conan)
- [catchorg/Catch2](https://github.com/catchorg/Catch2)
- [google/benchmark](https://github.com/google/benchmark)

And many others!

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=caomengxuan666/CMakeHub&type=Date)](https://star-history.com/#caomengxuan666/CMakeHub&Date)

---

<div align="center">

Made with ❤️ by the CMakeHub community

[⬆ Back to Top](#cmakehub)

</div>