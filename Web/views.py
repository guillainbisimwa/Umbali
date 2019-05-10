# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import View

from django.template.loader import render_to_string
from django.utils import timezone

from django.http import Http404
from django.contrib.auth import login, authenticate

from Web.forms import *

from Event.models import *
from Web.models import *
from MyEvent.models import *
from paypal.standard.forms import PayPalPaymentsForm

from django.conf import settings
import thread
import json


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

def index(request):
    now = timezone.now()
    if 'event' in request.GET:
        last_event = get_object_or_404(EventLive,slug=request.GET.get('event',None),is_active=True,end_time__gt=timezone.now())
    else:
        last_event = EventLive.objects.filter(is_active=True,end_time__gt=timezone.now()).order_by('-created_on')
        if last_event.count() > 0:
            last_event = last_event.last()
        else:
            last_event = None
    return render(request,"Web/base.html",locals())

def contact(request):
    return render(request,"Web/contact.html",locals())

#---------------------------------------------------------------------------------------------------------------------
# Register views
class RegisterUserView(View):
    template = "Web/register.html"
    def get(self,request):
        if request.user.is_authenticated():
            return redirect('Web:index')
        form = SignUpForm()
        return render(request,self.template,locals())

    def post(self,request):
        if request.user.is_authenticated():
            return redirect('Web:index')
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Send thanks mail process
            current_site = get_current_site(request)
            subject = 'Bienvenue | Umbali'
            message = render_to_string('Mail/thank_register_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            #user.email_user(subject, message,settings.EMAIL_GROUP_CONTACT)
            thread.start_new_thread(user.email_user,args=(subject, message,settings.EMAIL_SENDER_GROUP))

            if 'next' in request.GET:
                return redirect(request.GET.get('next','index'))
            return redirect('/?sign_up=1')
        return render(request, self.template, locals())

#---------------------------------------------------------------------------------------------------------------------
class CheckoutView(View):
    template = "Web/pay.html"
    def get(self,request,event_slug):
        if not request.user.is_authenticated():
            return redirect('/login/?next=/pay/'+str(event_slug)+'/')
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
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
        return render(request,self.template,locals())

class CheckoutSuccessView(View):
    template = "Web/pay_success.html"
    def get(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        return render(request,self.template,locals())

class CheckoutFailView(View):
    template = "Web/pay_fail.html"
    def get(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        return render(request,self.template,locals())


class LiveView(View):
    template_tizen = "Web/live_on_tizen.html"
    template = "Web/live.html"
    def get(self,request,event_slug):
        event = get_object_or_404(EventLive, slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,event=event,user=request.user)
        if myEvent.watcher_ip != None and myEvent.watcher_ip != get_client_ip(request):
            myEvent = None
        elif myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            myEvent.watcher_ip = get_client_ip(request)
            myEvent.save()
        return render(request,self.template,locals())

class GetMyLive(View):
    def get(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,event=event,user=request.user)
        if myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            streamConf = get_object_or_404(EventLiveStreamConf,event=event)
            response_data = {}
            response_data['hls'] = streamConf.hls
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        raise Http404("Please disconnect from other device to watch here, contact us if the problem persist")

    def post(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,event=event,user=request.user)
        if myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            myEvent.watcher_ip = get_client_ip(request)
            myEvent.save()
            streamConf = get_object_or_404(EventLiveStreamConf,event=event)
            response_data = {}
            response_data['hls'] = streamConf.hls
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        raise Http404("Please disconnect from other device to watch here, contact us if the problem persist")

    def delete(self,request,event_slug):
        event = get_object_or_404(EventLive,slug=event_slug,is_active=True)
        myEvent = get_object_or_404(MyEventLive,event=event,user=request.user)
        if myEvent.watcher_ip == None or myEvent.watcher_ip == get_client_ip(request):
            myEvent.watcher_ip = None
            myEvent.save()
            streamConf = get_object_or_404(EventLiveStreamConf,event=event)
            response_data = {}
            response_data['hls'] = streamConf.hls
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        raise Http404("Please disconnect from other device to watch here, contact us if the problem persist")

class PageView(View):
    template = "Web/page.html"
    def get(self,request,page_slug):
        page = get_object_or_404(Page,slug=page_slug)
        return render(request,self.template,locals())

def handler404(request):
    return render(request, "Web/404.html", status=404)

def handler500(request):
    return render(request, "Web/500.html", status=404)
