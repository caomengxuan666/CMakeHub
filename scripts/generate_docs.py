#!/usr/bin/env python3
"""
Generate documentation for all CMakeHub modules
"""

import json
from pathlib import Path


def generate_module_docs(modules_json_path, output_dir):
    """Generate markdown documentation for all modules"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read modules.json
    with open(modules_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate index
    index_content = """# CMakeHub Module Documentation

CMakeHub provides 61+ curated CMake modules for modern C++ development.

## Table of Contents

### Categories

"""
    
    # Group modules by category
    categories = {}
    for module in data['modules']:
        cat = module['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(module)
    
    # Generate category index
    for cat in sorted(categories.keys()):
        index_content += f"- [{cat}](#{cat.lower().replace('_', '-')})\n"
    
    index_content += "\n"
    
    # Generate per-category documentation
    for cat in sorted(categories.keys()):
        index_content += f"## {cat}\n\n"
        index_content += f"{data['categories'].get(cat, cat)}\n\n"
        
        for module in sorted(categories[cat], key=lambda x: x['name']):
            name = module['name']
            desc = module['description']
            repo = module['repository']
            license_type = module['license']
            cmake_min = module.get('cmake_minimum_required', 'N/A')
            cpp_min = module.get('cpp_minimum_required', 'N/A')
            
            # Generate link to individual module doc
            module_file = output_dir / f"{name}.md"
            
            index_content += f"- **[{name}]({name}.md)**: {desc}\n"
    
    # Write index
    index_file = output_dir / "README.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Generate individual module docs
    for module in data['modules']:
        name = module['name']
        desc = module['description']
        category = module['category']
        author = module['author']
        repo = module['repository']
        path = module['path']
        license_type = module['license']
        stars = module.get('stars', 'N/A')
        version = module.get('version', 'main')
        cmake_min = module.get('cmake_minimum_required', 'N/A')
        cpp_min = module.get('cpp_minimum_required', 'N/A')
        last_updated = module.get('last_updated', 'N/A')
        dependencies = module.get('dependencies', [])
        conflicts = module.get('conflicts', [])
        tags = module.get('tags', [])
        
        module_doc = f"""# {name}

**Category**: {category}  
**Author**: {author}  
**License**: {license_type}  
**Stars**: {stars}

## Description

{desc}

## Repository

[{repo}]({repo})

## Usage

```cmake
cmakehub_use({name})
```

## Requirements

- **CMake**: {cmake_min}
- **C++**: {cpp_min}

## Module Information

- **Path**: {path}
- **Version**: {version}
- **Last Updated**: {last_updated}

## Dependencies

{', '.join(dependencies) if dependencies else 'None'}

## Conflicts

{', '.join(conflicts) if conflicts else 'None'}

## Tags

{', '.join(tags) if tags else 'None'}
"""
        
        module_file = output_dir / f"{name}.md"
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write(module_doc)
    
    print(f"Generated documentation for {len(data['modules'])} modules")
    print(f"Output directory: {output_dir}")
    print(f"Index file: {index_file}")


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    modules_json = project_root / 'modules.json'
    docs_output = project_root / 'docs' / 'modules'
    
    generate_module_docs(modules_json, docs_output)