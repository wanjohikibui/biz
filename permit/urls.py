from django.conf.urls import patterns, include, url
from django.contrib import admin
from permit.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from permit.models import *
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views
from django.contrib.auth import urls
#from registration.backends.default.views import ActivationView
#from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',
     url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
     url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),    
     url(r'^signup/$', 'permit.views.signup', name='signup'),

     url(r'^settings/$', 'permit.views.settings', name='settings'),
     url(r'^settings/picture/$', 'permit.views.picture', name='picture'),
     url(r'^settings/upload_picture/$', 'permit.views.upload_picture', name='upload_picture'),
     url(r'^settings/save_uploaded_picture/$', 'permit.views.save_uploaded_picture', name='save_uploaded_picture'),
     url(r'^settings/password/$', 'permit.views.password', name='password'),

     url(r'^network/$', 'permit.views.network', name='network'),
     url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
     url(r'^index/$', TemplateView.as_view(template_name='index.html'), name='index'),
     url(r'^apply/$', 'permit.views.application_portal', name='apply'),
     url(r'^our_story/$', TemplateView.as_view(template_name='our_story.html'), name='our_story'),
     url(r'^product/$', TemplateView.as_view(template_name='product.html'), name='product'),
     url(r'^services/$', TemplateView.as_view(template_name='services.html'), name='services'),
     url(r'^map/$','permit.views.mapping', name='mapping'),
     url(r'^map/admin$','permit.views.map_admin', name='admin'),
     url(r'^map/get_business/$', 'permit.views.get_business', name='get_business'),   					
     url(r'^map/business/filter/$','permit.views.business_filter', name='business_filter'),
     url(r'^business_data/$', GeoJSONLayerView.as_view(model=Business_profile, properties=('business_name', 'business_type','business_class','geom','business_compliance' )), name='data'),
     url(r'^county_data/$', GeoJSONLayerView.as_view(model=County, properties=('name2','count')), name='county_data'),
     url(r'^location_data/$', GeoJSONLayerView.as_view(model=Locations, properties=('location_b','subloc_b','division_b' )), name='location_data'),
     url(r'^parcel_data/$', GeoJSONLayerView.as_view(model=Parcels, properties=('id','parcel_no','blockid','sectcode')), name='parcel_data'),
     url(r'^impacts/$', TemplateView.as_view(template_name='impacts.html'), name='impacts'),
     url(r'^contact_us/$', TemplateView.as_view(template_name='contact_us.html'), name='contact_us'),
     url(r'^info/$', TemplateView.as_view(template_name='info.html'), name='info'),
     url(r'^analytics/$', TemplateView.as_view(template_name='analytics.html'), name='analytics'),
     url(r'^dashboard/$', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
     url(r'^customer_portal/$', 'permit.views.customer_portal', name='customer_portal'),
     url(r'^business_portal/$', 'permit.views.add_business_profile', name='business_portal'),
     url(r'^permit', 'permit.views.create_permit', name='permit'),    
     url(r'^payment_customer', 'permit.views.payment_customer', name='payment_customer'),
     url(r'^generate_permit', 'permit.views.generate_permit', name='generate_permit'),
					    
)