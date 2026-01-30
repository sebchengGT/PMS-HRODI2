def check_marker():
    with open('HTML_backup.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = '</main>'
    idx = content.find(marker)
    print(f"Marker '{marker}' found at: {idx}")
    print(f"Total length: {len(content)}")
    
    if idx != -1:
        print(f"Surrounding text: {content[idx-20:idx+20]!r}")

if __name__ == "__main__":
    check_marker()
