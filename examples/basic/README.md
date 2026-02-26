# Basic CMakeHub Example

This example demonstrates the basic usage of CMakeHub with sanitizers and code coverage modules.

---

## What This Example Does

This example:
1. Loads CMakeHub
2. Enables sanitizers (Address Sanitizer and Undefined Behavior Sanitizer)
3. Sets up code coverage reporting
4. Provides test code that can trigger sanitizers

---

## Prerequisites

- CMake 3.19 or higher
- A C++ compiler with sanitizer support (GCC 7+, Clang 8+, or MSVC 2019+)
- For coverage: lcov (Linux) or appropriate coverage tools

---

## Building

### Linux/macOS

```bash
mkdir build
cd build
cmake ..
make
```

### Windows (Visual Studio)

```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### Windows (MinGW)

```bash
mkdir build
cd build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

---

## Running

```bash
# Run the executable
./CMakeHubBasicExample  # Linux/macOS
CMakeHubBasicExample.exe  # Windows
```

---

## Testing Sanitizers

The example includes code that can trigger sanitizers:

### To Test Memory Leak Detection

1. Uncomment the memory leak code in `main.cpp`:
   ```cpp
   // Uncomment this to test memory leak detection
   // int* leaked = new int[100];
   // (void)leaked;  // Suppress unused warning
   ```

2. Rebuild with sanitizers enabled:
   ```bash
   cd build
   cmake ..
   cmake --build .
   ```

3. Run the executable:
   ```bash
   ./CMakeHubBasicExample
   ```

4. You should see a memory leak report from the sanitizer.

### To Test Buffer Overflow

1. Uncomment the buffer overflow code in `main.cpp`:
   ```cpp
   // Uncomment this to test buffer overflow detection
   // int arr[10];
   // arr[10] = 42;  // Buffer overflow
   ```

2. Rebuild and run. The sanitizer should detect the overflow.

---

## Code Coverage

### Generate Coverage Report (Linux with lcov)

```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build .

# Run tests to generate coverage data
ctest

# Generate coverage report
lcov --capture --directory . --output-file coverage.info
lcov --remove coverage.info '/usr/*' --output-file coverage_filtered.info
genhtml coverage_filtered.info --output-directory coverage_report

# View report
open coverage_report/index.html  # macOS
xdg-open coverage_report/index.html  # Linux
```

### Coverage on Windows

Use Visual Studio's built-in code coverage tools or other Windows-compatible coverage tools.

---

## CMakeLists.txt Explanation

```cmake
# Include CMakeHub
include(${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/hub/loader.cmake)

# Load sanitizers module
cmakehub_use(sanitizers)

# Load coverage module
cmakehub_use(coverage)

# Enable sanitizers for the project
if(COMMAND enable_sanitizers)
    enable_sanitizers(${PROJECT_NAME} ADDRESS UNDEFINED)
    message(STATUS "Sanitizers enabled for ${PROJECT_NAME}")
endif()

# Set up coverage
if(COMMAND setup_target_for_coverage)
    setup_target_for_coverage(${PROJECT_NAME}
        COVERAGE_TARGET coverage
        EXECUTABLE_NAME ${PROJECT_NAME}
    )
endif()
```

---

## Understanding the Code

### main.cpp

The example program:
1. Prints a greeting message
2. Demonstrates Fibonacci calculation
3. Includes optional code for testing sanitizers
4. Shows memory management patterns

### CMakeLists.txt

The CMake configuration:
1. Sets up the project
2. Loads CMakeHub modules
3. Enables sanitizers
4. Configures code coverage
5. Builds the example executable

---

## Troubleshooting

### Sanitizers Not Working

- **Linux/macOS**: Ensure you're using GCC 7+ or Clang 8+
- **Windows**: Ensure you're using MSVC 2019+ with sanitizer support
- **Check**: Verify that sanitizers are actually enabled by checking compiler flags

### Coverage Not Working

- **Linux**: Install lcov: `sudo apt install lcov` (Ubuntu) or `brew install lcov` (macOS)
- **Check**: Ensure you're building in Debug mode: `cmake -DCMAKE_BUILD_TYPE=Debug ..`

### Build Errors

- **CMake version**: Ensure you have CMake 3.19 or higher: `cmake --version`
- **CMakeHub path**: Verify the path to CMakeHub is correct
- **Network**: Ensure you have internet connection to download modules

---

## Next Steps

- Try loading other modules from CMakeHub
- Experiment with different sanitizers (Thread Sanitizer, Memory Sanitizer)
- Add more test cases to demonstrate module features
- Explore other examples (when available)

---

## References

- [CMakeHub README](../../README.md)
- [Sanitizers Documentation](https://github.com/google/sanitizers)
- [Code Coverage with lcov](https://ltp.sourceforge.net/coverage/lcov.php)

---

## License

This example is part of CMakeHub and is licensed under the Apache License 2.0.