import logging
import os
from django.conf import settings
from django import forms
from django.http import HttpResponse
from django.shortcuts import render

import api.photo_validator as photo_validator
import api.photo_validator_dir  as photo_validator_dir
import api.tinkerdirectory as tinker
from .models import Config
import urllib.parse

# Create your views here.
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def startPage(request):
    context = {}
    config = Config.objects.all()[0]
    return render(request, 'api/index1.html', {'config': config})

def process_image(request):

    #print(request.POST)

    path = request.POST['path']
    type = request.POST['type']

    logging.info("Validating images from path: " + path)
    if type == 'folder':
      photo_validator_dir.main(path)
      return HttpResponse("Photo Validation Completed")
    else:
      message = photo_validator.main(path)
      return HttpResponse("Results:" + "\n" + message)

def dialogueBox(request):
    folderpath = tinker.opendialogForDirectory(request.POST['type'])

    return HttpResponse(folderpath)

def save_config(request):

    minHeight = request.POST['minHeight']
    maxHeight = request.POST['maxHeight']
    minWidth = request.POST['minWidth']
    maxWidth= request.POST['maxWidth']
    minSize= request.POST['minSize']
    maxSize= request.POST['maxSize']
    jpgchecked= request.POST.get('jpgchecked', 'True')
    pngchecked= request.POST.get('pngchecked', 'True')
    jpegchecked = request.POST.get('jpegchecked', 'True')

    config = Config.objects.all()
    config.delete()

    config = Config()
    config.min_height = minHeight
    config.max_height = maxHeight
    config.min_width = minWidth
    config.max_width = maxWidth
    config.min_size = minSize
    config.max_size = maxSize
    config.is_jpg='True' if jpgchecked == 'True' else  'False'
    config.is_png='True' if pngchecked == 'True' else  'False'
    config.is_jpeg='True' if jpegchecked == 'True' else  'False'

    config.save()

    return HttpResponse("Updated configurations")

def image_gallery(request):
    images = []

    invalid_images_directory = os.path.join(settings.STATIC_ROOT, 'api', 'static', 'api', 'images', 'invalid')
    
    for filename in os.listdir(invalid_images_directory):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            images.append(os.path.join(invalid_images_directory, filename))

    return render(request, 'api/image_gallery.html', {'images': images})
