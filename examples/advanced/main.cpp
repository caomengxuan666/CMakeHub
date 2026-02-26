#include <iostream>

int main() {
    std::cout << "CMakeHub Advanced Example" << std::endl;
    std::cout << "=====================================" << std::endl;
    std::cout << "This example demonstrates various CMakeHub features:" << std::endl;
    std::cout << "- Module discovery (cmakehub_list, cmakehub_search)" << std::endl;
    std::cout << "- Version selection (VERSION parameter)" << std::endl;
    std::cout << "- Config parameters (passing arguments to modules)" << std::endl;
    std::cout << "- Cache management (cmakehub_cache_clear, cmakehub_cache_info)" << std::endl;
    std::cout << "- Dependency graph (cmakehub_dependency_graph)" << std::endl;
    std::cout << "- Module information (cmakehub_info)" << std::endl;
    std::cout << "- Compatibility check (cmakehub_check_compatibility)" << std::endl;
    std::cout << "- Resource embedding (embed_resources)" << std::endl;
    std::cout << "- Code coverage (coverage_cg)" << std::endl;
    std::cout << "- Compiler warnings (compiler_warnings)" << std::endl;
    std::cout << std::endl;
    std::cout << "Check the CMakeLists.txt for more details." << std::endl;
    return 0;
}