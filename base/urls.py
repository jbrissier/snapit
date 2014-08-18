from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView

from snapit.views import upload_file

admin.autodiscover()

urlpatterns = patterns('',
    # admin page
    #url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^$', upload_file, name="snapit_upload"),
    url(r'^admin/', include(admin.site.urls))
)
