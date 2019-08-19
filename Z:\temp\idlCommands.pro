
dataRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test0/test0.hsi')
locationRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test0/test0_igm')

dataFID = ENVIRastertoFID(dataRaster)
locationFID = ENVIRastertoFID(locationRaster)

inputProjection = ENVI_PROJ_CREATE(/geographic)

ENVI_FILE_QUERY, locationFID, DIMS=locationDims

ENVI_DOIT, 'ENVI_GLT_DOIT', DIMS=locationDims, I_PROJ=inputProjection, O_PROJ=inputProjection, R_FID=gltFID, OUT_NAME=tempGltFile, ROTATION=20, X_FID=locationFID, Y_FID=locationFID, X_POS=1, Y_POS=0

ENVI_FILE_QUERY, gltFID, DIMS=gltDims

ENVI_DOIT, 'ENVI_GEOREF_FROM_GLT_DOIT', BACKGROUND=0, FID=dataFID, GLT_DIMS=gltDims, GLT_FID=gltFID, OUT_NAME='Z:\temp/refGltFile_0', POS=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149], R_FID=refGltFID_0

dataRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test1/test1.hsi')
locationRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test1/test1_igm')

dataFID = ENVIRastertoFID(dataRaster)
locationFID = ENVIRastertoFID(locationRaster)

inputProjection = ENVI_PROJ_CREATE(/geographic)

ENVI_FILE_QUERY, locationFID, DIMS=locationDims

ENVI_DOIT, 'ENVI_GLT_DOIT', DIMS=locationDims, I_PROJ=inputProjection, O_PROJ=inputProjection, R_FID=gltFID, OUT_NAME=tempGltFile, ROTATION=20, X_FID=locationFID, Y_FID=locationFID, X_POS=1, Y_POS=0

ENVI_FILE_QUERY, gltFID, DIMS=gltDims

ENVI_DOIT, 'ENVI_GEOREF_FROM_GLT_DOIT', BACKGROUND=0, FID=dataFID, GLT_DIMS=gltDims, GLT_FID=gltFID, OUT_NAME='Z:\temp/refGltFile_1', POS=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149], R_FID=refGltFID_1

dataRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test3/test3.hsi')
locationRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test3/test3_igm')

dataFID = ENVIRastertoFID(dataRaster)
locationFID = ENVIRastertoFID(locationRaster)

inputProjection = ENVI_PROJ_CREATE(/geographic)

ENVI_FILE_QUERY, locationFID, DIMS=locationDims

ENVI_DOIT, 'ENVI_GLT_DOIT', DIMS=locationDims, I_PROJ=inputProjection, O_PROJ=inputProjection, R_FID=gltFID, OUT_NAME=tempGltFile, ROTATION=20, X_FID=locationFID, Y_FID=locationFID, X_POS=1, Y_POS=0

ENVI_FILE_QUERY, gltFID, DIMS=gltDims

ENVI_DOIT, 'ENVI_GEOREF_FROM_GLT_DOIT', BACKGROUND=0, FID=dataFID, GLT_DIMS=gltDims, GLT_FID=gltFID, OUT_NAME='Z:\temp/refGltFile_2', POS=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149], R_FID=refGltFID_2

dataRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test2/test2.hsi')
locationRaster = E.OpenRaster('/Users/fletcheaston/Desktop/envi/Test_Good/test2/test2_igm')

dataFID = ENVIRastertoFID(dataRaster)
locationFID = ENVIRastertoFID(locationRaster)

inputProjection = ENVI_PROJ_CREATE(/geographic)

ENVI_FILE_QUERY, locationFID, DIMS=locationDims

ENVI_DOIT, 'ENVI_GLT_DOIT', DIMS=locationDims, I_PROJ=inputProjection, O_PROJ=inputProjection, R_FID=gltFID, OUT_NAME=tempGltFile, ROTATION=20, X_FID=locationFID, Y_FID=locationFID, X_POS=1, Y_POS=0

ENVI_FILE_QUERY, gltFID, DIMS=gltDims

ENVI_DOIT, 'ENVI_GEOREF_FROM_GLT_DOIT', BACKGROUND=0, FID=dataFID, GLT_DIMS=gltDims, GLT_FID=gltFID, OUT_NAME='Z:\temp/refGltFile_3', POS=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149], R_FID=refGltFID_3

ENVI_FILE_QUERY, refGltFID_0, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b100 + b33 * 400)', FID=[refGltFID_0, refGltFID_0], OUT_NAME='Z:\temp/bandedOutFile_0', POS=[32, 99], R_FID=bandedFID_0

ENVI_FILE_QUERY, refGltFID_1, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b100 + b33 * 400)', FID=[refGltFID_1, refGltFID_1], OUT_NAME='Z:\temp/bandedOutFile_1', POS=[32, 99], R_FID=bandedFID_1

ENVI_FILE_QUERY, refGltFID_2, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b100 + b33 * 400)', FID=[refGltFID_2, refGltFID_2], OUT_NAME='Z:\temp/bandedOutFile_2', POS=[32, 99], R_FID=bandedFID_2

ENVI_FILE_QUERY, refGltFID_3, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b100 + b33 * 400)', FID=[refGltFID_3, refGltFID_3], OUT_NAME='Z:\temp/bandedOutFile_3', POS=[32, 99], R_FID=bandedFID_3

Task = ENVITask('BuildMosaicRaster')

