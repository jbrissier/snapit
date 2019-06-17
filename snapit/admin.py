from django.contrib import admin
from .models import ImageUpload, Message, Event
# Register your models here.
admin.site.register(ImageUpload)
admin.site.register(Message)
admin.site.register(Event)

