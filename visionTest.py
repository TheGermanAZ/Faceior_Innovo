import os, io
from google.cloud import vision


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\jonat\Documents\Hophacks\hophacks-52ea2c3c8fe5.json'

client = vision.ImageAnnotatorClient()

file_name = 'right.jpg'
image_path = r'C:\Users\jonat\Documents\Hophacks\Photos\right.jpg'

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.face_detection(image=image)
faceAnnotations = response.face_annotations

likehood = ('Unknown', 'Very Unlikely', 'Unlikely', 'Possibly', 'Likely', 'Very Likely')

print('Faces:')
x=0

for face in faceAnnotations:
    print("Pan tilt " + str(face.pan_angle))
    print("Face tilt "+ str(face.tilt_angle))
    # print('Headwear likelyhood: {0}'.format(likehood[face.headwear_likelihood]))
    # face_vertices = ['({0},{1})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
    # print('Face bound: {0}'.format(', '.join(face_vertices)))
    x=x+1
    print("Count %d"%x)
    print('')
