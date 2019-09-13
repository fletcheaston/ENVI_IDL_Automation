# Created by Fletcher Easton

import os.path
import sys
import time
from PIL import Image


def writeToFile(string, filename=r"coloredMosaicPaths.txt"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


def readImage(path):
    if(os.path.isfile(path)):
        try:
            raster = Image.open(path)
            img = raster.convert("RGB")
            return(img)
        except:
            pass

    return(None)


def saveImage(img, path):
    img.save(path)


def placeLegend(legendImg, mapImg, legendToMapScale=0.25, side="LEFT"):
    mapWidth, mapHeight = mapImg.size
    legendWidth, legendHeight = legendImg.size
    
    scalingFactor = mapHeight / legendHeight * legendToMapScale
    scaledHeight = int(legendHeight * scalingFactor)
    scaledWidth  = int(legendWidth * scalingFactor)
    
    mapWithLegendImg = Image.new('RGB', (mapWidth + scaledWidth, max(mapHeight, scaledHeight)), (0, 0, 0))

    legendImg = legendImg.resize((scaledWidth, scaledHeight))

    if(side == "LEFT"):
        legendOffset = (0, 0)
        mapOffset = (scaledWidth, 0)
    elif(side == "RIGHT"):
        legendOffset = (mapWidth, 0)
        mapOffset = (0, 0)

    mapWithLegendImg.paste(legendImg, legendOffset)
    mapWithLegendImg.paste(mapImg, mapOffset)

    return(mapWithLegendImg)


if __name__ == '__main__':
    legend = readImage("Legend.png")
    
    with open("coloredMosaicPaths.txt") as f:
        allFilePaths = f.readlines()
    
    for path in allFilePaths:
        path = path.strip()
        map = readImage(path)

        if(map is not None):
            mapWithLegend = placeLegend(legend, map)
            savePath = "test.png".format(path)
            saveImage(mapWithLegend, savePath)
        else:
            writeToFile(path, "coloredMosaicPaths.txt")
