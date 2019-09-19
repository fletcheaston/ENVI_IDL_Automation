# Created by Fletcher Easton

import os
import tasks
import tkinter
import sys
import logging
from configparser import SafeConfigParser
import io
import gui
import settings


def clearFile(filename=r"idlCommands.pro"):
    with open(filename, "w+") as file:
        pass


def writeToFile(string, filename=r"idlCommands.pro"):
    with open(filename, "a+") as file:
        file.write("\n")
        file.write(string.strip())
        file.write("\n")


if __name__ == '__main__':
    settings.init()
    tasks.setup()
    clearFile()

    config = SafeConfigParser()
    config.read('config.ini')

    gui.selectFlightData()

    if(len(settings.allFlightDirs) == 0 or settings.allFlightDirs[0] == ""):
        root = tkinter.Tk()
        root.withdraw()
        writeToFile("exit")
        tkinter.messagebox.showerror("Error", "No flight data selected. Exiting program.")
        sys.exit(1)

    saveDir = gui.askDir("Select Save Directory")

    pathNames = tasks.getFilePairsFromDirs(settings.allFlightDirs)
    taskOneFIDs = tasks.runTaskOne(pathNames, config, execute=writeToFile, saveDir=saveDir)
    savedRasterPath = tasks.runTaskTwo(taskOneFIDs, config, execute=writeToFile, saveDir=saveDir)

    writeToFile(saveDir, "coloredMosaicPaths.txt")
