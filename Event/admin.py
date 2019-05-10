# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from Event.models import *

# Register your models here.
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','updated_on','created_on')
    search_fields = ('title',)
    date_hierarchy = 'created_on'
admin.site.register(EventCategory,EventCategoryAdmin)

class EventLiveAdmin(admin.ModelAdmin):
    list_display = ('category','title','start_time','end_time','prestator','price','is_active','created_on')
    list_filter = ('category','is_active')
    search_fields = ('title','prestator','short_description','keywords')
    date_hierarchy = 'created_on'
admin.site.register(EventLive,EventLiveAdmin)

class EventLiveStreamConfAdmin(admin.ModelAdmin):
    list_display = ('event','created_on')
    date_hierarchy = 'created_on'
admin.site.register(EventLiveStreamConf,EventLiveStreamConfAdmin)
