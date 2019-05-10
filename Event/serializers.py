from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User

from Event.models import *

from django.utils.timesince import timeuntil
from django.utils import timezone

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        exclude = ("created_on",)

class EventLiveSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(many=False)
    second = serializers.SerializerMethodField('getSecond')

    def getSecond(self,obj):
        if obj.start_time != None:
            return (obj.start_time-timezone.now()).total_seconds()
        return None

    class Meta:
        model = EventLive
        exclude = ("created_on",)

class EventLiveStreamConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLiveStreamConf
        exclude = ("created_on",)
