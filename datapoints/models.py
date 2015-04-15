from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
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
    shape_file_path  = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    slug = AutoSlugField(populate_from='name',max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source)
    is_high_risk = models.BooleanField(default=False)
    parent_region = models.ForeignKey("self",null=True)

    def __unicode__(self):
        return unicode(self.name)

    def get_all_children(self):

        r = []

        for c in Region.objects.filter(parent_region=self):
            # r.append(c.get_all_children())
            r.append(c)

        second_leaf = Region.objects.filter(parent_region__in=r)

        r.extend(second_leaf)

        return r

    class Meta:

        db_table = 'region'
        unique_together = ('name','region_type','office')
        ordering = ('name',)

        permissions = (
            ('view_region', 'View region'),
        )



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
        return unicode(self.office.name + '-' + unicode(self.start_date))


    def get_full_name(self):
        full_name = self.__unicode__()
        return full_name

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

class MissingMapping(models.Model):

    datapoint = models.ForeignKey(DataPoint)
    document = models.ForeignKey('source_data.SourceDataPoint')
    what_is_missing = models.CharField(max_length=255)

    class Meta:
        db_table = 'vw_missing_mappings'
        managed = False


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

class EntityType(models.Model):
    
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    default_sort_direction = models.NullBooleanField()
    content_type = models.ForeignKey(ContentType)

    class Meta:
        db_table = 'entity_type'
        ordering = ('name',)

class EntityFieldStyle(models.Model):
    table_weight = models.IntegerField(default=2)
    weight_form = models.IntegerField(default=2)

    class Meta:
        db_table = 'entity_field_style'

class EntityAllowedValuesTable(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_allowed_values_table'

class EntityAllowedValuesColumn(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_allowed_values_column'

class EntityFieldBasicAttributes(models.Model):

    field_style = models.ForeignKey(EntityFieldStyle)
    allowed_values_table = models.ForeignKey(EntityAllowedValuesTable)
    allowed_values_column = models.ForeignKey(EntityAllowedValuesColumn)

    class Meta:
        db_table = 'entity_field_attributes'

class EntityFieldBasicConstraints(models.Model):
    pattern = models.CharField(max_length=255)
    required = models.BooleanField()
    unique = models.BooleanField()

    class Meta:
        db_table = 'entity_field_basic_constraint'

class EntityFieldAttributeType(models.Model):
    string = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_field_attribute_type'

class EntityTypeAttributes(models.Model):
    default_sort_direction = models.IntegerField(default=1)

    class Meta:
        db_table = 'content_type_attributes'

class EntityFieldInputType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_field_input_type'

class EntityFieldDataType(models.Model):
    name = models.CharField(max_length=255)
    input_type = models.ForeignKey(EntityFieldInputType)

    class Meta:
        db_table = 'entity_field_data_type'

class EntityField(models.Model):
    
    name = models.CharField(max_length=255)
    ref = models.ForeignKey(ContentType)
    entity_type = models.ForeignKey(EntityType)
    description = models.CharField(max_length=1000)
    basic_attributes = models.ForeignKey(EntityFieldBasicAttributes)
    basic_constraints = models.ForeignKey(EntityFieldBasicConstraints)

    class Meta:
        db_table = 'entity_field'
        ordering = ('name',)

class EntityFieldDynamicAttribute(models.Model):
    ''' ex: sortable, searchable, filterable, editable, on_table '''
    name = models.CharField(max_length=255)
    is_default_sort = models.BooleanField()
    attribute_type = models.ForeignKey(EntityFieldAttributeType)
    basic_constraints = models.ForeignKey(EntityFieldBasicConstraints)

    class Meta:
        db_table = 'entity_field_dynamic_attribute'

class EntityFieldDynamicAttributeMapping(models.Model):
    dynamic_attribute = models.ForeignKey(EntityFieldDynamicAttribute)
    field = models.ForeignKey(EntityField)

    class Meta:
        db_table = 'entity_field_dynamic_attribute_mapping'

class EntityFieldDynamicConstraintRelation(models.Model):
    ''' ex: lt, gt, eq '''
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'entity_field_constraint_relation'

class EntityFieldDynamicConstraint(models.Model):
    ''' ex: min_date, int_min, within_geo_area, etc. '''
    name = models.CharField(max_length=255)
    constraint_type = models.ForeignKey(EntityFieldAttributeType)
    constraint_relation = models.ForeignKey(EntityFieldDynamicConstraintRelation)
    constraint_value_as_string_format = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_field_dynamic_constraint'

class EntityFieldDynamicConstraintMapping(models.Model):
    dynamic_constraint = models.ForeignKey(EntityFieldDynamicConstraint)
    field = models.ForeignKey(EntityField)
    value_as_string = models.CharField(max_length=255)

    class Meta:
        db_table = 'entity_field_dynamic_constraint_mapping'

