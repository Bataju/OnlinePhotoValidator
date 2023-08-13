import logging
import os
from django.conf import settings
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

import api.photo_validator as photo_validator
import api.photo_validator_dir  as photo_validator_dir
import api.tinkerdirectory as tinker
from .models import Config
import urllib.parse
import shutil

import csv

# Create your views here.
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def startPage(request):
    context = {}
    config = Config.objects.all()[0]
    return render(request, 'api/index1.html', {'config': config})

def process_image(request):

    path = request.POST['path']
    type = request.POST['type']

    logging.info("Validating images from path: " + path)
    if type == 'folder':
      request.session['path'] = path
      photo_validator_dir.main(path)
      return redirect('http://127.0.0.1:8000/image_gallery')
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
    
     #read the reasons for invalidity from the results.csv file
    result_file = os.path.join(settings.STATIC_ROOT, 'api', 'static', 'api', 'images', 'result.csv')
    reasons_for_invalidity = {}#a dict

    with open(result_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            image_filename = row[0]  # The image filename is in the first column
            reasons = row[1:] # Initialize the list of reasons
            reasons_for_invalidity[image_filename] = reasons

    context = {
        'images_with_paths': images,
        'reasons_for_invalidity': reasons_for_invalidity,
    }

    for filename in os.listdir(invalid_images_directory):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            images.append(os.path.join(invalid_images_directory, filename))

    return render(request, 'api/image_gallery.html', context)

def process_selected_images(request):
    if request.method == 'POST':
        path = request.session.get('path')
        validDirectory = path + "/" + "valid/"
        result_file = os.path.join(settings.STATIC_ROOT, 'api', 'static', 'api', 'images', 'result.csv')

        if not os.path.exists(validDirectory):
            os.mkdir(validDirectory)

        selected_images = request.POST.getlist('selected_images')

        # read the CSV file into a list of rows
        rows_to_keep = []
        with open(result_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                image_filename = row[0]
                if image_filename not in selected_images:
                    rows_to_keep.append(row)  # Keep the row if the image is not in the selected list

        # Write the updated rows (excluding the removed row) back to the CSV file
        with open(result_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(rows_to_keep)

        for image_name in selected_images:
            image_path =  os.path.join(settings.STATIC_ROOT, 'api', 'static', 'api', 'images', 'invalid', image_name)
            destination_path = os.path.join(validDirectory, image_name)

            try:
                shutil.move(image_path, destination_path)
                print(f"Moved from {image_path} to {destination_path}: {e}")

            except Exception as e:
                print(f"Error moving {image_path} to {destination_path}: {e}")


        #now that the directory's content is changed
        images = []
        invalid_images_directory = os.path.join(settings.STATIC_ROOT, 'api', 'static', 'api', 'images', 'invalid')
    
        #read the reasons for invalidity from the results.csv file
        reasons_for_invalidity = {}#a dict

        with open(result_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                image_filename = row[0]  # The image filename is in the first column
                reasons = row[1:] # Initialize the list of reasons
                reasons_for_invalidity[image_filename] = reasons

        context = {
            'images_with_paths': images,
            'reasons_for_invalidity': reasons_for_invalidity,
        }

        for filename in os.listdir(invalid_images_directory):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                images.append(os.path.join(invalid_images_directory, filename))

        return render(request, 'api/image_gallery.html', context)
    
    return HttpResponse('Method not allowed', status=405)