#include <algorithm>
#include <iostream>
#include <vector>

// Simple function to demonstrate sanitizers and coverage
std::vector<int> generate_fibonacci(int n) {
    if (n <= 0) return {};
    if (n == 1) return {0};
    if (n == 2) return {0, 1};

    std::vector<int> fib(n);
    fib[0] = 0;
    fib[1] = 1;

    for (int i = 2; i < n; ++i) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }

    return fib;
}

// Function with potential buffer overflow for sanitizer testing
void unsafe_array_access(int index) {
    int arr[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    // This will trigger AddressSanitizer if index is out of bounds
    // Comment out the next line to avoid sanitizer warnings
    // std::cout << "Value at index " << index << ": " << arr[index] << std::endl;

    // Safe access
    if (index >= 0 && index < 10) {
        std::cout << "Value at index " << index << ": " << arr[index] << std::endl;
    } else {
        std::cout << "Invalid index: " << index << std::endl;
    }
}

// Function with potential memory leak for sanitizer testing
void memory_leak_example(bool should_leak) {
    if (should_leak) {
        // This will trigger LeakSanitizer
        // int* leaked = new int[100];
        // std::cout << "Allocated memory (will leak)" << std::endl;
        // Uncomment above lines to test LeakSanitizer
    } else {
        // Proper memory management
        int* not_leaked = new int[100];
        delete[] not_leaked;
        std::cout << "Allocated and freed memory properly" << std::endl;
    }
}

int main() {
    std::cout << "=== CMakeHub Basic Example ===" << std::endl;
    std::cout << std::endl;

    // Test fibonacci generation
    std::cout << "Fibonacci sequence (10 terms):" << std::endl;
    auto fib = generate_fibonacci(10);
    for (int num : fib) {
        std::cout << num << " ";
    }
    std::cout << std::endl << std::endl;

    // Test array access (commented out to avoid sanitizer warnings)
    std::cout << "Testing array access:" << std::endl;
    unsafe_array_access(5);   // Valid access
    unsafe_array_access(15);  // Invalid access (will be caught)
    std::cout << std::endl;

    // Test memory management
    std::cout << "Testing memory management:" << std::endl;
    memory_leak_example(false);  // No leak
    // memory_leak_example(true);  // Will leak (uncomment to test LeakSanitizer)
    std::cout << std::endl;

    std::cout << "Example completed successfully!" << std::endl;
    std::cout << std::endl;
    std::cout << "This example demonstrates:" << std::endl;
    std::cout << "  - CMakeHub module loading (sanitizers, coverage)" << std::endl;
    std::cout << "  - Safe C++ coding practices" << std::endl;
    std::cout << "  - Memory management" << std::endl;
    std::cout << "  - Bound checking" << std::endl;
    std::cout << std::endl;

    return 0;
}