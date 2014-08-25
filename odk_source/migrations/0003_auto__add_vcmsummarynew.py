# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VCMSummaryNew'
        db.create_table(u'odk_source_vcmsummarynew', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SubmissionDate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deviceid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('simserial', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('DateOfReport', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Date_Implement', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('SettlementCode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CensusNewBornsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CensusNewBornsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Newborns', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Census2_11MoF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Census2_11MoM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_2_11Months', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Census12_59MoF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Census12_59MoM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_12_59Months', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Census', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VaxNewBornsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VaxNewBornsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_VaxNewBorn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax3', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Vax2_11MoF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Vax2_11MoM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Vax2_11Mo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax4', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax6', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Vax12_59MoF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Vax12_59MoM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Vax12_59Mo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Vax', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Tot_Missed', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax7', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax8', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_vax9', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_msd1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_msd2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PlaygroundF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PlaygroundM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SocEventF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SocEventM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_MarketF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_MarketM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_FarmF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_FarmM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SchoolF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SchoolM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_ChildSickF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_ChildSickM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SideEffectsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SideEffectsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoFeltNeedF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoFeltNeedM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_TooManyRoundsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_TooManyRoundsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_RelBeliefsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_RelBeliefsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolDiffsF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolDiffsM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_UnhappyWTeamF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_UnhappyWTeamM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoPlusesF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoPlusesM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoGovtServicesF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoGovtServicesM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolioUncommonF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolioUncommonM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolioHasCureF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_PolioHasCureM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_OtherProtectionF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_OtherProtectionM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoConsentF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_NoConsentM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_HHNotVisitedF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_HHNotVisitedM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SecurityF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_SecurityM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_AgedOutF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_AgedOutM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_FamilyMovedF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_FamilyMovedM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_ChildDiedF', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Msd_ChildDiedM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_Tot_Missed_Check', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_msd_chd_display_msd3', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('spec_grp_choice', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_ZeroDose', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_PregnantMother', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_Newborn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_VCMAttendedNCer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_CMAMReferral', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_RIReferral', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_AFPCase', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_MslsCase', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_OtherDisease', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group_spec_events_Spec_FIC', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_instanceID', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('KEY', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('odk_source', ['VCMSummaryNew'])


    def backwards(self, orm):
        # Deleting model 'VCMSummaryNew'
        db.delete_table(u'odk_source_vcmsummarynew')


    models = {
        'odk_source.vcmbirthrecord': {
            'DOB': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'HouseHoldNumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'VCMBirthRecord'},
            'NameOfChild': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCM0Dose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMNameCAttended': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMRILink': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'odk_source.vcmsummarynew': {
            'Census12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Date_Implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'VCMSummaryNew'},
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_12_59Months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_2_11Months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Census': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Missed': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Newborns': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax12_59Mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax2_11Mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_VaxNewBorn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_msd1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_msd2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax6': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax7': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax8': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax9': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_AgedOutF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_AgedOutM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildDiedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildDiedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildSickF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildSickM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FamilyMovedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FamilyMovedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FarmF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FarmM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_HHNotVisitedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_HHNotVisitedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_MarketF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_MarketM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoConsentF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoConsentM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoFeltNeedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoFeltNeedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoGovtServicesF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoGovtServicesM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoPlusesF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoPlusesM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_OtherProtectionF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_OtherProtectionM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PlaygroundF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PlaygroundM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolDiffsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolDiffsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioHasCureF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioHasCureM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioUncommonF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioUncommonM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_RelBeliefsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_RelBeliefsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SchoolF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SchoolM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SecurityF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SecurityM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SideEffectsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SideEffectsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SocEventF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SocEventM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_TooManyRoundsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_TooManyRoundsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_UnhappyWTeamF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_UnhappyWTeamM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Tot_Missed_Check': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_display_msd3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_AFPCase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_CMAMReferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_FIC': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_MslsCase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_Newborn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_OtherDisease': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_PregnantMother': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_RIReferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_VCMAttendedNCer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_ZeroDose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['odk_source']