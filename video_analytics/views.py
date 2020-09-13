from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'home.html'

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']

    return render(request, 'upload.html')

def index(request):
    return HttpResponse('hello there')
