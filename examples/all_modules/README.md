# CMakeHub All Modules Example

This example loads **ALL** available CMakeHub modules to demonstrate the dependency graph generation.

## Purpose

- Test that all modules can be loaded successfully
- Generate a comprehensive dependency graph
- Show module relationships and dependencies

## Build

```bash
cd examples/all_modules
mkdir build && cd build
cmake ..
```

## Output

After building, you'll find:

1. **Dependency Graph**: `build/cmakehub_all_modules.dot`
   - Visual representation of all module relationships
   - Shows connections from CMakeHub to each module
   - Shows inter-module dependencies (dashed lines)

2. **Visualization**: Convert DOT to PNG
   ```bash
   dot -Tpng cmakehub_all_modules.dot -o dependencies.png
   ```

## Note

Some modules may not be compatible with your platform or CMake version.
The example is designed to work with CMake 3.19+ and C++17 on most platforms.

Modules that may have issues:
- `cuda`: Requires CUDA toolkit
- `conan`: Requires Conan package manager
- `android_toolchain`: Cross-compilation for Android
- `ios_toolchain`: Cross-compilation for iOS

These will be skipped automatically if requirements are not met.