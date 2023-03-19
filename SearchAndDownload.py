import json
import requests
import sys
import time
import argparse

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

    # User Input: Date Filter and Spatial Filter
    from_date = input("Enter start date (YYYY-MM-DD): ")
    to_date = input("Enter end date (YYYY-MM-DD): ")
    latitude1 = float(input("Enter lower left latitude: "))
    longitude1 = float(input("Enter lower left longitude: "))
    latitude2 = float(input("Enter upper right latitude: "))
    longitude2 = float(input("Enter upper right longitude: "))

    #Spatial Filter
    spatialFilter = {'filterType': 'mbr',
                    'lowerLeft': {'latitude': latitude1, 'longitude': longitude1},
                    'upperRight': {'latitude': latitude2, 'longitude': longitude2}}

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



'''
Todo:
    - Open Link, download, move file to working dir
    - Unzip
    - list files
    - Analyze
'''