cmake_minimum_required(VERSION 3.19)
project(CMakeHub_All_Modules_Example VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard")
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include CMakeHub
include(${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/hub/loader.cmake)

# Enable verbose output for debugging
set(CMAKEHUB_VERBOSE TRUE)

# ==============================================================================
# Generate dependency graph for ALL modules
# ==============================================================================

# Generate dependency graph without loading modules (avoids network issues)
cmakehub_dependency_graph_all(${CMAKE_BINARY_DIR}/cmakehub_all_modules.dot)

message(STATUS "")
message(STATUS "==============================================================================")
message(STATUS "Dependency graph generated: ${CMAKE_BINARY_DIR}/cmakehub_all_modules.dot")
message(STATUS "To visualize, run:")
message(STATUS "  dot -Tpng ${CMAKE_BINARY_DIR}/cmakehub_all_modules.dot -o dependencies.png")
message(STATUS "  dot -Tsvg ${CMAKE_BINARY_DIR}/cmakehub_all_modules.dot -o dependencies.svg")
message(STATUS "==============================================================================")
message(STATUS "")

# ==============================================================================
# Simple test target
# ==============================================================================

# Create a dummy target to verify CMake works
add_executable(dummy_target dummy.cpp)
target_include_directories(dummy_target PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Print summary
message(STATUS "")
message(STATUS "==============================================================================")
message(STATUS "CMakeHub All Modules Example")
message(STATUS "==============================================================================")
message(STATUS "This example generates a dependency graph for ALL CMakeHub modules")
message(STATUS "Check the dependency graph to see module relationships")
message(STATUS "==============================================================================")