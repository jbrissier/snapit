from django.core.management.base import BaseCommand
from snapit.models import ImageUpload


class Command(BaseCommand):

    def handle(self, *args, **options):
        ImageUpload.objects.all().delete()
        print("all images deleted")
