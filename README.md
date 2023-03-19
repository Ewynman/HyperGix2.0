<p align="center">
  <a href="" rel="noopener">
 <img width=500px height=200px src="./images/logo.png" alt="Bot logo"></a>
</p>

<h3 align="center">Development of a Processing Workflow for Hyperspectral Images</h3>


---

## 📝 Table of Contents

- [About](#about)
- [Demo / Working](#demo)
- [How it works](#working)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

Hyperspectral images (HSI) are collections of grayscale images of the same scene collected over narrow light wavelength intervals. HSI’s have been widely used in a variety of fields, be it earth sciences, manufacturing, agriculture, food safety, or defense and homeland security. The growing number of sensing platforms provides a unique opportunity for hyperspectral data to be easily accessible (and usable) not only by scientists and practitioners but also by the broader public in a similar fashion as, say Google Earth, potentially opening unique opportunities for hyperspectral citizen science. Yet, publicly available comprehensive sets of data continue to be limited, and full workflow interfaces (that includes data search and access, visualization, and processing) are missing. In preliminary work a prototype desktop application for downloading, viewing, and processing hyperspectral data was developed. The application, built using Python, allows an user to browse their hyperspectral image library, examine the spectra of any pixel in the image, assign pixels to material classes, and perform Principal Component Analysis (PCA) and automatic spectra classification using a spectral angle mapping. It also allows the user to create custom material classes of their own and examine the spectra of pixels assigned to each class. The data ingestion provided by an USGS Search module provides an easy search engine to query the United States Geological Survey’s vast repository of Hyperion hyperspectral images and seamlessly download them for analysis in the application. 
We are now re-writing the application to read an image and perform a much more complex set of operations with it. Not only can we get the basic image data such as the number of bands and the shape of the image but we can also get some more in depth views of the image using Spectral Python. With this we can display a class map for the image with an overlay on to it displaying each class with a unique color. We have also been able to connect to the USGS repository of Hyperion hyperspectral images to download them and perform the aforementioned analysis. Up to this point in time we do not have the full connection to the database as we are waiting for access approval to the database itself. By developing better workflows and interfaces for hyperspectral data, we can help make this technology more accessible and usable for a wider range of scientists, practitioners, and even members of the general public. This, in turn, can help unlock new opportunities for scientific discovery and practical applications.


## 🎥 Demo / Working <a name = "demo"></a>

Come Back SOon!!

## 💭 How it works <a name = "working"></a>

This is a Python script that uses the USGS (United States Geological Survey) M2M (Machine-to-Machine) API to search, download and retrieve satellite images. The script sends HTTP requests to the M2M API and receives responses in JSON format. It includes a sendRequest() function that is used to handle the HTTP requests. This function takes a URL, a dictionary of data to be sent, and an optional API key as arguments, and returns a dictionary containing the response data. The script first logs in to the API by sending a POST request with the username and password to the login endpoint. It then performs a search for satellite imagery by sending a POST request to the dataset-search endpoint with parameters for the dataset name, a spatial filter (bounding box defined by lower left and upper right latitudes and longitudes), and a temporal filter (start and end dates). The API returns a list of datasets matching the search criteria, and the script prints out the number of datasets found. The script then loops through the list of datasets and performs a scene search by sending a POST request to the scene-search endpoint with the dataset alias, a spatial filter, and an acquisition filter (start and end dates). The API returns a list of scenes matching the search criteria, and the script aggregates a list of scene IDs. The script then sends a POST request to the download-options endpoint with the dataset alias and scene IDs to retrieve download options for the scenes. The API returns a list of available products for each scene, and the script aggregates a list of product IDs and entity IDs. The script then sends a POST request to the download-request endpoint with the product and entity IDs and a label for the download request. The API returns a response that includes a list of download IDs. If there are any preparing downloads, the script sends a POST request to the download-retrieve endpoint to retrieve the direct download URLs for the downloads that are available for immediate download. The script then loops through the list of downloads and prints out the download URL for each download.

We are doing more and more with this each and every day so come back for some updates


### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
git clone https://github.com/Ewynman/HyperGix2.0.git
```

To Run use this command and your USGS Username and Password

```
python SearchAndDownload.py -u username -p password
```

End with an example of getting some data out of the system or using it for a little demo.

## ✍️ Authors <a name = "authors"></a>

- [@Ewynman](https://github.com/Ewynman) 


<!-- ## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References -->
