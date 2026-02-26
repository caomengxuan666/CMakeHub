# CMakeHub Advanced Usage Example
cmake_minimum_required(VERSION 3.19)
project(AdvancedExample VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include CMakeHub
include(${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/hub/loader.cmake)

# Example 1: Module with config parameters (配置穿透)
message(STATUS "=== Example 1: Config Parameters ===")
cmakehub_use(sanitizers
    ADDRESS_SANITIZER ON
    UNDEFINED_SANITIZER ON
)

# Example 2: Module with specific version (版本选择)
message(STATUS "=== Example 2: Version Selection ===")
cmakehub_use(cotire VERSION "master")

# Example 3: List all available modules (模块发现)
message(STATUS "=== Example 3: List All Modules ===")
# cmakehub_list()  # Uncomment to see all modules

# Example 4: Search for modules
message(STATUS "=== Example 4: Search Modules ===")
# cmakehub_search(sanitizer)  # Uncomment to search for sanitizer modules

# Example 5: Load all modules from a category
message(STATUS "=== Example 5: Load by Category ===")
# cmakehub_use_category(code_quality)  # Uncomment to load all code quality modules

# Example 6: Module information
message(STATUS "=== Example 6: Module Info ===")
cmakehub_info(sanitizers)

# Example 7: Cache management
message(STATUS "=== Example 7: Cache Management ===")
# cmakehub_cache_info()  # Uncomment to see cache info
# cmakehub_cache_clear(sanitizers)  # Uncomment to clear specific module cache

# Example 8: Dependency graph
message(STATUS "=== Example 8: Dependency Graph ===")
# cmakehub_dependency_graph(dependencies.dot)  # Uncomment to generate graph

# Example 9: Update modules
message(STATUS "=== Example 9: Update Modules ===")
# cmakehub_update(sanitizers)  # Uncomment to update specific module

# Example 10: Compatibility check
message(STATUS "=== Example 10: Compatibility Check ===")
cmakehub_check_compatibility(sanitizers)

# Example 11: Show licenses
message(STATUS "=== Example 11: Licenses ===")
# cmakehub_show_licenses()  # Uncomment to show all licenses

# Example 12: List compatible modules
message(STATUS "=== Example 12: Compatible Modules ===")
# cmakehub_list_compatible_modules()  # Uncomment to list compatible modules

# Create a simple executable
add_executable(main main.cpp)
target_link_libraries(main PRIVATE ${CMAKE_DL_LIBS})

# Example 13: Resource embedding
message(STATUS "=== Example 13: Resource Embedding ===")
cmakehub_use(embed_resources)
# Uncomment below to embed resources
# add_embedded_binary_resources(
#   resources
#   OUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/generated
#   HEADER resources.hpp
#   NAMESPACE resources
#   RESOURCE_NAMES config
#   RESOURCES ${CMAKE_CURRENT_SOURCE_DIR}/config.json
# )
# target_sources(main PRIVATE generated/resources.cpp)
# target_include_directories(main PRIVATE generated)

# Example 14: Code coverage
message(STATUS "=== Example 14: Code Coverage ===")
cmakehub_use(coverage_cg)

# Example 15: Compiler warnings
message(STATUS "=== Example 15: Compiler Warnings ===")
cmakehub_use(compiler_warnings)