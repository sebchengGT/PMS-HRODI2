def map_ids():
    ids = [
        'base-careerprog',
        'base-mentalhealth',
        'base-workforceplan',
        'base-hrodprocess',
        'base-careeropp',
        'base-prioritization',
        'base-otherpaps'
    ]
    
    with open('HTML_backup.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    positions = []
    for i in ids:
        idx = content.find(f'id="{i}"')
        positions.append((i, idx))
        
    # Sort by index
    positions.sort(key=lambda x: x[1])
    
    print("Correct Order:")
    for i, p in enumerate(positions):
        print(f"{i+1}. {p[0]} at {p[1]}")

if __name__ == "__main__":
    map_ids()
