import spectral as s
import matplotlib.pyplot as plt

path = '92AV3C.lan'
img = s.open_image(path)
arr = img.load()

# Display hyperspectral image and save it
view = s.imshow(arr, (29, 19, 9))
plt.savefig('hyperspectral_image.png')

# Load and display Ground truth image and save it
gt = s.open_image('92AV3GT.GIS').read_band(0)
view = s.imshow(classes=gt)
plt.savefig('ground_truth_image.png')