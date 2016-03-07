#Customer Building Permit Profile

class Building_profile(models.Model):

    """Fully featured Building Profile: Building Details """

    customer_detail = models.ForeignKey(User)
    project_type = models.CharField(
        _('Project Type'),
        choices=choices_project_type,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('type of project'))
    building_name = models.CharField(
        _('Building Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('name of the responsible organization/building'))
    building_profile = models.TextField(_('Building Profile'), null=True, blank=True, help_text=_('introduce your building'))
    building_use = models.CharField(
        _('Building Use'),
        choices=choices_building_use,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building use'))
    building_type = models.CharField(_('Building Type'),choices=choices_building_type, max_length=254, null=True, blank=True, help_text=_('building type'))
    building_class = models.CharField(
        _('Building Class'),
        choices=choices_building_class,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building class'))
    building_category = models.CharField(_('Building Category'),choices=choices_building_category, max_length=255, blank=True, null=True, help_text=_(
        'building category'))
    building_state = models.CharField(_('Building Scope'),choices=choices_building_inspectionstate, max_length=255, blank=True, null=True, help_text=_(
        'building state'))
    building_rates = models.CharField(
        _('Building Rates'),
        choices=choices_building_rates,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building rates'))
    building_rent_metresq = models.FloatField(
        _('Building Rent/Metre Sq'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building rent/metre sq'))
    building_town_location = models.CharField(
        _('Building Town'),
        choices=choices_towns,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building physical town location'))
    building_street_location = models.CharField(
        _('Building Street'),
        max_length=255,
        choices=choices_streets,
        blank=True,
        null=True,
        help_text=_('physical town location street'))
    building_manager = models.CharField(
        _('Building Manager'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building manager'))
    building_zone = models.CharField(
        _('Building Zone'),
        choices=choices_zones,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building zone'))
    building_address = models.CharField( 
        _('Building Address'),       
        max_length=3,
        blank=True,
        null=True,
        help_text=_('building physical address'))
    building_phone_no = models.CharField(
        _('Building Phone No'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('building phone no'))
    building_registration_date = models.DateField(
        _('Building Registration Date'),
        auto_now=True,
        auto_now_add=False,
        null=True,
        #default= datetime.now().strftime("%d.%m.%Y"),
        help_text=_('building registration date'))
    building_inspection_date = models.DateField(
        _('Building Inspection Date'),
        auto_now= True,
        auto_now_add=False,
        null=True,
        help_text=_('building inspection date'))
    building_location = gis_models.PointField(u"longitude/latitude", srid=4326, geography=True, blank=True, null=True)
    gis = gis_models.GeoManager()
    #Upload Files/Documents: Building Permit
    #Copy of Certified Site Plan
    #Signed Application Form
    #Building Plan I & IV

    

    def __unicode__(self):
        return '%s %s %s %s %s' % (self.building_use, self.building_class, self.building_zone, self.building_type, self.building_street_location)

    class Meta:
        ordering = ('building_use','building_rates', 'building_rent_metresq','building_zone', )
        verbose_name_plural = "Building Profiles"
        #order_with_respect_to = 'building_class'


class Land_rate(models.Model):
    owner = models.ForeignKey(User)
    landrates_number = models.CharField(max_length=8)

    def __unicode__(self):
        return self.landrates_number

class Building_permit(models.Model):
    owner = models.ForeignKey(User)
    buildingpermit_number = models.CharField(max_length=8)

    def __unicode__(self):
        return self.buildingpermit_number

#Customer Land Parcels Profile

class Land_profile(models.Model):

    """Fully featured Land Profile: Parcel Details """

    customer_detail = models.ForeignKey(User)
    parcel_use = models.CharField(
        _('Parcel Use'),
        choices=choices_parcel_use,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('usage of the land parcel'))
    parcel_profile = models.TextField(_('Parcel Profile'), max_length=254, null=True, blank=True, help_text=_('About the land parcel'))
    parcel_registration_id = models.CharField(
        _('Parcel Registration ID'),
        choices=choices_towns,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel reg. id'))
    parcel_zone = models.CharField(
        _('Parcel Zone'),
        choices=choices_zones,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel zone'))
    parcel_size= models.FloatField(_('Parcel Size:Acres'), max_length=255, blank=True, null=True, help_text=_(
        'size of the land parcel'))
    parcel_town_location = models.CharField(_('Parcel Location Town'),choices=choices_towns, max_length=255, blank=True, null=True, help_text=_(
        'parcel town location'))    
    parcel_rates_no= models.CharField(
        _('Parcel Rates No'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel rates no'))
    parcel_rates= models.CharField(
        _('Parcel Rates '),
        choices= choices_parcel_rates,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel rates '))
    parcel_location_name = models.CharField(
        _('Parcel Location Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel location'))
    parcel_category = models.CharField(
        _('Parcel Category'),
        choices=choices_parcel_category,
        max_length=255,
        blank=True,
        null=True,
        help_text=_('parcel category'))
    parcel_class = models.CharField( 
        _('Parcel Class'),
        choices=choices_parcel_class,       
        max_length=30,
        blank=True,
        null=True,
        help_text=_('parcel class'))
    parcel_location = gis_models.PolygonField(srid=4326, geography=True, blank=True, null=True)
    gis = gis_models.GeoManager()

    def __unicode__(self):
        return '%s %s %s %s %s' % (self.parcel_use, self.parcel_class, self.parcel_zone, self.parcel_size, self.parcel_town_location)

    class Meta:
        ordering = ('parcel_use','parcel_zone', 'parcel_location','parcel_category', )
        verbose_name_plural = "Land Profiles"
        order_with_respect_to = 'customer_detail'


#Views.py

@login_required
def land_portal(request):
    form = LandProfilesForm
    if request.POST:
        form = LandProfilesForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return HttpResponseRedirect(reverse("building_portal"))
    return render_to_response("permit_portal/land_portal.html", locals(), context_instance=RequestContext(request))


@login_required
def building_portal(request):
    form = BuildingProfilesForm
    if request.POST:
        form = BuildingProfilesForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            return HttpResponseRedirect(reverse("business_portal"))
    return render_to_response("permit_portal/building_portal.html", locals(), context_instance=RequestContext(request))

