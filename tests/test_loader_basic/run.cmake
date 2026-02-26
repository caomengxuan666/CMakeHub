# Test 1: Basic module loading
# Verify that module info can be retrieved and parsed correctly

cmake_minimum_required(VERSION 3.19)

# Disable verbose output for cleaner test output
set(CMAKEHUB_VERBOSE OFF CACHE BOOL "")

# Get test directory
get_filename_component(TEST_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)
get_filename_component(PROJECT_ROOT "${TEST_DIR}/../.." ABSOLUTE)

# Include CMakeHub loader
include(${PROJECT_ROOT}/cmake/hub/loader.cmake)

message(STATUS "=== Test: Basic Module Loading ===")
message(STATUS "")

# Test 1: Get module info
message(STATUS "Test 1: Getting module info...")
cmakehub_get_module_info(sanitizers success)
if(success)
    message(STATUS "✓ Module info retrieved successfully")
else()
    message(FATAL_ERROR "✗ Failed to get module info")
endif()

# Test 2: Get module properties
message(STATUS "")
message(STATUS "Test 2: Getting module properties...")
cmakehub_get_module_property(sanitizers repository repo)
cmakehub_get_module_property(sanitizers description desc)
cmakehub_get_module_property(sanitizers license license)

if(repo AND desc AND license)
    message(STATUS "✓ Module properties retrieved successfully")
    message(STATUS "  Repository: ${repo}")
    message(STATUS "  Description: ${desc}")
    message(STATUS "  License: ${license}")
else()
    message(FATAL_ERROR "✗ Some properties are missing")
endif()

# Test 3: Check version requirements
message(STATUS "")
message(STATUS "Test 3: Checking version requirements...")
cmakehub_get_module_property(sanitizers cmake_minimum_required cmake_min)
if(cmake_min)
    message(STATUS "✓ Version requirement: ${cmake_min}")
    if(CMAKE_VERSION VERSION_GREATER_EQUAL cmake_min)
        message(STATUS "  Current CMake version (${CMAKE_VERSION}) is compatible")
    else()
        message(FATAL_ERROR "  Current CMake version (${CMAKE_VERSION}) is not compatible")
    endif()
else()
    message(STATUS "✓ No version requirement specified")
endif()

# Test 4: Parse empty array
message(STATUS "")
message(STATUS "Test 4: Parsing empty array...")
cmakehub_parse_list("[]" result)
if(NOT result OR result STREQUAL "")
    message(STATUS "✓ Empty array parsed correctly")
else()
    message(FATAL_ERROR "✗ Empty array parsing failed")
endif()

# Test 5: Parse non-empty array
message(STATUS "")
message(STATUS "Test 5: Parsing non-empty array...")
cmakehub_parse_list("[\"item1\", \"item2\"]" result2)
if(result2)
    message(STATUS "✓ Non-empty array parsed correctly: ${result2}")
else()
    message(FATAL_ERROR "✗ Non-empty array parsing failed")
endif()

message(STATUS "")
message(STATUS "=== Test Passed ===")
message(STATUS "Note: Actual module downloading is tested in project mode")
message(STATUS "      Use 'python run_tests.py' to run all tests including download tests")