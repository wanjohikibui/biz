from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
#from userena.models import UserenaBaseProfile
import datetime
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db import models
from django.contrib.gis import geos
#geonode
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.db.models.signals import post_save
from django.conf import settings
import os.path
#from activities.models import Notification
import urllib, hashlib
#from taggit.managers import TaggableManager
#from geonode.groups.models import GroupProfile
import simplejson

def upload_folder(instance, filename):
    return "staff_images/%s" % (filename)

choices_constituency = (       
    ('Kimilili', 'Kimilili'),
    ('Sirisia', 'Sirisia'),
    ('Bumula', 'Bumula'),
    ('Kanduyi', 'Kanduyi'),  
)

choices_towns = (
    ('Bungoma', 'Bungoma'),		
	('Webuye', 'Webuye'),
	('Malakisi', 'Malakisi'),
)

choices_streets = (
    ('Street1', 'Street1'),
    ('Street2', 'Street2'),
    ('Street3', 'Street3'),
)

choices_zones = (       
    ('CBD','CBD'),
    ('Industrial', 'Industrial'),
    ('Residential', 'Residential'),
    #('Agricultural', 'Agricultural'),

)

choices_customer_type = (
    ('Owner','Owner'),
    ('Employee', 'Employee'),
    ('Agent', 'Agent'),
    #('County Official', 'County Official'),

)

#business

choices_business_scope = (      
    ('Single', 'Single'),    
    ('Chain_Stores', 'Chain_Stores'),
    ('Franchise', 'Franchise'),
    
)

choices_business_form = (       
    ('Sole Proprietorship', 'Sole Proprietorship'),
    ('Patnership', 'Patnership'),
    ('Corporation', 'Corporation'),
    #('Cooperative', 'Cooperative'),   
)

choices_business_type = (
    ('Retail Shops', 'Retail Shops'),
    ('Alcohol Sales', 'Alcohol Sales'),
    ('Cybers', 'Cybers'),   
)

choices_business_class = (      #Check 
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    #('D', 'D'),
)

choices_business_category = (       
    ('Commmercial', 'Commmercial'),
    ('NGO', 'NGO'),
    ('Non Profit', 'Non Profit'),   
)

choices_no_employees= (       
    ('Less than 5', '5'),
    ('Less than 10', '10'),
    ('Less than 20', '20')
    
)

choices_business_compliance= (
    ('Yes', 'Yes'),
    ('No', 'No')
)
#payments

choices_payment_mode = (
    ('Mpesa', 'Mpesa'),
    ('Banks', (
            ('KCB', 'KCB'),
            ('Equity', 'Equity'),
            ('StandardChartered', 'StandardChartered'),
        )
    ),
        
)

#Payment Period

PERIODS = (
    ('Yearly', 'Yearly'),
    ('Bi_annual', 'Bi_annual'),
    ('Quarterly', 'Quarterly'),
    #('Monthly', 'Monthly'),
)


#Models: Customer Profile Account
'''
Customer_detail
Land_profile
Building_profile
Business_profile
Customer_payments

'''
# Details about the customer
#Customer profile registration
class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    customer_type = models.CharField(
        _('Customer Type'), 
        choices= choices_customer_type, 
        max_length= 54, 
        blank= True, 
        null=True)
    id_no = models.CharField(
        _('ID No'),
        max_length=255,
        blank=True,
        null=True
        )   
    phone_no = models.CharField(
        _('Phone no:'), 
        max_length=255, 
        blank=True, 
        null=True
       )      
    address = models.CharField(
        _('Postal Code'),
        max_length=255,
        blank=True,
        null=True
        )
    picture = models.ImageField(
        upload_to= upload_folder,
        blank=True)

    #reputation = models.IntegerField(default=0)
    #language = models.CharField(max_length=5, default='en')
    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = u'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d':no_picture, 's':'256'})
                    )
                return gravatar_url
        except Exception, e:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

   

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Parcels(models.Model):
    id = models.IntegerField(primary_key=True)
    blockid = models.CharField(max_length=80,null=True,blank=True)
    sectcode = models.CharField(max_length=80,null=True,blank=True)
    parcel_no = models.CharField(max_length=50,null=True,blank=True)
    geom = models.MultiPolygonField(srid=4326)


    def __unicode__(self):
        return "%s %s" %(self.parcel_no, self.blockid)
    
    class Meta:
        verbose_name_plural = "Land Parcels" 

