# Created by Fletcher Easton
import tasks

#  Doesn't print the string. Used to skip output for tasks in testing.
def dontPrint(string):
    pass

tasks.setup()

pathNames = tasks.getFilePairs(r"Test_Good")
taskOneFIDs = tasks.runTaskOne(pathNames, taskOneFilename="tasks.1", execute=print)
taskTwoFIDs = tasks.runTaskTwo(taskOneFIDs, taskTwoFilename="tasks.2", execute=print)
taskThreeRaster = tasks.runTaskThree(taskTwoFIDs, 0, taskThreeFilename="tasks.3", execute=print)
