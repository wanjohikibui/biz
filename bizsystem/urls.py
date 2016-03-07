from django.conf.urls import patterns, include, url
from django.contrib import admin
from permit.views import * 
import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from permit.models import *
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views
from django.contrib.auth import urls
#from registration.backends.simple.views import *

admin.autodiscover()
admin.site.site_header = 'Bungoma County Business Revenue Collection - Tracking System'
admin.site.site_title = 'Admin'

urlpatterns = patterns('',

			    url(r'^admin/', include(admin.site.urls)),
			    # Apps
			    url(r'^', include('permit.urls')),   

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)