def check_careeropp():
    with open('HTML_backup.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = 'id="base-careeropp"'
    idx = content.find(marker)
    print(f"Marker '{marker}' found at: {idx}")
    
    if idx != -1:
        # Show preceding 200 chars
        print(f"Preceding context:\n{content[idx-200:idx+50]!r}")
        
        # Check div_start logic
        div_start = content.rfind('<div ', 0, idx)
        print(f"div_start found at: {div_start}")
        print(f"div tag context: {content[div_start:idx+50]!r}")
        
        tag_end = content.find('>', div_start)
        print(f"tag_end at: {tag_end}")
        
        if tag_end < idx:
             print("CRITICAL: tag_end is BEFORE marker index! Logic is flawed.")

if __name__ == "__main__":
    check_careeropp()
