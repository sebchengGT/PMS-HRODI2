
import re

def wipe_basecamp_content():
    file_path = 'index.html'
    print(f"Propocessing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # List of Basecamp IDs to clear
    # Based on sidebar/earlier analysis
    basecamp_ids = [
        'base-careerprog',
        'base-mentalhealth', 
        'base-workforceplan', 
        'base-hrodprocess', 
        'base-prioritization', 
        'base-careeropp', 
        'base-otherpaps'
    ]
    
    new_content = content
    
    for pid in basecamp_ids:
        # Find the div opening tag
        # <div id="base-careerprog" class="...">
        pattern = r'(<div[^>]*id="' + pid + r'"[^>]*>)'
        match = re.search(pattern, new_content)
        
        if match:
            start_pos = match.start()
            # Find end of this div block
            open_divs = 1
            scan = match.end()
            end_pos = -1
            
            # Simple div counter
            while True:
                next_tag = new_content.find('<', scan)
                if next_tag == -1: break
                
                if new_content.startswith('<div', next_tag):
                    open_divs += 1
                    scan = next_tag + 4
                elif new_content.startswith('</div', next_tag):
                    open_divs -= 1
                    scan = next_tag + 5
                    
                if open_divs == 0:
                    end_pos = new_content.find('>', scan) + 1
                    break
                scan = next_tag + 1
            
            if end_pos != -1:
                # We found the block.
                # Replace content with Empty State.
                # Keep the wrapper div (match.group(1)) and closing div </div>
                
                # We can also add a placeholder header or something?
                # User said "remove all contents ... I want to restructure".
                # Best to leave it empty or with a placeholder title matching the ID.
                
                wrapper_open = match.group(1)
                
                clean_html = f'''{wrapper_open}
                    <div class="flex items-center justify-center h-64 border-2 border-dashed border-slate-200 rounded-xl">
                        <div class="text-center text-slate-400">
                            <i data-lucide="package-open" class="w-12 h-12 mx-auto mb-2 opacity-50"></i>
                            <p>Content cleared for restructuring</p>
                        </div>
                    </div>
                </div>'''
                
                # Replace safely
                # Since we modify `new_content`, indexes shift.
                # We should probably do this in one pass or rebuild string.
                # Rebuilding is safer. But regex find on `new_content` works if we do it one by one and re-search.
                
                prefix = new_content[:start_pos]
                suffix = new_content[end_pos:]
                new_content = prefix + clean_html + suffix
                
                print(f"Cleared {pid}")
            else:
                print(f"Could not find end of {pid}")
        else:
            print(f"Could not find {pid}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Basecamp sections cleared.")

if __name__ == "__main__":
    wipe_basecamp_content()
