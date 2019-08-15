# Created by Fletcher Easton
import tasks

#  Doesn't print the string. Used to skip output for tasks in testing.
def dontPrint(string):
    pass

tasks.setup()

pathNames = tasks.getFilePairs(r"Test_Good")
taskOneFIDs = tasks.runTaskOne(pathNames, taskOneFilename="tasks.1", execute=dontPrint)
expressionsAndBands = tasks.getAllExpressions(r"Expressions")
for exp, bnds in expressionsAndBands:
    taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, exp, bnds, taskTwoFilename="tasks.2", execute=dontPrint)
    taskThreeRaster = tasks.runTaskThree(taskTwoFIDs, 0, taskThreeFilename="tasks.3", execute=dontPrint)
    tasks.runTaskFour(taskThreeRaster, taskFourFilename="tasks.4", execute=print)