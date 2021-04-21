from django.contrib import admin

# Register your models here.

from .models import Sign , Event
admin.site.register(Sign)
admin.site.register(Event)