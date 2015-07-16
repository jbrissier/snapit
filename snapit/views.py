from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from forms import UploadFileForm
from django.template import RequestContext
from django.conf import settings
import os
from models import ImageManager, ImageUpload
import uuid

image_manager = ImageManager()


def get_latest_picture(self):

    image = image_manager.get_image()
    if image:
        return HttpResponse(os.path.relpath(image.file_path, settings.MEDIA_ROOT))
    else:
        return HttpResponse(None)


def handle_uploaded_file(f):
    #import pdb; pdb.set_trace()
    # todo save this in the db

    if not os.path.exists(settings.MEDIA_ROOT):
        os.mkdir(settings.MEDIA_ROOT)

    wp = os.path.join(settings.MEDIA_ROOT, f._name)

    if os.path.exists(wp):
        uid = uuid.uuid4()
        name, extention = os.path.splitext(wp)
        wp = os.path.join(settings.MEDIA_ROOT, str(uid) + "." + extention)

    with open(wp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    upload = ImageUpload()
    upload.file_path = wp
    upload.save()


def upload_file(request):
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # new form
            form = UploadFileForm()
            return render_to_response('upload.html', {'form': form, 'thanks': 'Danke, Bild wird gleich angezeigt'}, RequestContext(request, {}))
        else:
            print 'form not valid'
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form}, RequestContext(request, {}))


def view_images(request):
    return render_to_response('viewer.html', RequestContext(request, {}))
