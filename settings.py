# Created by Fletcher Easton

def init():
    global allFlightDirs
    allFlightDirs = set()
    
    global typeChecker
    typeChecker = {
        "ENVI_GLT_DOIT": "function",
        "ENVI_GEOREF_FROM_GLT_DOIT": "function",
        "EXPORT": "function",
        "MATH_DOIT": "function",
        "BuildMosaicRaster": "task",
        "ColorSliceClassification": "task"
    }
    
    global excludeParameter
    excludeParameter = [
        ("EXPORT", "FORMAT")
    ]
    
    global multipleValues
    multipleValues = [
        ("BuildMosaicRaster", "FEATHERING_DISTANCE")
    ]