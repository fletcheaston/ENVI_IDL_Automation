# Created by Fletcher Easton
import tasks


# Doesn't print the string. Used to skip output for tasks in testing.
def dontPrint(string):
    pass


def clearFile(filename=r"Z:\\temp\\idlCommands.pro"):
    with open(filename, "w+") as file:
        pass


# Writes the string to a file.
def writeToFile(string, filename=r"Z:\\temp\\idlCommands.pro"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


flightDataDir = r"Test_Good"
expressionDir = r"Expressions"

tasks.setup()
clearFile()
pathNames = tasks.getFilePairs(flightDataDir)
taskOneFIDs = tasks.runTaskOne(pathNames, taskOneFilename="tasks.1", execute=writeToFile)
expressionsAndBands = tasks.getAllExpressions(expressionDir)
count = 0
for exp, bnds in expressionsAndBands:
    taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, exp, bnds, taskTwoFilename="tasks.2", execute=writeToFile)
    taskThreeRaster = tasks.runTaskThree(taskTwoFIDs, count, taskThreeFilename="tasks.3", execute=writeToFile)
    tasks.runTaskFour(taskThreeRaster, taskFourFilename="tasks.4", execute=print)
    count += 1
