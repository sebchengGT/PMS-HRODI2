HRODI Knowledge Management Dashboard Package
============================================

This package contains the HRODI Knowledge Management Dashboard and its source files.

Contents:
1. HTML DepED v1.html           - The main dashboard file. Open this in any modern web browser used to view the dashboard.
2. HRODI Accomplishments.csv    - The source data file containing accomplishments, milestones, etc.
3. generate_basecamp_html.py    - Python script to parse the CSV and generate HTML content.
4. fix_html_structure.py        - Python script to inject the generated content into the HTML structure.

How to Update Data:
1. Edit "HRODI Accomplishments.csv" with your new data.
2. Run "python generate_basecamp_html.py" to generate the new content segments.
3. Run "python fix_html_structure.py" to update the HTML file with the new segments.
4. Open "HTML DepED v1.html" to see changes.

Requirements:
- Python 3.x for running the update scripts.
- No special requirements for viewing the HTML file (internet connection recommended for fonts/icons).
