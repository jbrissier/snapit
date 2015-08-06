from django.core.management.base import BaseCommand
from snapit.models import ImageUpload


class Command(BaseCommand):

    def handle(self, *args, **options):
        image_len = len(ImageUpload.objects.all())
        print "total images %s" % image_len
