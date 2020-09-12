import os
import io
from google.cloud import vision

"""
Iterates over all images in a given directory and determines the pan(horizontal) and face(vertical) tilt of
all faces in each image. At the moment prints to console - will need to create output file.
"""

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\jonat\Documents\Hophacks\hophacks-52ea2c3c8fe5.json'
client = vision.ImageAnnotatorClient()

def google_vision(image,content):
    image = vision.types.Image(content=content)
    response = client.face_detection(image=image)
    faceAnnotations = response.face_annotations

    likehood = ('Unknown', 'Very Unlikely', 'Unlikely', 'Possibly', 'Likely', 'Very Likely')

    print('Faces:')
    x=0

    for face in faceAnnotations:
        print("Pan tilt " + str(face.pan_angle))
        print("Face tilt "+ str(face.tilt_angle))
        x=x+1
        print("Count %d"%x)
        print('')

def iterate_on_dir(imgPath):
    for img in os.listdir(imgPath):
        file_name = os.path.abspath(os.path.join(imgPath, img))
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        google_vision(image, content)


if __name__ == "__main__":
    iterate_on_dir(os.path.join(os.getcwd(),"frames"))
