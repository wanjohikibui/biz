__author__ = 'alphabuddha'

from permit.forms import *
from permit.models import * 
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from vectorformats.Formats import Django, GeoJSON
from django.core.context_processors import csrf
from django.contrib.gis.geos import Point
import uuid
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.core import serializers
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth import logout
from django.contrib.auth import views

def our_story(request):
    return render_to_response("our_story.html", locals(), context_instance=RequestContext(request))

def product(request):
    return render_to_response("product.html", locals(), context_instance=RequestContext(request))

def services(request):
    return render_to_response("services.html", locals(), context_instance=RequestContext(request))

def map(request):
    return render_to_response("map.html", locals(), context_instance=RequestContext(request))

def map_admin(request):
    return render_to_response("map_admin.html", locals(), context_instance=RequestContext(request))

def impacts(request):
    return render_to_response("impacts.html", locals(), context_instance=RequestContext(request))

def contact_us(request):
    return render_to_response("contact_us.html", locals(), context_instance=RequestContext(request))

def info(request):
    return render_to_response("info.html", locals(), context_instance=RequestContext(request))

def analytics(request):
    return render_to_response("analytics.html", locals(), context_instance=RequestContext(request))

def dashboard(request):
    return render_to_response("dashboard.html", locals(), context_instance=RequestContext(request))

@api_view(['GET'])
def get_business(request):
    result = Business_profile.gis.all()
    data = serializers.serialize('json', result)
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    
@api_view(['GET'])
def business_filter(request):
    request_data = request.QUERY_PARAMS
    filtered_fields = request_data['fields']

    kwargs = {}

    if "business_form" in filtered_fields:
        kwargs['business_form'] = request_data['business_form']
    if "business_type" in filtered_fields:
        kwargs['business_type'] = request_data['business_type']
    if "business_compliance" in filtered_fields:
        kwargs['business_compliance'] = request_data['business_compliance']
    try:
        result = Business_profile.gis.filter(**kwargs)
        data = serializers.serialize('json', result)
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def application_portal(request):
    form = BusinessProfilesForm
    if request.method == 'POST':
        form = BusinessProfilesForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            cd = form.cleaned_data

            email_to = cd['email']
            subject = "{0} Update".format(cd['first_name'])
            message = "Applicant: {0}\n\n Your application has been received".format(
                cd['last_name'])
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email_to,])
            new_form.save()
            messages.success(request, 'Application Sent successfully')
            return HttpResponseRedirect(reverse("apply"))
        else:
            print form.errors
    else:
        form = BusinessProfilesForm()
    return render(request, 'apply.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'auth/signup.html', {'form': form})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = u'{0} has joined the network.'.format(user.username, user.username)
            #feed = Feed(user=user, post=welcome_post)
            #feed.save()
            return HttpResponseRedirect('/')
    else:
        return render(request, 'auth/signup.html', {'form': SignUpForm()})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def feeds(request):
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))

def mapping(request):
    return render_to_response("mapping.html", locals(), context_instance=RequestContext(request))

def home(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render(request, 'auth/login.html')
    #return render_to_response("portal/portal.html", locals(), context_instance=RequestContext(request))

@login_required
def network(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'core/network.html', {'users': users})

@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    return render(request, 'core/profile.html', {'page_user': page_user, 'page': 1})

@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.customer_type = form.cleaned_data.get('customer_type')
            user.profile.id_no = form.cleaned_data.get('id_no')
            user.profile.phone_no = form.cleaned_data.get('phone_no')
            user.email = form.cleaned_data.get('email')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.picture = form.cleaned_data.get('picture')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile was successfully edited.')
    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location,
            'customer_type': user.profile.customer_type,
            'id_no': user.profile.id_no,
            'phone_no': user.profile.phone_no,
            'address': user.profile.address,
            'picture': user.profile.picture,
            })
    return render(request, 'core/settings.html', {'form':form})

@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        pass
    return render(request, 'core/picture.html', {'uploaded_picture': uploaded_picture})

@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed.')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'core/password.html', {'form':form})

@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)    
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        return redirect('/settings/picture/?upload_picture=uploaded')
    except Exception, e:
        return redirect('/settings/picture/')

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except Exception, e:
        pass
    return redirect('/settings/picture/')



@login_required(login_url='/login/')
def index(request):    
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))

@login_required
def customer_portal(request):
    form = CustomerDetailsForm
    if request.POST:
        form = CustomerDetailsForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            messages.success(request, 'Details updated successfully.Now add business your details')
            record.save()
            return HttpResponseRedirect(reverse("business_portal"))
    return render_to_response("permit/customer_portal.html", locals(), context_instance=RequestContext(request))



