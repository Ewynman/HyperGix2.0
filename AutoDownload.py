import os
import shutil
import time
import urllib.request
import zipfile
import webbrowser

download_folder = r"C:\Users\edwar\Downloads\\"
working_directory = r"C:\Users\edwar\OneDrive\Research\MyCode\HyperGix2.0\\"

# prompt user to input download URL
url = input("Enter a download URL: ")

# open URL in browser
webbrowser.open(url)

# download file
filename = url.split("/")[-1]
filepath = download_folder + filename
print("Downloaded:", filename)

# extract files
for filename in os.listdir(download_folder):
    if filename.endswith(".zip"):
        filepath = download_folder + filename
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(download_folder)
        os.remove(filepath)  # delete zip file after extraction
        print("Extracted and deleted:", filename)

# move .hdr files
for filename in os.listdir(download_folder):
    if filename.endswith(".hdr"):
        src_filepath = download_folder + filename
        dst_filepath = working_directory + filename
        shutil.move(src_filepath, dst_filepath)
        print("Moved:", filename)
    else:
        print("Does not include an hdr file:", filename)

print("Done!")
