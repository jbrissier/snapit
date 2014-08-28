from datetime import datetime, timedelta
from django.db import models
from Queue import Queue
# Create your models here.

class ImageUpload(models.Model):
    file_path = models.CharField(max_length=512)
    upload_time = models.TimeField(auto_now_add = True)
    display_time = models.TimeField(blank=True, null=True)
    displayed = models.BooleanField(default=False)


class ImageManager(object):
    change_interval = timedelta(seconds=10) # 10s

    def __init__(self):
        self.imageQueue = Queue()
        self.change_time = datetime.now()
        self.request_time = datetime.now()
        self.last_image = None
        self.load_images_from_db()

    def load_images_from_db(self):
        images = ImageUpload.objects.filter(displayed=False)

        for i in images:
            self.imageQueue.put(i)

    def add_image(self, path):
        im = ImageUpload()
        im.file_path = path
        im.save()

        self.imageQueue.put(im)



    def get_image(self):

        #import pdb; pdb.set_trace();

        self.request_time = datetime.now()

        if not self.last_image:
            try:
                self.last_image = self.imageQueue.get_nowait()
            except:
                pass



        # task done is every x seconds
        if self.request_time - self.change_time > self.change_interval:
            try:
                self.last_image =  self.imageQueue.get_nowait()

                self.change_time = self.request_time
            except:
                return self.last_image

        return self.last_image
