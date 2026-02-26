# Contributing to CMakeHub

Thank you for your interest in contributing to CMakeHub! This document provides guidelines and instructions for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Adding New Modules](#adding-new-modules)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

---

## Getting Started

### Prerequisites

- CMake 3.19 or higher
- Python 3.6 or higher
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/caomengxuan666/CMakeHub.git
cd CMakeHub

# Run tests to verify setup
python run_tests.py
```

---

## Development Workflow

1. **Fork the repository**
   - Create your own fork on GitHub

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, well-commented code
   - Follow existing code style
   - Test your changes

4. **Run tests**
   ```bash
   python run_tests.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to https://github.com/caomengxuan666/CMakeHub
   - Click "New Pull Request"
   - Provide a clear description of your changes

---

## Adding New Modules

### Module Requirements

To add a new module to CMakeHub, it must:

1. **Be hosted on GitHub**
   - Provide the repository URL

2. **Have a clear license**
   - Specify the license (MIT, Apache 2.0, BSD, etc.)

3. **Be actively maintained**
   - Check last commit date
   - Ensure it's not abandoned

4. **Be well-documented**
   - Include README or documentation
   - Provide usage examples

5. **Be tested**
   - Prefer modules with tests
   - Ensure they work with CMake 3.19+

### Module Categories

We accept modules in the following categories:

- **build_optimization**: Tools to speed up builds
- **code_quality**: Static analysis, sanitizers, coverage
- **debugging**: Debug helpers and tools
- **packaging**: Installation and packaging helpers
- **dependency**: Dependency management tools
- **platform**: Platform-specific tools
- **testing**: Testing frameworks integration
- **docs**: Documentation generation
- **utils**: Utility functions

### How to Add a Module

1. **Verify the module exists and works**
   ```bash
   # Test the module manually
   curl -O https://raw.githubusercontent.com/user/repo/branch/module.cmake
   cmake -P module.cmake
   ```

2. **Update modules.json**
   ```json
   {
     "name": "your_module",
     "description": "Brief description of the module",
     "category": "utils",
     "author": "Author Name",
     "repository": "https://github.com/user/repo.git",
     "path": "module.cmake",
     "license": "MIT",
     "stars": 100,
     "last_updated": "2024-01-01",
     "version": "main",
     "cmake_minimum_required": "3.19",
     "cpp_minimum_required": "",
     "dependencies": [],
     "conflicts": [],
     "tags": ["tag1", "tag2"]
   }
   ```

3. **Add to categories section** (if new category)
   ```json
   {
     "categories": {
       "new_category": "Description of the category"
     }
   }
   ```

4. **Test the module**
   ```bash
   python run_single_test.py test_loader_basic
   ```

5. **Submit a Pull Request**
   - Include module name in PR title
   - Provide module documentation link
   - Explain why this module should be included

### Module Metadata Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the module |
| `description` | Yes | Brief description of what the module does |
| `category` | Yes | Category from predefined list |
| `author` | Yes | Module author/maintainer |
| `repository` | Yes | GitHub repository URL |
| `path` | Yes | Path to the module file in the repository |
| `license` | Yes | Module license (MIT, Apache 2.0, etc.) |
| `stars` | No | GitHub stars count |
| `last_updated` | No | Last update date (YYYY-MM-DD) |
| `version` | Yes | Default version to use (branch, tag, or commit) |
| `cmake_minimum_required` | Yes | Minimum CMake version |
| `cpp_minimum_required` | No | Minimum C++ standard |
| `dependencies` | Yes | Array of module dependencies |
| `conflicts` | Yes | Array of conflicting modules |
| `tags` | No | Array of search tags |

---

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test
python run_single_test.py test_loader_basic

# Verify module paths
cmake -P verify_modules.cmake
```

### Writing Tests

Tests are located in `tests/` directory. Each test is a CMake script:

```cmake
# tests/test_your_feature/run.cmake
cmake_minimum_required(VERSION 3.19)

include(${CMAKE_CURRENT_LIST_DIR}/../../cmake/hub/loader.cmake)

# Your test code here
message(STATUS "Testing your feature...")

# Assert conditions
if(NOT condition)
    message(FATAL_ERROR "Test failed")
endif()

message(STATUS "Test passed!")
```

### Test Categories

- **test_loader_basic**: Basic module loading
- **test_cache**: Cache mechanism
- **test_version_check**: Version checking
- **test_dependencies**: Dependency resolution
- **test_conflicts**: Conflict detection

---

## Submitting Changes

### Pull Request Guidelines

1. **Use clear titles**
   - ✅ Good: "Add sanitizers module to index"
   - ❌ Bad: "Update stuff"

2. **Provide detailed descriptions**
   - Explain what you changed and why
   - Link to related issues
   - Include screenshots if applicable

3. **Keep PRs focused**
   - One feature or fix per PR
   - Small, atomic changes
   - Easy to review

4. **Update documentation**
   - Update README if needed
   - Add comments to code
   - Update CHANGELOG (if exists)

### Code Style

- Use CMake 3.19+ features
- Follow existing indentation (4 spaces)
- Use descriptive variable names
- Add comments for complex logic

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(module): Add sanitizers module to index

- Added sanitizers module with ASan, UBSan, TSan support
- Updated module count to 21
- Added unit tests for sanitizers module

Closes #42
```

---

## Reporting Issues

### Before Reporting

1. **Search existing issues**
   - Check if the issue has already been reported
   - Add comments to existing issues if relevant

2. **Reproduce the issue**
   - Provide steps to reproduce
   - Include error messages
   - Specify your environment

### Issue Template

```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- CMake version: [e.g., 3.19.0]
- Python version: [e.g., 3.8]

## Additional Information
Any other relevant information
```

---

## Questions?

Feel free to:
- Open an issue with your question
- Start a discussion in the Discussions tab
- Contact maintainers directly

Thank you for contributing to CMakeHub! 🎉