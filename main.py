# Created by Fletcher Easton
import tasks
import tkinter
import tkfilebrowser
import sys
import logging
from configparser import SafeConfigParser
import io


def clearFile(filename=r"idlCommands.pro"):
    with open(filename, "w+") as file:
        pass


def writeToFile(string, filename=r"idlCommands.pro"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


def askDir(title):
    root = tkinter.Tk()
    directory = tkfilebrowser.askopendirname(title=title, foldercreation=True)
    root.withdraw()
    if(directory == ""):
        tkinter.messagebox.showerror("Error", "No directory selected for saving data. Exiting program.")
        sys.exit(1)
    return(directory)


def askDirs(title):
    root = tkinter.Tk()
    dirs = tkfilebrowser.askopendirnames(title=title, foldercreation=False)
    root.withdraw()
    return(dirs)


def dirsSelectedString(dirs):
    return("\n".join(dirs))
 

tasks.setup()
clearFile()

config = SafeConfigParser()
config.read('config.ini')

flightDirs = []

while(True):
    flightDirs += askDirs("Select Flight Data Directory")
    flightDirs = list(set(flightDirs))

    answer = tkinter.messagebox.askyesno("", "All data selected?\n\nDirectories selected:\n{0}".format(dirsSelectedString(flightDirs)))
    if(answer):
        break

if(len(flightDirs) == 0):
    tkinter.messagebox.showerror("Error", "No flight data selected. Exiting program.")
    sys.exit(1)

saveDir = askDir("Select Save Directory")

pathNames = tasks.getFilePairsFromDirs(flightDirs)
taskOneFIDs = tasks.runTaskOne(pathNames, config, execute=writeToFile, saveDir=saveDir)
taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, config, execute=writeToFile, saveDir=saveDir)
tasks.runTaskThree(taskTwoFIDs, config, execute=writeToFile, saveDir=saveDir)
