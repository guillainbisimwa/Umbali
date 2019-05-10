# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from autoslug import AutoSlugField
from django.db import models

from tinymce.models import HTMLField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import datetime

# Create your models here.
class Page(models.Model):
    title = models.CharField(blank=True, max_length=100)
    content = HTMLField()
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(blank=True, default=datetime.datetime.now)

    slug = AutoSlugField(populate_from="title",
                         unique_with=['created_on__month',])

    def __unicode__(self):
        return self.title

    def str(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Page(s)"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
