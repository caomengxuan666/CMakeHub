"""
Init project - Initialize a new project with CMakeHub
"""

import os
import shutil
import sys


def get_loader_path():
    """Get the path to loader.cmake"""
    possible_paths = [
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "cmake",
            "hub",
            "loader.cmake",
        ),
        os.path.join(os.getcwd(), "cmake", "hub", "loader.cmake"),
        os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ),
            "cmake",
            "hub",
            "loader.cmake",
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("loader.cmake not found. Are you in a CMakeHub project directory?")


def init_project(args):
    """Initialize a new project with CMakeHub"""
    try:
        project_name = args.name
        project_dir = os.path.join(os.getcwd(), project_name)

        # Check if project directory already exists
        if os.path.exists(project_dir):
            print(f"Error: Directory '{project_name}' already exists", file=sys.stderr)
            return 1

        # Create project structure
        print(f"Initializing project: {project_name}")
        print("-" * 80)

        # Create project directory
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, "cmake", "hub"))
        os.makedirs(os.path.join(project_dir, "src"))

        print(f"✓ Created directory structure")

        # Copy loader.cmake
        loader_path = get_loader_path()
        loader_dest = os.path.join(project_dir, "cmake", "hub", "loader.cmake")
        shutil.copy(loader_path, loader_dest)
        print(f"✓ Copied loader.cmake to cmake/hub/")

        # Create CMakeLists.txt
        cmake_content = f"""cmake_minimum_required(VERSION 3.19)
project({project_name} VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard")
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include CMakeHub
include(${{CMAKE_CURRENT_SOURCE_DIR}}/cmake/hub/loader.cmake)

# Enable testing
enable_testing()

# Add your modules here
# cmakehub_use(sanitizers)
# cmakehub_use(coverage)

# Add source files
file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE HEADERS "src/*.h")

# Create executable
add_executable(${{PROJECT_NAME}} ${{SOURCES}} ${{HEADERS}})

# Target settings
target_include_directories(${{PROJECT_NAME}} PUBLIC
    ${{CMAKE_CURRENT_SOURCE_DIR}}/src
)

# Optional: Install rules
install(TARGETS ${{PROJECT_NAME}}
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
"""

        with open(os.path.join(project_dir, "CMakeLists.txt"), "w", encoding="utf-8") as f:
            f.write(cmake_content)
        print(f"✓ Created CMakeLists.txt")

        # Create main.cpp
        main_content = f"""#include <iostream>
#include <string>

int main(int argc, char* argv[]) {{
    std::cout << "Hello from {project_name}!" << std::endl;
    std::cout << "CMake version: " << CMAKE_VERSION << std::endl;
    return 0;
}}
"""

        with open(os.path.join(project_dir, "src", "main.cpp"), "w", encoding="utf-8") as f:
            f.write(main_content)
        print(f"✓ Created src/main.cpp")

        # Create .gitignore
        gitignore_content = """# Build directories
build/
cmake-build-*/
out/

# CMake
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
Makefile
*.cmake

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# CMakeHub cache
.cmakehub/

# OS
.DS_Store
Thumbs.db
"""

        with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print(f"✓ Created .gitignore")

        # Create README.md
        readme_content = f"""# {project_name}

A C++ project initialized with CMakeHub.

## Build

```bash
mkdir build && cd build
cmake ..
cmake --build .
./{project_name}
```

## Adding Modules

Use the CMakeHub CLI to add modules:

```bash
# List available modules
cmakehub list

# Search for modules
cmakehub search sanitizer

# Add a module
cmakehub use sanitizers --append CMakeLists.txt

# Check module compatibility
cmakehub check sanitizers
```

## Features

- CMake 3.19+
- C++17 standard
- CMakeHub integration
- Testing enabled

## License

[Your License Here]
"""

        with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"✓ Created README.md")

        print()
        print("=" * 80)
        print(f"✅ Project '{project_name}' initialized successfully!")
        print("=" * 80)
        print()
        print(f"Next steps:")
        print(f"  1. cd {project_name}")
        print(f"  2. mkdir build && cd build")
        print(f"  3. cmake ..")
        print(f"  4. cmake --build .")
        print(f"  5. ./{project_name}")
        print()
        print(f"To add CMakeHub modules:")
        print(f"  cmakehub use <module_name> --append CMakeLists.txt")
        print()

        return 0

    except Exception as e:
        print(f"Error initializing project: {e}", file=sys.stderr)
        # Clean up if failed
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        return 1
