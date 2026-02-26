# CMakeHub Module Documentation

CMakeHub provides 61+ curated CMake modules for modern C++ development.

## Table of Contents

### Categories

- [build_optimization](#build-optimization)
- [code_quality](#code-quality)
- [debugging](#debugging)
- [dependency](#dependency)
- [docs](#docs)
- [packaging](#packaging)
- [platform](#platform)
- [testing](#testing)
- [utils](#utils)

## build_optimization

Build speed optimization tools

- **[c_standards](c_standards.md)**: C standards configuration
- **[compile_options](compile_options.md)**: Compiler options management
- **[cotire](cotire.md)**: Automates precompiled header (PCH) and unity build generation
- **[cpp_standards](cpp_standards.md)**: C++ standards configuration
- **[lto_optimization](lto_optimization.md)**: Link Time Optimization (LTO/IPO) support
- **[precompiled_header](precompiled_header.md)**: Precompiled header setup for CMake (alternative to cotire)
## code_quality

Static analysis, sanitizers, coverage

- **[clang_tidy_cg](clang_tidy_cg.md)**: Clang-Tidy integration from cginternals cmake-init
- **[clang_tidy_tools](clang_tidy_tools.md)**: clang-tidy, IWYU, and cppcheck integration tools
- **[code_coverage_bilke](code_coverage_bilke.md)**: Code coverage from bilke/cmake-modules
- **[code_formatter](code_formatter.md)**: clang-format and cmake-format integration
- **[compiler_warnings](compiler_warnings.md)**: Compiler warning and option helpers
- **[coverage](coverage.md)**: Code coverage support using gcov/lcov for C/C++ projects
- **[coverage_cg](coverage_cg.md)**: Code coverage from cginternals cmake-init
- **[cppcheck_cg](cppcheck_cg.md)**: Cppcheck integration from cginternals cmake-init
- **[gcov](gcov.md)**: Gcov coverage tool
- **[sanitizers](sanitizers.md)**: Sanitizer integration (ASan, UBSan, TSan, MSan) for C/C++ projects
## debugging

Debugging helpers and tools

- **[compiler_info](compiler_info.md)**: Get detailed compiler information and version strings
- **[launchers](launchers.md)**: Create launcher scripts for easy execution in IDEs
## dependency

Dependency management tools

- **[conan](conan.md)**: Conan package manager integration
- **[cpm](cpm.md)**: Lightweight CMake package manager
## docs

docs

- **[dependency_graph](dependency_graph.md)**: Generate dependency graphs for CMake projects
- **[doxygen_helper](doxygen_helper.md)**: Doxygen documentation generation helper
## packaging

Installation and packaging helpers

- **[component_install](component_install.md)**: Component installation helper
- **[install_helpers](install_helpers.md)**: Simplified install rules and helpers
- **[runtime_dependencies](runtime_dependencies.md)**: Runtime dependencies management
## platform

Platform-specific tools

- **[android_toolchain](android_toolchain.md)**: Android NDK toolchain file
- **[cuda](cuda.md)**: CUDA integration helper
- **[glsl_shaders](glsl_shaders.md)**: GLSL shader compilation support
- **[ios_toolchain](ios_toolchain.md)**: iOS/macOS/watchOS/tvOS toolchain file
- **[use_folders](use_folders.md)**: Enable USE_FOLDERS property for MSVC projects
## testing

Testing frameworks integration

- **[add_gtest](add_gtest.md)**: Google Test integration helper
- **[afl_fuzzing](afl_fuzzing.md)**: AFL fuzzing instrumentation
- **[catch2_cmake](catch2_cmake.md)**: Catch2 testing framework CMake integration
- **[doctest](doctest.md)**: Doctest testing framework integration
- **[find_or_build_gtest](find_or_build_gtest.md)**: Find GTest or build from source
## utils

Utility functions

- **[bin2cpp](bin2cpp.md)**: Convert files to C++ for embedding
- **[check_function](check_function.md)**: Check if function exists in compiler
- **[cmake_checks](cmake_checks.md)**: CMake checks cache helper modules
- **[embed_resources](embed_resources.md)**: Embed resources (files) into C++ executables
- **[export_header](export_header.md)**: Generate template export header
- **[find_assimp](find_assimp.md)**: Find ASSIMP 3D model library
- **[find_curl](find_curl.md)**: Find cURL library
- **[find_egl](find_egl.md)**: Find EGL library
- **[find_ffmpeg](find_ffmpeg.md)**: Find FFMPEG library
- **[find_glesv2](find_glesv2.md)**: Find OpenGL ES 2.0 library
- **[find_glew](find_glew.md)**: Find GLEW OpenGL library
- **[find_gtk3](find_gtk3.md)**: Find GTK3 library
- **[find_gtk4](find_gtk4.md)**: Find GTK4 library
- **[find_hidapi](find_hidapi.md)**: Find HIDAPI library
- **[find_jpeg](find_jpeg.md)**: Find JPEG library
- **[find_libevent](find_libevent.md)**: Find libevent library
- **[find_nodejs](find_nodejs.md)**: Find Node.js
- **[find_png](find_png.md)**: Find PNG library
- **[find_sdl2](find_sdl2.md)**: Find SDL2 library
- **[find_sqlite](find_sqlite.md)**: Find SQLite database library
- **[find_vulkan](find_vulkan.md)**: Find Vulkan library
- **[find_zlib](find_zlib.md)**: Find zlib compression library
- **[git_version](git_version.md)**: Get git revision description for version management
- **[pycmake](pycmake.md)**: Python module version checking for CMake
- **[qt_helper](qt_helper.md)**: Qt integration helper
- **[target_utils](target_utils.md)**: Target utility helpers
