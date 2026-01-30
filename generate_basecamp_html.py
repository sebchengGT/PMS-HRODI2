import csv
import json
import base64
import html

def safe_get(row, key):
    # Strip whitespace AND remove Zero Width Space (U+200B)
    return row.get(key, '').replace('\u200b', '').strip()

def create_card_html(title, subtitle, type_color, type_label, detail_html_base64, preview_items=None):
    """
    Creates the clickable card HTML.
    """
    # Truncate title if too long for the card preview
    display_title = (title[:75] + '...') if len(title) > 80 else title
    
    # Escape strictly for JS: replace newlines to avoid invalid string literals
    # Must escape backslashes first, then single quotes (for JS), then html escape (for attribute)
    safe_title = title.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    safe_title_js = html.escape(safe_title, quote=True)

    # Preview Text HTML
    preview_html = ""
    if preview_items:
        list_items = "".join([f"<li>{html.escape(item)}</li>" for item in preview_items])
        preview_html = f'<ul class="list-disc list-inside text-xs text-slate-500 mb-4 space-y-1">{list_items}</ul>'
    
    return f"""
    <div onclick="openModal('{safe_title_js}', '{detail_html_base64}')" 
         class="bg-white rounded-lg shadow-sm border border-slate-200 p-5 hover:shadow-md transition-all cursor-pointer group hover:border-blue-300 relative overflow-hidden flex flex-col h-full">
        
        <div class="absolute top-0 left-0 w-1 h-full bg-{type_color}-500"></div>
        
        <div class="mb-3 flex justify-between items-start">
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-{type_color}-50 text-{type_color}-700">
                {type_label}
            </span>
            <span class="text-2xl font-bold text-{type_color}-600 leading-none">
                {subtitle.split(' ')[0] if subtitle[0].isdigit() else ''}
            </span>
        </div>
        
        <h4 class="text-md font-bold text-slate-800 mb-2 group-hover:text-blue-700 transition-colors line-clamp-2">
            {html.escape(display_title)}
        </h4>
        
        {preview_html}
        
        <p class="text-xs text-slate-500 mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
            <span class="flex items-center">
                <span class="bg-slate-100 rounded-full p-1 mr-2 group-hover:bg-blue-100 group-hover:text-blue-600 transition-colors">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" /></svg>
                </span>
                View List
            </span>
            <span class="text-slate-400 font-medium">{subtitle}</span>
        </p>
    </div>
    """

def create_detail_html(title, data_dict):
    """
    Creates an HTML string for the modal content representing the details.
    data_dict: { 'Label': 'Value' }
    """
    rows_html = ""
    for label, value in data_dict.items():
        if value:
            rows_html += f"""
            <div class="border-b border-slate-100 last:border-0 py-3">
                <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">{label}</p>
                <div class="text-slate-800 text-sm whitespace-pre-wrap">{html.escape(value)}</div>
            </div>
            """
    
    return f"""
    <div class="space-y-2">
        {rows_html}
    </div>
    """

def create_summary_list_html(items):
    """
    Creates an HTML string for the modal content representing a LIST of items.
    items: list of dicts { 'title': str, 'subtitle': str, 'details': dict }
    """
    list_html = ""
    for item in items:
        detail_html = create_detail_html(item['title'], item['details'])
        
        list_html += f"""
        <div class="bg-slate-50 rounded-lg p-5 border border-slate-200 shadow-sm">
            <h4 class="text-lg font-bold text-slate-800 mb-2">{html.escape(item['title'])}</h4>

            <div class="bg-white p-4 rounded border border-slate-100">
                {detail_html}
            </div>
        </div>
        """
        
    return f"""
    <div class="space-y-6">

        {list_html}
    </div>
    """



