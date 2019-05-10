# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

from Event.models import *
from Event.serializers import *

from MyEvent.models import *
from MyEvent.serializers import *

from API.serializers import *

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from rest_framework.authtoken.models import Token

from paypal.standard.forms import PayPalPaymentsForm

from django.utils import timezone
from django.core.urlresolvers import reverse

from django.conf import settings


# Get Client IP address from request obj
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



# Get single object from args
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist or Exception as e:
        return None


# Get Single user detail only GET request accept [ header authentication not required ]
class UserDetail(APIView):
    """
    List all active and ready event
    """
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request):
        return Response(UserSerializer(request.user).data)

# Get event list [ header authentication required ]
class EventList(APIView):
    """
    List all active and ready event
    """
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, format=None):
        events = EventLive.objects.filter(is_active=True)
        events = events.filter(Q(start_time__gt=timezone.now()))

        serializer = EventLiveSerializer(events, many=True)
        return Response(serializer.data)


# Get single event, Post Client IP adress requested and Delete Client IP adress
class MyEvent(APIView):
    """
    MyEvent Single
    """
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,user=request.user,event=event)
        myEvent = MyEventLiveSerializer(myEvent)
        return Response(myEvent.data)

    def post(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,user=request.user,event=event)
        if myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            myEvent.watcher_ip = get_client_ip(request)
            myEvent.save()
        else:
            raise Http404("Please disconnect from other device to watch here, contact us if the problem persist")
        return Response(EventLiveSerializer(event).data)

    def delete(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,user=request.user,event=event)
        if myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            myEvent.watcher_ip = None
            myEvent.save()
        return Response(EventLiveSerializer(event).data)


# Get client events
class MyEventList(APIView):
    """
    MyEvent List
    """
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request):
        myEvents = MyEventLive.objects.filter(user=request.user,event__start_time__gt=timezone.now(),event__is_active=True)
        myEvents = myEvents.values_list('event',flat=True)
        myEvents = EventLive.objects.filter(id__in=myEvents)

        serializer = EventLiveSerializer(myEvents, many=True)
        return Response(serializer.data)

# Payment process page
def Process_payment(request,token,event_slug):
    # Get user
    user = get_object_or_404(Token,key=token)
    user = user.user

    # check if i already own this event ticket
    if get_or_none(MyEventLive,user=user,event__slug=event_slug,event__is_active=True) != None:
        raise Http404("Error: it seems like you already owe this event, try again if the problem persist please mail us on hello@umbali.live")

    event = get_object_or_404(EventLive,slug=event_slug)

    # What you want the button to do.
    paypal_dict = {
        "cmd":"_xclick",
        "business": settings.PAYPAL_BUSINESS,
        "lc":"GB",
        "amount": event.price.amount,
        "currency_code": event.price.currency,
        "notify_url": request.build_absolute_uri(reverse('paypal:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('Web:checkout_success',args=[event.slug,])),
        "cancel_return": request.build_absolute_uri(reverse('Web:checkout_fail',args=[event.slug,])),
        "invoice": str(event.id)+"#"+str(request.user.id),  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request,"API/process_payment.html",locals())
