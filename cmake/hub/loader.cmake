# CMakeHub - Unified CMake Module Manager
# Loader script for managing and loading CMake modules

cmake_minimum_required(VERSION 3.19)

# =============================================================================
# Configuration Variables
# =============================================================================

# Cache directory configuration
if(NOT DEFINED CMH_CACHE_DIR)
    if(DEFINED ENV{CMH_CACHE_DIR})
        set(CMH_CACHE_DIR "$ENV{CMH_CACHE_DIR}" CACHE PATH "CMakeHub cache directory")
    elseif(CMAKE_HOST_WIN32)
        set(CMH_CACHE_DIR "$ENV{USERPROFILE}/.cmakehub/cache" CACHE PATH "CMakeHub cache directory")
    else()
        set(CMH_CACHE_DIR "$ENV{HOME}/.cmakehub/cache" CACHE PATH "CMakeHub cache directory")
    endif()
endif()

# Version check mode: STRICT, WARNING, SILENT
if(NOT DEFINED CMAKEHUB_VERSION_CHECK_MODE)
    set(CMAKEHUB_VERSION_CHECK_MODE "STRICT" CACHE STRING "Version check mode: STRICT, WARNING, SILENT")
endif()

# Verbose mode
if(NOT DEFINED CMAKEHUB_VERBOSE)
    set(CMAKEHUB_VERBOSE FALSE CACHE BOOL "Enable verbose output")
endif()

