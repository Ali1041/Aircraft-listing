from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finning_aircraft',
        'USER': 'finning_aircraft',
        'PASSWORD': 'z2pthAvvWT4yFQJh',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

MEDIA_DEBUG = True

ALLOWED_HOSTS = ['*.rightaircraft.com']
DOMAIN_URL = "http://www.rightaircraft.com"
CONTACT_EMAILS = ['info@moonjetgroup.com']
CONTACT_MAIN_EMAIL = CONTACT_EMAILS[0]
CONTACT_PHONE_NUMBER = '+44 (0) 7534 165 816'