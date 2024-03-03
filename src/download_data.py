import zipfile
import os

zip_file_path = os.getcwd() + '/data/archive.zip'
extract_dir = os.getcwd() + '/data/extracted/'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print('Zip file extracted successfully to:', extract_dir)