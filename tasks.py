# Created by Fletcher Easton
import os
import sys
import logging
from datetime import datetime
import settings

def setup():
    logging.basicConfig(filename=r"automatedENVI.log", filemode="a+", format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)


def datetimeString():
    return(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))


# Takes a string specifying what directory to seach.
# Returns a list of tuples, each tuples containing strings of absoulte filesystem paths.
# The path to a .hsi file is the first element in each tuple.
# The path to an _igm file is the second element in each tuple.
def getFilePairsFromDirs(dirs):
    allPathPairs = set()
    filePairErrors = 0

    for directory in dirs:
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
                    allPathPairs.add(pathPair)

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


# Returns the stringified option for functions if the option is considered valid.
def functionOption(config, section, option, arrayLen=None):
    if((section, option.upper()) in settings.excludeParameter):
        return("{0}".format(config.get(section, option)))

    if((section, option.upper()) in settings.multipleValues):
        return("{0}={1}".format(option.upper(), [int(config.get(section, option)) for _ in range(arrayLen)]))
        return("{0}={1}".format(option.upper(), [config.get(section, option) for _ in range(arrayLen)]))

    try:
        if(config.getfloat(section, option).is_integer()):
            return("{0}={1}".format(option.upper(), config.getint(section, option)))
        else:
            return("{0}={1}".format(option.upper(), config.getfloat(section, option)))
    except:
        try:
            if(config.getboolean(section, option)):
                return(option.upper())
        except:
            return("{0}={1}".format(option.upper(), config.get(section, option)))


# Returns the stringified option for tasks if the option is considered valid.
def taskOption(taskName, config, section, option, arrayLen=None):
    if((section, option.upper()) in settings.excludeParameter):
        return("{0}".format(config.get(section, option)))

    if((section, option.upper()) in settings.multipleValues):
        try:
            return("{0}.{1}={2}".format(taskName, option.upper(), [int(config.get(section, option)) for _ in range(arrayLen)]))
        except:
            return("{0}.{1}={2}".format(taskName, option.upper(), [config.get(section, option) for _ in range(arrayLen)]))

    try:
        if(config.getfloat(section, option).is_integer()):
            return("{0}.{1}={2}".format(taskName, option.upper(), config.getint(section, option)))
        else:
            return("{0}.{1}={2}".format(taskName, option.upper(), config.getfloat(section, option)))
    except:
        try:
            if(config.getboolean(section, option)):
                return("{0}.{1}".format(taskName, option.upper()))
        except:
            return("{0}.{1}={2}".format(taskName, option.upper(), config.get(section, option)))


# Reads the config file for the parameters of the specified section.
# Returns a string formatted for the parameters of that section.
def getConfigParameters(config, section, taskName=None, arrayLen=None):
    parameters = ""

    if(settings.typeChecker[section] == "function"):
        allValidOptions = [functionOption(config, section, option) for option in config.options(section) if(functionOption(config, section, option))]
        parameters = ", ".join(allValidOptions)

    elif(settings.typeChecker[section] == "task"):
        allValidOptions = [taskOption(taskName, config, section, option, arrayLen=arrayLen) for option in config.options(section) if(taskOption(taskName, config, section, option, arrayLen=arrayLen))]
        parameters = "\n".join(allValidOptions)

    return(parameters)


# Returns a list of strings, corresponding to FID variable names.
def runTaskOne(pathNames, config, execute=print, taskOneFilename="georeference.task", saveDir="temp"):
    taskOneFIDs = []
    count = 0
    
    # Start of the .pro file, activates ENVI through IDL.
    execute("E = ENVI()")

    for hsi, igm in pathNames:
        idlCommands, uniqueFID = getTaskOneInstructions(hsi, igm, config, count, taskOneFilename=taskOneFilename, saveDir=saveDir)
        taskOneFIDs.append(uniqueFID)
        for command in idlCommands:
            execute(command)
        count += 1

    return(taskOneFIDs)


# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the refGltFID_count.
def getTaskOneInstructions(hsiFilename, igmFilename, config, count, taskOneFilename="georeference.task", saveDir="temp"):
    hsiFile = "'{0}'".format(hsiFilename)
    igmFile = "'{0}'".format(igmFilename)
    refGltFile = "'{0}'".format(os.path.join(saveDir, "refGltFile_{0}".format(count)))
    refGltFID = "refGltFID_{0}".format(count)
    savePath = "'{0}'".format(os.path.join(saveDir, "georeferencedFile_{0}_{1}".format(count, datetimeString())))

    ENVI_GLT_DOIT_Parameters = getConfigParameters(config, "ENVI_GLT_DOIT")
    ENVI_GEOREF_FROM_GLT_DOIT_Parameters = getConfigParameters(config, "ENVI_GEOREF_FROM_GLT_DOIT")
    EXPORT_Parameters = getConfigParameters(config, "EXPORT")

    allInstructions = getTaskFileLines(taskOneFilename).format(hsiFile=hsiFile,
        igmFile=igmFile,
        refGltFile=refGltFile,
        refGltFID=refGltFID,
        savePath=savePath,
        ENVI_GLT_DOIT_Parameters=ENVI_GLT_DOIT_Parameters,
        ENVI_GEOREF_FROM_GLT_DOIT_Parameters=ENVI_GEOREF_FROM_GLT_DOIT_Parameters,
        EXPORT_Parameters=EXPORT_Parameters).split("\n")
    
    return((allInstructions, refGltFID))


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


