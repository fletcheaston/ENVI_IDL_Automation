# Created by Fletcher Easton
import os
import sys
import logging

def setup():
    logging.basicConfig(filename=r"Z:\temp\automatedENVI.log", filemode="a+", format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

# Takes a string specifying what directory to seach.
# Returns a list of tuples, each tuples containing strings of absoulte filesystem paths.
# The path to a .hsi file is the first element in each tuple.
# The path to an _igm file is the second element in each tuple.
def getFilePairs(directory):
    allPathPairs = []
    filePairErrors = 0

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
                    logging.warning("{0} .hsi files found in {1}, 1 required.".format(len(hsiFiles), os.path.abspath(dirpath)))
                    filePairErrors += 1
                if(len(igmFiles) != 1):
                    logging.warning("{0} _igm files found in {1}, 1 required.".format(len(igmFiles), os.path.abspath(dirpath)))
                    filePairErrors += 1
            else:
                # Throw the absolute paths into a tuple and append it to the list.
                logging.info("{0},{1}: File pair found in {2}.".format(hsiFiles[0], igmFiles[0], os.path.abspath(dirpath)))
                pathPair = (os.path.join(os.path.abspath(dirpath), hsiFiles[0]), os.path.join(os.path.abspath(dirpath), igmFiles[0]))
                allPathPairs.append(pathPair)

    if(filePairErrors > 0):
        # Notably, this can now detect extra .hsi or _igm files across multiple directories, and will alert the operator to all of them.
        logging.error("{0} file pairing errors found.".format(filePairErrors))

    if(len(allPathPairs) == 0):
        logging.error("No .hsi/_igm pair files found. Exiting program.")
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


# Takes a list of tuples, two optional strings, and an optional function.
# The list of tuples contains strings of the .hsi/_igm file paris.
# The first optional string is the relative filesystem path to the tasks.1 file, which provides the base instructions for IDL.
# The second optional string is a path of the temporary directory where we want to store intermediate files.
# The optional function will be called on all the IDL commands.
# Returns a list of strings, corresponding to FID variable names.
def runTaskOne(pathNames, taskOneFilename="tasks.1", tempDir="Z:\\temp", execute=print):
    taskOneFIDs = []
    count = 0
    for hsi, igm in pathNames:
        idlCommands, uniqueFID = getTaskOneInstructions(hsi, igm, taskOneFilename, count, tempDir=tempDir)
        taskOneFIDs.append(uniqueFID)
        for command in idlCommands:
            execute(command)
        count += 1
    
    return(taskOneFIDs)


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


def getAllExpressions(directory):
    # Recursively walks through all the sub-directories in the specified directory.
    for dirpath, _, allFiles in os.walk(directory):

        # We're only looking for .exp files.
        if(any(file.endswith(".exp") for file in allFiles)):

            # We're now obtaining all of the .exp files in the current directory.
            expFiles = [file for file in allFiles if file.endswith(".exp")]
            expressions = [getBandMathExpression(os.path.join(os.path.abspath(directory), filename)) for filename in expFiles]
        else:
            logging.error("No .exp files found in {0}. Exiting program.".format(directory))
            sys.exit(1)

    return([(exp, parseBandsFromExpression(exp)) for exp in expressions])


# Takes a string representing an expression.
# All bands must be written as b#, where the # is any number 1 - 150.
# Returns a sorted list of strings, each string the band number specified in the expression.
def parseBandsFromExpression(string):
    bands = set()
    band = ""
    foundBand = False

    for char in string:
        if(foundBand):
            if(char.isdigit()):
                band += char
            else:
                bands.add(int(band) - 1)
                band = ""
                foundBand = False
        if(char.lower() == "b"):
            foundBand = True

    bands = list(bands)
    bands.sort()
    return([str(x) for x in bands])


# Returns a string read from the bandMathExpression file.
def getBandMathExpression(filename):
    with open(filename, "r") as file:
        header = file.readline()
        expression = file.readline().strip()
    return(expression)


# Takes a list of strings, a string, a list of strings, two optional strings, and an optional function.
# The first list of strings corresponds to the FID variable names.
# The first string is the expression we're running band math on.
# The second list of strings is the bands we're running band math on.
# The first optional string is the relative filesystem path to the tasks.2 file, which provides the base instructions for IDL.
# The second optional string is a path of the temporary directory where we want to store intermediate files.
# The optional function will be called on all the IDL commands.
def runTaskTwo(taskOneFIDs, expression, bandNumbers, taskTwoFilename="tasks.2", tempDir="Z:\\temp", execute=print):
    taskTwoFIDs = []
    count = 0
    for fid in taskOneFIDs:
        idlCommands, uniqueFID = getTaskTwoInstructions(fid, expression, bandNumbers, "tasks.2", count)
        taskTwoFIDs.append(uniqueFID)
        for command in idlCommands:
            execute(command)
        count += 1
    return(taskTwoFIDs)


# Takes two strings, a list of strings, a string, an int, and an optional string.
# The first string is the variable name of a unique FID from task one.
# The second string is the expression we're running band math on.
# The list of strings is the bands we're running band math on.
# The third string is the relative filesystem path to the tasks.2 file, which provides the base instructions for IDL.
# The int is the counter, to give each of the final variables in IDL unique names.
# The optional string is a path of the temporary directory where we want to store intermediate files.
# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the refGltFID_count.
def getTaskTwoInstructions(FID, expression, bandNumbers, taskTwoFilename, count, tempDir="Z:\\temp"):
    geoRefFID = FID        
    bandMathExpression = "'{0}'".format(expression)
    bandMathNumbers = ", ".join(bandNumbers)
    geoRefFIDArrayList = [FID for _ in range(len(bandNumbers))]
    geoRefFIDArray = ", ".join(geoRefFIDArrayList)
    bandedOutFile = "'{0}'".format(os.path.join(tempDir, "bandedOutFile_{0}".format(count)))
    bandedFID = "bandedFID_{0}".format(count)

    allInstructions = getTaskFileLines(taskTwoFilename).format(geoRefFID=geoRefFID,
        bandMathExpression=bandMathExpression,
        bandMathNumbers=bandMathNumbers,
        geoRefFIDArray=geoRefFIDArray,
        bandedOutFile=bandedOutFile,
        bandedFID=bandedFID).split("\n")
    
    return((allInstructions, bandedFID))


# Takes a list of strings, an int, two optional strings, and an optional function.
# The list of strings corresponds to the FID variable names.
# The int is the counter, to give each of the final variables in IDL unique names.
# The first optional string is the relative filesystem path to the tasks.3 file, which provides the base instructions for IDL.
# The second optional string is a path of the temporary directory where we want to store intermediate files.
# The optional function will be called on all the IDL commands.
def runTaskThree(taskTwoFIDs, count, taskThreeFilename="tasks.3", tempDir="Z:\\temp", execute=print):
    idlCommands, mosaicRaster = getTaskThreeInstructions(taskTwoFIDs, taskThreeFilename, count)
    for command in idlCommands:
        execute(command)
    return(mosaicRaster)


# Takes a list of strings, a string, an int, and an optional string.
# The list of strings contains the FID variable names for all of the band-math files.
# The string is the relative filesystem path to the tasks.3 file, which provides the base instructions for IDL.
# The int is the counter, to give each of the final variables in IDL unique names.
# The optional string is a path of the temporary directory where we want to store intermediate files.
# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the mosaic raster variable name.
def getTaskThreeInstructions(FIDs, taskThreeFilename, count, tempDir="Z:\\temp"):
    inputRasters = ", ".join(["ENVIFIDToRaster({0})".format(fid) for fid in FIDs])
    colorMatchingActionsList = ["'Adjust'" for _ in FIDs]
    colorMatchingActionsList[-1] = "'Reference'"
    colorMatchingActions = ", ".join(colorMatchingActionsList)
    featheringDistance = ", ".join(["0" for _ in FIDs])
    mosaicRaster = "mosaicRaster_{0}".format(count)

    allInstructions = getTaskFileLines(taskThreeFilename).format(inputRasters=inputRasters,
        colorMatchingActions=colorMatchingActions,
        featheringDistance=featheringDistance,
        mosaicRaster=mosaicRaster).split("\n")
    
    return((allInstructions, mosaicRaster))


# Takes a list of strings, an int, two optional strings, and an optional function.
# The list of strings corresponds to the FID variable names.
# The first optional string is the relative filesystem path to the tasks.4 file, which provides the base instructions for IDL.
# The second optional string is a path of the temporary directory where we want to store intermediate files.
# The optional function will be called on all the IDL commands.
def runTaskFour(inputRaster, taskFourFilename="tasks.4", execute=print):
    idlCommands = getTaskFourInstructions(inputRaster, taskFourFilename)
    for command in idlCommands:
        execute(command)


# Takes two strings.
# The first string is the name of the mosaicRaster variable.
# The string is the relative filesystem path to the tasks.4 file, which provides the base instructions for IDL.
# Returns a list of strings, corresponding to the relevant IDL instructions.
def getTaskFourInstructions(inputRaster, taskFourFilename):
    allInstructions = getTaskFileLines(taskFourFilename).format(inputRaster=inputRaster).split("\n")
    return(allInstructions)