class Customer_detail(models.Model):
    user = models.OneToOneField(
        User,
        unique=True, 
        verbose_name=_('user'), 
        related_name='customer')
    customer_type = models.CharField(
        _('Customer Type'), 
        choices= choices_customer_type, 
        max_length= 54, 
        blank= True, 
        null=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        blank=True,
        null=True
        )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        blank=True,
        null=True
       )
    id_no = models.CharField(
        _('ID No'),
        max_length=255,
        blank=True,
        null=True
        )   
    phone_no = models.CharField(
        _('Phone no:'), 
        max_length=255, 
        blank=True, 
        null=True
       )      
    email = models.EmailField(
        _('Email'),
        max_length=254,
        blank=True,
        null=True
        )
    address = models.CharField(
        _('Postal Code'),
        max_length=255,
        blank=True,
        null=True
        )
    picture = models.ImageField(
        upload_to= upload_folder,
        blank=True)
    town = models.CharField(
        _('town'),
        choices=choices_towns,
        max_length=255,
        blank=True,
        null=True
        )

    def __unicode__(self):
        return '%s' % (self.first_name)

	class Meta:
	    ordering = ('first_name' )
	    verbose_name_plural = "Customer_detail"
        order_with_respect_to = 'first_name'

#Customer Business Profile   
class Business_profile(models.Model):

    """Business Details """

    user = models.ForeignKey(
        User)
    business_name = models.CharField(
        max_length=254,
        null=True
       )
    business_no = models.CharField(      
        max_length=50,
        blank=True,
        null=True)
    business_email = models.EmailField(
        _('Business Email'),
        max_length=254,
        blank=True,
        null=True
        )
    business_phone_no = models.CharField(
        _('Business Phone No'),
        max_length=255,
        blank=True,
        null=True
       )
    business_address = models.CharField( 
        _('Business Address'),       
        max_length=10,
        blank=True,
        null=True
        )
    parcel_no = models.CharField(      
        max_length=50,
        blank=True,
        null=True)
    business_form = models.CharField(
        _('Business Form'), 
        max_length= 25, 
        choices=choices_business_form, 
        null=True, 
        blank=True 
        )
    business_type = models.CharField(
        _('Business Type'),  
        max_length= 256, 
        choices=choices_business_type, 
        null=True, 
        blank=True
       )
    business_no_employees = models.CharField(
        _('Business No. Employees'),
        choices=choices_no_employees,
        max_length=255,
        blank=True,
        null=True
        )
    business_class = models.CharField(
        _('Business Class'),
        choices=choices_business_class,
        max_length=255,
        blank=True,
        null=True
       )
    business_category = models.CharField(
        _('Businenss Category'),
        choices=choices_business_category, 
        max_length=255, 
        blank=True, 
        null=True
        )
    business_scope = models.CharField(
        _('Business Scope'),
        choices=choices_business_scope, 
        max_length=255, 
        blank=True, 
        null=True)
    business_town = models.CharField(
        _('Business Town'),
        choices=choices_towns,
        max_length=255,
        blank=True,
        null=True
        )
    business_street = models.CharField(
        _('Business Street'),
        choices=choices_streets,
        max_length=255,
        blank=True,
        null=True
       )
    business_building = models.CharField(
        _('Business Buildings'),
        max_length=255,
        blank=True,
        null=True
        )
    business_zone = models.CharField(
        _('Business Zone'),
        choices=choices_zones,
        max_length=255,
        blank=True,
        null=True
        )
    business_compliance = models.BooleanField(
        _('Business Compliance'),
        max_length=10,
        default = False)
    business_profile = models.TextField(
        _('Business Profile'),
        null=True,
        blank=True)
    geom = models.PointField(srid=4326)  
    
    objects = models.GeoManager()
    

    def __unicode__(self):
        return '%s %s %s %s %s' % (self.business_name, self.business_zone, self.business_address, self.business_building, self.business_town)

    class Meta:
        ordering = ('business_name','business_zone', 'business_address','business_town', )
        verbose_name_plural = "Business Profiles"
        #order_with_respect_to = 'business_type'
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

