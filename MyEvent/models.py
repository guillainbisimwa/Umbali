# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from paypal.standard.ipn.models import PayPalIPN

from Event.models import EventLive

import datetime

from paypal.standard.ipn.signals import payment_was_successful

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

# local function
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist or Exception as e:
        return None

class MyEventLive(models.Model):
    user = models.ForeignKey(User,related_name="myEventLiveUser")
    event = models.ForeignKey(EventLive,related_name="myEventLiveEvent")
    paypal = models.OneToOneField(PayPalIPN)
   
    # Meta detail
    watcher_ip = models.CharField(max_length=100,null=True,default=None,blank=True)
    user_agent = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return "%s - %s"%(self.user.get_full_name(),self.event.title)

    def str(self):
        return "%s - %s"%(self.user.get_full_name(),self.event.title)

    class Meta:
        verbose_name = "My Event Live"
        verbose_name_plural = "My Event Lives"


def show_me_the_money(sender, **kwargs):
   ipn_obj = sender
   # Undertake some action depending upon `ipn_obj`.
   event_id = ipn_obj.invoice.split("#")[0]
   user_id = ipn_obj.invoice.split("#")[1]

   event = get_or_none(EventLive,id=event_id)
   user = get_or_none(User,id=user_id)
   price = event.price == Money(ipn_obj.mc_gross,"USD")
   if event != None and user != None and price:
       myEvent = MyEventLive(user=user)
       myEvent.event = event
       myEvent.paypal = ipn_obj
       myEvent.save()

       subject = 'Confirmation de paiement | Umbali'
       message = render_to_string('Mail/payment_confirmation.html', {
           'user': user,
           'domain': "www.umbali.live",
           'myEvent_title':event.title,
           'myEvent_id':myEvent.id,
       })
       user.email_user(subject, message,settings.EMAIL_HOST_USER)

payment_was_successful.connect(show_me_the_money)
