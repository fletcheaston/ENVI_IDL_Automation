# Created by Fletcher Easton

import cv2
import os.path
import numpy as np
import sys
import time


def writeToFile(string, filename=r"coloredMosaicPaths.txt"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


def readImage(path):
    if(os.path.isfile(path)):
        try:
            return(cv2.imread(path))
        except:
            pass

    return(None)


def saveImage(img, path):
    cv2.imwrite(path, img)


def placeLegend(legendImg, mapImg, legendToMapScale=0.5, side="LEFT"):
    mapHeight, mapWidth, mapChannels = mapImg.shape
    legendHeight, legendWidth, legendChannels = legendImg.shape
    
    scalingFactor = mapHeight / legendHeight * legendToMapScale
    scaledHeight = int(legendHeight * scalingFactor)
    scaledWidth  = int(legendWidth * scalingFactor)
    
    resizedLegendImg = cv2.resize(legendImg, (scaledWidth, scaledHeight))
    
    mapWithLegendImg = np.zeros((max(mapHeight, scaledHeight), mapWidth + scaledWidth, 3), np.uint8)
    
    if(side.upper() == "LEFT"):
        mapWithLegendImg[0:scaledHeight, 0:scaledWidth] = resizedLegendImg
        mapWithLegendImg[0:mapHeight, scaledWidth:mapWidth + scaledWidth] = mapImg
    elif(side.upper() == "RIGHT"):
        mapWithLegendImg[0:scaledHeight, mapWidth:mapWidth + scaledWidth] = resizedLegendImg
        mapWithLegendImg[0:mapHeight, 0:mapWidth] = mapImg
    
    return(mapWithLegendImg)


if __name__ == '__main__':
    legend = readImage("Legend.png")
    
    with open("coloredMosaicPaths.txt") as f:
        allFilePaths = f.readlines()
    
    for path in allFilePaths:
        map = readImage(path.strip())

        if(map is not None):
            mapWithLegend = placeLegend(legend, map)
            savePath = "{0}_withLegend.png".format(path)
            saveImage(mapWithLegend, savePath)
        elif:
            writeToFile(path, "coloredMosaicPaths.txt")
