# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntityAllowedValuesTable'
        db.create_table('entity_allowed_values_table', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityAllowedValuesTable'])

        # Adding model 'EntityFieldInputType'
        db.create_table('entity_field_input_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldInputType'])

        # Adding model 'EntityType'
        db.create_table('entity_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_sort_direction', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityType'])

        # Adding model 'EntityFieldAttributeType'
        db.create_table('entity_field_attribute_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldAttributeType'])

        # Adding model 'EntityField'
        db.create_table('entity_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ref', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('entity_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityType'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('basic_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldBasicAttributes'])),
            ('basic_constraints', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldBasicConstraints'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityField'])

        # Adding model 'EntityFieldDynamicConstraintRelation'
        db.create_table('entity_field_constraint_relation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDynamicConstraintRelation'])

        # Adding model 'EntityFieldDynamicConstraintMapping'
        db.create_table('entity_field_dynamic_constraint_mapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dynamic_constraint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldDynamicConstraint'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityField'])),
            ('value_as_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDynamicConstraintMapping'])

        # Adding model 'EntityTypeAttributes'
        db.create_table('content_type_attributes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('default_sort_direction', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'datapoints', ['EntityTypeAttributes'])

        # Adding model 'EntityAllowedValuesColumn'
        db.create_table('entity_allowed_values_column', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityAllowedValuesColumn'])

        # Adding model 'EntityFieldDynamicConstraint'
        db.create_table('entity_field_dynamic_constraint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('constraint_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldAttributeType'])),
            ('constraint_relation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldDynamicConstraintRelation'])),
            ('constraint_value_as_string_format', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDynamicConstraint'])

        # Adding model 'EntityFieldBasicConstraints'
        db.create_table('entity_field_basic_constraint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('required', self.gf('django.db.models.fields.BooleanField')()),
            ('unique', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldBasicConstraints'])

        # Adding model 'EntityFieldDynamicAttributeMapping'
        db.create_table('entity_field_dynamic_attribute_mapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dynamic_attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldDynamicAttribute'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityField'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDynamicAttributeMapping'])

        # Adding model 'EntityFieldDynamicAttribute'
        db.create_table('entity_field_dynamic_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_default_sort', self.gf('django.db.models.fields.BooleanField')()),
            ('attribute_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldAttributeType'])),
            ('basic_constraints', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldBasicConstraints'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDynamicAttribute'])

        # Adding model 'EntityFieldStyle'
        db.create_table('entity_field_style', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table_weight', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('weight_form', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldStyle'])

        # Adding model 'EntityFieldDataType'
        db.create_table('entity_field_data_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('input_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldInputType'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldDataType'])

        # Adding model 'EntityFieldBasicAttributes'
        db.create_table('entity_field_attributes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityFieldStyle'])),
            ('allowed_values_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityAllowedValuesTable'])),
            ('allowed_values_column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.EntityAllowedValuesColumn'])),
        ))
        db.send_create_signal(u'datapoints', ['EntityFieldBasicAttributes'])


    def backwards(self, orm):
        # Deleting model 'EntityAllowedValuesTable'
        db.delete_table('entity_allowed_values_table')

        # Deleting model 'EntityFieldInputType'
        db.delete_table('entity_field_input_type')

        # Deleting model 'EntityType'
        db.delete_table('entity_type')

        # Deleting model 'EntityFieldAttributeType'
        db.delete_table('entity_field_attribute_type')

        # Deleting model 'EntityField'
        db.delete_table('entity_field')

        # Deleting model 'EntityFieldDynamicConstraintRelation'
        db.delete_table('entity_field_constraint_relation')

        # Deleting model 'EntityFieldDynamicConstraintMapping'
        db.delete_table('entity_field_dynamic_constraint_mapping')

        # Deleting model 'EntityTypeAttributes'
        db.delete_table('content_type_attributes')

        # Deleting model 'EntityAllowedValuesColumn'
        db.delete_table('entity_allowed_values_column')

        # Deleting model 'EntityFieldDynamicConstraint'
        db.delete_table('entity_field_dynamic_constraint')

        # Deleting model 'EntityFieldBasicConstraints'
        db.delete_table('entity_field_basic_constraint')

        # Deleting model 'EntityFieldDynamicAttributeMapping'
        db.delete_table('entity_field_dynamic_attribute_mapping')

        # Deleting model 'EntityFieldDynamicAttribute'
        db.delete_table('entity_field_dynamic_attribute')

        # Deleting model 'EntityFieldStyle'
        db.delete_table('entity_field_style')

        # Deleting model 'EntityFieldDataType'
        db.delete_table('entity_field_data_type')

        # Deleting model 'EntityFieldBasicAttributes'
        db.delete_table('entity_field_attributes')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'datapoints.aggdatapoint': {
            'Meta': {'unique_together': "(('region_id', 'campaign_id', 'indicator_id'),)", 'object_name': 'AggDataPoint', 'db_table': "'agg_datapoint'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.baddata': {
            'Meta': {'object_name': 'BadData', 'db_table': "'bad_data'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.CacheJob']"}),
            'datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.DataPoint']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            'error_type': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.cachejob': {
            'Meta': {'ordering': "('-date_attempted',)", 'object_name': 'CacheJob', 'db_table': "'cache_job'"},
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 15, 0, 0)'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {}),
            'response_msg': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.calculatedindicatorcomponent': {
            'Meta': {'object_name': 'CalculatedIndicatorComponent', 'db_table': "'calculated_indicator_component'"},
            'calculation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicator_master'", 'to': u"orm['datapoints.Indicator']"}),
            'indicator_component': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicator_component'", 'to': u"orm['datapoints.Indicator']"})
        },
        u'datapoints.campaign': {
            'Meta': {'ordering': "('-start_date',)", 'unique_together': "(('office', 'start_date'),)", 'object_name': 'Campaign', 'db_table': "'campaign'"},
            'campaign_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.CampaignType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'get_full_name'", 'unique_with': '()'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'datapoints.campaigntype': {
            'Meta': {'object_name': 'CampaignType', 'db_table': "'campaign_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.datapoint': {
            'Meta': {'ordering': "['region', 'campaign']", 'unique_together': "(('indicator', 'region', 'campaign'),)", 'object_name': 'DataPoint', 'db_table': "'datapoint'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'source_datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.SourceDataPoint']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.datapointabstracted': {
            'Meta': {'unique_together': "(('region', 'campaign'),)", 'object_name': 'DataPointAbstracted', 'db_table': "'datapoint_abstracted'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_json': ('jsonfield.fields.JSONField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"})
        },
        u'datapoints.datapointcomputed': {
            'Meta': {'unique_together': "(('region_id', 'campaign_id', 'indicator_id'),)", 'object_name': 'DataPointComputed', 'db_table': "'datapoint_with_computed'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.entityallowedvaluescolumn': {
            'Meta': {'object_name': 'EntityAllowedValuesColumn', 'db_table': "'entity_allowed_values_column'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityallowedvaluestable': {
            'Meta': {'object_name': 'EntityAllowedValuesTable', 'db_table': "'entity_allowed_values_table'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfield': {
            'Meta': {'ordering': "('name',)", 'object_name': 'EntityField', 'db_table': "'entity_field'"},
            'basic_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldBasicAttributes']"}),
            'basic_constraints': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldBasicConstraints']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ref': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"})
        },
        u'datapoints.entityfieldattributetype': {
            'Meta': {'object_name': 'EntityFieldAttributeType', 'db_table': "'entity_field_attribute_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfieldbasicattributes': {
            'Meta': {'object_name': 'EntityFieldBasicAttributes', 'db_table': "'entity_field_attributes'"},
            'allowed_values_column': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityAllowedValuesColumn']"}),
            'allowed_values_table': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityAllowedValuesTable']"}),
            'field_style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldStyle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.entityfieldbasicconstraints': {
            'Meta': {'object_name': 'EntityFieldBasicConstraints', 'db_table': "'entity_field_basic_constraint'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'required': ('django.db.models.fields.BooleanField', [], {}),
            'unique': ('django.db.models.fields.BooleanField', [], {})
        },
        u'datapoints.entityfielddatatype': {
            'Meta': {'object_name': 'EntityFieldDataType', 'db_table': "'entity_field_data_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldInputType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfielddynamicattribute': {
            'Meta': {'object_name': 'EntityFieldDynamicAttribute', 'db_table': "'entity_field_dynamic_attribute'"},
            'attribute_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldAttributeType']"}),
            'basic_constraints': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldBasicConstraints']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default_sort': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfielddynamicattributemapping': {
            'Meta': {'object_name': 'EntityFieldDynamicAttributeMapping', 'db_table': "'entity_field_dynamic_attribute_mapping'"},
            'dynamic_attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldDynamicAttribute']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityField']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.entityfielddynamicconstraint': {
            'Meta': {'object_name': 'EntityFieldDynamicConstraint', 'db_table': "'entity_field_dynamic_constraint'"},
            'constraint_relation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldDynamicConstraintRelation']"}),
            'constraint_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldAttributeType']"}),
            'constraint_value_as_string_format': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfielddynamicconstraintmapping': {
            'Meta': {'object_name': 'EntityFieldDynamicConstraintMapping', 'db_table': "'entity_field_dynamic_constraint_mapping'"},
            'dynamic_constraint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityFieldDynamicConstraint']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.EntityField']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value_as_string': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfielddynamicconstraintrelation': {
            'Meta': {'object_name': 'EntityFieldDynamicConstraintRelation', 'db_table': "'entity_field_constraint_relation'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfieldinputtype': {
            'Meta': {'object_name': 'EntityFieldInputType', 'db_table': "'entity_field_input_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entityfieldstyle': {
            'Meta': {'object_name': 'EntityFieldStyle', 'db_table': "'entity_field_style'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table_weight': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'weight_form': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'datapoints.entitytype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'EntityType', 'db_table': "'entity_type'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'default_sort_direction': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.entitytypeattributes': {
            'Meta': {'object_name': 'EntityTypeAttributes', 'db_table': "'content_type_attributes'"},
            'default_sort_direction': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.expecteddata': {
            'Meta': {'unique_together': "(('region', 'campaign'),)", 'object_name': 'ExpectedData', 'db_table': "'expected_data'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ex_parent_region'", 'to': u"orm['datapoints.Region']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ex_child_region'", 'to': u"orm['datapoints.Region']"})
        },
        u'datapoints.historicaldatapointentry': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalDataPointEntry'},
            'cache_job_id': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'source_datapoint_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.indicator': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Indicator', 'db_table': "'indicator'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reported': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"})
        },
        u'datapoints.missingmapping': {
            'Meta': {'object_name': 'MissingMapping', 'db_table': "'vw_missing_mappings'", 'managed': 'False'},
            'datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.DataPoint']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.SourceDataPoint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'what_is_missing': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.office': {
            'Meta': {'object_name': 'Office', 'db_table': "'office'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.recondata': {
            'Meta': {'unique_together': "(('region', 'campaign', 'indicator'),)", 'object_name': 'ReconData', 'db_table': "'recon_data'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'is_raw': ('django.db.models.fields.BooleanField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'success_flag': ('django.db.models.fields.BooleanField', [], {}),
            'target_value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.region': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'region_type', 'office'),)", 'object_name': 'Region', 'db_table': "'region'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_high_risk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']", 'null': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'region_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.RegionType']"}),
            'shape_file_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"})
        },
        u'datapoints.regionheirarchy': {
            'Meta': {'object_name': 'RegionHeirarchy', 'db_table': "'region_heirarchy_cache'", 'managed': 'False'},
            'contained_by_region_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_type_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'datapoints.regionpolygon': {
            'Meta': {'object_name': 'RegionPolygon', 'db_table': "'region_polygon'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polygon': ('jsonfield.fields.JSONField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']", 'unique': 'True'}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_len': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.regiontype': {
            'Meta': {'object_name': 'RegionType', 'db_table': "'region_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'datapoints.responsibility': {
            'Meta': {'ordering': "('indicator',)", 'unique_together': "(('user', 'indicator', 'region'),)", 'object_name': 'Responsibility', 'db_table': "'responsibility'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'datapoints.source': {
            'Meta': {'object_name': 'Source', 'db_table': "'source'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'source_data.document': {
            'Meta': {'ordering': "('-id',)", 'unique_together': "(('docfile', 'doc_text'),)", 'object_name': 'Document'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'doc_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'master_datapoint_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_datapoint_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'source_data.processstatus': {
            'Meta': {'object_name': 'ProcessStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status_text': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'source_data.sourcedatapoint': {
            'Meta': {'unique_together': "(('source', 'source_guid', 'indicator_string'),)", 'object_name': 'SourceDataPoint', 'db_table': "'source_datapoint'"},
            'campaign_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cell_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 15, 0, 0)'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'row_number': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"})
        }
    }

    complete_apps = ['datapoints']