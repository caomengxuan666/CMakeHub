# Advanced CMakeHub Usage Example

This example demonstrates advanced features of CMakeHub.

## Features Demonstrated

### 1. Config Parameters (配置穿透)
Pass parameters directly to modules:
```cmake
cmakehub_use(sanitizers
    ADDRESS_SANITIZER ON
    UNDEFINED_SANITIZER ON
)
```

### 2. Version Selection (版本选择)
Specify which version of a module to use:
```cmake
cmakehub_use(cotire VERSION "master")
```

### 3. Module Discovery
List all available modules:
```cmake
cmakehub_list()
```

Search for modules:
```cmake
cmakehub_search(sanitizer)
```

### 4. Load by Category
Load all modules from a specific category:
```cmake
cmakehub_use_category(code_quality)
```

### 5. Module Information
Get detailed information about a module:
```cmake
cmakehub_info(sanitizers)
```

### 6. Cache Management
View cache information:
```cmake
cmakehub_cache_info()
```

Clear cache for a specific module:
```cmake
cmakehub_cache_clear(sanitizers)
```

Clear all cache:
```cmakehub_cache_clear()
```

### 7. Dependency Graph
Generate a DOT graph of module dependencies:
```cmake
cmakehub_dependency_graph(dependencies.dot)
```

### 8. Update Modules
Update a specific module:
```cmake
cmakehub_update(sanitizers)
```

Update all used modules:
```cmakehub_update()
```

### 9. Compatibility Check
Check if your system is compatible with a module:
```cmake
cmakehub_check_compatibility(sanitizers)
```

### 10. Show Licenses
Display licenses of all used modules:
```cmake
cmakehub_show_licenses()
```

### 11. List Compatible Modules
List all modules compatible with your CMake version:
```cmake
cmakehub_list_compatible_modules()
```

### 12. Resource Embedding
Embed files into your executable:
```cmake
cmakehub_use(embed_resources)
add_embedded_binary_resources(
  resources
  OUT_DIR generated
  HEADER resources.hpp
  NAMESPACE resources
  RESOURCE_NAMES config
  RESOURCES config.json
)
```

### 13. Code Coverage
Set up code coverage:
```cmake
cmakehub_use(coverage_cg)
```

### 14. Compiler Warnings
Configure compiler warnings:
```cmake
cmakehub_use(compiler_warnings)
```

## Building

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## Running

```bash
./AdvancedExample  # Linux/macOS
AdvancedExample.exe  # Windows
```

## Notes

- Uncomment the features you want to try in CMakeLists.txt
- Some features (like dependency graph) require additional tools (e.g., Graphviz for DOT files)
- Resource embedding requires the `xxd` program to be available
- Check [module documentation](../../docs/modules/) for more details on each module