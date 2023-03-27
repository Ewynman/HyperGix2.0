import time
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import json
import numpy as np
import requests
import sys
import argparse
import os
import shutil
import zipfile
import time
from tqdm import tqdm
import spectral as sp

geolocator = Nominatim(user_agent='myapplication')

#Make search window 
window = tk.Tk()
window.title('Location Finder')

header_label = tk.Label(window, text='Enter an address:')
header_label.pack(pady=10)

address_entry = tk.Entry(window, width=50)
address_entry.pack(pady=10)

from_label = tk.Label(window, text='Enter a from date (YYYY-MM-DD):')
from_label.pack(pady=5)

from_entry = tk.Entry(window, width=50)
from_entry.pack(pady=5)

to_label = tk.Label(window, text='Enter a to date (YYYY-MM-DD):')
to_label.pack(pady=5)

to_entry = tk.Entry(window, width=50)
to_entry.pack(pady=5)

latitude = 0.0
longitude = 0.0

# Create a function to display the latitude and longitude
def show_location():
    global from_date, to_date, dataset
    address = address_entry.get()
    from_date = from_entry.get()
    to_date = to_entry.get()

    
    from_label.config(text=f'From date: {from_date}')
    to_label.config(text=f'To date: {to_date}')
    
    try:
        location = geolocator.geocode(address, exactly_one=False)

        # Check if the location was found
        if location is not None:
            # Create a new window to display the possible locations
            location_window = tk.Toplevel(window)
            location_window.title('Choose a location')

            # Create a label for the possible locations
            possible_label = tk.Label(location_window, text=f'Found {len(location)} possible locations:')
            possible_label.pack(pady=50)

            # Create a listbox to display the possible locations
            location_listbox = tk.Listbox(location_window, width=50)
            location_listbox.pack(pady=100)

            # Add each location to the listbox
            for loc in location:
                location_listbox.insert(tk.END, loc.address)

            # Create a function to select a location
            def select_location(index, location):
                selected_location = location[index]
                
                global latitude, longitude
                # Get the latitude and longitude of the selected location
                latitude, longitude = selected_location.latitude, selected_location.longitude
                
                # Display the latitude and longitude in the main window
                lat_label.config(text=f'Latitude: {latitude}')
                long_label.config(text=f'Longitude: {longitude}')
                error_label.config(text='')

                

                # Close the location window
                location_window.destroy()

            # Create a button to select a location
            select_button = tk.Button(location_window, text='Select', command=lambda: select_location(location_listbox.curselection()[0], location))
            select_button.pack(pady=10)
        else:
            # Display an error message if the location was not found
            error_label.config(text='Location not found')
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        # Display an error message if there was a problem connecting to the geolocation service
        error_label.config(text='Error: Unable to connect to the geolocation service. Please check your internet connection and try again.')

# Create a button to show the location
show_button = tk.Button(window, text='Show', command=show_location)
show_button.pack(pady=10)

# Create labels to display the latitude and longitude
lat_label = tk.Label(window, text='')
lat_label.pack(pady=5)
long_label = tk.Label(window, text='')
long_label.pack(pady=5)

# Create a label to display errors
error_label = tk.Label(window, fg='red')
error_label.pack(pady=10)

# Run the GUI main loop
window.mainloop()

#Use this for analysis
print(latitude, longitude)

# send http request
def sendRequest(url, data, apiKey = None):  
    json_data = json.dumps(data)
    
    if apiKey == None:
        response = requests.post(url, json_data)
    else:
        headers = {'X-Auth-Token': apiKey}              
        response = requests.post(url, json_data, headers = headers)    
    
    try:
      httpStatusCode = response.status_code 
      if response == None:
          print("No output from service")
          sys.exit()
      output = json.loads(response.text)	
      if output['errorCode'] != None:
          print(output['errorCode'], "- ", output['errorMessage'])
          sys.exit()
      if  httpStatusCode == 404:
          print("404 Not Found")
          sys.exit()
      elif httpStatusCode == 401: 
          print("401 Unauthorized")
          sys.exit()
      elif httpStatusCode == 400:
          print("Error Code", httpStatusCode)
          sys.exit()
    except Exception as e: 
          response.close()
          print(e)
          sys.exit()
    response.close()
    
    return output['data']