Task.INPUT_RASTERS = [ENVIFIDToRaster(bandedFID_0), ENVIFIDToRaster(bandedFID_1), ENVIFIDToRaster(bandedFID_2), ENVIFIDToRaster(bandedFID_3)]

Task.COLOR_MATCHING_ACTIONS = ['Adjust', 'Adjust', 'Adjust', 'Reference']

Task.COLOR_MATCHING_METHOD = 'None'

Task.BACKGROUND = 0

Task.FEATHERING_DISTANCE = [5, 5, 5, 5]

Task.FEATHERING_METHOD = 'Seamline'
Task.SEAMLINE_METHOD = 'Geometry'

Task.Execute

mosaicRaster_0 = Task.OUTPUT_RASTER

View = E.GetView()
Layer = View.CreateLayer(Task.OUTPUT_RASTER)

Task = ENVITask('ColorSliceClassification')
Task.INPUT_RASTER = mosaicRaster_0
Task.CLASS_COLORS = [[114, 251, 253], [134, 219, 252], [154, 186, 251], [174, 154, 250], [194, 121, 249], [214, 89, 248], [234, 56, 247]]
Task.CLASS_RANGES = [[-3,0], [0,6], [6,8], [8,10], [10,12], [12,14], [14,17]]
Task.Execute

Task.OUTPUT_RASTER.Export, E.GetTemporaryFilename(), 'TIFF'

ENVI_FILE_QUERY, refGltFID_0, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b70 gt b40)*(-1)+(b70 le b40)  *(14.6909920+0.5242874*(b29)-0.7918500*(b141)+0.33766089*(b147)-0.0219860*(b120*b42)+0.0234555*(b120*b46)+0.0219184*(b101*b66)-0.0301020*(b86*b70)+0.0068835*(b141*b86)-0.0028940*(b147*b107))', FID=[refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0, refGltFID_0], OUT_NAME='Z:\temp/bandedOutFile_0', POS=[28, 39, 41, 45, 65, 69, 85, 100, 106, 119, 140, 146], R_FID=bandedFID_0

ENVI_FILE_QUERY, refGltFID_1, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b70 gt b40)*(-1)+(b70 le b40)  *(14.6909920+0.5242874*(b29)-0.7918500*(b141)+0.33766089*(b147)-0.0219860*(b120*b42)+0.0234555*(b120*b46)+0.0219184*(b101*b66)-0.0301020*(b86*b70)+0.0068835*(b141*b86)-0.0028940*(b147*b107))', FID=[refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1, refGltFID_1], OUT_NAME='Z:\temp/bandedOutFile_1', POS=[28, 39, 41, 45, 65, 69, 85, 100, 106, 119, 140, 146], R_FID=bandedFID_1

ENVI_FILE_QUERY, refGltFID_2, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b70 gt b40)*(-1)+(b70 le b40)  *(14.6909920+0.5242874*(b29)-0.7918500*(b141)+0.33766089*(b147)-0.0219860*(b120*b42)+0.0234555*(b120*b46)+0.0219184*(b101*b66)-0.0301020*(b86*b70)+0.0068835*(b141*b86)-0.0028940*(b147*b107))', FID=[refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2, refGltFID_2], OUT_NAME='Z:\temp/bandedOutFile_2', POS=[28, 39, 41, 45, 65, 69, 85, 100, 106, 119, 140, 146], R_FID=bandedFID_2

ENVI_FILE_QUERY, refGltFID_3, dims=geoRefDims

ENVI_DOIT, 'MATH_DOIT', DIMS=geoRefDims, EXP='(b70 gt b40)*(-1)+(b70 le b40)  *(14.6909920+0.5242874*(b29)-0.7918500*(b141)+0.33766089*(b147)-0.0219860*(b120*b42)+0.0234555*(b120*b46)+0.0219184*(b101*b66)-0.0301020*(b86*b70)+0.0068835*(b141*b86)-0.0028940*(b147*b107))', FID=[refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3, refGltFID_3], OUT_NAME='Z:\temp/bandedOutFile_3', POS=[28, 39, 41, 45, 65, 69, 85, 100, 106, 119, 140, 146], R_FID=bandedFID_3

Task = ENVITask('BuildMosaicRaster')

Task.INPUT_RASTERS = [ENVIFIDToRaster(bandedFID_0), ENVIFIDToRaster(bandedFID_1), ENVIFIDToRaster(bandedFID_2), ENVIFIDToRaster(bandedFID_3)]

Task.COLOR_MATCHING_ACTIONS = ['Adjust', 'Adjust', 'Adjust', 'Reference']

Task.COLOR_MATCHING_METHOD = 'None'

Task.BACKGROUND = 0

Task.FEATHERING_DISTANCE = [5, 5, 5, 5]

Task.FEATHERING_METHOD = 'Seamline'
Task.SEAMLINE_METHOD = 'Geometry'

Task.Execute

mosaicRaster_0 = Task.OUTPUT_RASTER

View = E.GetView()
Layer = View.CreateLayer(Task.OUTPUT_RASTER)

Task = ENVITask('ColorSliceClassification')
Task.INPUT_RASTER = mosaicRaster_0
Task.CLASS_COLORS = [[114, 251, 253], [134, 219, 252], [154, 186, 251], [174, 154, 250], [194, 121, 249], [214, 89, 248], [234, 56, 247]]
Task.CLASS_RANGES = [[-3,0], [0,6], [6,8], [8,10], [10,12], [12,14], [14,17]]
Task.Execute

Task.OUTPUT_RASTER.Export, E.GetTemporaryFilename(), 'TIFF'
