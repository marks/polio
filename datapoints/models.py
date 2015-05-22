from datetime import datetime

from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords
from jsonfield import JSONField

class Source(models.Model):
    source_name = models.CharField(max_length=55,unique=True)
    source_description = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return unicode(self.source_name)

    class Meta:
        db_table = 'source'

class CacheJob(models.Model):

    date_attempted = models.DateTimeField(default=datetime.now())
    date_completed = models.DateTimeField(null=True)
    is_error = models.BooleanField()
    response_msg = models.CharField(max_length=255)

    class Meta:
        db_table = 'cache_job'
        ordering = ('-date_attempted',)


class Indicator(models.Model):

    short_name = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='name',unique=True,max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'
        ordering = ('name',)


class IndicatorAbstracted(models.Model):

    description = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    bound_json = JSONField()

    def __unicode__(self):
        return unicode(self.slug)

    class Meta:
        db_table = 'indicator_abstracted'

class UserAbstracted(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.BooleanField()
    email = models.CharField(max_length=255)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    group_json = JSONField()
    region_permission_json = JSONField()

    class Meta:
        db_table = 'user_abstracted'



class CalculatedIndicatorComponent(models.Model):
    '''
    the indicator is for example "pct missed due to refusal," the component
    "total missed" and calculation is "denominator"
    '''

    indicator = models.ForeignKey(Indicator, related_name='indicator_master')
    indicator_component = models.ForeignKey(Indicator,related_name='indicator_component')
    calculation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.indicator.name)

    class Meta:
        db_table = 'calculated_indicator_component'

class IndicatorBound(models.Model):
    '''
    If a Low / High reporesents an error, or a particular grouping of values
    i.e. (good, ok, bad) we have how ever many rows for an indicator as their
    are groupings for that indicator's values.
    '''

    indicator = models.ForeignKey(Indicator)
    mn_val = models.FloatField(null=True)
    mx_val = models.FloatField(null=True)
    bound_name = models.CharField(max_length=255)
    direction = models.IntegerField(default=1)


    def __unicode__(self):
        return unicode(self.bound_name.name)

    class Meta:
        db_table = 'indicator_bound'



class Office(models.Model):

    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'office'

        permissions = (
            ('view_office', 'View office'),
        )

class RegionType(models.Model):

    name = models.CharField(max_length=55, unique=True)

    def __unicode__(self):
        return unicode(self.name)


    class Meta:
        db_table = 'region_type'

class Region(models.Model):

    name = models.CharField(max_length=255,unique=True)
    region_code = models.CharField(max_length=255, unique=True)
    region_type = models.ForeignKey(RegionType)
    office = models.ForeignKey(Office)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    slug = AutoSlugField(populate_from='name',max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source)
    is_high_risk = models.BooleanField(default=False)
    parent_region = models.ForeignKey("self",null=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:

        db_table = 'region'
        unique_together = ('name','region_type','office')


class RegionPolygon(models.Model):

    region = models.ForeignKey(Region,unique=True)
    shape_len  = models.FloatField()
    shape_area = models.FloatField()
    polygon = JSONField()

    class Meta:
        db_table = 'region_polygon'

class RegionHeirarchy(models.Model):

    region_id = models.IntegerField()
    contained_by_region_id = models.IntegerField()
    region_type_id = models.IntegerField()

    class Meta:
        db_table = 'region_heirarchy_cache'
        managed = False

class CampaignType(models.Model):

    name = models.CharField(max_length=55)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'campaign_type'

class Campaign(models.Model):

    office = models.ForeignKey(Office)
    campaign_type = models.ForeignKey(CampaignType)
    start_date = models.DateField()
    end_date = models.DateField()
    slug = AutoSlugField(populate_from='get_full_name',unique=True)
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.slug)

    def get_full_name(self):
        return unicode(self.office.name + '-' + unicode(self.start_date))

    class Meta:
        db_table = 'campaign'
        ordering = ('-start_date',)
        unique_together = ('office','start_date')

class DataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    value = models.FloatField()
    note = models.CharField(max_length=255,null=True,blank=True)
    changed_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now=True)
    source_datapoint = models.ForeignKey('source_data.SourceDataPoint')
    cache_job = models.ForeignKey(CacheJob,default=-1)


    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'
        unique_together = ('indicator','region','campaign')
        ordering = ['region', 'campaign']
        permissions = (
            ('view_datapoint', 'View datapoint'),
        )

class DataPointEntry(DataPoint):
    """Proxy subclass of DataPoint, for use only in API
    methods used by the manual data entry form. This model
    stores records of all changes in a separate DB table.
    """

    history = HistoricalRecords()

    class Meta:
        proxy = True


class Responsibility(models.Model):

    user = models.ForeignKey('auth.User')
    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)

    class Meta:
        db_table = 'responsibility'
        ordering = ('indicator',)
        unique_together = ('user','indicator','region')


class DataPointAbstracted(models.Model):

    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    indicator_json = JSONField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'datapoint_abstracted'
        unique_together = ('region','campaign')

class DataPointComputed(models.Model):

    region_id = models.IntegerField()
    campaign_id = models.IntegerField()
    indicator_id = models.IntegerField()
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'datapoint_with_computed'
        unique_together = ('region_id','campaign_id','indicator_id')

class AggDataPoint(models.Model):

    region_id = models.IntegerField()
    campaign_id = models.IntegerField()
    indicator_id = models.IntegerField()
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'agg_datapoint'
        unique_together = ('region_id','campaign_id','indicator_id')


class ExpectedData(models.Model):

    region = models.ForeignKey(Region,related_name='ex_child_region')
    campaign = models.ForeignKey(Campaign)
    parent_region = models.ForeignKey(Region,related_name='ex_parent_region')

    class Meta:
        db_table = 'expected_data'
        unique_together = ('region','campaign')


class ReconData(models.Model):

    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    indicator = models.ForeignKey(Indicator)
    target_value = models.FloatField()
    is_raw = models.BooleanField()
    success_flag = models.BooleanField()

    class Meta:
        db_table = 'recon_data'
        unique_together = ('region','campaign','indicator')


class BadData(models.Model):

    datapoint = models.ForeignKey(DataPoint)
    document = models.ForeignKey('source_data.Document')
    error_type = models.CharField(max_length=55)
    cache_job = models.ForeignKey(CacheJob)

    class Meta:
        db_table = 'bad_data'


class RegionPermission(models.Model):
    '''
    Individual Users must be assigned regional permissions.  If i am assigned
    a region, I will be able to view all of its children recursively.  The
    default for a user

    Regional permissions must also specify the read/write flag.  So for instance
    as a Cluster Supervisor in Sokoto, I should be able to see all of Nigeria's
    data, but i only should be able to insert / edit data for Sokoto. Thus i
    would have two records, one that says "i can read all of NG", and one that
    says, "i can write data in Sokoto."
    '''

    user = models.ForeignKey('auth.User')
    region = models.ForeignKey(Region)
    read_write = models.CharField(max_length=1)

    class Meta:
        db_table = 'region_permission'
        unique_together = ('user','region','read_write')


class IndicatorPermission(models.Model):
    '''
    All users can read all indicators, but permission to update/insert/delete
    are assigned to a group.  For instance, the security_analyst role, will be
    permitted to edit data on the security indicators, but not for instance
    OPV supply indicators.
    '''

    group = models.ForeignKey('auth.Group')
    indicator = models.ForeignKey(Indicator)

    class Meta:
        db_table = 'indicator_permission'
        unique_together = ('group','indicator')


class UserGroup(models.Model):
    '''
    '''

    user = models.ForeignKey('auth.User')
    group = models.ForeignKey('auth.Group')

    class Meta:
        db_table = 'auth_user_groups'
        managed = False

class ColumnAttributes(models.Model):

    table_name = models.CharField(max_length=255)
    column_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    display_on_table_flag = models.BooleanField()

    class Meta:
        db_table = 'column_attributes'
