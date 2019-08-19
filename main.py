# Created by Fletcher Easton
import tasks


# Doesn't print the string. Used to skip output for tasks in testing.
def dontPrint(string):
    pass


def clearFile(filename=r"Z:\temp\idlCommands.pro"):
    with open(filename, "w+") as file:
        pass


# Writes the string to a file.
def writeToFile(string, filename=r"Z:\temp\idlCommands.pro"):
    with open(filename, "a+") as file:
        file.write(string.strip())
        file.write("\n")


tasks.setup()
clearFile()
pathNames = tasks.getFilePairs(r"Test_Good")
taskOneFIDs = tasks.runTaskOne(pathNames, taskOneFilename="tasks.1", execute=writeToFile)
expressionsAndBands = tasks.getAllExpressions(r"Expressions")
for exp, bnds in expressionsAndBands:
    taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, exp, bnds, taskTwoFilename="tasks.2", execute=writeToFile)
    taskThreeRaster = tasks.runTaskThree(taskTwoFIDs, 0, taskThreeFilename="tasks.3", execute=writeToFile)
    tasks.runTaskFour(taskThreeRaster, taskFourFilename="tasks.4", execute=writeToFile)