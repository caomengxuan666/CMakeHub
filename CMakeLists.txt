cmake_minimum_required(VERSION 3.19)
project(CMakeHub VERSION 0.1.0 LANGUAGES NONE)

# CMakeHub - Unified CMake Module Manager
# This project itself is used for development and testing purposes.

# Options
option(CMAKEHUB_BUILD_EXAMPLES "Build CMakeHub examples" ON)
option(CMAKEHUB_BUILD_TESTS "Build CMakeHub tests" ON)

# Export CMakeHub modules path for internal use
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/hub" ${CMAKE_MODULE_PATH})

# Include CMakeHub loader for self-testing
include(${CMAKE_SOURCE_DIR}/cmake/hub/loader.cmake)

set(CMAKEHUB_VERBOSE ON)

set(CMAKEHUB_VERSION_CHECK_MODE "STRICT")

# Add subdirectories
if(CMAKEHUB_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

if(CMAKEHUB_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Installation
install(DIRECTORY cmake/
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/cmakehub
    FILES_MATCHING PATTERN "*.cmake"
)

install(FILES modules.json
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/cmakehub
)

# CPack configuration
set(CPACK_PACKAGE_NAME "CMakeHub")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Unified CMake Module Manager")
set(CPACK_PACKAGE_VENDOR "CMakeHub Contributors")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE")
set(CPACK_RESOURCE_FILE_README "${CMAKE_SOURCE_DIR}/README.md")

include(CPack)