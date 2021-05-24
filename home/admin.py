from django.contrib import admin


# Register your models here.

from .models import ReportBug, Sign , Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'user_id',  'sign_id','recognition_date','accuracy', )
    list_filter =   ('sign_id','recognition_date','user_id',)
    search_fields = ('user_id__username','sign_id__name',)
    

class SignAdmin(admin.ModelAdmin):
    list_display = ('sign_id','name', 'avg','lower_than_50','higher_than_50',)
    list_filter =   ('name',)
    search_fields = ('name',)
    

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)


admin.site.register(Sign, SignAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ReportBug, ReportAdmin)