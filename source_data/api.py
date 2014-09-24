from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication


from source_data.models import EtlJob
from source_data.etl_tasks.transform_odk import VcmTransform
from source_data.etl_tasks.refresh_odk_work_tables import WorkTableTask
from time import strftime

import subprocess,sys,time

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings

class EtlResource(ModelResource):
    '''Region Resource'''

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']

        authorization = Authorization()
        authentication = ApiKeyAuthentication()

    # http://localhost:8000/api/v1/etl/?task=pull_odk
    def get_object_list(self, request):

        task_string = request.GET['task']
        print task_string
        tic = strftime("%Y-%m-%d %H:%M:%S")

        ## stage the job ##
        created = EtlJob.objects.create(
            date_attempted = tic,
            task_name = task_string,
            status = 'PENDING'
        )

        ## MAKE THIS A CALL BACK FUNCTION ##
        et = EtlTask(task_string,created.guid)

        toc = strftime("%Y-%m-%d %H:%M:%S")
        created.date_completed = toc
        created.status = 'COMPLETE'

        created.save()

        return EtlJob.objects.filter(guid=created.guid)


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string,task_guid):

        print 'initializing etl task\n'

        self.task_guid = task_guid

        x = task_string + '\n'

        self.function_mappings = {
              'pull_odk' : self.pull_odk,
              'refresh_odk_work_tables' : self.refresh_work_tables,
              'pre_process_odk' : self.pre_process_odk,
              # 'refresh_master' : self.refresh_master,
              'transform_odk' : self.transform_odk,
              'test_api' : self.test_api,
            }

        fn = self.function_mappings[task_string]

        fn()

    def pull_odk(self):

        for form_id in odk_settings.FORM_LIST:

            subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
                '--form_id',form_id, \
                '--export_filename',form_id+'.csv', \
                '--aggregate_url',odk_settings.AGGREGATE_URL, \
                '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
                '--export_directory',odk_settings.EXPORT_DIRECTORY, \
                '--odk_username',odk_settings.USERNAME, \
                '--odk_password',odk_settings.PASSWORD, \
                '--overwrite_csv_export' ,\
                '--exclude_media_export' \
              ])

    def refresh_work_tables(self):

        for source_file in odk_settings.FORM_LIST:

              t = WorkTableTask(self.task_guid,source_file)


    def pre_process_odk(self):

        e = VcmTransform(self.task_guid)
        e.pre_process_odk()

    # def refresh_master(self):
    #
    #     e = VcmEtl(self.task_guid)
    #     e.ingest_vcm_datapoints()

    def transform_odk(self):

        v = VcmTransform(self.task_guid)

    def test_api(self):

        print 'API TEST IS WORKING \n' * 5
