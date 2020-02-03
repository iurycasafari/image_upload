"""
Provide views for core application.
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render, redirect

from webapp.core.models import Image
from webapp.core.forms import ImageForm


def home(request):
    images = Image.objects.all()

    return render(request, 'core/home.html', { 'images': images })


def model_form_upload(request):
    if request.method == 'POST':
        
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            message = f'{form.cleaned_data["name"]} image uploaded'

            image = Image.objects.filter(name=form.cleaned_data['name'].lower()).first()
            
            if image:
                message = f'{form.cleaned_data["name"]} image changed'

            form.save()

            return render(request, 'core/upload_message.html', { 'message': message })

    else:
        form = ImageForm()

    return render(request, 'core/model_form_upload.html', {
        'form': form
    })


def get_image(request, image_name):
    if request.method == 'GET':
        image = Image.objects.filter(name=image_name.lower()).first()

        if image:
            return render(request, 'core/render_image.html', { 'image': image })

    raise Http404("Image does not exist")
