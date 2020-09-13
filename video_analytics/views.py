from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import  FileSystemStorage
from gcloud import storage
import os
import math
import io
from google.cloud import vision
import cv2
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'hophacks-a78f8c494166.json'

saving_client = storage.Client()
reading_client = storage.Client.from_service_account_json('hophacks-a78f8c494166.json')

client = vision.ImageAnnotatorClient()
DISTRACT_THRESHOLD = 18.0

class Home(TemplateView):
    template_name = 'home.html'

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        bucket = saving_client.get_bucket('hophacks-289306.appspot.com')
        blob = bucket.blob(uploaded_file.name)
        with open(r'C:\Users\dmars\PycharmProjects\HopHacks\Faceior_Innovo\media\Media1.mp4', "rb") as file:
            blob.upload_from_file(file)

        runVisionAnalytics(uploaded_file.name)
        # RUN GOOGLE MERGED (PULLS FROM STORAGE)
        # PUSH JSON TO Web page.
        return render(request, 'dashboard.html')


    return render(request, 'upload.html')


def extract_frames(inputvid):
    #Creates frames folder to store images
    framePath = os.path.join(os.getcwd(),'frames')
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
            filename = "frame%d.jpg" % count
            count += 1
            cv2.imwrite(os.path.join(framePath,filename), frame) # Writes image of frame.

    capture.release() # Close video reader

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
    if(x>0):
        return (numDistracted / x) * 100
    return 0.0

def iterate_on_dir(imgPath):
    percentDistracted = []
    for img in os.listdir(imgPath):
        file_name = os.path.abspath(os.path.join(imgPath, img))
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        percentDistracted.append(google_vision(image, content))

    return percentDistracted

def runVisionAnalytics(filename):
    bucket = reading_client.get_bucket('hophacks-289306.appspot.com')
    blob = bucket.get_blob(filename)
    blob.download_to_filename('video')
    extract_frames(inputvid='video')
    distList = iterate_on_dir(os.path.join(os.getcwd(), 'frames'))
    with open(os.path.join(os.getcwd(), 'data.json'), 'w') as f:
        json.dump(distList, f)
        print("Done!")

def index(request):
    return HttpResponse('hello there')
