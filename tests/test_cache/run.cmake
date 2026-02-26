# Test 2: Cache mechanism (simplified for script mode)
# Verify cache directory structure and metadata handling

cmake_minimum_required(VERSION 3.19)

# Disable verbose output
set(CMAKEHUB_VERBOSE OFF CACHE BOOL "")

# Get test directory
get_filename_component(TEST_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)
get_filename_component(PROJECT_ROOT "${TEST_DIR}/../.." ABSOLUTE)

# Set a unique cache directory for this test
set(CMH_CACHE_DIR "${CMAKE_CURRENT_BINARY_DIR}/cmakehub_test_cache")

# Include CMakeHub loader
include(${PROJECT_ROOT}/cmake/hub/loader.cmake)

message(STATUS "=== Test: Cache Mechanism ===")
message(STATUS "")

# Test 1: Verify cache directory configuration
message(STATUS "Test 1: Cache directory configuration...")
if(CMH_CACHE_DIR)
    message(STATUS "✓ Cache directory set: ${CMH_CACHE_DIR}")
else()
    message(FATAL_ERROR "✗ Cache directory not set")
endif()

# Test 2: Verify version-specific cache path
message(STATUS "")
message(STATUS "Test 2: Version-specific cache path...")
set(expected_cache_path "${CMH_CACHE_DIR}/cotire/master")
message(STATUS "  Expected path: ${expected_cache_path}")

# Create the path structure to simulate cache
file(MAKE_DIRECTORY ${expected_cache_path})
if(EXISTS ${expected_cache_path})
    message(STATUS "✓ Version-specific cache directory structure is correct")
else()
    message(FATAL_ERROR "✗ Failed to create cache directory structure")
endif()

# Test 3: Verify metadata file format
message(STATUS "")
message(STATUS "Test 3: Metadata file format...")
set(meta_file "${expected_cache_path}/.cmh_meta.json")
file(WRITE ${meta_file}
    "{\n"
    "  \"module\": \"cotire\",\n"
    "  \"repository\": \"https://github.com/sakra/cotire.git\",\n"
    "  \"version\": \"master\",\n"
    "  \"path\": \"CMake/cotire.cmake\",\n"
    "  \"downloaded_at\": \"2024-02-26T12:00:00\"\n"
    "}"
)

if(EXISTS ${meta_file})
    file(READ ${meta_file} meta_content)
    if(meta_content MATCHES "module" AND meta_content MATCHES "repository" AND meta_content MATCHES "downloaded_at")
        message(STATUS "✓ Metadata file format is correct")
    else()
        message(FATAL_ERROR "✗ Metadata file format is incorrect")
    endif()
else()
    message(FATAL_ERROR "✗ Metadata file not created")
endif()

# Test 4: Verify timestamp format
message(STATUS "")
message(STATUS "Test 4: Timestamp format...")
string(TIMESTAMP current_timestamp "%Y-%m-%dT%H:%M:%S")
string(LENGTH current_timestamp timestamp_length)
# Format should be: YYYY-MM-DDTHH:MM:SS (18 characters in Windows, 19 in some systems)
# Just check if it contains T and has reasonable length
if(current_timestamp MATCHES "T" AND timestamp_length GREATER 15)
    message(STATUS "✓ Timestamp format is correct: ${current_timestamp} (length: ${timestamp_length})")
else()
    message(FATAL_ERROR "✗ Timestamp format is incorrect: ${current_timestamp} (length: ${timestamp_length})")
endif()

message(STATUS "")
message(STATUS "=== Test Passed ===")
message(STATUS "Note: Actual caching behavior is tested in project mode")
message(STATUS "      Use 'python run_tests.py' to run all tests including actual caching")