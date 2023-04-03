import os
import pandas as pd
import shutil

images_folder = r'C:\Users\edwar\OneDrive\Research\MyCode\HyperGix2.0\Images'
extract_folder = r'C:\Users\edwar\OneDrive\Research\MyCode\HyperGix2.0\Extracted'

# Create a dataframe of all .hdr files in images_folder
hdr_df = pd.DataFrame(columns=['Filename', 'Path'])
for root, dirs, files in os.walk(images_folder):
    for f in files:
        if f.lower().endswith('.hdr'):
            path = os.path.join(root, f)
            hdr_df = pd.concat([hdr_df, pd.DataFrame({'Filename': [f], 'Path': [path]})], ignore_index=True)

print(hdr_df)

# Create a dataframe of all .jpg, .JPG, .jpeg, .JPEG files in images_folder
jpg_df = pd.DataFrame(columns=['Filename', 'Path'])
for root, dirs, files in os.walk(images_folder):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
            path = os.path.join(root, f)
            jpg_df = pd.concat([jpg_df, pd.DataFrame({'Filename': [f], 'Path': [path]})], ignore_index=True)

print(jpg_df)

# Compare the filenames of the .hdr and .jpg dataframes
matches = []
for hdr_index, hdr_row in hdr_df.iterrows():
    for jpg_index, jpg_row in jpg_df.iterrows():
        if hdr_row['Filename'].split('.')[0] == jpg_row['Filename'].split('.')[0]:
            matches.append((hdr_row['Path'], jpg_row['Path']))
            break

print(len(matches))

# Move the matching files to the extract_folder
for match in matches:
    hdr_path, jpg_path = match
    print(hdr_path)
    print(jpg_path)
    shutil.move(hdr_path, extract_folder)
    shutil.move(jpg_path, extract_folder)