# Returns a list of strings, corresponding to FID variable names.
def runTaskTwo(taskOneFIDs, config, taskTwoFilename="bandmath.task", execute=print, saveDir="temp"):
    taskTwoFIDs = []
    fidCount = 0
    for fid in taskOneFIDs:
        idlCommands, uniqueFID = getTaskTwoInstructions(fid, config, fidCount, taskTwoFilename=taskTwoFilename, saveDir=saveDir)
        taskTwoFIDs.append(uniqueFID)
        for command in idlCommands:
            execute(command)
        fidCount += 1
    return(taskTwoFIDs)


# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the refGltFID_count.
def getTaskTwoInstructions(FID, config, fidCount, taskTwoFilename="bandmath.task", saveDir="temp"):
    geoRefFID = FID        
    bandMathNumbers = ", ".join(parseBandsFromExpression(config.get("MATH_DOIT", "EXP")))
    geoRefFIDArrayList = [FID for _ in range(len(parseBandsFromExpression(config.get("MATH_DOIT", "EXP"))))]
    geoRefFIDArray = ", ".join(geoRefFIDArrayList)
    bandedOutFile = "'{0}'".format(os.path.join(saveDir, "bandedMathFile_{0}".format(fidCount)))
    bandedFID = "bandedFID_{0}".format(fidCount)
    savePath = "'{0}'".format(os.path.join(saveDir, "bandedMathFile_{0}_{1}".format(fidCount, datetimeString())))

    MATH_DOIT_Parameters = getConfigParameters(config, "MATH_DOIT")
    EXPORT_Parameters = getConfigParameters(config, "EXPORT")

    allInstructions = getTaskFileLines(taskTwoFilename).format(geoRefFID=geoRefFID,
        bandMathNumbers=bandMathNumbers,
        geoRefFIDArray=geoRefFIDArray,
        bandedOutFile=bandedOutFile,
        bandedFID=bandedFID,
        savePath=savePath,
        MATH_DOIT_Parameters=MATH_DOIT_Parameters,
        EXPORT_Parameters=EXPORT_Parameters).split("\n")
    
    return((allInstructions, bandedFID))


def runTaskThree(taskTwoFIDs, config, taskThreeFilename="mosaic.task", execute=print, saveDir="temp"):
    idlCommands, savedRasterPath = getTaskThreeInstructions(taskTwoFIDs, config, taskThreeFilename=taskThreeFilename,  saveDir=saveDir)
    for command in idlCommands:
        execute(command)

    # End of line argument for the .pro file, allows the program to be compiled and run easily.
    execute("END")
    
    return(savedRasterPath)


# Returns a tuple, containing...
# A list of strings, corresponding to the relevant IDL instructions.
# A string, corresponding to the path of the final file.
def getTaskThreeInstructions(FIDs, config, taskThreeFilename="mosaic.task", saveDir="temp"):
    inputRasters = ", ".join(["ENVIFIDToRaster({0})".format(fid) for fid in FIDs])
    colorMatchingActionsList = ["'Adjust'" for _ in FIDs]
    colorMatchingActionsList[-1] = "'Reference'"
    colorMatchingActions = ", ".join(colorMatchingActionsList)
    mosaicSavePath = "'{0}'".format(os.path.join(saveDir, "dataMosaicFile_{0}".format(datetimeString())))
    coloredMosaicSavePath = "'{0}'".format(os.path.join(saveDir, "coloredMosaicFile_{0}".format(datetimeString())))
    
    BuildMosaicRaster_Parameters = getConfigParameters(config, "BuildMosaicRaster", taskName="MosaicTask", arrayLen=len(FIDs))
    RecolorTask_Parameters = getConfigParameters(config, "ColorSliceClassification", taskName="RecolorTask", arrayLen=len(FIDs))
    EXPORT_Parameters = getConfigParameters(config, "EXPORT")

    allInstructions = getTaskFileLines(taskThreeFilename).format(inputRasters=inputRasters,
        colorMatchingActions=colorMatchingActions,
        mosaicSavePath=mosaicSavePath,
        coloredMosaicSavePath=coloredMosaicSavePath,
        BuildMosaicRaster_Parameters=BuildMosaicRaster_Parameters,
        RecolorTask_Parameters=RecolorTask_Parameters,
        EXPORT_Parameters=EXPORT_Parameters).split("\n")

    return((allInstructions, mosaicSavePath.strip("'")))
