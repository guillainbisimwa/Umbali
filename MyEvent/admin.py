# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from MyEvent.models import *

# Register your models here.

class MyEventLiveAdmin(admin.ModelAdmin):
    list_display = ('user','event','paypal','watcher_ip','updated_on')
    list_filter = ('event',)
    search_fields = ('user','event','watcher_ip',)
    date_hierarchy = 'created_on'
admin.site.register(MyEventLive,MyEventLiveAdmin)
