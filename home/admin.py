from django.contrib import admin

# Register your models here.

from .models import ReportBug, Sign , Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'user_id',  'sign_id','recognition_date','accuracy')
    list_filter =   ('sign_id','recognition_date','user_id','accuracy')
class SignAdmin(admin.ModelAdmin):
    list_display = ('sign_id',   'name', )
    list_filter =   ('name',)

    

admin.site.register(Sign, SignAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ReportBug)