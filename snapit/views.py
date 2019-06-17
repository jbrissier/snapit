# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
import os
import uuid
from io import BytesIO
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from constance import config
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View, TemplateView

from .models import ImageManager, ImageUpload, Message, Event
from .forms import UploadFileForm

from django.contrib import messages


image_manager = ImageManager()


class LatesImage(APIView):

    def get(self, request):
        message = None
        try:

            message = Message.objects.first().message
        except:
            pass

        image = image_manager.get_image()
        re = {
            'image_id': image.pk,
            'image_name': os.path.relpath(image.file_path, settings.MEDIA_ROOT),
            'image_src': os.path.join(settings.MEDIA_URL, os.path.relpath(image.file_path, settings.MEDIA_ROOT)),
            'interval': 10000,
            'message': message,
            'animate': config.ANIMATE_IMAGE,
        }
        return Response(re)


def get_latest_picture(self):

    image = image_manager.get_image()
    if image:
        return HttpResponse(os.path.relpath(image.file_path, settings.MEDIA_ROOT))
    else:
        return HttpResponse(None)


def handle_uploaded_file(f):

    if not os.path.exists(settings.MEDIA_ROOT):
        os.mkdir(settings.MEDIA_ROOT)

    wp = os.path.join(settings.MEDIA_ROOT, f._name)

    if os.path.exists(wp):
        uid = uuid.uuid4()
        name, extention = os.path.splitext(wp)
        wp = os.path.join(settings.MEDIA_ROOT, str(uid) + extention)

    with BytesIO() as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        upload = ImageUpload()
        upload.file_path = wp

        destination.seek(0)

        image = Image.open(destination)
        try:
            exif = image._getexif()
            rotations = {
                1: 0,
                3: -180,
                8: -270,
                6: -90,
            }
            exif_rt = exif.get(274, None)
            if exif_rt:
                image = image.rotate(rotations[exif_rt])
        except AttributeError:
            pass

        image.save(wp)

    upload.save()


class EventList(ListView):
    template_name = 'event_list.haml'
    model = Event

class UploadView(TemplateView):
    template_name = 'upload.haml'
    form_class = UploadFileForm


    def get_contex_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['eventuuid'] = kwargs.get('eventuuid')

        return context


    # def get_success_url(self):
    #     return reverse_lazy('snapit_upload')

    # def get(self, *arg, **kwargs):
    #     return HttpResponse('hello')



    def form_valid(self, form):

        messages.add_message(self.request, messages.INFO, 'Bild wurder erfolgreich hinzugefügt')
        return HttpResponseRedirect(self.get_success_url())


def upload_file(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # new form
            form = UploadFileForm()
            return render(request, 'upload.haml', context={'form': form, 'thanks': 'Danke, Bild wird gleich angezeigt'})
        else:
            print('not valid')
    else:
        form = UploadFileForm()
    return render(request, 'upload.haml', context={'form': form})


def view_images(request):
    return render(request, 'viewer.haml')
