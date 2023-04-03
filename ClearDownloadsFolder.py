import os

# Set the downloads folder
downloads_folder = r'C:\Users\edwar\OneDrive\VS-Code\GitHub Stuff\HyperGix2.0\images'

# Loop through all files in the downloads folder and delete .zip and .jpg files
for file in os.listdir(downloads_folder):
    if file.endswith('.zip') or file.endswith('.jpeg'):
        os.remove(os.path.join(downloads_folder, file))
        print(f"Deleted file: {file}")

print("Done!")
