import json

with open('modules.json') as f:
    data = json.load(f)

for m in data['modules']:
    if m['name'] in ['compiler_info', 'launchers', 'use_folders']:
        m['version'] = 'main'
        print(f"Fixed {m['name']}: {m['version']}")

with open('modules.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Fixed 3 modules")