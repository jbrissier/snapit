from datetime import datetime, timedelta
from django.db import models
from Queue import Queue
# Create your models here.


class Image(models.Manager):

    def get_queryset(self):
        qs = super(Image, self).get_queryset()
        im = qs.filter(displayed=False).order_by('upload_time')
        if im.count() > 0:
            return im
        else:
            return qs.order_by('?')


class ImageUpload(models.Model):
    file_path = models.CharField(max_length=512)
    upload_time = models.TimeField(auto_now_add=True)
    display_time = models.TimeField(blank=True, null=True)
    displayed = models.BooleanField(default=False)

    last_image = Image()
    objects = models.Manager()

    def __unicode__(self):
        return self.file_path



class ImageManager(object):
    change_interval = timedelta(seconds=10)  # 10s

    def __init__(self):
        self.change_time = datetime.now()
        self.request_time = datetime.now()
        self.last_image = None

    def get_new_image(self):
        self.last_image = ImageUpload.last_image.first()
        if self.last_image:
            if not self.last_image.displayed:
            # reset the timer
            #   self.change_time = datetime.now()
                self.last_image.displayed = True
                self.last_image.save()

            return self.last_image

    def get_image(self):

        self.request_time = datetime.now()

        if not self.last_image:
            self.get_new_image()

        # task done is every x seconds
        if self.request_time - self.change_time > self.change_interval:
            print "select new image"
            try:
                self.get_new_image()
                self.change_time = self.request_time
            except:
                return self.last_image

        return self.last_image
