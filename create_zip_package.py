import zipfile
import os
import datetime

def create_package():
    files_to_zip = [
        "HTML DepED v1.html",
        "HRODI Accomplishments.csv",
        "generate_basecamp_html.py",
        "fix_html_structure.py",
        "README.txt"
    ]
    
    zip_filename = "HRODI_Dashboard_Package.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            print(f"Creating {zip_filename}...")
            for file in files_to_zip:
                if os.path.exists(file):
                    print(f"  Adding {file}...")
                    zipf.write(file)
                else:
                    print(f"  Warning: {file} not found, skipping.")
        
        print(f"Successfully created {zip_filename}")
        
    except Exception as e:
        print(f"Error creating zip: {e}")

if __name__ == "__main__":
    create_package()
