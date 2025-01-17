# Created by Fletcher Easton

import cv2
import numpy
import os.path
import sys
import time
from PIL import Image
from tkinter import messagebox

def clearFile(filename=r"coloredMosaicPaths.txt"):
    with open(filename, "w+") as file:
        pass


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
    cv2.imwrite(path, img)


def placeLegend(legendImg, mapImg, legendToMapScale=0.25, side="LEFT"):
    numpyMap = numpy.array(mapImg)
    numpyLegend = numpy.array(legendImg)

    legendHeight, legendWidth, _ = numpyLegend.shape
    mapHeight, mapWidth, _ = numpyMap.shape

    largestSize = int(mapHeight * 0.10)
    increment = int(mapHeight * 0.01)
    finalSize = 0.9

    startPixel = numpyMap[0][0]

    while(True):
        ratio = largestSize / legendWidth
        maxY = int(legendHeight * ratio)
        maxX = int(legendWidth * ratio)

        if(numpy.unique(numpyMap[:maxY,:maxX]).size > 3):
            break

        largestSize += increment

    maxX = int(maxX * finalSize)
    maxY = int(maxY * finalSize)

    numpyLegend = cv2.resize(numpyLegend,(maxX, maxY))
    numpyMap[0:maxY, 0:maxX] = numpyLegend

    numpyMap = cv2.cvtColor(numpyMap, cv2.COLOR_RGB2BGR)
    return(numpyMap)


if __name__ == '__main__':
    legend = readImage("Legend.png")

    with open("coloredMosaicPaths.txt") as f:
        allFilePaths = f.readlines()

    allDirs = set([path.strip() for path in allFilePaths])
    clearFile("coloredMosaicPaths.txt")
    
    notFoundDirs = set()
    foundDirs = set()

    for directory in allDirs:
        # Recursively walks through all the sub-directories in the specified directory.
        for dirpath, _, allFiles in os.walk(directory):

            mosaicFiles = [file for file in allFiles if file.startswith("coloredMosaicFile")]

            if(len(mosaicFiles) > 0):
                for fileName in mosaicFiles:
                    fullPath = os.path.join(os.path.abspath(dirpath), fileName)
                    map = readImage(fullPath)

                    if(map is not None):
                        mapWithLegend = placeLegend(legend, map)
                        savePath = os.path.join(os.path.abspath(dirpath), "finalMap.png")
                        saveImage(mapWithLegend, savePath)
                        foundDirs.add(savePath)
                    else:
                        notFoundDirs.add(directory)

            else:
                notFoundDirs.add(directory)
    
    for dir in notFoundDirs:
        writeToFile(dir, "coloredMosaicPaths.txt")

    if(len(notFoundDirs) > 0):
        messagebox.showwarning("Files Not Found", "\n".join(notFoundDirs))

    if(len(foundDirs) > 0):
        messagebox.showinfo("Found Files", "\n".join(foundDirs))
    else:
        messagebox.showwarning("No Files Found", "Warning: No maps found in the specified directories.")
