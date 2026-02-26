# Test 5: Conflict detection
# Verify that conflicting modules are detected and rejected

cmake_minimum_required(VERSION 3.19)

# Disable verbose output
set(CMAKEHUB_VERBOSE OFF CACHE BOOL "")

# Get test directory
get_filename_component(TEST_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)
get_filename_component(PROJECT_ROOT "${TEST_DIR}/../.." ABSOLUTE)

# Include CMakeHub loader
include(${PROJECT_ROOT}/cmake/hub/loader.cmake)

message(STATUS "=== Test: Conflict Detection ===")
message(STATUS "")

# Test 1: Check module conflict declarations
message(STATUS "Test 1: Checking conflict declarations...")
cmakehub_get_module_info(cpm success1)
cmakehub_get_module_property(cpm conflicts conflicts_json)
cmakehub_parse_list("${conflicts_json}" conflicts)

if(success1)
    message(STATUS "✓ cpm module info retrieved")
    if("conan" IN_LIST conflicts AND "vcpkg" IN_LIST conflicts)
        message(STATUS "✓ cpm correctly declares conflicts with: ${conflicts}")
    else()
        message(FATAL_ERROR "✗ cpm conflict list is incorrect: ${conflicts}")
    endif()
else()
    message(FATAL_ERROR "✗ Failed to get cpm module info")
endif()

# Test 2: Check reverse conflicts
message(STATUS "")
message(STATUS "Test 2: Checking reverse conflicts...")
cmakehub_get_module_info(conan success2)
cmakehub_get_module_property(conan conflicts conflicts2_json)
cmakehub_parse_list("${conflicts2_json}" conflicts2)

if(success2)
    message(STATUS "✓ conan module info retrieved")
    if("cpm" IN_LIST conflicts2 AND "vcpkg" IN_LIST conflicts2)
        message(STATUS "✓ conan correctly declares conflicts with: ${conflicts2}")
    else()
        message(FATAL_ERROR "✗ conan conflict list is incorrect: ${conflicts2}")
    endif()
else()
    message(FATAL_ERROR "✗ Failed to get conan module info")
endif()

# Test 3: Verify mutual conflict
message(STATUS "")
message(STATUS "Test 3: Verifying mutual conflict...")
message(STATUS "  cpm conflicts with: ${conflicts}")
message(STATUS "  conan conflicts with: ${conflicts2}")
if("conan" IN_LIST conflicts AND "cpm" IN_LIST conflicts2)
    message(STATUS "✓ Mutual conflict correctly detected")
else()
    message(FATAL_ERROR "✗ Mutual conflict not detected")
endif()

# Test 4: Test with custom conflicting modules
message(STATUS "")
message(STATUS "Test 4: Testing custom conflict scenario...")

# Create test index with custom conflicts
set(test_index "${CMAKE_CURRENT_BINARY_DIR}/test_conflicts.json")
file(WRITE ${test_index}
    "{\n        \"schema_version\": \"1.0\",\n        \"modules\": [\n            {\n                \"name\": \"module_x\",\n                \"description\": \"Module X\",\n                \"category\": \"test\",\n                \"repository\": \"https://github.com/CLIUtils/cmake.git\",\n                \"path\": \"CodeCoverage.cmake\",\n                \"license\": \"MIT\",\n                \"version\": \"master\",\n                \"cmake_minimum_required\": \"3.19\",\n                \"dependencies\": [],\n                \"conflicts\": [\"module_y\"]\n            },\n            {\n                \"name\": \"module_y\",\n                \"description\": \"Module Y\",\n                \"category\": \"test\",\n                \"repository\": \"https://github.com/CLIUtils/cmake.git\",\n                \"path\": \"CodeCoverage.cmake\",\n                \"license\": \"MIT\",\n                \"version\": \"master\",\n                \"cmake_minimum_required\": \"3.19\",\n                \"dependencies\": [],\n                \"conflicts\": [\"module_x\"]\n            }\n        ]\n    }"
)

set(CMAKEHUB_MODULES_INDEX ${test_index})

cmakehub_get_module_info(module_x success3)
cmakehub_get_module_property(module_x conflicts conflicts3_json)
cmakehub_parse_list("${conflicts3_json}" conflicts3)

if("module_y" IN_LIST conflicts3)
    message(STATUS "✓ Custom conflict test passed: module_x conflicts with module_y")
else()
    message(FATAL_ERROR "✗ Custom conflict test failed")
endif()

# Test 5: Verify no conflict case
message(STATUS "")
message(STATUS "Test 5: Verifying no conflict case...")

# Restore original index
set(CMAKEHUB_MODULES_INDEX "${PROJECT_ROOT}/modules.json")

cmakehub_get_module_info(sanitizers success4)
cmakehub_get_module_property(sanitizers conflicts conflicts4_json)
cmakehub_parse_list("${conflicts4_json}" conflicts4)

if(NOT conflicts4 OR conflicts4 STREQUAL "")
    message(STATUS "✓ sanitizers has no conflicts (correct)")
else()
    message(FATAL_ERROR "✗ sanitizers should have no conflicts: ${conflicts4}")
endif()

message(STATUS "")
message(STATUS "=== Test Passed ===")
message(STATUS "Note: Actual conflict enforcement with FetchContent is tested in project mode")
message(STATUS "      This test verifies the conflict detection logic")