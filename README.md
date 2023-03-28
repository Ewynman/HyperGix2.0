<p align="center">
  <a href="" rel="noopener">
 <img width=500px height=200px src="./images/logo.png" alt="Bot logo"></a>
</p>

<h3 align="center">Development of a Processing Workflow for Hyperspectral Images</h3>


---

## 📝 Table of Contents

- [About](#about)
- [Requiremnets](#requiremnets)
- [How it works](#working)
- [Authors](#authors)
<!-- - [Acknowledgments](#acknowledgement) -->

## 🧐 About <a name = "about"></a>

This code is designed to search for and download satellite images using the United States Geological Survey (USGS) API. The user inputs an address, date range, and selects from a list of possible locations to search for images in the EO-1 Hyperion dataset. The images are then downloaded and extracted to a specified folder. From there some data is grabed and displayed about each image

## Installation 

```
git clone https://github.com/Ewynman/HyperGix2.0.git
cd HyperGix2.0
```

## 🎥 Requiremnets<a name = "requiremnets"></a>

- Python 3.x
- geopy
```
pip install geopy
```
- tkinter
```
pip install tkinter
```
- requests
```
pip install request
```
- tqdm
```
pip install tqdm
```
- spectral
```
pip install spectral
```

## 💭 How to Use <a name = "working"></a>

1. Open the SearchApp.py file in a Python editor or IDE.<br>
2. Install the required libraries if they are not already installed.<br>
3. Run the SearchApp.py file.<br>
4. Enter an address, date range, and select a location from the list of possible locations.<br>
5. The latitude and longitude of the selected location will be displayed and close the window<br>
6. Satellite images in the EO-1 Hyperion dataset will be searched for within the specified date range and location.<br>
7. Select download links from the list and press continue when downloads are complete.
8. The images will be extracted to the specified folder.<br>
9. The file names of the downloaded images will be displayed.<br>
10. Spectral analysis will be done on the images (Coming Soon)

## ✍️ Authors <a name = "authors"></a>

- [@Ewynman](https://github.com/Ewynman) 


<!-- ## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References -->
