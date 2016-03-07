__author__ = 'alphabuddha'

from django.forms import ModelForm
from .models import Customer_detail, Business_profile, Customer_payment, Business_permit
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from bizsystem.settings import ALLOWED_SIGNUP_DOMAINS

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

class CustomerDetailsForm(ModelForm):
    class Meta:
        model = Customer_detail
        exclude = ['user']

class BusinessProfilesForm(ModelForm):
    class Meta:
        model = Business_profile
        exclude = ['user', 'geom', 'business_compliance']

class CustomerPaymentsForm(ModelForm):
    class Meta:
        model = Customer_payment
        exclude = ['user']

class businesspermitForm(forms.Form):
    class Meta:
        model = Business_permit
        fields = ['business_profile']

    def __init__(self, user=None, **kwargs):
        super(businesspermitForm, self).__init__(**kwargs)
        if user:
            self.fields['business_profile'].queryset = Business_profile.objects.filter(user=user)

class businessForm(forms.Form):
    business_name = forms.CharField(max_length=50)
    business_no=forms.CharField(max_length=50)
    business_email = forms.EmailField(max_length=50)
    business_phone_no = forms.CharField(max_length=50, required=True)
    business_address = forms.CharField(max_length=50, required=True)
    parcel_no = forms.CharField(max_length=50, required=True)
    business_form = forms.ChoiceField(choices=choices_business_form) 
    business_type = forms.ChoiceField(choices=choices_business_type)
    business_no_employees = forms.ChoiceField(choices=choices_no_employees)
    business_class = forms.ChoiceField(choices=choices_business_class)
    business_category = forms.ChoiceField(choices=choices_business_category)
    business_scope = forms.ChoiceField(choices=choices_business_scope) 
    business_town = forms.ChoiceField(choices=choices_towns)
    business_street = forms.ChoiceField(choices=choices_streets)
    business_building = forms.CharField(max_length=50)
    business_zone = forms.ChoiceField(choices=choices_zones)
    business_profile = forms.CharField(widget = forms.Textarea, max_length=250,required=False)
    coordinates=forms.CharField(max_length=200, required=True)

    def clean(self):

        cleaned_data = self.cleaned_data

        business_name = cleaned_data.get("business_name")
        business_no = cleaned_data.get("price")
        business_email = cleaned_data.get("business_email")
        business_phone_no = cleaned_data.get("business_phone_no")
        business_address = cleaned_data.get("business_address")
        parcel_no = cleaned_data.get("parcel_no")
        business_form = cleaned_data.get("business_form")
        business_type = cleaned_data.get("business_type")
        business_no_employees = cleaned_data.get("business_no_employees")
        business_class = cleaned_data.get("business_class")
        business_category = cleaned_data.get("business_category")
        business_scope = cleaned_data.get("business_scope")
        business_town = cleaned_data.get("business_town")
        business_street = cleaned_data.get("business_street")
        business_building = cleaned_data.get("business_building")
        business_zone = cleaned_data.get("business_zone")
        business_profile = cleaned_data.get("business_profile")
        coordinates = cleaned_data.get("coordinates")
    

        return cleaned_data

class ProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=75,
        required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    customer_type = forms.ChoiceField(choices=choices_customer_type, required=False)
    id_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    picture = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'job_title', 'email', 'url', 'customer_type','id_no','phone_no','address','picture','location',]



class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Old password",
        required=True)

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="New password",
        required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        
def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError(u'Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))
        except Exception, e:
            raise ValidationError(u'Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))

def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 
        'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search', 
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'questions', 'articles', 'network',]
    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')

def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value or '/' in value:
        raise ValidationError('Enter a valid username.')

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=30,
        required=True,
        help_text='Usernames may contain <strong>alphanumeric</strong> , <strong> _ </strong> and <strong> . </strong> characters')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Confirm your password",
        required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}), 
        required=True,
        max_length=75)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password',]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords didn\'t match'])
        return self.cleaned_data