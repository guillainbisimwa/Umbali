# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Web.models import Page

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','is_active','updated_on','created_on')
    search_fields = ('title','content')
    date_hierarchy = 'created_on'
admin.site.register(Page,PageAdmin)

# Set up admin panel
admin.site.site_header = 'Umbali Admin Panel'
