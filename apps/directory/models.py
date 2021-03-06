import datetime
import random
from imagekit.models import ImageModel

from django.db import models
from django.db import backend
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from django.core import serializers

from directory.templatetags.my_slugify import my_slugify

from django.template.defaultfilters import slugify


def rating_random():
    return random.choice([3.0, 3.5, 4.0])

def short_description(self):
    """ returns slice of desc """
    try:
        if len(self.description) > 100:
            short = "%s..." % self.description[:100]
        else:
            short = self.description
        return short
    except Exception, err:
        return ''
short_description.short_description = 'Desc'
short_description.admin_order_field = 'description'


class Region(models.Model): # Europe, Australia etc
    name = models.CharField('Region name', max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Country(models.Model): # Germany, UK etc
    name = models.CharField('Country name', max_length=50, unique=True)
    region = models.ForeignKey(Region, related_name='region_countries')
    slug = models.SlugField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.country', (), {
            'slug': self.slug,
        })

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "countries"


class CountryDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    short_description = short_description
    country = models.ForeignKey(Country)
    site = models.ForeignKey(Site)
    objects = models.Manager()
    current_site_only = CurrentSiteManager('site')


    def __unicode__(self):
        return self.description


class State(models.Model):
    name = models.CharField('state name', max_length=20, unique=True)
    usps_name = models.CharField('USPS 2 letters state codename', max_length=2, unique=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.usps_name)

    class Meta:
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.state', (), {
            'state_usps_name': str(self.usps_name.lower()),
        })

class State2(State):
    class Meta:
        proxy = True

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.state2', (), {
            'state_usps_name': str(self.usps_name.lower()),
        })


class StateDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    short_description = short_description
    state = models.ForeignKey(State)
    site = models.ForeignKey(Site)
    objects = models.Manager()
    current_site_only = CurrentSiteManager('site')

    def __unicode__(self):
        return self.description

class StateDescription2(models.Model):
    description = models.TextField(blank=True, null=True)
    short_description = short_description
    state = models.ForeignKey(State2)
    site = models.ForeignKey(Site)
    objects = models.Manager()
    current_site_only = CurrentSiteManager('site')

    def __unicode__(self):
        return self.description

class City(models.Model):
    name = models.CharField('City name', max_length=50)
    state = models.ForeignKey(State, blank=True, null=True) # US state
    country = models.ForeignKey(Country, related_name='country_cities', blank=True, null=True) # World country

    class Meta:
        verbose_name_plural = "cities"
        ordering = ['state','name']
        unique_together = ('state', 'name')

    def __unicode__(self):
        if self.state:
            return '%s, %s' % (self.name, self.state.usps_name)
        if self.country:
            return '%s, %s' % (self.name, self.country.name)
        return self.name

    def state_name(self):
        return self.state
    state_name.short_description = 'State'
    state_name.admin_order_field = 'state'

    def country_name(self):
        return self.country
    country_name.short_description = 'Country'
    country_name.admin_order_field = 'country'

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.city', (), {
            'city_id': str(self.id),
            'city_urlsafe_name': str(my_slugify(self.name.lower())),
        })



class OpenClubsFromCurrentSiteManager(models.Manager):
    def get_query_set(self):
        return super(OpenClubsFromCurrentSiteManager, self).get_query_set().filter(sites__id__exact=settings.SITE_ID, is_closed=False)


class SearchManager(models.Manager):
    """ full text search manager """
    def __init__(self, fields):
        super(SearchManager, self).__init__()
        self._search_fields = fields

    def get_query_set(self):
        return SearchQuerySet(self.model, self._search_fields)

    def search(self, query):
        return self.get_query_set().search(query)

class OpenHookupsWhichPublishedManager(models.Manager):
    def get_query_set(self):
        return super(OpenHookupsWhichPublishedManager, self).get_query_set().filter(sites__id__exact=settings.SITE_ID, datetime_of_publish__range=[datetime.date(1900, 1, 1),datetime.date.today()])

class Hookup(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField('Street address', max_length=100, blank=True)
    state = models.ForeignKey(State2, blank=True, null=True, related_name = 'hookups')
    city = models.ForeignKey(City, blank=True, null=True, related_name = 'hookups')
    date_of_publish = models.DateField(default=datetime.date.today)
    datetime_of_publish = models.DateTimeField(default=datetime.datetime.today)
    age =  models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    body_art =  models.CharField(max_length=100)
    diet =  models.CharField(max_length=100)
    dislikes =  models.CharField(max_length=100)
    drinks =  models.CharField(max_length=100)
    drugs =  models.CharField(max_length=100)
    education =  models.CharField(max_length=100)
    ethnicity =  models.CharField(max_length=100)
    eye_color =  models.CharField(max_length=100)
    facial_hair =  models.CharField(max_length=100)
    fears =  models.CharField(max_length=100)
    hair =  models.CharField(max_length=100)
    hiv_hsv_hpv =  models.CharField(max_length=100)
    interests =  models.CharField(max_length=100)
    kids_have =  models.CharField(max_length=100)
    kids_want =  models.CharField(max_length=100)
    likes =  models.CharField(max_length=100)
    native_language =  models.CharField(max_length=100)
    occupation =  models.CharField(max_length=100)
    personality =  models.CharField(max_length=100)
    pets =  models.CharField(max_length=100)
    politics =  models.CharField(max_length=100)
    religion =  models.CharField(max_length=100)
    resembles =  models.CharField(max_length=100)
    smokes =  models.CharField(max_length=100)
    zodiac =  models.CharField(max_length=100)

    sites = models.ManyToManyField(Site)

    # managers
    objects = models.Manager()
    # objects = SearchManager(('name', 'description', 'address', 'phone', 'email', 'homepage'))
    current_site_only = CurrentSiteManager('sites')
    published_only = OpenHookupsWhichPublishedManager()
    short_description = short_description


    class Meta:
        ordering = ['title']
        # ordering = ['id']

    def __unicode__(self):
        return self.title

    def description_length(self):
        return len(self.description)
    description_length.short_description = 'Length'

    def country_name(self):
        return self.city.country.name
    country_name.short_description = 'Country'
    country_name.admin_order_field = 'city__country'

    def state_name(self):
        return self.state
    state_name.short_description = 'State'
    state_name.admin_order_field = 'state'

    def city_name(self):
        return self.city.name
    city_name.short_description = 'City'
    city_name.admin_order_field = 'city'

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.hookup', (), {
            'hookup_id': int(self.id),
            'hookup_urlsafe_title': str(my_slugify(self.title)) if my_slugify(self.title) else 'index',
        })