if __name__ == '__main__': 
    username = 'wynmane1'
    password = 'Edtv10052002!'  
    
    print("\nRunning Scripts...\n")
    
    serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    
    # login
    payload = {'username' : username, 'password' : password}
    
    apiKey = sendRequest(serviceUrl + "login", payload)
    
    print("API Key: " + apiKey + "\n")
    
    #Dataset To Be Searched
    datasetName = "EO-1 Hyperion"

    #Spatial Filter
    spatialFilter = {'filterType': 'mbr',
                    'lowerLeft': {'latitude': latitude, 'longitude': longitude},
                    'upperRight': {'latitude': latitude, 'longitude': longitude}}

    #Date Filter
    temporalFilter = {'start': from_date, 'end': to_date}
    
    payload = {'datasetName' : datasetName,
                               'spatialFilter' : spatialFilter,
                               'temporalFilter' : temporalFilter}                     
    
    #Search and Display number of datasets
    print("Searching datasets...\n")
    datasets = sendRequest(serviceUrl + "dataset-search", payload, apiKey)
    
    print("Found ", len(datasets), " datasets\n")
    
    # download datasets
    for dataset in datasets:
        acquisitionFilter = {"end": to_date,
                             "start": from_date }        
            
        payload = {'datasetName' : dataset['datasetAlias'], 
                                 'maxResults' : 2,
                                 'startingNumber' : 1, 
                                 'sceneFilter' : {
                                                  'spatialFilter' : spatialFilter,
                                                  'acquisitionFilter' : acquisitionFilter}}
        
        # Now I need to run a scene search to find data to download
        print("Searching scenes...\n\n")   
        
        scenes = sendRequest(serviceUrl + "scene-search", payload, apiKey)
    
        # Did we find anything?
        if scenes['recordsReturned'] > 0:
            # Aggregate a list of scene ids
            sceneIds = []
            for result in scenes['results']:
                # Add this scene to the list I would like to download
                sceneIds.append(result['entityId'])
            
            # Find the download options for these scenes
            # NOTE :: Remember the scene list cannot exceed 50,000 items!
            payload = {'datasetName' : dataset['datasetAlias'], 'entityIds' : sceneIds}
                                
            downloadOptions = sendRequest(serviceUrl + "download-options", payload, apiKey)
        
            # Aggregate a list of available products
            downloads = []
            for product in downloadOptions:
                    # Make sure the product is available for this scene
                    if product['available'] == True:
                         downloads.append({'entityId' : product['entityId'],
                                           'productId' : product['id']})
                         
            # Did we find products?
            if downloads:
                requestedDownloadsCount = len(downloads)
                # set a label for the download request
                label = "download-sample"
                payload = {'downloads' : downloads,
                                             'label' : label}
                # Call the download to get the direct download urls
                requestResults = sendRequest(serviceUrl + "download-request", payload, apiKey)          
                              
                # PreparingDownloads has a valid link that can be used but data may not be immediately available
                # Call the download-retrieve method to get download that is available for immediate download
                if requestResults['preparingDownloads'] != None and len(requestResults['preparingDownloads']) > 0:
                    payload = {'label' : label}
                    moreDownloadUrls = sendRequest(serviceUrl + "download-retrieve", payload, apiKey)
                    
                    downloadIds = []  
                    
                    for download in moreDownloadUrls['available']:
                        if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                            downloadIds.append(download['downloadId'])
                            print("DOWNLOAD: " + download['url'])
                        
                    for download in moreDownloadUrls['requested']:
                        if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                            downloadIds.append(download['downloadId'])
                            print("DOWNLOAD: " + download['url'])
                     
                    # Didn't get all of the reuested downloads, call the download-retrieve method again probably after 30 seconds
                    while len(downloadIds) < (requestedDownloadsCount - len(requestResults['failed'])): 
                        preparingDownloads = requestedDownloadsCount - len(downloadIds) - len(requestResults['failed'])
                        print("\n", preparingDownloads, "downloads are not available. Waiting for 30 seconds.\n")
                        time.sleep(30)
                        print("Trying to retrieve data\n")
                        moreDownloadUrls = sendRequest(serviceUrl + "download-retrieve", payload, apiKey)
                        for download in moreDownloadUrls['available']:                            
                            if download['downloadId'] not in downloadIds and (str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']):
                                downloadIds.append(download['downloadId'])
                                print("DOWNLOAD: " + download['url']) 
                            
                else:
                    # Get all available downloads
                    for download in requestResults['availableDownloads']:
                        # TODO :: Implement a downloading routine
                        print("DOWNLOAD: " + download['url'])   
                print("\nAll downloads are available to download.\n")
        else:
            print("Search found no results.\n")
                
    # Logout so the API Key cannot be used anymore
    endpoint = "logout"  
    if sendRequest(serviceUrl + endpoint, None, apiKey) == None:        
        print("Logged Out\n\n")
    else:
        print("Logout Failed\n\n")

while True:
    response = input("Are you done downloading the needed files? (Y/N)")
    if response.upper() == "Y":
        # If the user enters Y (or y), move on to other code
        print("Great, moving on to other code!")
        break
    elif response.upper() == "N":
        # If the user enters N (or n), sleep for 30 seconds and ask again
        print("Please download the needed files and try again in 30 seconds.")
        time.sleep(30)
    else:
        # If the user enters anything else, ask again
        print("Invalid response, please enter Y or N.")

# Set the download folder and the destination folder
download_folder = r'C:\Users\edwar\Downloads'
extract_folder = r'C:\Users\edwar\OneDrive\Research\MyCode\HyperGix2.0\Extracted'
images_folder = r'C:\Users\edwar\OneDrive\VS-Code\GitHub Stuff\HyperGix2.0\images'

# Extract all files from download_folder to extract_folder with a progress bar
for root, dirs, files in os.walk(download_folder):
    for f in files:
        # Check if file is a zip file
        if f.endswith(('.zip', '.ZIP')):
            # Construct paths for the source zip file and the destination folder
            zip_path = os.path.join(root, f)
            dest_folder = os.path.join(extract_folder, os.path.splitext(f)[0])
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
for root, dirs, files in os.walk(extract_folder):
    for f in files:
        # Check if file is a .hdr or .lan file
        if f.endswith(('.hdr', '.lan')):
            # Construct paths for the source file and the destination file
            src_path = os.path.join(root, f)
            dst_path = os.path.join(images_folder, f)
            # Move the file to the destination folder
            shutil.move(src_path, dst_path)

# List the files in the images_folder
if os.path.exists(images_folder):
    print("The following files have been moved to the 'images' folder:")
    for f in os.listdir(images_folder):
        print(f)

# path to the images folder
images_folder = r'C:\Users\edwar\OneDrive\VS-Code\GitHub Stuff\HyperGix2.0\images'

# loop over all .hdr files in the images folder
for file in os.listdir(images_folder):
    if file.endswith('.hdr'):
        print(f'File: {file}')
        
        # read the ENVI header file
        hdr_file = os.path.join(images_folder, file)
        hdr = sp.envi.read_envi_header(hdr_file)

        # extract some metadata
        num_bands = hdr['bands']
        wavelengths = np.array([float(w) for w in hdr['wavelength']])
        interleave = hdr['interleave']
        rows, cols = hdr['lines'], hdr['samples']
        datatype = hdr['data type']

        # print the metadata
        print(f'Number of bands: {num_bands}')
        print(f'Wavelength range: {wavelengths[0]:.1f} - {wavelengths[-1]:.1f} nm')
        print(f'Interleave: {interleave}')
        print(f'Spatial dimensions: {rows} rows x {cols} columns')
        print(f'Data type: {datatype}')
        print()