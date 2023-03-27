import os
import shutil
import zipfile
import numpy as np
import spectral as sp
from tqdm import tqdm
from tkinter import *
from tkinter import filedialog

# Functions for handling button clicks
def browse_download_folder():
    download_folder.set(filedialog.askdirectory())

def browse_extract_folder():
    extract_folder.set(filedialog.askdirectory())

def browse_images_folder():
    images_folder.set(filedialog.askdirectory())

def process_files():
    # Extract all files from download_folder to extract_folder with a progress bar
    for root, dirs, files in os.walk(download_folder.get()):
        for f in files:
            # Check if file is a zip file
            if f.endswith(('.zip', '.ZIP')):
                # Construct paths for the source zip file and the destination folder
                zip_path = os.path.join(root, f)
                dest_folder = os.path.join(extract_folder.get(), os.path.splitext(f)[0])
                # Create the destination folder if it does not exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                # Extract the zip file to the destination folder with a progress bar
                with tqdm(total=100, desc=f"Extracting {zip_path} ...") as pbar:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        for member in zip_ref.infolist():
                            zip_ref.extract(member, dest_folder)
                            pbar.update(100 / len(zip_ref.infolist()))

    # Move all .hdr and .lan files to images_folder
    for root, dirs, files in os.walk(extract_folder.get()):
        for f in files:
            # Check if file is a .hdr or .lan file
            if f.endswith(('.hdr', '.lan')):
                # Construct paths for the source file and the destination file
                src_path = os.path.join(root, f)
                dst_path = os.path.join(images_folder.get(), f)
                # Move the file to the destination folder
                shutil.move(src_path, dst_path)

    output_text.delete(1.0, END)
    # List the files in the images_folder
    if os.path.exists(images_folder.get()):
        output_text.insert(INSERT, "The following files have been moved to the 'images' folder:\n")
        for f in os.listdir(images_folder.get()):
            output_text.insert(INSERT, f"{f}\n")

# Create the main window
root = Tk()
root.title("File Processing GUI")

# Create StringVars for storing folder paths
download_folder = StringVar()
extract_folder = StringVar()
images_folder = StringVar()

# Create input widgets
Label(root, text="Download folder:").grid(row=0, column=0, sticky=W)
Entry(root, textvariable=download_folder, width=50).grid(row=0, column=1)
Button(root, text="Browse", command=browse_download_folder).grid(row=0, column=2)

Label(root, text="Extract folder:").grid(row=1, column=0, sticky=W)
Entry(root, textvariable=extract_folder, width=50).grid(row=1, column=1)
Button(root, text="Browse", command=browse_extract_folder).grid(row=1, column=2)

Label(root, text="Images folder:").grid(row=2, column=0, sticky=W)
Entry(root, textvariable=images_folder, width=50).grid(row=2, column=1)
Button(root, text="Browse", command=browse_images_folder).grid(row=2, column=2)

# Create output text widget
Label(root, text="Output:").grid(row=3, column=0, sticky=W)
output_text = Text(root, wrap=WORD, width=60, height=10)
output_text.grid(row=3, column=1, columnspan=2)

# Create the process button
Button(root, text="Process Files", command=process_files).grid(row=4, column=1, pady=10)

# Start the main loop
root.mainloop()
