# Created by Fletcher Easton
# Only tested on Mac, not Windows.
from tasks import *

pathNames = getFilePairs("Test_Good")

taskOneFIDs = []
count = 0
for hsi, igm in pathNames:
    idlCommands, uniqueFID = getTaskOneInstructions(hsi, igm, "tasks.1", count)
    taskOneFIDs.append(uniqueFID)
    for command in idlCommands:
        print(command)
    print()
    count += 1

print()

taskTwoFIDs = []
count = 0
for fid in taskOneFIDs:
    idlCommands, uniqueFID = getTaskTwoInstructions(fid, "tasks.2", count)
    taskTwoFIDs.append(uniqueFID)
    for command in idlCommands:
        print(command)
    print()
    count += 1
