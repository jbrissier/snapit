from django.core.management.base import BaseCommand
from snapit.models import ImageUpload, Event
import os
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        for img in os.listdir(settings.MEDIA_ROOT):
            wp = os.path.join('media', img)

            event = Event.objects.filter(active=True).order_by('-id').first()

            im, created = ImageUpload.objects.get_or_create(file_path=wp, event=event)

            print("%s is created:%s" % (wp, created))
