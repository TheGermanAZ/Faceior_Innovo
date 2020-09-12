import os
import math
import io
from google.cloud import vision
import cv2

def extract_frames(inputvid):
    #Creates frames folder to store images
    framePath = os.path.join(os.getcwd(),r'C:\Users\jonat\Documents\Hophacks\Media Sample');
    if not os.path.exists(framePath):
        os.mkdir(framePath)

    count = 0
    capture = cv2.VideoCapture(inputvid)  # capture the video from the given path
    frameRate = capture.get(5)  # Get framerate of video
    while (capture.isOpened()):
        frameNum = capture.get(1)  # Get current frame number
        ret, frame = capture.read()
        if (ret != True): # If there are no frames left to read
            break
        if (frameNum % math.floor(frameRate) == 0):
            filename = "frame%d.jpg" % count;
            count += 1
            cv2.imwrite(os.path.join(framePath,filename), frame) # Writes image of frame.

    capture.release() # Close video reader

"""
Iterates over all images in a given directory and determines the pan(horizontal) and face(vertical) tilt of
all faces in each image. At the moment prints to console - will need to create output file.

Vision API Docs:
https://googleapis.dev/python/vision/latest/gapic/v1p4beta1/types.html#google.cloud.vision_v1p4beta1.types.FaceAnnotation.pan_angle
"""

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\jonat\Documents\Hophacks\hophacks-52ea2c3c8fe5.json'

client = vision.ImageAnnotatorClient()
DISTRACT_THRESHOLD = 18.0

def google_vision(image,content):
    image = vision.types.Image(content=content)
    response = client.face_detection(image=image,max_results=30)
    faceAnnotations = response.face_annotations


    x=0
    numDistracted = 0

    for face in faceAnnotations:
        x=x+1
        if (abs(face.pan_angle) >= DISTRACT_THRESHOLD):
            numDistracted += 1
    print(x)
    if(x>0):
        return (numDistracted / x) * 100
    return 0;
def iterate_on_dir(imgPath):
    percentDistracted = []
    for img in os.listdir(imgPath):
        file_name = os.path.abspath(os.path.join(imgPath, img))
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        percentDistracted.append(google_vision(image, content))

    return percentDistracted

if __name__ == "__main__":
    extract_frames(inputvid=r'C:\Users\jonat\Documents\Hophacks\Media Sample\Media1.mp4')
    print(iterate_on_dir(os.path.join(os.getcwd(),r'C:\Users\jonat\Documents\Hophacks\Media Sample')))
