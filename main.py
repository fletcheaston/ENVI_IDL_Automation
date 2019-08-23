# Created by Fletcher Easton
import tasks
import tkinter
import tkfilebrowser
import sys
import logging

# Doesn't print the string. Used to skip output for tasks in testing.
def dontPrint(string):
    pass


def clearFile(filename=r"Z:\\idlCommands.pro"):
    with open(filename, "w+") as file:
        pass


# Writes the string to a file.
def writeToFile(string, filename=r"Z:\\idlCommands.pro"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


def askDir(title):
    root = tkinter.Tk()
    directory = tkfilebrowser.askopendirname(title=title, foldercreation=True)
    root.withdraw()
    return(directory)


def askDirs(title):
    root = tkinter.Tk()
    dirs = tkfilebrowser.askopendirnames(title=title)
    root.withdraw()
    if(not dirs):
        logging.error("No directories selected for flight data. Exiting program.")
        sys.exit(1)
    return(dirs)


def askFiles(title, filetypes):
    root = tkinter.Tk()
    files = tkfilebrowser.askopenfilenames(title=title, filetypes=filetypes)
    root.withdraw()
    if(not files):
        logging.error("No files selected for expressions. Exiting program.")
        sys.exit(1)
    return(files)
 

tasks.setup()
clearFile()

flightDirs = askDirs("Select Flight Directories")
expressionFiletypes = [("Expressions", "*.exp")]
expressionFiles = askFiles("Select Expression Files", expressionFiletypes)
saveDir = askDir("Select Save Directory")

pathNames = tasks.getFilePairsFromDirs(flightDirs)
taskOneFIDs = tasks.runTaskOne(pathNames, taskOneFilename="tasks.1", execute=writeToFile, saveDir=saveDir)
expressionsAndBands = tasks.getExpressionsFromMultiFiles(expressionFiles)
count = 0
for exp, bnds in expressionsAndBands:
    taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, exp, bnds, count, taskTwoFilename="tasks.2", execute=writeToFile, saveDir=saveDir)
    taskThreeRaster = tasks.runTaskThree(taskTwoFIDs, count, taskThreeFilename="tasks.3", execute=writeToFile, saveDir=saveDir)
    tasks.runTaskFour(taskThreeRaster, count, taskFourFilename="tasks.4", execute=writeToFile, saveDir=saveDir)
    count += 1

# End of line argument for the .pro file, allows the file to be compiled and run easily.
writeToFile("END")