import os
import math
import io
from google.cloud import vision

"""
Iterates over all images in a given directory and determines the pan(horizontal) and face(vertical) tilt of
all faces in each image. At the moment prints to console - will need to create output file.
"""

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\dmars\Downloads\hophacks-a78f8c494166.json'

client = vision.ImageAnnotatorClient()
DISTRACT_THRESHOLD = 18.0

def google_vision(image,content):
    image = vision.types.Image(content=content)
    response = client.face_detection(image=image)
    faceAnnotations = response.face_annotations

    likehood = ('Unknown', 'Very Unlikely', 'Unlikely', 'Possibly', 'Likely', 'Very Likely')

    x=0
    numDistracted = 0

    for face in faceAnnotations:
        x=x+1
        if (abs(face.pan_angle) >= DISTRACT_THRESHOLD):
            numDistracted += 1


    return (numDistracted / x) * 100

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
    print(iterate_on_dir(os.path.join(os.getcwd(),"frames")))
