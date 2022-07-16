import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show, show_hist
import folium

"""
Final image band structure:
Arr        Band
img[0]  -   blue
img[1]  -   green
img[2]  -   red
img[2]  -   NIR
More info about sentinel-2 L1C bands at: https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/#available-bands-and-data
"""

# Dataset selection, default: outFile
def dataSetSelect(op):
    if op == 1:
        return ["data/2018-10-13, Sentinel-2B L1C, B02.tiff",
                "data/2018-10-13, Sentinel-2B L1C, B03.tiff",
                "data/2018-10-13, Sentinel-2B L1C, B04.tiff",
                "data/2018-10-13, Sentinel-2B L1C, B08.tiff"]
    else:
        return ["data/outFile_B02.tiff",
                "data/outFile_B03.tiff",
                "data/outFile_B04.tiff",
                "data/outFile_B08.tiff"]

# Applies sigmoidal contrast enhancement to all pixels equally
def contrast(img, k=0.035):
    return (255 / (1 + np.exp(-k * (img.astype(np.int32) - 127)))).astype(np.uint8)

# Applies the contrast adjustment without modifying any chromatic component
def contrast_hsv(img, k=0.035):
    img_hsv = mpl.colors.rgb_to_hsv(img)
    img_hsv[:, :, 2] = contrast(img_hsv[:, :, 2].astype(np.uint32), k=k)

    return mpl.colors.hsv_to_rgb(img_hsv).astype(np.uint8)

# Normalize an image
def normalize(img):
    img = 255 * (img - np.min(img)) / (np.max(img) - np.min(img))

    return img

# Applies highlight
def highlight(img, rates=np.zeros(img.shape[-1])):
    img = img.astype(np.float32)

    for index, rate in enumerate(rates):
        img[:, :, index] = normalize(img[:, :, index] * (1 + rate)) if rate != -1 else np.zeros(img.shape[: 2])

    return img.astype(np.uint8)

# --- Loading bands blue, green, red and NIR respectively
bands = dataSetSelect(int(input("Dataset selection [1, 2]: ")))
arr = []
for band in bands:
    with rasterio.open(band) as f:
        arr.append(f.read(1))

# No need for a clip (for now) since the raster is relatively small
# And the there is not much use of computing resorces
img = np.array(arr, dtype=arr[0].dtype)
print("Image shape: {}".format(img.shape))

#--- NDVI
# Ignoring erros related to NaN pixels
np.seterr(divide='ignore', invalid='ignore')

# Separating bands of interest
red = img[2]
NIR = img[3]

# Normalized Difference Vegetation Index
NDVI = (NIR.astype(float) - red.astype(float)) / \
    (NIR.astype(float) + red.astype(float))

#--- Visualization - Image and histogram
# Image
fig, (axImg, axHist) = plt.subplots(1, 2, figsize=(20, 20))
show(img[[2, 1, 0], :, :], ax=axImg,
     title='Image (blue, green, red and NIR bands)')

# Histogram
rasterio.plot.show_hist(img, ax=axHist, bins=50,
                        histtype='stepfilled', lw=0.0, stacked=False, alpha=0.8)
axHist.get_legend().remove()

plt.show()

# NDVI
plt.title("NDVI")
plt.imshow(NDVI, cmap="RdYlGn")
plt.colorbar()
plt.show()
