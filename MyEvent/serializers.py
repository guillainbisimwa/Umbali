from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User

from MyEvent.models import *
from Event.models import EventLiveStreamConf

from django.utils.timesince import timeuntil
from django.utils import timezone



# Get single object from args
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist or Exception as e:
        return None


class MyEventLiveSerializer(serializers.ModelSerializer):
    hls = serializers.SerializerMethodField('getHls')
    has_started = serializers.SerializerMethodField('getHasStarted')

    def getHasStarted(self,obj):
        if obj.event.start_time != None:
            return obj.event.start_time < timezone.now()
        return False

    def getHls(self,obj):
        stream_conf = get_or_none(EventLiveStreamConf,event=obj.event)
        if stream_conf != None:
            return stream_conf.hls
        return None


    class Meta:
        model = MyEventLive
        exclude = ("created_on",)
