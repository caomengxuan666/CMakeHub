# Basic CMakeHub Example
# This example demonstrates how to use CMakeHub to load modules

cmake_minimum_required(VERSION 3.19)
project(CMakeHubBasicExample VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable verbose output for demonstration
option(CMAKEHUB_VERBOSE "Enable CMakeHub verbose output" ON)

# Include CMakeHub loader
# Note: This assumes CMakeHub is located at ../../ relative to this example
include(${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/hub/loader.cmake)

# Load CMakeHub modules
# Enable sanitizers for development builds
cmakehub_use(sanitizers)

# Enable code coverage
#cmakehub_use(coverage)

# Create a simple executable
add_executable(${PROJECT_NAME} main.cpp)

# Set compile options
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -pedantic)
endif()

# Enable sanitizers for the target (if available)
if(COMMAND enable_sanitizers)
    enable_sanitizers(${PROJECT_NAME} ADDRESS UNDEFINED)
    message(STATUS "Sanitizers enabled for ${PROJECT_NAME}")
else()
    message(WARNING "enable_sanitizers command not found. Sanitizers may not be properly configured.")
endif()

# Enable coverage (if available)
if(COMMAND setup_target_for_coverage)
    # Note: The actual function name may vary depending on the coverage module
    message(STATUS "Coverage setup command available")
else()
    message(WARNING "Coverage setup command not found. Coverage may not be properly configured.")
endif()


cmakehub_dependency_graph(dependencies.dot)


# Print information about loaded modules
message(STATUS "")
message(STATUS "=== CMakeHub Example ===")
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "")

# Show licenses of used modules
cmakehub_show_licenses()

message(STATUS "")
message(STATUS "Build the project with:")
message(STATUS "  mkdir build && cd build")
message(STATUS "  cmake ..")
message(STATUS "  cmake --build .")
message(STATUS "")
message(STATUS "Run with sanitizers:")
message(STATUS "  cmake --build . --target ${PROJECT_NAME}")
message(STATUS "  ./${PROJECT_NAME}")
message(STATUS "")