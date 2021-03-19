import os, sys, site

sys.path.append('/home/airplanes')
sys.path.append('/home/airplanes/airplanes')

os.environ['DJANGO_SETTINGS_MODULE'] = 'airplanes.prod_settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()