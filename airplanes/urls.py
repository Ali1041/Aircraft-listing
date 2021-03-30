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
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from classifieds import views as classifieds_views
from classifieds import forms as classifieds_forms
from django.conf import settings

urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # registration urls
    path('accounts/register/', classifieds_views.signup,
         name='registration_register'),
    path('accounts/login/', classifieds_views.views_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # classifieds urls
    path('',include('classifieds.urls')),
    path('mobile-api/',include('classifieds_mobile.urls')),


    # all auth authentication
    path('accounts/', include('allauth.urls')),

    # reset password urls
    path('reset_password/', PasswordResetView.as_view(template_name='registration/reset_password.html'),
         name='reset_password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         PasswordResetCompleteView.as_view(template_name='registration/last_reset.html'),
         name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
