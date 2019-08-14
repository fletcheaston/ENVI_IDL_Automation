# Created by Fletcher Easton
import tasks

tasks.setup()

pathNames = tasks.getFilePairs(r"Test_Good")

taskOneFIDs = []
count = 0
for hsi, igm in pathNames:
    idlCommands, uniqueFID = tasks.getTaskOneInstructions(hsi, igm, "tasks.1", count)
    taskOneFIDs.append(uniqueFID)
    for command in idlCommands:
        print(command)
    print()
    count += 1

print()

taskTwoFIDs = []
count = 0
for fid in taskOneFIDs:
    idlCommands, uniqueFID = tasks.getTaskTwoInstructions(fid, "tasks.2", count)
    taskTwoFIDs.append(uniqueFID)
    for command in idlCommands:
        print(command)
    print()
    count += 1

idlCommands, mosaicRaster = tasks.getTaskThreeInstructions(taskTwoFIDs, "tasks.3", 0)
for command in idlCommands:
    print(command)
