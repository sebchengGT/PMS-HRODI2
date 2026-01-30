import json

def fix_html():
    try:
        # Load generated content
        with open("generated_content.json", "r", encoding='utf-8') as f:
            generated_content = json.load(f)
            
        # Load HTML
        html_file = "HTML DepED v1.html"
        with open(html_file, "r", encoding='utf-8') as f:
            html_content = f.read()
            
        # Identify split points
        # 1. Start of Basecamp section (follows School Effectiveness or is the first base-*)
        # We know base-careerprog is the first one in the clean list.
        # But let's be safer: Find the FIRST occurrence of ANY basecamp ID.
        
        base_ids = [
            'base-careerprog',
            'base-mentalhealth',
            'base-workforceplan',
            'base-hrodprocess',
            'base-prioritization',
            'base-careeropp',
            'base-otherpaps'
        ]
        
        # Find the earliest index among these
        start_index = len(html_content)
        first_id = None
        
        for bid in base_ids:
            # Search for id="{bid}"
            marker = f'id="{bid}"'
            idx = html_content.find(marker)
            if idx != -1 and idx < start_index:
                start_index = idx
                first_id = bid
                
        if start_index == len(html_content):
            print("Error: Could not find any Basecamp panels.")
            return

        # Find the actual start of the DIV tag containing this ID
        # Search backwards from start_index for '<div'
        split_point_1 = html_content.rfind('<div ', 0, start_index)
        
        if split_point_1 == -1:
            print("Error: Could not find opening div for basecamp section.")
            return
            
        print(f"Found start of Basecamp section at index {split_point_1} (ID: {first_id})")
        
        # 2. End of Basecamp section
        # Logic: The Basecamp section ends before </main>
        # We can simply assume everything from split_point_1 up to </main> is the Basecamp section 
        # (and potentially garbage/malformed tags) that we want to replace.
        
        split_point_2 = html_content.find('</main>')
        
        if split_point_2 == -1:
            print("Error: Could not find </main>.")
            return
            
        print(f"Found end of section at index {split_point_2}")
        
        # Construct new content
        new_basecamp_html = ""
        
        # Order we want them to appear
        ordered_ids = [
            'base-careerprog',
            'base-mentalhealth',
            'base-workforceplan',
            'base-hrodprocess',
            'base-prioritization',
            'base-careeropp',
            'base-otherpaps'
        ]
        
        for bid in ordered_ids:
            content = generated_content.get(bid, "")
            if not content:
                print(f"Warning: No content for {bid}")
                # We can still create the panel, maybe placeholder?
                # Or just put empty content.
                pass
                
            panel_html = f'''
            <div id="{bid}" class="content-panel hidden fade-in space-y-6">
{content}
            </div>'''
            new_basecamp_html += panel_html
            
        # Reassemble
        final_html = html_content[:split_point_1] + new_basecamp_html + "\n            " + html_content[split_point_2:]
        
        with open(html_file, "w", encoding='utf-8') as f:
            f.write(final_html)
            
        print("Successfully rebuilt HTML Basecamp structure.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_html()
