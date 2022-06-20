# Landscape classification with satellite images
## Developed by:
* Diogo Castanho Emídio - 11297274
* Pedro Falcão Rocha - 12692408
* Pedro Henrique Magalhães Cisdeli - 10289804

## Introduction
The main objective is to classify the landscape of an satellite image to provide information for ambiental studies. The datasets used are from the satellite [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) and Google Earth.
The input images are rasters formed by eight bands that will be processed with the intention of providing indexes and other usefull statistics. The landscape and forest classification will be later developed with the help of a machine learning method that will be soon decided.


## Selected images
For now, [both datasets](https://github.com/falcaop/ProjectImgProc/tree/main/data) are composed by [eight bands (B01, ..., B08)](https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/#available-bands-and-data) and provided by Sentinel-2:

1. 2018-10-13, Sentinel-2B L1C

![dataset_1](/github/2018-10-13_Sentinel-2B_L1C_hist.png)

2. outFile

![dataset_2](/github/outFile_hist.png)

## Normalized Difference Vegetation Index
The Normalized Difference Vegetation Index **(NVDI)** is a simple graphical indicator used to avaluate live green vegetation:

1. 2018-10-13, Sentinel-2B L1C

![dataset_1_nvdi](/github/2018-10-13_Sentinel-2B_L1C_NDVI.png)

2. outFile

![dataset_2_nvdi](/github/outfile_NDVI.png)

## Future development expectations
With further development and processing we expect to be able to segmentate regions of interest, provide more useful information and classify the landscape.

## References
- ENGESAT. **Como escolher imagens de satélite**. *Available on*: http://www.engesat.com.br/wp-content/uploads/Ebook-ENGESAT-Como-escolher-imagens-de-sat%C3%A9lite-_geral.pdf. Accessed on: 18 jun. 2022.
- GRAY, Avatar Patrick. **Open Source Geoprocessing Tutorial**. 2022. Available on: https://github.com/patrickcgray/open-geo-tutorial. Accessed on: 18 june. 2022.
