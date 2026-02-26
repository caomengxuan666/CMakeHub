# Module Path Verification Script
# This script verifies that all modules in modules.json have valid paths

cmake_minimum_required(VERSION 3.19)

message(STATUS "=== CMakeHub Module Path Verification ===")
message(STATUS "")

# Get root directory (tests/../)
get_filename_component(ROOT_DIR "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)

# Read modules.json from root directory
file(READ "${ROOT_DIR}/modules.json" index_content)
string(JSON modules_array GET "${index_content}" modules)
string(JSON modules_length LENGTH "${modules_array}")

set(total_count 0)
set(valid_count 0)
set(invalid_count 0)

message(STATUS "Verifying ${modules_length} modules...")
message(STATUS "")

math(EXPR max_index "${modules_length} - 1")

foreach(index RANGE ${max_index})
    string(JSON module_obj GET "${modules_array}" ${index})
    string(JSON module_name GET "${module_obj}" name)
    string(JSON repository GET "${module_obj}" repository)
    string(JSON path GET "${module_obj}" path)
    string(JSON version GET "${module_obj}" version)

    math(EXPR total_count "${total_count} + 1")

    # Construct full URL
    string(REPLACE ".git" "" repo_no_git "${repository}")
    string(REPLACE "https://github.com/" "https://raw.githubusercontent.com/" raw_url "${repo_no_git}/${version}/${path}")

    message(STATUS "[${total_count}/${modules_length}] Checking ${module_name}...")
    message(STATUS "  Repository: ${repository}")
    message(STATUS "  Path: ${path}")
    message(STATUS "  URL: ${raw_url}")

    # Try to fetch the file
    file(DOWNLOAD ${raw_url} "${CMAKE_CURRENT_BINARY_DIR}/temp_verify_${module_name}.cmake"
        STATUS download_status
        TLS_VERIFY ON
        TIMEOUT 10
    )

    list(GET download_status 0 status_code)

    if(status_code EQUAL 0)
        message(STATUS "  Result: [OK] VALID")
        math(EXPR valid_tmp "${valid_count} + 1")
        set(valid_count ${valid_tmp})
        # Clean up
        file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/temp_verify_${module_name}.cmake")
    else()
        message(STATUS "  Result: [X] INVALID (status: ${status_code})")
        math(EXPR invalid_tmp "${invalid_count} + 1")
        set(invalid_count ${invalid_tmp})
    endif()

    message(STATUS "")
endforeach()

message(STATUS "========================================")
message(STATUS "Verification Summary:")
message(STATUS "  Total modules: ${total_count}")
message(STATUS "  Valid paths:   ${valid_count}")
message(STATUS "  Invalid paths: ${invalid_count}")
message(STATUS "========================================")

if(invalid_count GREATER 0)
    message(WARNING "Some modules have invalid paths. Please review the output above.")
else()
    message(STATUS "All module paths are valid!")
endif()