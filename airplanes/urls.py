"""airplanes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from classifieds import views as classifieds_views
from classifieds import forms as classifieds_forms
from django.conf import settings

# from registration.backends.simple.views import RegistrationView
from django_registration.backends.one_step.views import RegistrationView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$',classifieds_views.signup,
        name='registration_register'),
    url(r'^accounts/', include('django_registration.backends.one_step.urls')),

    url(r'^login/$', classifieds_views.views_login, name='login'),
    url(r'^logout/$', auth_views.auth_logout, {'next_page': '/'}, name='logout'),


    url(r'^$', classifieds_views.index, name='index'),
    url(r'^contacts/$', classifieds_views.contacts, name='contacts'),
    url(r'^classifieds/$', classifieds_views.classifieds, name='classifieds'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/$', classifieds_views.classified, name='classified'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/edit/$', classifieds_views.post_ad, name='classified_edit'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/pay/$', classifieds_views.classified_pay, name='classified_pay'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/confirm-payment/$', classifieds_views.classified_confirm_payment, name='classified_confirm_payment'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/activate/$', classifieds_views.classified_activate, name='classified_activate'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/deactivate/$', classifieds_views.classified_deactivate, name='classified_deactivate'),
    url(r'^my-classifieds/$', classifieds_views.my_classifieds, name='my_classifieds'),
    url(r'^post-ad/$', classifieds_views.post_ad, name='post_ad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
