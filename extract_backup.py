import zipfile
import os

zip_path = 'HRODI_Dashboard_Package.zip'
extract_path = '.'
target_file = 'HTML DepED v1.html'
backup_name = 'HTML_backup.html'

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if target_file in zip_ref.namelist():
            with zip_ref.open(target_file) as source, open(backup_name, 'wb') as target:
                target.write(source.read())
            print(f"Extracted {target_file} to {backup_name}")
        else:
            print(f"File {target_file} not found in zip.")
else:
    print(f"Zip file {zip_path} not found.")
