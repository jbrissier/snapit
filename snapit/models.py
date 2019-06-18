from datetime import datetime, timedelta
from django.db import models
import uuid

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_eventuuid(self):
        return str(self.uuid)


    def get_absolute_url(self):

        from django.urls import reverse
        return reverse('snapit_upload', args=[str(self.uuid)])


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

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    last_image = Image()
    objects = models.Manager()

    def __unicode__(self):
        return self.file_path


class Message(models.Model):
    message = models.TextField(max_length=200)

    def __unicode__(self):
        return self.message


class ImageManager(object):
    change_interval = timedelta(seconds=10)  # 10s

    def __init__(self):
        self.change_time = datetime.now()
        self.request_time = datetime.now()
        self.last_image = None

    def get_new_image(self, event):
        self.last_image = ImageUpload.last_image.filter(event=event).first()
        if self.last_image:
            if not self.last_image.displayed:
            # reset the timer
            #   self.change_time = datetime.now()
                self.last_image.displayed = True
                self.last_image.save()

            return self.last_image

    def get_image(self, event):

        self.request_time = datetime.now()

        if not self.last_image:
            self.get_new_image(event)

        # task done is every x seconds
        if self.request_time - self.change_time > self.change_interval:
            try:
                self.get_new_image(event)
                self.change_time = self.request_time
            except:
                return self.last_image

        return self.last_image