def generate_basecamp_html():
    csv_file = 'HRODI Accomplishments.csv'
    
    # Mapping of CSV header names
    # Basecamp, Program
    
    # Buckets
    categories = {
        'Accomplishments': {
            'color': 'green',
            'fields': [
                ('Title', 'Accomplishment Title'),
                ('Description', 'Accomplishment Description'),
                ('Date', 'Accomplishment Date')
            ]
        },
        'Milestones': {
            'color': 'blue',
            'fields': [
                ('Title', 'Milestone Title'),
                ('Description', 'Milestone Description'),
                ('Physical Target', 'Milestone Physical Accomplishment'),
                ('Financial Target', 'Milestone Financial Accomplishment'),
                ('Date', 'Milestone Date')
            ]
        },
        'Bottlenecks': {
            'color': 'red',
            'fields': [
                ('Issue', 'Bottlenecks') # Assuming this is the title/description
            ]
        },
        'Spillovers': {
            'color': 'orange',
            'fields': [
                ('Title', 'Spillover Title'),
                ('Description', 'Spillover Description'),
                ('Initial Target', 'Spillover Initial Target'),
                ('New Target', 'Spillover New Target')
            ]
        },
        'Catch-up Plans': {
            'color': 'purple',
            'fields': [
                ('Title', 'Catch-up Activities Title'),
                ('Description', 'Catchup Activities Description'),
                ('Target Date', 'Catchup Activities Target Date') 
            ]
        }
    }

    # Data Structure:
    # basecamp_data[basecamp][program][category_name] = [list of ITEM DICTS]
    basecamp_data = {}

    # Map Basecamp Names to IDs
    basecamp_id_map = {
        'Career Progression for DepEd Personnel': 'base-careerprog',
        'Mental Health Professionals for Schools': 'base-mentalhealth',
        'Workforce Plan and Management': 'base-workforceplan',
        'HROD Process Excellence': 'base-hrodprocess',
        'Prioritization Index for Education Facilities Allocation': 'base-prioritization',
        'Career Opportunities in DepEd for SHS Graduates': 'base-careeropp',
        'Other PAPs': 'base-otherpaps'
    }

    seen_items = set()

    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            print(f"DEBUG: Headers found: {reader.fieldnames}")
            
            for row in reader:
                basecamp = safe_get(row, 'Basecamp')
                program = safe_get(row, 'Program')
                
                if not basecamp or not program:
                    continue
                    
                if basecamp not in basecamp_data:
                    basecamp_data[basecamp] = {}
                
                if program not in basecamp_data[basecamp]:
                    basecamp_data[basecamp][program] = {cat: [] for cat in categories}
                
                # Check each category for data in this row
                for cat_name, cat_config in categories.items():
                    # We consider a category "present" if the FIRST field has data (Title/Issue)
                    first_field_csv_name = cat_config['fields'][0][1]
                    title_value = safe_get(row, first_field_csv_name)
                    
                    # Filter N/A or empty
                    if not title_value or title_value.lower() in ['n/a', 'na', 'none', '-']:
                        continue
                        
                    # Collect all details
                    detail_data = {}
                    for label, csv_col in cat_config['fields']:
                        val = safe_get(row, csv_col)
                        if val.lower() == 'n/a':
                            val = ""
                        detail_data[label] = val
                    
                    # Stricter N/A check
                    description_field = cat_config['fields'][1][1] if len(cat_config['fields']) > 1 else None
                    desc_value = safe_get(row, description_field) if description_field else ""
                    
                    if desc_value.lower() in ['n/a', 'na']:
                        continue

                    subtitle = desc_value
                    if len(subtitle) > 100: subtitle = subtitle[:100] + "..."
                    
                    # Deduplication
                    unique_key = (program, cat_name, title_value, desc_value)
                    if unique_key in seen_items:
                        continue
                    seen_items.add(unique_key)

                    # STORE DATA instead of HTML
                    item_data = {
                        'title': title_value,
                        'subtitle': subtitle,
                        'details': detail_data
                    }
                    
                    basecamp_data[basecamp][program][cat_name].append(item_data)

        # Generate Final HTML for each Basecamp ID
        output_json = {}
        
        for basecamp, programs in basecamp_data.items():
            base_id = basecamp_id_map.get(basecamp)
            if not base_id:
                print(f"Warning: No ID found for Basecamp '{basecamp}'")
                continue
                
            # Build the inner HTML for this panel
            panel_html = f"""
            <div>
                <h2 class="text-3xl font-bold text-slate-800 mb-6">{basecamp}</h2>
            </div>
            <div class="space-y-12">
            """
            
            for program, cats in programs.items():
                # Check if program has ANY data
                has_data = any(len(items) > 0 for items in cats.values())
                if not has_data:
                    continue
                    
                panel_html += f"""
                <div class="bg-slate-50 rounded-xl p-6 border border-slate-200">
                    <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center border-b border-slate-200 pb-2">
                        <i data-lucide="folder-open" class="w-5 h-5 mr-3 text-blue-600"></i>
                        {program}
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                """
                
                # Now loop through categories and generate ONE card per category
                for cat_name, items in cats.items():
                    if not items:
                        continue
                        
                    config = categories[cat_name]
                    color = config['color']
                    
                    # Generate Summary Logic
                    count = len(items)
                    summary_title = cat_name
                    summary_subtitle = f"{count} Items"
                    
                    # Generate Preview Items List
                    preview_items = [i['title'] for i in items[:3]]
                    if len(items) > 3:
                        preview_items.append(f"and {len(items)-3} more...")
                    
                    # Generate Modal HTML for ALL items
                    full_detail_html = create_summary_list_html(items)
                    detail_base64 = base64.b64encode(full_detail_html.encode('utf-8')).decode('utf-8')
                    
                    # Reuse create_card_html for the summary card
                    card_html = create_card_html(
                        title=summary_title, 
                        subtitle=summary_subtitle, 
                        type_color=color, 
                        type_label=cat_name, 
                        detail_html_base64=detail_base64,
                        preview_items=preview_items
                    )
                    
                    panel_html += card_html
                
                panel_html += """
                    </div>
                </div>
                """
            
            panel_html += "</div>"
            output_json[base_id] = panel_html

        # Save to JSON
        with open('generated_content.json', 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=4)
            
        print(f"Successfully generated HTML for ids: {list(output_json.keys())}")

    except Exception as e:
        print(f"Error generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_basecamp_html()
