# Landscape classification with satellite images
## Developed by:
* Diogo Castanho Emídio - 11297274
* Pedro Falcão Rocha - 12692408
* Pedro Henrique Magalhães Cisdeli - 10289804

## Introduction
The main objective is to classify the landscape of an satellite image to provide information for ambiental studies. The datasets used are from the satellite [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) and Google Earth.
The input images are rasters formed by eight bands that will be processed with the intention of providing indexes and other usefull statistics. The landscape and forest classification is determined by a machine learning method called Naive Bayes.


## Selected images
For now, [both datasets](https://github.com/falcaop/ProjectImgProc/tree/main/data) are composed by [eight bands (B01, ..., B08)](https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/#available-bands-and-data) and provided by Sentinel-2:

1. 2018-10-13, Sentinel-2B L1C

![dataset_1](/github/2018-10-13_Sentinel-2B_L1C_hist.png)

2. outFile

![dataset_2](/github/outFile_hist.png)

## Steps descriptions

1. Load a satellite image 
2. Extract the blue, red, green, and NIR bands in separate images
3. Apply contrast to the input image and compare the difference.
3. Calculate the Normalized Difference Vegetation index described in the next section
4. Calculate the Normalized Difference Water index described in the next section
5. Identify and highlight areas of live vegetation in the input image
6. Use this data to assist a machine learning method in better classifying the type of landscape

## Processing of the input image
A contrast filter was applied to the input images to compare its effects on the vegetation and water indexes. The k value from the contrast operation is 0.035.

1. 2018-10-13, Sentinel-2B L1C
![input_image_01](/github/filtered_01.png)

2. outFile
![input_image_02](/github/filtered_02.png)

The contrast filter applied removed some of the brightness of the input image, so the lower frequencies were lost with this operation.\
With more testing it was determined that brightening the image resulted in worse indexes. 

## Normalized Difference Vegetation Index and Normalized Difference Water Index 
The Normalized Difference Vegetation Index **(NVDI)** and Normalized Difference Water Index **(NVWI)** are a simple graphical indicator used to avaluate live green vegetation and water.

NDVI examples with both datasets:

1. 2018-10-13, Sentinel-2B L1C

![dataset_1_nvdi](/github/2018-10-13_Sentinel-2B_L1C_NDVI.png)

2. outFile

![dataset_2_nvdi](/github/outfile_NDVI.png)

## Contrast effects on Vegetation and Water indexes
The contrast filter helped with both indexes to highlight and differentiate regions on the landscape. 
1. 2018-10-13, Sentinel-2B L1C

![dataset_1_compare](/github/indices_01.png)

2. outFile

![dataset_2_compare](/github/indices_02.png)

## Classification process with naive Bayes
The training set used a shapefile to describe geospatial data with the form of a vector.\
After the classification process an algorithm was developed to color the predicted regions with the respective colors.


The classes used for the Naive Bayes model are:
* Emergent Wetland
* Forested Wetland
* Herbaceous
* Sand
* Subtidal Haline
* WetSand

1. 2018-10-13, Sentinel-2B L1C

![dataset_1_classification](/github/classify.png)

The naive bayes model was successful even with the hard task to classify the lower left section of the image where there is the presence of a bay mixed with some wetland, wich the dictionary represents it as purple.

## References
- ENGESAT. **Como escolher imagens de satélite**. *Available on*: http://www.engesat.com.br/wp-content/uploads/Ebook-ENGESAT-Como-escolher-imagens-de-sat%C3%A9lite-_geral.pdf. Accessed on: 18 jun. 2022.
- GRAY, Avatar Patrick. **Open Source Geoprocessing Tutorial**. 2022. Available on: https://github.com/patrickcgray/open-geo-tutorial. Accessed on: 18 june. 2022.
