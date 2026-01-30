
def analyze_structure():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Total size: {len(content)} chars")
    
    # Signatures
    start_sig = 'id="base-careerprog"'
    script_sig = '<script>' # Finding the first script tag might find header scripts.
    # We want the footer scripts.
    # "Tab switching functionality" comment is unique
    footer_sig = '// Tab switching functionality'
    
    start_idx = content.find(start_sig)
    print(f"Start of base-careerprog: {start_idx}")
    
    # Find footer
    footer_idx = content.rfind('<script') # Last script tag is likely footer
    # Or specifically the one we added.
    print(f"Last script tag: {footer_idx}")
    
    # Check what is between
    if start_idx != -1 and footer_idx != -1:
        print(f"Content blob size: {footer_idx - start_idx}")
        
    # We can perform the surgery here
    if start_idx != -1:
        # Find the line start of this div
        tag_start = content.rfind('<div', 0, start_idx)
        print(f"Tag start: {tag_start}")
        
        # We want to keep everything before `tag_start`
        preamble = content[:tag_start]
        
        # We want the footer.
        # But wait, the file has other panels?
        # Dashboard, Analytics, etc.
        # Are they BEFORE or AFTER base-careerprog?
        # Usually Dashboard is first.
        # Let's ensure we don't cut off the footer of the layout (closing main, body, html).
        
        # The structure is Sidebar + Main Content Area.
        # Main Content Area contains all panels.
        # We should only replacing the BASECAMP panels.
        # But if they are duplicated 100x times, they are the problem.
        
        # I propose to construct the standard basecamp panels HTML structure
        # and append the footer.
        
        # We need to find valid footer start.
        # Typically `</body>`.
        footer_start = content.rfind('</body>')
        if footer_start != -1:
             # Find the scripts before body close
             # Scan back for <script
             pass
        
        # Let's just create a new clean content chunk for the basecamps
        basecamps = [
            ("base-careerprog", "Career Progression for DepEd Personnel"),
            ("base-mentalhealth", "Mental Health Program"),
            ("base-workforceplan", "Strategic Human Resource & Workforce Plan"),
            ("base-hrodprocess", "HROD Process Excellence"),
            ("base-prioritization", "HROD Prioritization"),
            ("base-careeropp", "Career Opportunities"),
            ("base-otherpaps", "Other PAPs")
        ]
        
        clean_panels = []
        for pid, title in basecamps:
            panel = f'''
            <div id="{pid}" class="content-panel hidden fade-in space-y-6">
                <div>
                    <h2 class="text-3xl font-bold text-slate-800 mb-6">{title}</h2>
                </div>
                <div class="flex items-center justify-center h-64 border-2 border-dashed border-slate-200 rounded-xl">
                    <div class="text-center text-slate-400">
                        <i data-lucide="package-open" class="w-12 h-12 mx-auto mb-2 opacity-50"></i>
                        <p>Content cleared for restructuring</p>
                    </div>
                </div>
            </div>'''
            clean_panels.append(panel)
            
        clean_html = "\n".join(clean_panels)
        
        # Now stitch.
        # Preamble: Up to start of `base-careerprog`.
        # Postamble: From matching END of the panels container?
        # Or if the file is ruined, finding a safe anchor at the end.
        
        # Anchor: <script> at the end.
        # Or look for `<!-- End Main Content -->` if it exists.
        
        # Fallback: finding the last </main> or </body> is risky if duplications messed up tags.
        # But `rfind('</body>')` finds the LAST one.
        
        body_end = content.rfind('</body>')
        
        # We need to capture the scripts which are usually before body end.
        # Let's verify if there is a block of scripts.
        
        # Safe approach: 
        # keep content[:tag_start]
        # ADD clean_html
        # FIND valid footer start.
        
        # The mess is likely between `tag_start` and `body_end`.
        # However, `body_end` is at 40MB.
        # The scripts might be repeated?
        # `rfind` gets the last one.
        
        # Let's try to find the start of the scripts section.
        # Usually `<script>` implies start of JS.
        # The last distinct script block.
        
        # Let's apply the cut.
        
        # Check if there are other panels AFTER base-otherpaps?
        # Usually no, that's the end of content list.
        
        # So we cut from `tag_start` to `body_end` (excluding scripts if we can rescue them).
        
        # Finding the start of the final script block:
        # Look for `function switchPanel` or `document.addEventListener`.
        # `last_script = content.rfind('<script')`
        
        script_pos = content.rfind('<script')
        # We want to keep from this script pos onwards?
        # Assuming only footer scripts are there.
        
        if script_pos > tag_start:
            postamble = content[script_pos:]
            # But we miss closing divs for Main/Body?
            # </body> is inside postamble if we take from script.
            # But we might miss `</main>` `</div>` (wrapper).
            
            # Use `content.rfind('</main>')`?
            main_close = content.rfind('</main>')
            if main_close != -1:
                # We want to insert BEFORE main close.
                # So Postamble = content[main_close:]
                postamble = content[main_close:]
                
                # Check if we have scripts before main close? 
                # Usually scripts are AFTER main, before body.
                # So `main_close` < `script_pos`.
                
                final_content = preamble + clean_html + postamble
                
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print("Reconstruction complete.")
            else:
                print("Could not find </main>")
        else:
             print("Script pos issue")
    else:
        print("Could not find base-careerprog")

if __name__ == "__main__":
    analyze_structure()
