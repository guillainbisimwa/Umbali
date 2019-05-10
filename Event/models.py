# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from djmoney.models.fields import MoneyField
from djmoney.money import Money

import datetime

# Create your models here.
class EventCategory(models.Model):
    title = models.CharField(blank=True, max_length=100)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

    def str(self):
        return self.title

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categorie(s)"

class EventLive(models.Model):
    category = models.ForeignKey(EventCategory)
    title = models.CharField(blank=True, max_length=100)
    start_time = models.DateTimeField(null=True,default=None,blank=True)
    end_time = models.DateTimeField(null=True,default=None,blank=True)
    prestator = models.CharField(blank=True, max_length=250)
    cover = models.ImageField(upload_to="event/live/cover/")
    short_description = models.TextField(blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency=settings.CURRENCY)
    keywords = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=datetime.datetime.now)

    slug = AutoSlugField(populate_from="title",
                         unique_with=['created_on__month',])

    def __unicode__(self):
        return self.title

    def str(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class EventLiveStreamConf(models.Model):
    event = models.OneToOneField(EventLive, related_name='eventLiveStreamConf')
    hls = models.CharField(blank=False, max_length=250)
    player_embedded_code_web = models.CharField(max_length=100)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.event.title

    def str(self):
        return self.event.title

    class Meta:
        verbose_name = "Event Live Stream Configuration"
        verbose_name_plural = "Event Live Stream Configuration(s)"
