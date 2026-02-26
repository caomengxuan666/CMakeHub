# CMakeHub Test Suite
# This directory contains tests for CMakeHub core functionality

cmake_minimum_required(VERSION 3.19)
project(CMakeHubTests LANGUAGES NONE)

enable_testing()

# Include CMakeHub loader
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../cmake/hub" ${CMAKE_MODULE_PATH})
include(${CMAKE_CURRENT_SOURCE_DIR}/../cmake/hub/loader.cmake)

# Test 1: Basic module loading
add_test(NAME loader_basic COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/test_loader_basic/run.cmake)

# Test 2: Cache mechanism
add_test(NAME cache_mechanism COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/test_cache/run.cmake)

# Test 3: Version checking (STRICT mode)
add_test(NAME version_check_strict COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/test_version_check/run.cmake)

# Test 4: Dependency resolution
add_test(NAME dependency_resolution COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/test_dependencies/run.cmake)

# Test 5: Conflict detection
add_test(NAME conflict_detection COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/test_conflicts/run.cmake)

# Test 6: Example build
add_test(NAME example_build COMMAND ${CMAKE_COMMAND} --build ${CMAKE_CURRENT_BINARY_DIR}/example_build)

message(STATUS "CMakeHub tests configured")
message(STATUS "Run tests with: ctest --test-dir <build_dir> --output-on-failure")