#Customer Business, Building rents & Land rates Payments 

class Customer_payment(models.Model):

    """Business Customer Payments"""
    user = models.OneToOneField(User)

    #Payment method:Mpesa Bank or Cash
    payment_mode = models.CharField(
        _('Payment Mode'),
        choices = choices_payment_mode, 
        max_length=255, 
        blank=True, 
        null=True, 
        help_text=_('payment mode'))
    payment_code = models.CharField(
        _('Payment Code'), 
        max_length=255, 
        blank=True, 
        null=True, 
        help_text=_('payment code'))
    payment_period = models.CharField(
        max_length=10, 
        choices=PERIODS)  
    registration_date = models.DateField(
        _('Registration Date'), 
        auto_now=True, 
        #auto_now_add=True, 
        #default= datetime.now().strftime("%d.%m.%Y"),
        null=True, 
        blank=True, 
        help_text=_('registration date'))   
    #Business
    business_name = models.CharField(
        _('Business Name'), 
        max_length=255,
        blank=True, 
        null=True,
        help_text=_('name of the responsible organization'))
    business_rate= models.FloatField(
        _('Business Rates'), 
        null=True, 
        blank=True, 
        help_text=_('business rates'))
    #Business Permit
    business_permit_cost = models.FloatField(
        _('Business Permit Cost'), 
        null=True, 
        blank=True, 
        help_text=_('permit cost'))
    business_last_payment = models.DateField(
        _('Last Payment'), 
        auto_now=False, 
        auto_now_add=False, 
        max_length=255, 
        blank=True, 
        null=True, 
        help_text=_('last payment date'))
    business_next_payment = models.DateField(
        _('Next Payment'),
        auto_now=False, 
        auto_now_add=False, 
        max_length=255,
        blank=True, 
        null=True, 
        help_text=_('next payment date'))
    business_inspection_date = models.DateField(
        _('Inspection Date'), 
        auto_now=False,
        auto_now_add=False, 
        max_length=255, 
        blank=True, 
        null=True,
        help_text=_('Inspection Date'))
    permits = models.ForeignKey("Business_permit", null=True, blank=True)

    def __unicode__(self):
        return '%s %s' % ( self.business_name, self.payment_mode)

    class Meta:
        ordering = ('business_name',)
        verbose_name_plural = "Customer Payments Account"
        #order_with_respect_to = 'customer_detail'


class Business_permit(models.Model):
    user = models.OneToOneField(User)
    business_profile = models.ForeignKey(Business_profile,null=True)
    dateapplied = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return "%s" %(self.business_profile)

class Locations(models.Model):
    kenya_field = models.FloatField()
    kenya_id = models.FloatField()
    number = models.IntegerField()
    province_b = models.CharField(max_length=12)
    class1 = models.IntegerField()
    district_b = models.CharField(max_length=12)
    class2 = models.IntegerField()
    division_b = models.CharField(max_length=22)
    class3 = models.IntegerField()
    location_b = models.CharField(max_length=24)
    class4 = models.IntegerField()
    subloc_b = models.CharField(max_length=22)
    males = models.IntegerField()
    females = models.IntegerField()
    total = models.IntegerField()
    househds = models.IntegerField()
    pop_km2 = models.FloatField()
    hh_km2 = models.FloatField()
    av_hhs = models.FloatField()
    arekm2 = models.FloatField()
    dis = models.IntegerField()
    areakmsq = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __unicode__(self):
        return '%s %s %s ' % (self.division_b, self.location_b, self.subloc_b)

    class Meta:
        verbose_name_plural = "Bungoma Locations"

class County(models.Model):
    name2 = models.CharField(max_length=25)
    count = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __unicode__(self):
        return '%s' % (self.name2)

    class Meta:
        verbose_name_plural = "Bungoma County"
