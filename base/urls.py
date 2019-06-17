from django.conf.urls import include, url
from django.urls import path
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from snapit.views import upload_file, view_images, get_latest_picture, LatesImage, UploadView,EventList

admin.autodiscover()

urlpatterns = [
    # admin page
    #url(r'^$', TemplateView.as_view(template_name='home.html')),
    path(r'', EventList.as_view(), name="events"),
    path('upload/<uuid:eventuuid>/', UploadView.as_view(), name="snapit_upload"),
    url(r'^view/image/$', get_latest_picture, name="snapit_picture"),
    url(r'^view/last/$', LatesImage.as_view(), name="snapit_last_picture"),
    url(r'^view/', view_images, name="snapid_view"),
    path(r'admin/', admin.site.urls),
]



if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
