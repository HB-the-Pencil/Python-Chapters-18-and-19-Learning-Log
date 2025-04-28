from django.contrib import admin
from .models import Topic, Entry

# Register the models.
admin.site.register(Topic)
admin.site.register(Entry)