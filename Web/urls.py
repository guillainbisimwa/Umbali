from django.conf.urls import url
from Web import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^contact/', views.contact, name="contact"),
# ------------------------------------------------------
    url(r'^page/(?P<page_slug>[\w-]+)/$', views.PageView.as_view(), name="page"),
# ------------------------------------------------------
    url(r'^register/', views.RegisterUserView.as_view(), name="register"),
    url(r'^login/$', auth_views.login, {'template_name': 'Web/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
#-------------------------------------------------------
    url(r'^checkout/(?P<event_slug>[\w-]+)/$', views.CheckoutView.as_view(), name="checkout"),
    url(r'^checkout/success/(?P<event_slug>[\w-]+)/$', views.CheckoutSuccessView.as_view(), name="checkout_success"),
    url(r'^checkout/fail/(?P<event_slug>[\w-]+)/$', views.CheckoutFailView.as_view(), name="checkout_fail"),
#-------------------------------------------------------
    url(r'^live/(?P<event_slug>[\w-]+)/$', views.LiveView.as_view(), name="live"),
    url(r'^get/live/(?P<event_slug>[\w-]+)/$', views.GetMyLive.as_view(), name="get_my_live"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
