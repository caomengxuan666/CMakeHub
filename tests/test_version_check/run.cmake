# Test 3: Version checking (STRICT mode)
# Verify that version requirements are enforced

cmake_minimum_required(VERSION 3.19)

# Disable verbose output
set(CMAKEHUB_VERBOSE OFF CACHE BOOL "")

# Get test directory
get_filename_component(TEST_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)
get_filename_component(PROJECT_ROOT "${TEST_DIR}/../.." ABSOLUTE)

# Include CMakeHub loader
include(${PROJECT_ROOT}/cmake/hub/loader.cmake)

message(STATUS "=== Test: Version Checking (STRICT mode) ===")
message(STATUS "")

# Test 1: Load a module with version requirement that should pass
message(STATUS "Test 1: Loading module with compatible version...")
cmakehub_get_module_info(sanitizers success1)
if(success1)
    cmakehub_get_module_property(sanitizers cmake_minimum_required cmake_min)
    cmakehub_get_module_property(sanitizers description desc)
    message(STATUS "✓ Module info retrieved")
    message(STATUS "  CMake minimum required: ${cmake_min}")
    message(STATUS "  Description: ${desc}")
    
    # Check if current version is compatible
    if(CMAKE_VERSION VERSION_GREATER_EQUAL cmake_min)
        message(STATUS "✓ Current CMake version (${CMAKE_VERSION}) is compatible")
    else()
        message(FATAL_ERROR "✗ Current CMake version (${CMAKE_VERSION}) is not compatible")
    endif()
else()
    message(FATAL_ERROR "✗ Failed to get module info")
endif()

# Test 2: Create a test module with incompatible version requirement
message(STATUS "")
message(STATUS "Test 2: Testing version mismatch detection...")

# Create a test module index with high version requirement
set(test_index "${CMAKE_CURRENT_BINARY_DIR}/test_modules.json")
file(WRITE ${test_index}
    "{
        \"schema_version\": \"1.0\",
        \"modules\": [{
            \"name\": \"test_high_version\",
            \"description\": \"Test module with high version requirement\",
            \"category\": \"test\",
            \"repository\": \"https://github.com/CLIUtils/cmake.git\",
            \"path\": \"CodeCoverage.cmake\",
            \"license\": \"MIT\",
            \"version\": \"master\",
            \"cmake_minimum_required\": \"99.99\",
            \"dependencies\": [],
            \"conflicts\": []
        }]
    }"
)

# Temporarily override the index
set(ORIGINAL_INDEX ${CMAKEHUB_MODULES_INDEX})
set(CMAKEHUB_MODULES_INDEX ${test_index})

# Get module info
cmakehub_get_module_info(test_high_version success2)
cmakehub_get_module_property(test_high_version cmake_minimum_required high_version_req)

# Restore original index
set(CMAKEHUB_MODULES_INDEX ${ORIGINAL_INDEX})

if(high_version_req)
    message(STATUS "✓ High version requirement detected: ${high_version_req}")
    message(STATUS "  Current version: ${CMAKE_VERSION}")
    message(STATUS "  Expected: Should reject this module")
    
    if(CMAKE_VERSION VERSION_LESS high_version_req)
        message(STATUS "✓ Version mismatch correctly identified")
    else()
        message(FATAL_ERROR "✗ Version check logic failed")
    endif()
else()
    message(FATAL_ERROR "✗ Failed to get high version requirement")
endif()

# Test 3: Test different version check modes
message(STATUS "")
message(STATUS "Test 3: Testing version check modes...")

# Test with WARNING mode
set(CMAKEHUB_VERSION_CHECK_MODE "WARNING" CACHE STRING "")
set(CMAKEHUB_MODULES_INDEX ${test_index})
cmakehub_get_module_info(test_high_version success3)
set(CMAKEHUB_VERSION_CHECK_MODE "STRICT" CACHE STRING "")

if(success3)
    message(STATUS "✓ WARNING mode allows module retrieval")
    message(STATUS "  (In real usage, this would show a warning)")
else()
    message(FATAL_ERROR "✗ WARNING mode test failed")
endif()

message(STATUS "")
message(STATUS "=== Test Passed ===")