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
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from classifieds import views as classifieds_views
from classifieds import forms as classifieds_forms
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('accounts/register/',classifieds_views.signup,
        name='registration_register'),

    path('accounts/login/', classifieds_views.views_login, name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),


    path('', classifieds_views.index, name='index'),
    path('contacts/', classifieds_views.contacts, name='contacts'),
    path('classifieds/', classifieds_views.ClassifiedListView.as_view(), name='classifieds'),
    path('classifieds/<int:pk>/', classifieds_views.ClassifiedDetailView.as_view(), name='classified'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/pay/$', classifieds_views.classified_pay, name='classified_pay'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/confirm-payment/$', classifieds_views.classified_confirm_payment, name='classified_confirm_payment'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/activate/$', classifieds_views.classified_activate, name='classified_activate'),
    url(r'^classifieds/(?P<classified_id>[0-9]+)/deactivate/$', classifieds_views.classified_deactivate, name='classified_deactivate'),
    path('my-classifieds/', classifieds_views.my_classifieds, name='my_classifieds'),
    path('post-ad/', classifieds_views.post_ad, name='post_ad'),
    path('search/',classifieds_views.search,name='search'),
    path('post-ad-edit/<int:pk>/',classifieds_views.post_ad,name='post_ad_edit'),
    path('delete-ad/<int:pk>/',classifieds_views.delete_classified,name='delete-ad'),
    path('newsletter-subscribe/',classifieds_views.newsletter,name='newsletter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