# Location of modules.json (relative to this file)
get_filename_component(CMAKEHUB_ROOT_DIR "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)
set(CMAKEHUB_MODULES_INDEX "${CMAKEHUB_ROOT_DIR}/modules.json")

# Global property to track used modules
set_property(GLOBAL PROPERTY CMAKEHUB_USED_MODULES "")
set_property(GLOBAL PROPERTY CMAKEHUB_USED_MODULES_BRIEF_DOCS "List of modules used via CMakeHub")
set_property(GLOBAL PROPERTY CMAKEHUB_USED_MODULES_FULL_DOCS "List of module names that have been loaded through CMakeHub")

# =============================================================================
# Internal Helper Functions
# =============================================================================

function(cmakehub_log level message)
    if(CMAKEHUB_VERBOSE OR level STREQUAL "WARNING" OR level STREQUAL "FATAL_ERROR")
        message(${level} "CMakeHub: ${message}")
    endif()
endfunction()

function(cmakehub_get_module_info module_name out_var)
    if(NOT EXISTS ${CMAKEHUB_MODULES_INDEX})
        message(FATAL_ERROR "CMakeHub modules index not found at: ${CMAKEHUB_MODULES_INDEX}")
    endif()

    file(READ ${CMAKEHUB_MODULES_INDEX} index_content)
    
    # JSON parsing
    string(JSON modules_array GET "${index_content}" modules)
    
    set(found FALSE)
    set(module_obj "")
    
    string(JSON modules_length LENGTH "${modules_array}")
    math(EXPR max_index "${modules_length} - 1")
    
    foreach(index RANGE ${max_index})
        string(JSON current_module_obj GET "${modules_array}" ${index})
        string(JSON module_name_check GET "${current_module_obj}" name)
        
        if(module_name_check STREQUAL module_name)
            set(found TRUE)
            set(module_obj "${current_module_obj}")
            break()
        endif()
    endforeach()
    
    if(NOT found)
        message(FATAL_ERROR "Module '${module_name}' not found in CMakeHub index")
    endif()
    
    # Store module info in global properties to avoid semicolon parsing issues
    set_property(GLOBAL PROPERTY "CMH_MODULE_${module_name}_INFO_JSON" "${module_obj}")
    
    # Set result as boolean success indicator
    set(${out_var} TRUE PARENT_SCOPE)
endfunction()

function(cmakehub_get_module_property module_name property out_var)
    # Get the module JSON from property
    get_property(module_json GLOBAL PROPERTY "CMH_MODULE_${module_name}_INFO_JSON")
    
    if(NOT module_json)
        message(FATAL_ERROR "Module '${module_name}' info not found. Call cmakehub_get_module_info first.")
    endif()
    
    # Try to get the property, if it fails set to empty string
    string(JSON value ERROR_VARIABLE property_error GET "${module_json}" ${property})
    if(property_error)
        set(value "")
    endif()
    
    set(${out_var} "${value}" PARENT_SCOPE)
endfunction()

function(cmakehub_parse_list json_list out_list)
    set(result_list "")

    # Check if JSON list is empty
    if(json_list STREQUAL "[]" OR json_list STREQUAL "")
        set(${out_list} "" PARENT_SCOPE)
        return()
    endif()

    string(JSON length LENGTH "${json_list}")
    
    if(length GREATER 0)
        math(EXPR max_index "${length} - 1")
        foreach(index RANGE ${max_index})
            string(JSON item GET "${json_list}" ${index})
            list(APPEND result_list "${item}")
        endforeach()
    endif()
    
    set(${out_list} "${result_list}" PARENT_SCOPE)
endfunction()

function(cmakehub_check_cmake_version required_version)
    if(NOT required_version OR required_version STREQUAL "")
        return()
    endif()
    
    if(CMAKE_VERSION VERSION_LESS required_version)
        if(CMAKEHUB_VERSION_CHECK_MODE STREQUAL "STRICT")
            message(FATAL_ERROR
                "CMake version ${required_version} or higher is required. "
                "Current version: ${CMAKE_VERSION}"
            )
        elseif(CMAKEHUB_VERSION_CHECK_MODE STREQUAL "WARNING")
            message(WARNING
                "CMake version ${required_version} or higher is recommended. "
                "Current version: ${CMAKE_VERSION}. Some features may not work correctly."
            )
        endif()
    endif()
endfunction()

function(cmakehub_check_cpp_standard required_standard)
    if(NOT required_standard OR required_standard STREQUAL "")
        return()
    endif()
    
    # Check if CXX_STANDARD is set
    if(NOT CMAKE_CXX_STANDARD)
        cmakehub_log(WARNING 
            "CMAKE_CXX_STANDARD is not set. Cannot verify C++${required_standard} requirement."
        )
        return()
    endif()
    
    if(CMAKE_CXX_STANDARD LESS required_standard)
        if(CMAKEHUB_VERSION_CHECK_MODE STREQUAL "STRICT")
            message(FATAL_ERROR
                "C++${required_standard} or higher is required. "
                "Current standard: C++${CMAKE_CXX_STANDARD}"
            )
        elseif(CMAKEHUB_VERSION_CHECK_MODE STREQUAL "WARNING")
            message(WARNING
                "C++${required_standard} or higher is recommended. "
                "Current standard: C++${CMAKE_CXX_STANDARD}. Some features may not work correctly."
            )
        endif()
    endif()
endfunction()

function(cmakehub_check_conflicts module_name conflicts_json)
    cmakehub_parse_list("${conflicts_json}" conflict_list)
    
    if(NOT conflict_list)
        return()
    endif()
    
    get_property(used_modules GLOBAL PROPERTY CMAKEHUB_USED_MODULES)
    
    foreach(conflict ${conflict_list})
        if(conflict IN_LIST used_modules)
            message(FATAL_ERROR
                "Module '${module_name}' conflicts with already loaded module '${conflict}'"
            )
        endif()
    endforeach()
endfunction()

function(cmakehub_check_dependencies module_name dependencies_json)
    cmakehub_parse_list("${dependencies_json}" dependency_list)
    
    if(NOT dependency_list)
        return()
    endif()
    
    cmakehub_log(STATUS "Resolving dependencies for '${module_name}': ${dependency_list}")
    
    foreach(dep ${dependency_list})
        cmakehub_log(STATUS "Loading dependency: ${dep}")
        cmakehub_use(${dep})
    endforeach()
endfunction()

# =============================================================================
# Core API Functions
# =============================================================================

function(cmakehub_use module_name)
    cmakehub_log(STATUS "Loading module: ${module_name}")
    
    # Get module information
    cmakehub_get_module_info(${module_name} success)
    if(NOT success)
        message(FATAL_ERROR "Failed to get module info for '${module_name}'")
    endif()
    
    # Extract module properties using property-based access
    cmakehub_get_module_property(${module_name} repository REPOSITORY)
    cmakehub_get_module_property(${module_name} path PATH)
    cmakehub_get_module_property(${module_name} category CATEGORY)
    cmakehub_get_module_property(${module_name} license LICENSE)
    cmakehub_get_module_property(${module_name} description DESCRIPTION)
    cmakehub_get_module_property(${module_name} cmake_minimum_required CMAKE_MINIMUM_REQUIRED)
    cmakehub_get_module_property(${module_name} cpp_minimum_required CPP_MINIMUM_REQUIRED)
    cmakehub_get_module_property(${module_name} dependencies DEPENDENCIES_JSON)
    cmakehub_get_module_property(${module_name} conflicts CONFLICTS_JSON)
    cmakehub_get_module_property(${module_name} version VERSION)
    
    # Set defaults for optional fields
    if(NOT VERSION OR VERSION STREQUAL "")
        set(VERSION "main")
    endif()
    
    if(NOT DEPENDENCIES_JSON OR DEPENDENCIES_JSON STREQUAL "")
        set(DEPENDENCIES_JSON "[]")
    endif()
    
    if(NOT CONFLICTS_JSON OR CONFLICTS_JSON STREQUAL "")
        set(CONFLICTS_JSON "[]")
    endif()
    
    # Version checks
    cmakehub_check_cmake_version("${CMAKE_MINIMUM_REQUIRED}")
    cmakehub_check_cpp_standard("${CPP_MINIMUM_REQUIRED}")
    
    # Check conflicts
    cmakehub_check_conflicts(${module_name} "${CONFLICTS_JSON}")
    
    # Resolve dependencies
    cmakehub_check_dependencies(${module_name} "${DEPENDENCIES_JSON}")

    # Setup cache directory with version to avoid conflicts
    set(module_cache_dir "${CMH_CACHE_DIR}/${module_name}/${VERSION}")
    file(MAKE_DIRECTORY ${module_cache_dir})
    
    # Check if module is already cached
    set(module_file "${module_cache_dir}/${PATH}")
    set(meta_file "${module_cache_dir}/.cmh_meta.json")
    
    if(EXISTS ${module_file} AND EXISTS ${meta_file})
        cmakehub_log(STATUS "Using cached module: ${module_name}")
        
        # Verify metadata
        file(READ ${meta_file} meta_content)
        # In production, verify that the cached version matches expected version
        
    else()
        cmakehub_log(STATUS "Downloading module: ${module_name}")

        # Download using FetchContent
        include(FetchContent)

        FetchContent_Declare(
            ${module_name}
            GIT_REPOSITORY ${REPOSITORY}
            GIT_TAG ${VERSION}
            SOURCE_DIR ${module_cache_dir}
            SUBBUILD_DIR "${module_cache_dir}-subbuild"
        )

        # Check if already populated
        FetchContent_GetProperties(${module_name} POPULATED populated)
        if(NOT populated)
            # Try to download and populate
            FetchContent_MakeAvailable(${module_name})
        endif()

        # Verify population was successful
        FetchContent_GetProperties(${module_name} POPULATED populated)
        if(NOT populated)
            message(FATAL_ERROR "Failed to download module '${module_name}' from ${REPOSITORY}")
        endif()
        
        # Write metadata
        string(TIMESTAMP download_timestamp "%Y-%m-%dT%H:%M:%S")
        file(WRITE ${meta_file}
            "{\n"
            "  \"module\": \"${module_name}\",\n"
            "  \"repository\": \"${REPOSITORY}\",\n"
            "  \"version\": \"${VERSION}\",\n"
            "  \"path\": \"${PATH}\",\n"
            "  \"downloaded_at\": \"${download_timestamp}\"\n"
            "}"
        )
        
        cmakehub_log(STATUS "Module downloaded successfully")
    endif()
    
    # Include the module file
    if(EXISTS ${module_file})
        include(${module_file})
        cmakehub_log(STATUS "Module '${module_name}' loaded successfully")
    else()
        message(FATAL_ERROR 
            "Module file not found at: ${module_file}\n"
            "This might indicate the module structure has changed or the download failed."
        )
    endif()
    
    # Record as used module
    set_property(GLOBAL APPEND PROPERTY CMAKEHUB_USED_MODULES ${module_name})
endfunction()

function(cmakehub_use_category category_name)
    cmakehub_log(STATUS "Loading all modules in category: ${category_name}")
    
    if(NOT EXISTS ${CMAKEHUB_MODULES_INDEX})
        message(FATAL_ERROR "CMakeHub modules index not found at: ${CMAKEHUB_MODULES_INDEX}")
    endif()
    
    file(READ ${CMAKEHUB_MODULES_INDEX} index_content)
    string(JSON modules_array GET "${index_content}" modules)
    
    string(JSON modules_length LENGTH "${modules_array}")
    math(EXPR max_index "${modules_length} - 1")
    
    set(loaded_count 0)
    
    foreach(index RANGE ${max_index})
        string(JSON module_obj GET "${modules_array}" ${index})
        string(JSON module_category GET "${module_obj}" category)
        string(JSON module_name GET "${module_obj}" name)
        
        if(module_category STREQUAL category_name)
            cmakehub_log(STATUS "Loading module: ${module_name}")
            cmakehub_use(${module_name})
            math(EXPR loaded_count "${loaded_count} + 1")
        endif()
    endforeach()
    
    cmakehub_log(STATUS "Loaded ${loaded_count} module(s) from category '${category_name}'")
endfunction()

function(cmakehub_show_licenses)
    cmakehub_log(STATUS "Collecting license information...")
    
    get_property(used_modules GLOBAL PROPERTY CMAKEHUB_USED_MODULES)
    
    if(NOT used_modules)
        message(STATUS "No modules have been loaded via CMakeHub")
        return()
    endif()
    
    message(STATUS "")
    message(STATUS "CMakeHub Module Licenses:")
    message(STATUS "========================")
    
    foreach(module_name ${used_modules})
        # Get module info
        cmakehub_get_module_info(${module_name} success)
        if(success)
            cmakehub_get_module_property(${module_name} license license)
            cmakehub_get_module_property(${module_name} repository repo)
            cmakehub_get_module_property(${module_name} description description)
            
            message(STATUS "")
            message(STATUS "  Module: ${module_name}")
            message(STATUS "  License: ${license}")
            message(STATUS "  Repository: ${repo}")
            if(description)
                message(STATUS "  Description: ${description}")
            endif()
        endif()
    endforeach()
    
    message(STATUS "")
    message(STATUS "Please ensure your project complies with all license requirements.")
endfunction()

function(cmakehub_list_compatible_modules)
    cmakehub_log(STATUS "Listing modules compatible with CMake ${CMAKE_VERSION}...")
    
    if(NOT EXISTS ${CMAKEHUB_MODULES_INDEX})
        message(FATAL_ERROR "CMakeHub modules index not found at: ${CMAKEHUB_MODULES_INDEX}")
    endif()
    
    file(READ ${CMAKEHUB_MODULES_INDEX} index_content)
    string(JSON modules_array GET "${index_content}" modules)
    
    string(JSON modules_length LENGTH "${modules_array}")
    math(EXPR max_index "${modules_length} - 1")
    
    message(STATUS "")
    message(STATUS "Compatible Modules (CMake ${CMAKE_VERSION}):")
    message(STATUS "=======================================")
    
    set(compatible_count 0)
    set(incompatible_count 0)
    
    foreach(index RANGE ${max_index})
        string(JSON module_obj GET "${modules_array}" ${index})
        string(JSON module_name GET "${module_obj}" name)
        string(JSON module_description GET "${module_obj}" description)
        
        # Check version requirement - try to get the property, if it fails set to empty
        string(JSON cmake_min_required ERROR_VARIABLE cmake_min_error GET "${module_obj}" cmake_minimum_required)
        if(cmake_min_error)
            set(cmake_min_required "")
        endif()
        
        if(NOT cmake_min_required OR CMAKE_VERSION VERSION_GREATER_EQUAL cmake_min_required)
            message(STATUS "  ✓ ${module_name} - ${module_description}")
            math(EXPR compatible_count "${compatible_count} + 1")
        else()
            math(EXPR incompatible_count "${incompatible_count} + 1")
        endif()
    endforeach()
    
    message(STATUS "")
    message(STATUS "Compatible: ${compatible_count}, Incompatible: ${incompatible_count}")
endfunction()

function(cmakehub_info module_name)
    cmakehub_log(STATUS "Showing information for module: ${module_name}")
    
    cmakehub_get_module_info(${module_name} success)
    if(NOT success)
        message(FATAL_ERROR "Module '${module_name}' not found")
    endif()
    
    message(STATUS "")
    message(STATUS "Module Information: ${module_name}")
    message(STATUS "=====================")
    
    # Get all properties
    cmakehub_get_module_property(${module_name} name name)
    cmakehub_get_module_property(${module_name} description description)
    cmakehub_get_module_property(${module_name} category category)
    cmakehub_get_module_property(${module_name} author author)
    cmakehub_get_module_property(${module_name} repository repository)
    cmakehub_get_module_property(${module_name} path path)
    cmakehub_get_module_property(${module_name} license license)
    cmakehub_get_module_property(${module_name} version version)
    cmakehub_get_module_property(${module_name} cmake_minimum_required cmake_min)
    cmakehub_get_module_property(${module_name} cpp_minimum_required cpp_min)
    cmakehub_get_module_property(${module_name} stars stars)
    cmakehub_get_module_property(${module_name} last_updated last_updated)
    
    cmakehub_get_module_property(${module_name} dependencies deps_json)
    cmakehub_parse_list("${deps_json}" dependencies)
    
    cmakehub_get_module_property(${module_name} conflicts conflicts_json)
    cmakehub_parse_list("${conflicts_json}" conflicts)
    
    cmakehub_get_module_property(${module_name} tags tags_json)
    cmakehub_parse_list("${tags_json}" tags)
    
    # Display information
    if(name)
        message(STATUS "  Name: ${name}")
    endif()
    if(description)
        message(STATUS "  Description: ${description}")
    endif()
    if(category)
        message(STATUS "  Category: ${category}")
    endif()
    if(author)
        message(STATUS "  Author: ${author}")
    endif()
    if(repository)
        message(STATUS "  Repository: ${repository}")
    endif()
    if(path)
        message(STATUS "  Path: ${path}")
    endif()
    if(license)
        message(STATUS "  License: ${license}")
    endif()
    if(version)
        message(STATUS "  Version: ${version}")
    endif()
    if(cmake_min)
        message(STATUS "  CMake Minimum: ${cmake_min}")
    endif()
    if(cpp_min)
        message(STATUS "  C++ Minimum: ${cpp_min}")
    endif()
    if(stars)
        message(STATUS "  Stars: ${stars}")
    endif()
    if(last_updated)
        message(STATUS "  Last Updated: ${last_updated}")
    endif()
    
    if(dependencies)
        message(STATUS "  Dependencies: ${dependencies}")
    endif()
    
    if(conflicts)
        message(STATUS "  Conflicts: ${conflicts}")
    endif()
    
    if(tags)
        message(STATUS "  Tags: ${tags}")
    endif()
    
    message(STATUS "")
endfunction()

# =============================================================================
# Initialization
# =============================================================================

cmakehub_log(STATUS "CMakeHub initialized")
cmakehub_log(STATUS "Cache directory: ${CMH_CACHE_DIR}")
cmakehub_log(STATUS "Modules index: ${CMAKEHUB_MODULES_INDEX}")
cmakehub_log(STATUS "Version check mode: ${CMAKEHUB_VERSION_CHECK_MODE}")