import os

def restore_footer():
    current_file = 'HTML DepED v1.html'
    backup_file = 'HTML_backup.html'
    
    with open(current_file, 'r', encoding='utf-8') as f:
        current_content = f.read()
        
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
        
    split_marker = '</main>'
    
    if split_marker in current_content:
        print("</main> already exists. Checking for missing scripts anyway?")
        # Maybe check for switchPanel?
        if 'function switchPanel' in current_content:
             print("switchPanel already exists. Aborting restore.")
             return
        else:
             print("switchPanel missing. Proceeding with restore from </main>.")
             # Split current at </main> and take header
             current_pre = current_content.rsplit(split_marker, 1)[0]
    else:
        print("</main> missing. Using fallback logic.")
        # Try to find the last base-otherpaps?
        # Or just find the last </div>?
        # risky.
        # Let's assume the file is truncated at the last Basecamp content.
        # Check if "base-otherpaps" generates content ends with </div>
        pass
        
    if split_marker not in backup_content:
        print("Error: </main> not found in backup file.")
        return

    # Backup post logic
    backup_post = backup_content.rsplit(split_marker, 1)[1]
    
    if split_marker in current_content:
        # We restore from </main>
        new_content = current_pre + split_marker + backup_post
    else:
        # If </main> is missing from current, we assume current ends with some content 
        # that needs the footer appended.
        # BUT we must ensure we don't duplicate or miss the closing </div> of the last section.
        # Let's look for `id="base-otherpaps"`
        marker = 'id="base-otherpaps"'
        idx = current_content.find(marker)
        if idx != -1:
             # Find the end of this div?
             # If it was replaced by update_html, it might be terminated correctly with </div>
             # but missing </main>.
             # Let's peek at the end of current_content
             pass
        
        # Simpler: If </main> is missing, just append it + footer?
        # Check if file ends with </div>
        if current_content.strip().endswith('</div>'):
             print("File ends with </div>. Appending footer.")
             new_content = current_content + '\n' + split_marker + backup_post
        else:
             print("File structure unclear. Aborting.")
             return

    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully restored footer. New size: {len(new_content)} chars.")

if __name__ == "__main__":
    restore_footer()
