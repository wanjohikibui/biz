__author__ = 'alphabuddha'

from django.contrib import admin 
from leaflet.admin import LeafletGeoAdmin
from .models import *
from django.contrib.gis import admin as geoadmin

# Register your models here.
class Customer_detailAdmin(admin.ModelAdmin):

    list_display = ('user','first_name', 'last_name', 'id_no', 'phone_no', 'email', 'address', 'town',)
    search_fields = ['id_no', 'town',]    
    default_lon =  3847314.09577 #36.9654#
    default_lat =  63561.86961 #-0.4030
    default_zoom = 14
    map_info = True
    map_width = 800
    map_height = 500

class Business_profileAdmin(geoadmin.OSMGeoAdmin):

    list_display = ('business_no','business_name', 'business_email', 'business_phone_no', 'business_address','business_form', 'business_compliance')
    search_fields = ['business_name', 'business_type','customer_detail',]    
    default_lon =  3847314.09577 #36.9654#
    default_lat =  63561.86961 #-0.4030
    default_zoom = 14
    map_info = True
    map_width = 800
    map_height = 500

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user_id = request.user
        obj.save()

class locationsAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('location_b','subloc_b','division_b')
    search_fields = ['division_b','location_b']

class parcelsAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id','parcel_no','blockid','sectcode')
    search_fields = ['id','parcel_no']
    ordering = ('id',)

class countyAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('name2','count')
    search_fields = ['name2','count']

class permitAdmin(admin.ModelAdmin):

    list_display = ('user','business_profile', 'dateapplied')
    search_fields = ['user', 'business_profile',]

admin.site.register(Customer_detail, Customer_detailAdmin)
geoadmin.site.register(Business_profile, Business_profileAdmin)
admin.site.register(Business_permit,permitAdmin)
admin.site.register(Customer_payment)
admin.site.register(Parcels,parcelsAdmin)
admin.site.register(Profile)
admin.site.register(Locations,locationsAdmin)
admin.site.register(County,countyAdmin)
