import image_slicer
numberOfFaces =12
sliceAmount = int(round(numberOfFaces / 10, 1))+1
#print(sliceAmount)

if(sliceAmount>1and sliceAmount<4):
   # print(sliceAmount)
    image_slicer.slice(r'C:\Users\jonat\Documents\Hophacks\Zoom Sample\Capture.png', sliceAmount)
if(sliceAmount>=5):
    sliceAmount =5
    #print(sliceAmount)
    image_slicer.slice(r'C:\Users\jonat\Documents\Hophacks\Zoom Sample\Capture.png', sliceAmount)