class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    address = models.CharField('Street address', max_length=100, blank=True)
    state = models.ForeignKey(State, blank=True, null=True, related_name = 'clubs')
    city = models.ForeignKey(City, blank=True, null=True, related_name = 'clubs')
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField('e-mail', blank=True)
    homepage = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    RATING_CHOISES = (
        (0.5, 0.5),
        (1, 1),
        (1.5, 1.5),
        (2, 2),
        (2.5, 2.5),
        (3, 3),
        (3.5, 3.5),
        (4, 4),
        (4.5, 4.5),
        (5, 5),
    )
    rating = models.FloatField(choices=RATING_CHOISES, default=rating_random)
    date_of_review = models.DateField(default=datetime.date.today)
    is_closed = models.BooleanField( default=False )
    sites = models.ManyToManyField(Site)
    owner = models.ForeignKey(User, null=True, blank=True)
    # managers
    objects = models.Manager()
    # objects = SearchManager(('name', 'description', 'address', 'phone', 'email', 'homepage'))
    current_site_only = CurrentSiteManager('sites')
    open_only = OpenClubsFromCurrentSiteManager()
    full_text = SearchManager(('name', 'description', 'address', 'phone', 'email', 'homepage'))
    short_description = short_description

    class Meta:
        ordering = ['name']
        # ordering = ['id']

    def __unicode__(self):
        return self.name

    def description_length(self):
        return len(self.description)
    description_length.short_description = 'Length'

    def country_name(self):
        return self.city.country.name
    country_name.short_description = 'Country'
    country_name.admin_order_field = 'city__country'

    def state_name(self):
        return self.state
    state_name.short_description = 'State'
    state_name.admin_order_field = 'state'

    def city_name(self):
        return self.city.name
    city_name.short_description = 'City'
    city_name.admin_order_field = 'city'

    @models.permalink
    def get_absolute_url(self):
        return ('directory.views.club', (), {
            'club_id': int(self.id),
            'club_urlsafe_title': str(my_slugify(self.name)),
        })
    def homepage_url(self):
        """ returns html formatted homepage url """
        return "<a href='%(url)s' target='_blank'>%(url)s</a>" % {"url": self.homepage}
    homepage_url.allow_tags = True
    homepage_url.admin_order_field = 'homepage'

    def all_sites(self):
        sites_ = ",".join([s.name for s in self.sites.all()])
        # another way is return site domain. just change s.name with s.domain
        return sites_
    all_sites.short_description = 'Published on'

    def save(self, create_revision=False, *args, **kwargs):
        """checks the owner of club, if owner changed saves event to the ClubCapture table"""

        if self.id is not None:
            from tapes.models import ClubCapture
            if self.owner:
                if Club.objects.get(id=self.id).owner != self.owner:
                    capture = ClubCapture()
                    capture.user = self.owner
                    capture.club = self
                    capture.save()
            else:
                # admin removes owner
                self.email = ''
        super(Club, self).save(*args, **kwargs)

        if create_revision:
            from reversion.models import ClubReversion
            # get previous revision
            prev_revisions = ClubReversion.objects.filter(club=self).order_by("-created")
            prev_data = ""
            if prev_revisions.count() > 0:
                prev_data = prev_revisions[0].serialized_data

            # get current object serialization data
            current_data = serializers.serialize("json", [self])
            if prev_data != current_data:
                # print "club changed. save revision and need revision."
                rev = ClubReversion()
                rev.club = self
                rev.serialized_data = current_data
                rev.save()



class Photo(ImageModel):
    original_image = models.ImageField(upload_to='photos')
    club = models.ForeignKey(Club)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'directory.specs'
        cache_dir = 'resized'
        image_field = 'original_image'


class Photo2(ImageModel):
    original_image = models.ImageField(upload_to='photos')
    hookup = models.ForeignKey(Hookup)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'directory.specs'
        cache_dir = 'resized'
        image_field = 'original_image'


class SearchQuerySet(models.query.QuerySet):
    """full text search for clubs
    """
    def __init__(self, model=None, fields=None, using=None, query=None):
        super(SearchQuerySet, self).__init__(model=model, using=using, query=query)
        self._search_fields = fields

    def search(self, query):
        meta = self.model._meta

        # Get the table name and column names from the model
        # in `table_name`.`column_name` style
        columns = [meta.get_field(name, many_to_many=False).column
                   for name in self._search_fields]
        full_names = ["%s.%s" % (connection.ops.quote_name(meta.db_table),
                      connection.ops.quote_name(column))
                      for column in columns]

        # Create the MATCH...AGAINST expressions
        fulltext_columns = ", ".join(full_names)
        match_expr = ("MATCH(%s) AGAINST (%%s)" % fulltext_columns)
        # only current site clubs
        # Add the extra SELECT and WHERE options
        return self.filter(sites__id__exact=settings.SITE_ID).extra(where=[match_expr], params=[query])
