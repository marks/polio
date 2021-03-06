import json
import traceback
from pprint import pprint

from django.db import IntegrityError
from django.contrib.auth.models import User
from pandas import DataFrame

from datapoints.models import Region, Office, Source
from source_data.models import *
from source_data.etl_tasks.refresh_master import MasterRefresh

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings


class ODKDataPointTransform(object):

    def __init__(self,request_guid,input_df,form_name):

        self.form_name = form_name
        self.request_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id
        self.user_id = User.objects.get(username ='odk').id
        self.source_datapoints = []
        self.document_id = self.get_document_id()
        self.to_process_df = self.get_new_data_from_input_df(input_df)

        self.process_status_id = ProcessStatus.objects\
            .get(status_text='SUCCESS_INSERT').id

    def get_document_id(self):

        doc, created = Document.objects.get_or_create(
            docfile = odk_settings.EXPORT_DIRECTORY + self.form_name,
            created_by_id = User.objects.get(username='odk').id,
            source_id = Source.objects.get(source_name='odk').id,
        )

        return doc.id

    def get_new_data_from_input_df(self,input_df):
        '''
        Return a dataframe that only has the rows that we need to ingest.  That
        is rows that have not been processed before.  We can tell which
        rows these are because each ODK submission has a 'KEY' send every time
        data is sent from the phone.
        '''

        key_list = list(SourceDataPoint.objects.filter(document_id = \
            self.document_id).values_list('source_guid',flat=True))

        distinct_key_list = [str(k) for k in set(key_list)]
        filtered_df = input_df[~input_df.KEY.isin(distinct_key_list)]

        batch_df = filtered_df[:25]

        return batch_df

    def odk_form_data_to_datapoints(self):
        '''
        First transalate the csv into source datapoitns ( very similair to the
        csv upload process), and once the sdps are created, call
        "refresh_master" and pass the list of sdps.
        '''

        self.to_process_df.columns = map(str.lower, self.to_process_df)
        column_list = self.to_process_df.columns.tolist()

        #### DataFrame --> Source DP ####
        all_sdps = []
        for row_number, row in enumerate(self.to_process_df.values):

            row_dict = dict(zip(column_list,row))
            sdps = self.process_row(row_dict,row_number)
            all_sdps.extend(sdps)

        #### Source DP --> Master DP ####

        mr = MasterRefresh(self.user_id,self.document_id)
        dps = mr.source_dps_to_dps()

        response_string = 'created %s new soure_datapoints by processing: %s \
            nows for document_id: %s, yielding in: %s master datapoints' % \
            (len(all_sdps),len(self.to_process_df),self.document_id,len(dps))

        return response_string

    def process_row(self,row_dict,row_number):

        row_batch = []

        region_code = row_dict['settlementcode']
        campaign_string ='Nigeria ' + str(row_dict['date_implement'])
        source_guid = row_dict['key']
        sdps = []

        for column_name, cell_value in row_dict.iteritems():

            cell_guid = source_guid + '-' + column_name
            cleaned_cell_value = self.clean_cell_value(cell_value)

            try:
                sdp = SourceDataPoint.objects.create(**{
                    'region_code' : region_code,
                    'campaign_string' : campaign_string,
                    'indicator_string' : column_name,
                    'cell_value' : cleaned_cell_value,
                    'row_number' : row_number,
                    'source_id': self.source_id,
                    'document_id' : self.document_id,
                    'source_guid' : source_guid,
                    'status_id' : self.process_status_id,
                    'guid': cell_guid
                })
                sdps.append(sdp)
            except IntegrityError as err:
                pass

        return sdps

    def clean_cell_value(self,cell_value):

        if cell_value == 'yes':
            cleaned = 1
        elif cell_value == 'no':
            cleaned = 0
        else:
            cleaned = cell_value

        return cleaned
