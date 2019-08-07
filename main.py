# Created by Fletcher Easton
# Only tested on Mac, not Windows.
from tasks import *

pathNames = getFilePairs("Test_Good")
allFIDS = []
count = 0
for pair in pathNames:
    idlCommands, uniqueFID = getTaskOneInstructions(pair[0], pair[1], "tasks.1", count)
    allFIDS.append(uniqueFID)
    for t in idlCommands:
        print(t)
    count += 1
    print()

for fid in allFIDS:
    print(fid)
print()

pathNames = getFilePairs("Test_Bad")