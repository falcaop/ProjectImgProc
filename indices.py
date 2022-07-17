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
        return ["data/data_01/2018-10-13, Sentinel-2B L1C, B02.tiff",
                "data/data_01/2018-10-13, Sentinel-2B L1C, B03.tiff",
                "data/data_01/2018-10-13, Sentinel-2B L1C, B04.tiff",
                "data/data_01/2018-10-13, Sentinel-2B L1C, B08.tiff"]
    else:
        return ["data/data_02/outFile_B02.tiff",
                "data/data_02/outFile_B03.tiff",
                "data/data_02/outFile_B04.tiff",
                "data/data_02/outFile_B08.tiff"]

# Applies sigmoidal contrast enhancement to all pixels equally
def contrast(img, k=0.035):
    return (255 / (1 + np.exp(-k * (img.astype(np.int32) - 127)))).astype(np.uint8)

def getNDVI(img):
    # Ignoring erros related to NaN pixels
    np.seterr(divide='ignore', invalid='ignore')
    red = img[2]
    NIR = img[3]
    return (NIR.astype(float)-red.astype(float))/(NIR.astype(float)+red.astype(float))

def getNDWI(img):
    # Ignoring erros related to NaN pixels
    np.seterr(divide='ignore', invalid='ignore')
    green = img[1]
    NIR = img[3]
    return (green.astype(float)-NIR.astype(float))/(green.astype(float)+NIR.astype(float))

# --- Loading bands blue, green, red and NIR respectively
bands = dataSetSelect(int(input("Dataset selection [1, 2]: ")))
arr = []
for band in bands:
    with rasterio.open(band) as f:
        arr.append(f.read(1))

# No need for a clip (for now) since the raster is relatively small
# And the there is not much use of computing resorces
img = np.array(arr, dtype=arr[0].dtype)

k_input = float(input("k = "))
newImg = contrast(img, k=k_input)

#--- Indices
# Normalized Difference Vegetation Index
NDVI = getNDVI(img)

# Altered Normalized Difference Vegetation Index
_NDVI = getNDVI(newImg)

# Normalized Difference Water Index
NDWI = getNDWI(img)

# Altered Normalized Difference Water Index
_NDWI = getNDWI(newImg)

#--- Visualization - Image and histogram
# Image
fig, axs = plt.subplots(2, 2, figsize=(15, 7))
show(img[[2, 1, 0], :, :], ax=axs[0,0],
     title='Image (blue, green, red and NIR bands)')

show(newImg[[2, 1, 0], :, :], ax=axs[0,1],
     title='Filtered Image (blue, green, red and NIR bands)')

# Histogram
rasterio.plot.show_hist(img, ax=axs[1,0], bins=50,
                        histtype='stepfilled', lw=0.0, stacked=False, alpha=0.8)
rasterio.plot.show_hist(newImg, ax=axs[1,1], bins=50,
                        histtype='stepfilled', lw=0.0, stacked=False, alpha=0.8)
axs[1,0].get_legend().remove()
axs[1,1].get_legend().remove()
plt.show()

# --- Indices plot
fig, axs = plt.subplots(2, 2, figsize=(15, 7))

# NDVI
ndviPlot = axs[0, 0].imshow(NDVI, cmap="RdYlGn")
axs[0, 0].set_title("NDVI")
fig.colorbar(ndviPlot, ax=axs[0, 0])

# NDWI
ndwiPlot = axs[0, 1].imshow(NDWI, cmap="RdYlGn")
axs[0, 1].set_title("NDWI")
fig.colorbar(ndwiPlot, ax=axs[0, 1])

# Modified img NDVI
_ndviPlot = axs[1, 0].imshow(_NDVI, cmap="RdYlGn")
axs[1, 0].set_title("Altered NDVI")
fig.colorbar(_ndviPlot, ax=axs[1, 0])

# Modified img NDWI
_ndwiPlot = axs[1, 1].imshow(_NDWI, cmap="RdYlGn")
axs[1, 1].set_title("Altered NDWI")
fig.colorbar(_ndviPlot, ax=axs[1, 1])


plt.show()