@login_required
def business_portal(request):
    form = BusinessProfilesForm
    if request.POST:
        form = BusinessProfilesForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            messages.success(request, 'Application Sent successfully')
            return HttpResponseRedirect(reverse("business_portal"))
    return render_to_response("permit/business_portal.html", locals(), context_instance=RequestContext(request))


@login_required
def add_business_profile(request):

    if request.method == 'POST':
        form = businessForm(request.POST)
        if form.is_valid():
            new_point = Business_profile()
            cd = form.cleaned_data
            new_point.business_name = cd['business_name']
            new_point.business_no = cd['business_no']
            new_point.business_email = cd['business_email']
            new_point.business_phone_no = cd['business_phone_no']
            new_point.business_address = cd['business_address']
            new_point.parcel_no = cd['parcel_no']
            new_point.business_form = cd['business_form']
            new_point.business_type = cd['business_type']
            new_point.business_no_employees = cd['business_no_employees']
            new_point.business_class = cd['business_class']
            new_point.business_category = cd['business_category']
            new_point.business_scope = cd['business_scope']
            new_point.business_town = cd['business_town']
            new_point.business_street = cd['business_street']
            new_point.business_building = cd['business_building']
            new_point.business_zone = cd['business_zone']
            new_point.business_profile = cd['business_profile']
            #new_point.photo = cd['photo']
            coordinates = cd['coordinates'].split(',')
            new_point.geom = Point(float(coordinates[0]), float(coordinates[1]))
            new_point.user= request.user
            new_point.save()
            messages.success(request, 'Business profile updated successfully')
            
            return HttpResponseRedirect(reverse("payment_customer"))
        else:
            return HttpResponseRedirect(reverse("payment_customer"))

    else:
        form = businessForm()

    args = {}
    args.update(csrf(request))
    args['form'] = businessForm()
    #return render_to_response('temp/incidence.html', args)
    return render_to_response("permit/business.html", args)

@login_required
def permit(request):
    #business_no = Business_profile.objects.get(user=request.user).business_no
    #dateapplied = Business_profile.objects.get(user=request.user).dateapplied

    if request.method == 'POST':
        form = businesspermitForm(request.POST)
        if form.is_valid():
            permit= form.save(commit=False)
            permit.user= request.user            
            permit.save()
            messages.success(request, 'Business permit updated successfully')            
            return HttpResponseRedirect(reverse("/permit/"))
        else:
            return HttpResponseRedirect(reverse('/permit/'))
    else:
        form = businesspermitForm() 
        #form.fields["business_name"].queryset = Business_profile.objects.filter(user=request.user)       
    args = {}
    args.update(csrf(request))
    args['form'] = businesspermitForm()
    #return render_to_response('temp/incidence.html', args)
    return render_to_response("permit/permit.html", args)

@login_required
def create_permit(request):
    #user = request.user.get_full_name()
    if request.method == "POST":
        form = businesspermitForm(user=request.user)
        if form.is_valid():
            permit= form.save(commit=False)
            permit.user= request.user            
            permit.save()
            messages.success(request, 'Business permit updated successfully')            
            return HttpResponseRedirect(reverse("/permit/"))
        else:
            return HttpResponseRedirect(reverse('/permit/'))
            form.errors
        # Process form.
    else:
        form = businesspermitForm(user=request.user)
        # Get just the photos belonging to this user.

        #form.fields['user'].queryset = User.objects.filter(is_staff=True)
        #form.fields["business_name"].queryset = Business_profile.objects.filter(user=request.user)
 
    template_vars = RequestContext(request, {
        "form": form,
        "user": request.user
    })
    return render_to_response("permit/permit.html", template_vars)

