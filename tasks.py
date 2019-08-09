import os
import sys

# Takes a string specifying what directory to seach.
# Returns a list of tuples, each tuples containing strings of absoulte filesystem paths.
# The path to a .hsi file is the first element in each tuple.
# The path to an _igm file is the second element in each tuple.
def getFilePairs(directory):
    allPathPairs = []
    pairErrors = 0

    # Recursively walks through all the sub-directories in the specified directory.
    for dirpath, _, allFiles in os.walk(directory):

        # Each .hsi file requires a corresponding _igm file.
        # These files don't have the same name, so we instead search for what the files end with.
        # We're checking for at least one of each type in the current directory.
        if(any(file.endswith(".hsi") for file in allFiles) and any(file.endswith("_igm") for file in allFiles)):

            # We're now obtaining all of the .hsi and _igm files in the current directory.
            # There may be more than one of each, which is a problem.
            hsiFiles = [file for file in allFiles if file.endswith(".hsi")]
            igmFiles = [file for file in allFiles if file.endswith("_igm")]

            # Which is why we check to make sure exactly one of each is in the current directory.
            # There can't be zero of either, as we wouldn't have gotten to this line in the program.
            # However, there may be more than one of each. We print an error message and (eventually) end the program if this occurs.
            # If an error occurs, add to the error counter, and display this upon sys.exit().
            if(len(hsiFiles) != 1 or len(igmFiles) != 1):
                if(len(hsiFiles) != 1):
                    print("Error: {!r} .hsi files found in {!r}, 1 required.".format(len(hsiFiles), os.path.abspath(dirpath)))
                    pairErrors += 1
                if(len(igmFiles) != 1):
                    print("Error: {!r} _igm files found in {!r}, 1 required.".format(len(igmFiles), os.path.abspath(dirpath)))
                    pairErrors += 1
            else:
                # Throw the absolute paths into a tuple and append it to the list.
                pathPair = (os.path.join(os.path.abspath(dirpath), hsiFiles[0]), os.path.join(os.path.abspath(dirpath), igmFiles[0]))
                allPathPairs.append(pathPair)

    if(pairErrors > 0):
        # Notably, this can now detect extra .hsi or _igm files across multiple directories, and will alert the operator to all of them.
        print("{!r} file pairing errors found. Exiting program.".format(pairErrors))
        sys.exit(1)

    if(len(allPathPairs) == 0):
        print("Error: No .hsi/_igm pair files found. Exiting program.")
        sys.exit(1)
    
    # Why end the program? In case there was a mistake when moving files around, we don't want to run the full program only to find out we're missing data later.
    # Better to end the program here and let the operator know what the issue is.
    # But assuming we have no problems finding the file pairs, we return the list of tuples containing the relevent absoulte paths.
    return(allPathPairs)


# Reads all lines from a file into a single string, which is then returned.
def getTaskFileLines(taskFilename):
    with open(taskFilename, "r") as taskFile:
        taskFileLines = taskFile.readlines()

    allLines = ""
    for line in taskFileLines:
        if(not line.startswith("#") and line):
            allLines += line
    
    return(allLines)


# Takes three strings, an int, and an optional string.
# The first string is the absolute filesystem path to the relevant .hsi file.
# The second string is the absolute filesystem path to the relevant _igm file.
# The third string is the relative filesystem path to the tasks.1 file, which provides the base instructions for IDL.
# The int is the counter, to give each of the final variables in IDL unique names.
# The optional string is a path of the temporary directory where we want to store intermediate files.
# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the refGltFID_count.
def getTaskOneInstructions(hsiFilename, igmFilename, taskOneFilename, count, tempDir="Z:\\temp"):
    hsiFile = "'{0}'".format(hsiFilename)
    igmFile = "'{0}'".format(igmFilename)
    refGltFile = "'{0}'".format(os.path.join(tempDir, "refGltFile_{0}".format(count)))
    refGltFID = "refGltFID_{0}".format(count)

    allInstructions = getTaskFileLines(taskOneFilename).format(hsiFile=hsiFile,
        igmFile=igmFile,
        refGltFile=refGltFile,
        refGltFID=refGltFID).split("\n")
    
    return((allInstructions, refGltFID))


# Returns a string read from the bandMathExpression file.
def getBandMathExpression():
    with open("bandMathExpression", "r") as file:
        expression = file.readline().strip()
    return(expression)


# Returns a list of numbers read from the bandMathNumbers file.
def getBandMathNumbers():
    with open("bandMathNumbers", "r") as file:
        numbers = file.readline().split(',')

    # We subtract 1 because ENVI counts Bands starting at 1, but IDL counts Bands starting at 0.
    # We're converting from ENVI to IDL, so we subtract 1.
    return([int(x) - 1 for x in numbers])


# Takes two strings, an int, and an optional string.
# The first string is the variable name of a unique FID from task one.
# The second string is the relative filesystem path to the tasks.2 file, which provides the base instructions for IDL.
# The int is the counter, to give each of the final variables in IDL unique names.
# The optional string is a path of the temporary directory where we want to store intermediate files.
# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the refGltFID_count.
def getTaskTwoInstructions(FID, taskTwoFilename, count, tempDir="Z:\\temp"):
    geoRefFID = FID        
    bandMathExpression = "'{0}'".format(getBandMathExpression())
    bandMathNumbers = getBandMathNumbers()
    geoRefFIDArray = "{0}, ".format(FID) * (len(bandMathNumbers) - 1) + FID
    bandedOutFile = "'{0}'".format(os.path.join(tempDir, "bandedOutFile_{0}".format(count)))
    bandedFID = "bandedFID_{0}".format(count)

    allInstructions = getTaskFileLines(taskTwoFilename).format(geoRefFID=geoRefFID,
        bandMathExpression=bandMathExpression,
        bandMathNumbers=bandMathNumbers,
        geoRefFIDArray=geoRefFIDArray,
        bandedOutFile=bandedOutFile,
        bandedFID=bandedFID).split("\n")
    
    return((allInstructions, bandedFID))