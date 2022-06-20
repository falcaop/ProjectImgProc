# Segmentação de áreas de florestas em imagens via satélite
## Participantes
* Diogo Castanho Emídio - 11297274
* Pedro Falcão Rocha - 12692408
* Pedro Henrique Magalhães Cisdeli - 10289804

## Objetivo
O objetivo do presente projeto é realizar a segmentação/classificação de áreas de florestas em imagens aéreas, podendo ter como aplicação estudo e monitoramento ambiental para análise de avanço do desmatamento. Para isso, por meio de processos de segmentação e descrição, tais áreas serão tanto destacadas nas imagens originais quanto extraídas em representações isoladas. As fotos são oriundas do satélite [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2), do Google Earth e de outras fontes que utilizam esses serviços.

## Imagens de entrada
Como dados de entrada, inicialmente, foram selecionados dois datasets de [8 bandas (B01, ..., B08)](https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/#available-bands-and-data) da base do Sentinel-2 para formar a imagem rasterizada.

1. 2018-10-13, Sentinel-2B L1C

![area_urbana](/inputs/Bauru_1.png "Residência em área urbana")

Para verificar se o programa consegue distinguir as árvores das casas.

2. Outfile

![area_rural](/inputs/Bauru_2.png "Residência em área rural")
