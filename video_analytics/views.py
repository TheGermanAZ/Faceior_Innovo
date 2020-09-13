from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import  FileSystemStorage
import os
from gcloud import storage
import GoogleMerged

client = storage.Client()



class Home(TemplateView):
    template_name = 'home.html'

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        bucket = client.get_bucket('hophacks-289306.appspot.com')
        blob = bucket.blob(uploaded_file.name)
        with open(r'C:\Users\dmars\PycharmProjects\HopHacks\Faceior_Innovo\media\Media1.mp4', "rb") as file:
            blob.upload_from_file(file)

        # RUN GOOGLE MERGED (PULLS FROM STORAGE)
        # PUSH JSON TO Web page.


    return render(request, 'upload.html')



def index(request):
    return HttpResponse('hello there')
