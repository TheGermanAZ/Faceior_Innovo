import image_slicer
import os
imageFilePath =r'C:\Users\jonat\Documents\Hophacks\Zoom Sample\Capture.png'
numberOfFaces = 12
sliceAmount = int(round(numberOfFaces / 10, 1)) + 1
# print(sliceAmount)

if (sliceAmount > 1 and sliceAmount < 3):
    # print(sliceAmount)
    image_slicer.slice(imageFilePath, sliceAmount)
    os.remove(imageFilePath)
if (sliceAmount >= 3):
    sliceAmount = 3
    # print(sliceAmount)
    os.remove(imageFilePath)
    image_slicer.slice(imageFilePath, sliceAmount)