@login_required
def payment_customer(request):
    business_form = Business_profile.objects.get(user=request.user).business_form
    business_type = Business_profile.objects.get(user=request.user).business_type
    business_no_employees = Business_profile.objects.get(user=request.user).business_no_employees
    business_class = Business_profile.objects.get(user=request.user).business_class
    business_category = Business_profile.objects.get(user=request.user).business_category
    business_scope = Business_profile.objects.get(user=request.user).business_scope
    business_town = Business_profile.objects.get(user=request.user).business_town
    business_street = Business_profile.objects.get(user=request.user).business_street
    business_zone = Business_profile.objects.get(user=request.user).business_zone
    #
   
    #Business   
    if business_form == "Sole Proprietorship":
        business_rate = 1
    if business_form  == "Patnership":
        business_rate = 2
    if business_form  == "Corporation":
        business_rate = 3
        #
    if business_type == "Retail Shops":
        business_rate = 1
    if business_type == "Alcohol Sales":
        business_rate = 2
    if business_type == "Cybers":
        business_rate = 3
        #
    if business_no_employees == "Less than 5":
        business_rate = 1
    if business_no_employees == "Less than 10":
        business_rate = 2
    if business_no_employees == "Less than 20":
        business_rate = 3
        #
    if business_class == "A":
        business_rate = 1
    if business_class == "B":
        business_rate = 2
    if business_class == "C":
        business_rate = 3
        #
    elif business_category == "Commmercial":
        business_rate = 1
    elif business_category == "NGO":
        business_rate = 2
    elif business_category == "Non Profit":
        business_rate = 3
        #
    elif business_scope == "Single":
        business_rate = 1
    elif business_scope == "Chain_Stores":
        business_rate = 2
    elif business_scope == "Franchise":
        business_rate = 3
        #
    elif business_town == "Bungoma":
        business_rate = 1
    elif business_town == "Webuye":
        business_rate = 2
    elif business_town == "Malakisi":
        business_rate = 3
        #
    elif business_street == "Street1":
        business_rate = 1
    elif business_street == "Street2":
        business_rate = 2
    elif business_street == "Street3":
        business_rate = 3
        #
    elif business_zone == "CBD":
        business_rate = 1
    elif business_zone == "Residential":
        business_rate = 2
    elif business_zone == "Industrial":
        business_rate = 3
    #

    if request.POST:
        form = CustomerPaymentsForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.owner = request.user
            record.save()
            return HttpResponseRedirect(reverse("generate_permit"))
    form = CustomerPaymentsForm(initial={"business_rate": business_rate, })
    return render_to_response("permit/payment_customer.html", locals(), context_instance=RequestContext(request))


@login_required
def generate_permit(request):
       
    #Businesses
    business_form = Business_profile.objects.get(user=request.user).business_form
    business_type = Business_profile.objects.get(user=request.user).business_type
    business_no_employees = Business_profile.objects.get(user=request.user).business_no_employees
    business_class = Business_profile.objects.get(user=request.user).business_class
    business_category = Business_profile.objects.get(user=request.user).business_category
    business_town = Business_profile.objects.get(user=request.user).business_town
    business_street = Business_profile.objects.get(user=request.user).business_street
    business_zone = Business_profile.objects.get(user=request.user).business_zone
    #Payments
    schedule = Customer_payment.objects.get(user=request.user).payment_period
    #Customer
    customer = Profile.objects.get(user=request.user)
    if request.POST:
        #
        #Business   
        if business_form == "Sole Proprietorship":
            business_rate = 1
        if business_form  == "Patnership":
            business_rate = 2
        if business_form  == "Corporation":
            business_rate = 3
            #
        if business_type == "Retail Shops":
            business_rate = 1
        if business_type == "Alcohol Sales":
            business_rate = 2
        if business_type == "Cybers":
            business_rate = 3
            #
        if business_no_employees == "Less than 5":
            business_rate = 1
        if business_no_employees == "Less than 10":
            business_rate = 2
        if business_no_employees == "Less than 20":
            business_rate = 3
            #
        if business_class == "A":
            business_rate = 1
        if business_class == "B":
            business_rate = 2
        if business_class == "C":
            business_rate = 3
            #
        elif business_category == "Commmercial":
            business_rate = 1
        elif business_category == "NGO":
            business_rate = 2
        elif business_category == "Non Profit":
            business_rate = 3
            #
        elif business_scope == "Single":
            business_rate = 1
        elif business_scope == "Chain_Stores":
            business_rate = 2
        elif business_scope == "Franchise":
            business_rate = 3
            #
        elif business_town == "Nyeri_Town":
            business_rate = 1
        elif business_town == "Karatina":
            business_rate = 2
        elif business_town == "Othaya":
            business_rate = 3
            #
        elif business_street == "Gakere":
            business_rate = 1
        elif business_street == "Kimathi":
            business_rate = 2
        elif business_street == "Outer_Ring":
            business_rate = 3
            #
        elif business_zone == "CBD":
            business_rate = 1
        elif business_zone == "Residential":
            business_rate = 2
        elif business_zone == "Industrial":
            business_rate = 3
        #
        #Payment Schedule
        if schedule == "Yearly":
            rate = 12
        if schedule == "Bi_annnual":
            rate = 6
        elif schedule == "Quarterly":
            rate = 4

        #Totals
        business_total = business_rate * rate

        #Permit
        #first_name = customer.first_name
        #last_name = customer.last_name
        license = str(uuid.uuid4().fields[-1])[:6]
        #record = Permits(permit_number=license, owner=request.user)
        #record.save()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="interim_license.pdf"'
        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
       
        business_string = "Business total: %s" % business_total
        #names = "%s %s" %(first_name, last_name)
        p.drawString(100, 100, "Interim permit.")        
        p.drawString(150, 150, business_string)
        #p.drawString(70, 70, names)
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
    return render_to_response("permit/interim.html", locals(), context_instance=RequestContext(request))
