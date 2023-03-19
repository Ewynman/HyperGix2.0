import os
import shutil
import zipfile
import time
from tqdm import tqdm

extract_folder = r'C:\Users\edwar\OneDrive\Research\MyCode\HyperGix2.0'
images_folder = os.path.join(extract_folder, 'images')

# Get all zip files in the download folder
download_folder = r'C:\Users\edwar\Downloads'
zip_files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith(('.zip', '.ZIP'))]

# Unzip each file with a progress bar
for zip_path in tqdm(zip_files, desc='Extracting files'):
    while True:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            os.remove(zip_path)  # delete zip file after extraction
            break  # break out of the while loop
        except PermissionError:
            # If the zip file is in use, wait for 1 second and try again
            time.sleep(1)

print("Done Extracting")
# Move hdr and lan files to images folder
for root, dirs, files in os.walk(extract_folder):
    for f in files:
        if f.endswith(('.hdr', '.lan')):
            src_path = os.path.join(root, f)
            dst_path = os.path.join(images_folder, f)
            shutil.move(src_path, dst_path)
print("Done Moving")

print("Done!")