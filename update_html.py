import json
import re

def update_html():
    try:
        # Load generated content
        with open("generated_content.json", "r", encoding='utf-8') as f:
            generated_content = json.load(f)
            
        # Load HTML
        html_file = "HTML_backup.html"
        output_file = "HTML DepED v1.html"
        with open(html_file, "r", encoding='utf-8') as f:
            html_content = f.read()
            
        # Replace content
        # We look for <div id="base-xyz" class="content-panel hidden fade-in space-y-6"> ... </div>
        # But the class might vary slightly or there might be whitespace.
        # The structure is: <div id="base-..." ...> [CONTENT TO REPLACE] </div>
        # Wait, the closing div is hard to find with regex because of nested divs.
        
        # Alternative: use the exact strings I read earlier as anchors? No, that's what I wanted to avoid.
        
        # Let's try to find the start tag, and then find the next <div class="content-panel... or some other marker.
        # Actually, the file structure is very consistent.
        # <div id="base-..." ...>
        #    ... content ...
        # </div>
        # <div id="next-id" ...>
        
        # However, nested divs make regex replacement of "inner html" tricky.
        # I will use string replacement based on the "headings" currently inside the divs.
        
        # Current content starts with: <div class="flex justify-between items-end">
        # And ends before the next <div id="..."> or </main>
        
        for base_id, new_html in generated_content.items():
            print(f"Updating {base_id}...")
            
            # Find the start index of the div with this id
            start_marker = f'id="{base_id}"'
            start_index = html_content.find(start_marker)
            
            if start_index == -1:
                print(f"Warning: Could not find div with {start_marker}")
                continue
                
            # Find the closing specific to this structure.
            # We know the inner content starts after the opening tag >
            # The opening tag is like <div id="base-..." class="...">
            
            tag_end_index = html_content.find('>', start_index) + 1
            
            # Now we need to find where this div ends. 
            # Since I don't have a parser, and I know the file structure:
            # The div ends before the next <div id="base-..." or <div id="welfare-..." or </main>
            # But the next element might not be immediately adjacent if there's whitespace.
            
            # Let's rely on Indentation if possible? No.
            
            # Let's construct a reliable "End of Content" marker.
            # The Basecamp panels are sequential.
            # base-careerprog -> base-mentalhealth -> base-workforceplan -> base-hrodprocess -> base-careeropp -> base-prioritization -> </main>
            
            # Order in file:
            # 1. base-careerprog
            # 2. base-mentalhealth
            # 3. base-workforceplan
            # 4. base-hrodprocess
            # 5. base-careeropp
            # 6. base-prioritization
            
            next_markers = {
                'base-careerprog': 'id="base-mentalhealth"',
                'base-mentalhealth': 'id="base-workforceplan"',
                'base-workforceplan': 'id="base-hrodprocess"',
                'base-hrodprocess': 'id="base-careeropp"',
                'base-careeropp': 'id="base-prioritization"',
                'base-prioritization': '</main>'
            }
            
            next_marker = next_markers.get(base_id)
            if not next_marker:
                print(f"Error: Unknown order for {base_id}")
                continue
                
            end_search_start = tag_end_index
            end_index = html_content.find(next_marker, end_search_start)
            
            if end_index == -1:
                print(f"Error: Could not find next marker {next_marker} for {base_id}")
                continue
            
            # Now backtrack from end_index to find the last </div>
            # The content ends with a </div> which closes the main panel div.
            # We want to replace the INNER content.
            # So start replacement at tag_end_index.
            # And end replacement BEFORE the last </div> of this block.
            
            # This is risky doing strictly with string manipulation without parsing.
            
            # BETTER APPROACH:
            # I have the EXISTING content from `view_file` which I can trust.
            # I'll paste the start and end of the EXISTING content to locate it precisely.
            
            # Existing start of content: <div class="flex justify-between items-end">
            # Existing end of content: </div> (the one before the next ID)
            
            # Let's try to match the *entire* block including the wrapper div, then recreate the wrapper div.
            # We know the wrapper starts with <div id="{base_id}" class="content-panel hidden fade-in space-y-6">
            
            # Find the wrapper start
            wrapper_start_str = f'<div id="{base_id}" class="content-panel hidden fade-in space-y-6">'
            block_start = html_content.find(wrapper_start_str)
            
            if block_start == -1:
                 # Try finding just the ID if class changed
                 wrapper_start_str = f'<div id="{base_id}"'
                 block_start = html_content.find(wrapper_start_str)
            
            if block_start == -1:
                print(f"Could not find block for {base_id}")
                continue
                
            # Find the end of this block using the next_marker strategy, but subtract the closing div tag length
            # end_index is where the NEXT div starts (e.g. <div id="base-mental...")
            # So the current div ends right before that.
            
            # Let's find the last occurrences of "</div>" before end_index.
            # Note: There might be whitespace.
            
            substring = html_content[tag_end_index:end_index]
            # Verify the substring looks like the content we want to replace.
            
            # Actually, we can just replace the WHOLE file content. 
            # Since we are reading the whole file, we can reconstruct it.
            
            # But "base-careeropp" and "base-prioritization" swap order in my JSON vs File might be an issue?
            # No, I am iterating by ID.
            
            # The file order is fixed in the HTML file on disk.
            # I need to preserve everything OUTSIDE the basecamp divs.
            
            pass 
            
        # New Strategy:
        # 1. Read file.
        # 2. Split file by IDs to isolate chunks.
        # 3. Rebuild file.
        
        # Split markers
        markers = [
            'id="base-careerprog"', 
            'id="base-mentalhealth"', 
            'id="base-workforceplan"', 
            'id="base-hrodprocess"', 
            'id="base-careeropp"', 
            'id="base-prioritization"',
            '</main>'
        ]
        
        parts = []
        current_pos = 0
        
        # 1. Content BEFORE CareerProg
        marker0 = 'id="base-careerprog"'
        idx0 = html_content.find(marker0)
        # Find the start of the div tag containing this ID
        div_start0 = html_content.rfind('<div ', 0, idx0)
        
        parts.append(html_content[current_pos:div_start0])
        
        # IDS in order of appearance in the file (CONFIRMED via map_ids.py)
        ids_in_order = [
            'base-careerprog',
            'base-mentalhealth',
            'base-workforceplan',
            'base-hrodprocess',
            'base-prioritization',
            'base-careeropp',
            'base-otherpaps'
        ]
        
        # Determine next markers dynamically
        next_map = {}
        for i in range(len(ids_in_order) - 1):
             current_id = ids_in_order[i]
             next_id = ids_in_order[i+1]
             next_map[current_id] = f'id="{next_id}"'
             
        # Last one maps to footer marker
        next_map[ids_in_order[-1]] = '</main>'
        
        new_file_content = html_content
        reversed_ids = list(reversed(ids_in_order))
        
        for base_id in reversed_ids:
            if base_id not in generated_content:
                continue
                
            new_inner = generated_content[base_id]
            
            # Find start of DIV
            search_str = f'id="{base_id}"'
            id_pos = new_file_content.find(search_str)
            div_start = new_file_content.rfind('<div ', 0, id_pos)
            
            # Find content start (first > after div_start)
            content_start = new_file_content.find('>', div_start) + 1
            
            # Find end of DIV (element before the next marker)
            next_marker = next_map[base_id]
            next_marker_pos = new_file_content.find(next_marker)
            
            if next_marker_pos == -1:
                 print(f"Error: Marker '{next_marker}' not found for {base_id}")
                 continue
            
            # Determine correct split point
            if next_marker.startswith('id='):
                 # Find the start of the <div tag containing this ID
                 split_point = new_file_content.rfind('<div ', 0, next_marker_pos)
                 if split_point == -1:
                     print(f"CRITICAL ERROR: Could not find <div for next marker {next_marker}")
                     raise Exception("Split point not found")
            else:
                 # It's </main> or similar, so split exactly there
                 split_point = next_marker_pos
            
            # Robust Replacement Strategy:
            replacement_block = '\n' + new_inner + '\n            </div>\n            '
            
            # Debug indices
            print(f"DEBUG {base_id}: id_pos={id_pos}, div_start={div_start}, content_start={content_start}, split_point={split_point}")
            
            new_file_content = new_file_content[:content_start] + replacement_block + new_file_content[split_point:]
            
            print(f"Replaced content for {base_id}")

        with open(output_file, "w", encoding='utf-8') as f:
            f.write(new_file_content)
            
        print("Successfully updated HTML.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_html()
