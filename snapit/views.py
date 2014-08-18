from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import UploadFileForm
from django.template import RequestContext


def handle_uploaded_file(f):
    import pdb; pdb.set_trace()
    with open('/Users/jochenbrissier/Desktop/test.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
        else:
            print 'form not valid'
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form}, RequestContext(request, {}))
