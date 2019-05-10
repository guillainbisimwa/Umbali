from django.conf.urls import url
from rest_framework.authtoken import views as rest_views
from API.views import *

urlpatterns = [
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
    url(r'^user/detail/$', UserDetail.as_view()),

    url(r'^event/list/', EventList.as_view()),
    url(r'^myevent/list/', MyEventList.as_view()),
    url(r'^event/my/(?P<event_slug>[\w-]+)/', MyEvent.as_view()),

    url(r'^pay/(?P<token>[\w-]+)/(?P<event_slug>[\w-]+)/$', Process_payment, name='go_to_payment'),
]
