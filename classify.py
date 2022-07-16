import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show, show_hist, reshape_as_raster, reshape_as_image
from rasterio.windows import Window
from rasterio.mask import mask
from shapely.geometry import mapping
import geopandas as gpd
import folium
import os
from sklearn.naive_bayes import GaussianNB

# --- Auxiliar functions
colors = dict((
    (0, (48, 156, 214, 255)),   # Blue - Water
    (1, (139,69,19, 255)),      # Brown - WetSand
    (2, (96, 19, 134, 255)),    # Purple - Emergent Wetland
    (3, (244, 164, 96, 255)),   # Tan - Sand
    (4, (206, 224, 196, 255)),  # Lime - Herbaceous
    (5, (34, 139, 34, 255)),    # Forest Green - Forest
))

def color_stretch(image, index):
    colors = image[:, :, index].astype(np.float64)
    for b in range(colors.shape[2]):
        colors[:, :, b] = rasterio.plot.adjust_band(colors[:, :, b])
    return colors

def str_class_to_int(class_array):
    class_array[class_array == 'Subtidal Haline'] = 0
    class_array[class_array == 'WetSand'] = 1
    class_array[class_array == 'Emergent Wetland'] = 2
    class_array[class_array == 'Sand'] = 3
    class_array[class_array == 'Herbaceous'] = 4
    class_array[class_array == 'Forested Wetland'] = 5
    return(class_array.astype(int))

# Dataset selection, default: outFile
def dataSetSelect():
    filePath = "data/data_01"
    bandPaths = [os.path.join(filePath, f) for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
    bandPaths.sort()
    return bandPaths

# --- Loading bands
bandPaths = dataSetSelect()

# --- New Dir and preparing raster
dir = "data/rasters/"

# Check if already exists
if not os.path.exists(dir):
    os.makedirs(dir)

newFilePath = dir + 'raster.tif'

with rasterio.open(bandPaths[0]) as src0:
    meta = src0.meta
meta.update(count = len(bandPaths))

with rasterio.open(newFilePath, 'w', **meta) as dst:
    for id, layer in enumerate(bandPaths, start=1):
        with rasterio.open(layer) as src1:
            dst.write_band(id, src1.read(1))

# ---
data = rasterio.open(newFilePath)

# Raster check
clipped_img = data.read([4,3,2])[:, 150:600, 250:1400]
fig, ax = plt.subplots(figsize=(10,7))
show(clipped_img[:, :, :], ax=ax, transform=data.transform)

# Training set
shapefile = gpd.read_file("data/rcr/rcr_landcover.shp")
# Converting the projections
shapefile = shapefile.to_crs({'init': 'epsg:4326'})


# Shapely
geoms = shapefile.geometry.values
geometry = geoms[0]
# transform to GeoJSON format
feature = [mapping(geometry)] # can also do this using polygon.__geo_interface__

# Raster values
img, transform = mask(data, feature, crop=True)
data.close()

# --- Training Data for random forest
x = np.array([], dtype=np.int8).reshape(0,8)
y = np.array([], dtype=np.string_)

with rasterio.open(newFilePath) as src:
    bandCount = src.count
    for index, geom in enumerate(geoms):
        feature = [mapping(geom)]
        # the mask function returns an array of the raster pixels within this feature
        out_image, out_transform = mask(src, feature, crop=True)
        # eliminate all the pixels with 0 values for all 8 bands - AKA not actually part of the shapefile
        out_image_trimmed = out_image[:,~np.all(out_image == 0, axis=0)]
        # eliminate all the pixels with 255 values for all 8 bands - AKA not actually part of the shapefile
        out_image_trimmed = out_image_trimmed[:,~np.all(out_image_trimmed == 255, axis=0)]
        # reshape the array to [pixel count, bands]
        out_image_reshaped = out_image_trimmed.reshape(-1, bandCount)
        # append the labels to the y array
        y = np.append(y,[shapefile["Classname"][index]] * out_image_reshaped.shape[0])
        # stack the pizels onto the pixel array
        x = np.vstack((x,out_image_reshaped))


# What are our classification labels?
labels = np.unique(shapefile["Classname"])
print('\n')
print('The training data include {n} classes: {classes}\n'.format(n=labels.size,
                                                                classes=labels))
# --- ML Model
model = GaussianNB()
model.fit(x, y)

# --- Classification process
with rasterio.open(newFilePath) as src:
    img = src.read()[:, 150:600, 250:1400]

reshaped_img = reshape_as_image(img)
predict = model.predict(reshaped_img.reshape(-1, 8))
predict = predict.reshape(reshaped_img[:, :, 0].shape)
predict = str_class_to_int(predict)

# Max pixel value
max = int(np.max(predict))

# Normalize to float 0, 1
for k in colors:
    v = colors[k]
    _v = [_v / 255.0 for _v in v]
    colors[k] = _v

index_colors = [colors[key] if key in colors else
                (255, 255, 255, 0) for key in range(0, max+1)]
cmap = plt.matplotlib.colors.ListedColormap(index_colors, 'Classification', max+1)

# --- Visualization
fig, axs = plt.subplots(2,1,figsize=(10,7))

img_stretched = color_stretch(reshaped_img, [4, 3, 2])
axs[0].imshow(img_stretched)

axs[1].imshow(predict, cmap=cmap, interpolation='none')

fig.show()
plt.show()
