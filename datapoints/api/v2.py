import json
import datetime
import traceback
from pprint import pprint
from collections import defaultdict

from django.core.serializers import json as djangojson
from django.db.models import Model, ManyToManyField
from django.db.models.query import RawQuerySet
from django.db.models.sql.constants import QUERY_TERMS
from django.db.models.options import Options
from django.db.models.fields import AutoField, FieldDoesNotExist
from django.db import connection

from django.forms.models import model_to_dict
from django.utils.encoding import smart_str
from django.contrib.auth.models import User, Group
from django.core import serializers

from datapoints.models import *
from source_data.models import *

class v2Request(object):

    def __init__(self, request, content_type):
        '''
        The v2 request when instatiated setts up class variables for the request
        the content type and the user_id sending the request.

        Most importantly howver, the v2 api uses the dictionary below in order
        to translate the content type in the api ( api/v1/<content_type> ) into
        a database model (Region, Campaign, Indicator) as well as an optional
        function to perform filtering based on the user's permissions or any
        other transformation to the data before return to the application.
        '''

        self.request = request
        self.content_type = content_type
        self.user_id = request.user.id
        self.data = None
        self.meta = None
        self.err = None

        # Tells the API which models are avail for GET / POST / META requests #
        self.orm_mapping = {
            'campaign': {'orm_obj':Campaign,
                'permission_function':self.apply_campaign_permissions},
            'region': {'orm_obj':Region,
                'permission_function':self.apply_region_permissions},
            'document_review' : {'orm_obj':DocumentDetail,
                'permission_function': self.group_document_metadata},
            'indicator': {'orm_obj':IndicatorAbstracted,
                'permission_function':self.apply_indicator_permissions},
            'user_permission': {'orm_obj':UserAuthFunction,
                'permission_function':self.filter_permissions_to_current_user},
            'document': {'orm_obj':Document,
                'permission_function':self.apply_document_permissions },
            'custom_dashboard': {'orm_obj':CustomDashboard,
                'permission_function':self.apply_cust_dashboard_permissions},
            'group_permission': {'orm_obj':IndicatorPermission,
                'permission_function':None},
            'group': {'orm_obj':Group,
                'permission_function':None},
            'user': {'orm_obj':User,
                'permission_function':None},
            'region_permission': {'orm_obj':RegionPermission,
                'permission_function':None},
            'user_group': {'orm_obj':UserGroup,
                'permission_function':None},
            'office': {'orm_obj':Office,
                'permission_function':None},
            'indicator_map': {'orm_obj':IndicatorMap,
                'permission_function':None},
            'region_map': {'orm_obj':RegionMap,
                'permission_function':None},
            'campaign_map': {'orm_obj':CampaignMap,
                'permission_function':None},
            'indicator_tag': {'orm_obj':IndicatorTag,
                'permission_function':None},
            'campaign_type': {'orm_obj':CampaignType,
                'permission_function':None},
            'region_type': {'orm_obj':RegionType,
                'permission_function':None},
        }


    def main(self):
        '''
        Put together a response with the data, meta, and error objects, returing
        this all to the django view.
        '''

        response_data = {
            'objects':self.data,
            'meta':self.meta,
            'error':self.err,
        }

        return response_data

    ## permissions functions ##
    def apply_cust_dashboard_permissions(self,list_of_object_ids):

        '''
        This a fairly simple resource except for the fast that we need to
        determine if the resource is owned_by_current_user as well as the
        username of the user who owns this dashboard.
        '''

        data = CustomDashboard.objects.raw("""
        	SELECT
        		cd.*
                , au.username as owner_username
        		, CAST(CASE WHEN %s = au.id THEN 1 ELSE 0 END AS BOOLEAN) as owned_by_current_user
        	FROM custom_dashboard cd
        	INNER join auth_user au
        	ON cd.owner_id = au.id
        	WHERE cd.id = ANY(COALESCE(%s,ARRAY[cd.id]));
        """,[self.user_id,list_of_object_ids])

        return None, data

    def filter_permissions_to_current_user(self, list_of_object_ids):
        '''
        By default the api should retrieve only the user permissions for
        the current user, that is why the filter kwargs has the current
        user_id set up when this method is run.

        Setting the id__in filter kwargs allows for the django orm filters
        to be applied to the final queryset, so for instance you can see only
        permissions that a user has that starts with 'a' or that has an id
        greater than 100.
        '''

        filter_kwargs = {'user_id': self.user_id}

        if list_of_object_ids:
            filter_kwargs['id__in'] = list_of_object_ids

        data = UserAuthFunction.objects.filter(**filter_kwargs)

        return None, data

    def apply_region_permissions(self, list_of_object_ids):
        '''
        This returns a raw queryset, that is the query itself isn't actually
        executed until the data is unpacked in the serialize method.

        For more information on how region permissions work, take a look
        at the definition of the stored proc called below.
        '''

        data = Region.objects.raw("SELECT * FROM\
            fn_get_authorized_regions_by_user(%s,%s,%s,%s)",[self.request.user.id,
            list_of_object_ids,self.read_write,self.depth_level])

        return None, data

    def apply_campaign_permissions(self, list_of_object_ids):
        '''
        As in above, this returns a raw queryset, and will be executed in the
        serialize method.

        The below query reads: "show me all campaigns for regions that I am
        permitted to see."  As indicated below, this deduction is made by
        joining my permitted regions to the campaigns table on the office_id
        column.
        '''

        data = Campaign.objects.raw("""
            SELECT DISTINCT c.* FROM campaign c
            INNER JOIN region r
                ON c.office_id = r.office_id
            INNER JOIN region_permission rm
                ON r.id = rm.region_id
                AND rm.user_id = %s
            WHERE c.id = ANY(COALESCE(%s,ARRAY[c.id]))
            ORDER BY c.start_date DESC
        """, [self.user_id, list_of_object_ids])

        return None, data

    def apply_indicator_permissions(self, list_of_object_ids):
        '''
        The API allows the application to pass a read_write parameter.  While
        all users can read all indicators and all data, they can not write to
        all indicators.

        This functionlaity is largely based on the use case that a user who
        only has avalibility to write to 2 indicators should only see these
        two as an option for him to insert / update when navigating to the
        data entry page.
        '''

        if self.read_write == 'r':

            data = IndicatorAbstracted.objects.raw("""
                SELECT ia.*
                FROM indicator_abstracted ia
                WHERE 1=1
                AND ia.id = ANY(COALESCE(%s,ARRAY[ia.id]))
            """,[list_of_object_ids])

        else:
            data = IndicatorAbstracted.objects.raw("""
                SELECT ia.*
                FROM indicator_abstracted ia
                WHERE 1=1
                AND ia.id = ANY(COALESCE(%s,ARRAY[ia.id]))
                AND EXISTS (
                	SELECT * FROM auth_user_groups aug
                	INNER JOIN indicator_permission gp
                	ON aug.group_id = gp.group_id
                	AND ia.id = gp.indicator_id
                	AND aug.user_id = %s
                )
            """,[list_of_object_ids,self.user_id])

        return None, data

    def apply_document_permissions(self, list_of_object_ids):
        '''
        The default behavior of the Document api is to send all of the documents
        uploaded by the current user.  If however, the show_all flag is set then
        all documents are returned.  We also make sure here that the basic
        API filters are applied here by filtering the document table by the list
        of IDs we retreived in the prior step

        '''

        filter_kwargs = {}

        if list_of_object_ids:
            filter_kwargs['id__in'] = list_of_object_ids

        if not self.show_all:
            filter_kwargs['created_by_id'] = self.user_id

        data = Document.objects.filter(**filter_kwargs)

        return None, data

    def group_document_metadata(self,list_of_object_ids):
        '''
        This function is not actually about permissions, but rather data
        manipulation needed for the front end.  Here i create three nodes
        (region, campaign, indicator) and add all metadata here.
        '''

        raw_data = DocumentDetail.objects.raw("""
            SELECT * FROM
            document_detail dd
            WHERE dd.id = ANY(COALESCE(%s,ARRAY[-1]))
        """,[list_of_object_ids]
        )

        cleaned_data = {
            'region':[],
            'campaign':[],
            'indicator':[],
        }

        for row in raw_data:

            row_dict = dict(row.__dict__)
            del row_dict['_state']

            cleaned_data[row.db_model].append(row_dict)

        return None, cleaned_data


class v2PostRequest(v2Request):
    '''
    Inherited from the V2 request, so the api_mapper, request, user_id are
    avaliable by this class.

    As demostrated in datapoints/cache_tasks.py, some of the metadata models
    that we return to the api are transformed outside of the API, for instance
    the indicator table is transformed into the indicator_abstraced table
    by finding key-ed information, serializing it as json and dumping the
    results into the indicator_anstracted table.

    Here we override the indicator namespace so that when a POST request comes
    in the application knows to write to the Indicator model as opposed to the
    IndicatorAbstracted model, whci is used in GET requests.

    As the parameters are handled differently here than in the GET request,
    this class has its own clean_kwargs method which processes the POST data
    that the endpoint uses throught the cycle.
    '''

    def __init__(self, request, content_type):

        super(v2PostRequest, self).__init__(request, content_type)

        ## DB obj can be different between GET and POST requests ##
        self.orm_mapping['indicator']['orm_obj'] = Indicator

        ## find the DB obj we want to POST to
        self.db_obj = self.orm_mapping[content_type]['orm_obj']

        ## klean URL parameters
        self.kwargs = self.clean_kwargs(request.POST)

    def clean_kwargs(self,query_dict):
        '''
        Create a dictionary from the parsed parameters, and also add the
        mapped_by_id parameter when necessary ( used in the meta_mapping
        endpoints )
        '''

        cleaned_kwargs = {}

        for k,v in query_dict.iteritems():
            cleaned_kwargs[k] = v

        ## add mapped_by id for mapping endpoints ##
        if self.content_type in ['region_map','indicator_map','campaign_map']:
            cleaned_kwargs['mapped_by_id'] = self.user_id

        return cleaned_kwargs

    def main(self):
        '''
        - Return error if not implemented
        - For custom dashboards, set the owner_id to the user making the request
          as well as ensuring the JSON is valid.
        - Determine ( based on the convention of this API ) if the request is an
          insert, update or delete.

        If method is create:
         Create an object in accordance to the URL kwargs and return the new ID

        If delete:
            query for objects taht match what was passed in the post params and
            delete all objects that fulfill those conditions
        If update
            set the object with the ID that has been passed via the URL to the
            json parameters associated with the request params.

        note: hacking the custom dashboard api right now but will clean up using
        the same "permission_function" structure that allows me to handle per
        resource fixes as we do in GET.
        '''

        ## Create, Update or Delete ##
        request_type = self.determined_request_type()

        if self.content_type == 'user':

            self.err = 'User POST not implemented in v2 api.'
            return super(v2PostRequest, self).main()


        ## Insert / Update / Delete Data ##

        try:

            ## for custom dashboard api - validate the json posted is valid
            ## this should be re-organized.. moving this for a last minute
            ## fix pre our first UNICEF production release. Hack alert below
            if self.content_type == 'custom_dashboard':
                self.kwargs['owner_id'] = self.user_id

                try:
                    cleaned_json = json.loads(self.kwargs['dashboard_json'])
                    self.kwargs['dashboard_json'] = cleaned_json
                except KeyError: # if dashboard json null
                    pass
                except ValueError:
                    self.err = 'Invalid JSON!'
                    return super(v2PostRequest, self).main()

            if request_type == 'CREATE':

                ## done with the custom_dashboard case, now i create the object
                ## fot all content types
                new_obj = self.db_obj.objects.create(**self.kwargs)
                self.data = {'new_id':new_obj.id}

            elif request_type == 'DELETE':

                old_obj = self.db_obj.objects.get(**self.kwargs)
                self.data = {'deleted_id': old_obj.id }

                old_obj.delete()

            elif request_type == 'UPDATE':

                obj_to_update = self.db_obj(id=self.id_param, **self.kwargs)
                obj_to_update.save()

                self.data = data = {'updated_id': obj_to_update.id
                , 'updated_values': self.kwargs }

        except Exception, e:
            self.err = traceback.format_exc()

        return super(v2PostRequest, self).main()

    def determined_request_type(self):
        '''
        POST can be create, update, or delete.

        DELETE - pass {'id':''}
        UPDATE - pass {'id':<id_of_object>,
                       'field_to_update_1':'val_1',
                       'field_to_update_2':'val_2'
                      }
        INSERT - pass a json dictionary with all of the required columns to
        create the object associated with the url's content_type.
        '''

        try:
            self.id_param = self.kwargs['id']
            del self.kwargs['id']

            if self.id_param == '':
                return 'DELETE'
            else:
                return 'UPDATE'

        except KeyError:
            self.id_param = None
            return 'CREATE'


class v2MetaRequest(v2Request):
    '''
    A set of endpoints that tells the application what fields and data types
    are associated with each model / api resource.
    '''

    def __init__(self, request, content_type):
        '''
        Instatiate the parent v2 request then determin the database object by
        Performing a lookup on the orm_mapping dictionary.
        '''

        super(v2MetaRequest, self).__init__(request, content_type)
        self.db_obj = self.orm_mapping[content_type]['orm_obj']

    def main(self):
        '''
        Use information about the django model in order to send meta data
        about the resource to the API.  This is used by the front end to
        dynamically generate table views and forms to interact with these
        models.
        '''

        self.data = {}

        self.all_field_meta = []
        self.meta_data = {
                'slug':self.content_type,
                'name':self.content_type,
                'primary_key':'id',
                'search_field':'slug',
                'defaultSortField':'id',
                'defaultSortDirection':'asc',
        }


        db_table = self.db_obj._meta.db_table
        ca_dct = ColumnAttributes.objects.filter(table_name = \
            db_table).values('column_name','display_name',\
            'display_on_table_flag')

        self.column_lookup = {}
        for row in ca_dct:
            column_name = row['column_name']
            del row['column_name']
            self.column_lookup[column_name] = row


        ## BUILD METADATA FOR EACH FIELD ##
        for ix,(field) in enumerate(self.db_obj._meta.get_all_field_names()):

            try:
                self.build_field_meta_dict(field,ix)
            except KeyError:
                pass

        self.data['fields'] = self.all_field_meta

        ## url_patterns ##
        self.url_patterns = {
            'create': "datapoints/" + self.content_type + "s/create",
            'update': "datapoints/" + self.content_type + "s/update/?<id>/"

        }
        self.data['fields'] = self.all_field_meta
        self.data['url_patterns'] = self.url_patterns

        return super(v2MetaRequest, self).main()

    def build_field_meta_dict(self, field, ix):
        '''
        Examine model instance to find meta data
        Query the Column Attributes table to find metadata on what django model
        does not store.
        '''
        try:
            field_object = self.db_obj._meta.get_field(field)
        except FieldDoesNotExist:
            return None

        ## DICT TO MAP DJANNGO FIELD DEFINITION TO THE TYPES THE FE EXPECTS ##
        field_type_mapper = {'AutoField':'number','FloatField':'number',
            'ForeignKey':'array','CharField':'string','ManyToManyField':'array',
            'DateTimeField':'datetime','DateField':'datetime','BooleanField':
            'boolean','SlugField':'string','TextField':'string'}

        ## BUILD A DICTIONARY FOR EACH FIELD ##
        field_object_dict = {
            'name': field_object.name,
            'title': self.column_lookup[field_object.name]['display_name'],
            'type': field_type_mapper[field_object.get_internal_type()],
            'max_length': field_object.max_length,
            'editable' : field_object.editable,
            'default_value' : str(field_object.get_default()),
                'display' : {
                    'on_table':self.column_lookup[field_object.name]\
                        ['display_on_table_flag'],
                    'weightTable':ix,
                    'weightForm':ix,
                },
            'constraints': self.build_field_constraints(field_object)
            }

        self.all_field_meta.append(field_object_dict)


    def build_field_constraints(self,field_object):
        '''
        This method should be removed.  The functionality that this peice of
        code was supposed to provide is no longer in scope.
        '''

        field_constraints = {
            'unique':field_object.unique
            }

        try:
            field_constraints['required'] = field_object.required
        except AttributeError:
            field_constraints['required'] = False

        if field_object.name == 'groups':

            ## SAMPEL DATA FOR DAN TO IMPLEMENT UFADMIN FOR USERS ##
            dict_list = [{'value':1,'label':'UNICEF HQ'}]
            field_constraints['items'] = {'oneOf':dict_list}

        return field_constraints


class v2GetRequest(v2Request):
    '''
    Inheritng form the v2Request above, this class handles all GET requests in
    the v2 api.
    '''

    def __init__(self, request, content_type):
        '''
        Instantiate the v2Request then find the permission function, database
        object associated with the content_type, finally cleaning the api params
        and creating the class attribute self.kwargs.
        '''
        super(v2GetRequest, self).__init__(request, content_type)

        self.db_obj = self.orm_mapping[content_type]['orm_obj']
        self.permission_function = self.orm_mapping[content_type]\
            ['permission_function']

        self.kwargs = self.clean_kwargs(request.GET)


    def main(self):
        '''
        Get the list of database objects ( ids ) by applying the URL kwargs to
        the filter method of the djanog ORM.
        '''

        # for a get request.. dont show any ids < 0 ( see POLIO-856 ) #

        try:
            id_gt = self.kwargs['id__gt']
        except KeyError:
            self.kwargs['id__gt'] = 0


        ## IF THERE ARE NO FILTERS, THE API DOES NOT NEED TO ##
        ## QUERY THE DATABASE BEFORE APPLYING PERMISSIONS ##
        if not self.kwargs and self.content_type in ['campaign','region']:
            qset = None
        else:
            qset = list(self.db_obj.objects.filter(**self.kwargs).values())

        err, filtered_data = self.apply_permissions(qset)
        err, data = self.serialize(filtered_data)

        ## apply limit and offset.  Not ideal that this does happen at the
        ## data base level, but applying limit/offset at here and querying for
        ## all the data is fine for now as these endpoints are fast.

        try:
            self.data = data[self.offset:self.limit + self.offset]
        except TypeError:
            self.data = data

        self.full_data_length = len(data)
        self.err = err
        self.meta = self.build_meta()

        return super(v2GetRequest, self).main()


    def clean_kwargs(self,query_dict):
        '''
        When passing filters make sure that what is in the URL string is
        actually a field of the model.

        This includes parsing the query terms out of the parameter key.  i.e.
        when the API receives id__gte=50, we need to check to see if "id"
        is a field ,not id__gte=50.
        '''

        cleaned_kwargs = {}
        operator_lookup = {}

        ## MAP THE QUERY PARAMETER WITH ITS OPERATOR, TO THE DB MODEL ##
        for param in query_dict.keys():

            try:
                operator_lookup[param[0:param.index('__')]] = param
            except ValueError:
                operator_lookup[param] = param

        ## ONLY WANT TO CLEAN KWARGS FOR COLUMNS THAT EXISTS FOR THIS MODEL ##
        db_model_keys = list(set(self.db_obj._meta.get_all_field_names()).\
            intersection(set(k for k in operator_lookup.keys())))

        ## FINALLY CREATE ONE DICT (cleaned_kwargs) WITH THE ORIGINAL K,V ##
        ## IN THE URL, BUT FILTERED ON COLUMNS AVAILABLE TO THE MODEL ##
        for k in db_model_keys:

            query_key = operator_lookup[k]
            query_value = query_dict[operator_lookup[k]]#[]

            if "," in query_value:
                cleaned_kwargs[query_key] = query_value.split(',')
            else:
                cleaned_kwargs[query_key] = query_value


        ## FIND THE LIMIT AND OFFSET AND STORE AS CLASS ATTRIBUETS ##
        try:
            self.limit = int(query_dict['limit'])
        except KeyError:
            self.limit = 1000000000

        try:
            self.offset = int(query_dict['offset'])
        except KeyError:
            self.offset = 0

        ## Find the Read/Write param for regions ( see POLIO-779 ) ##

        try:
            self.read_write = query_dict['read_write']
        except KeyError:
            self.read_write = 'r'

        ## Find the Depth Level param ( see POLIO-839 ) ##
        try:
            self.depth_level = query_dict['depth_level']
        except KeyError:
            self.depth_level = 10

        try:
            self.show_all = query_dict['show_all']
        except KeyError:
            self.show_all = None

        return cleaned_kwargs

    def build_meta(self):
        '''
        Create a dictionary with the meta data of the request to allow for
        pagination on the front end.
        '''

        meta_dict = {
            'limit': self.limit,
            'offset': self.offset,
            'total_count': self.full_data_length,
        }

        return meta_dict


    def apply_permissions(self, queryset):
        '''
        Only some of the content types have an associated permission_function
        in the orm_mapper.  When there is no permission function this method
        simply returns the eqisting data, but when there is, the permission
        function is executed with the list_of_object_ids that came from the
        initial ORM filter.

        So for example the region permission function knows to not only filter
        data based on my permissions, but to additionally filter data based on
        the parameters passed in the url.
        '''

        if not self.permission_function:
            return None, queryset

        ## if filters then create that list of IDs, otherwise pass ##
        ## None, and the permissions function wont filter on an ID list ##
        if not queryset:
            list_of_object_ids = None
        else:
            list_of_object_ids = [x['id'] for x in queryset]

        err, data = self.permission_function(list_of_object_ids)

        return err, data


    def serialize(self, data):
        '''
        document_review has a custom serialization in which 'region', 'campaign'
        and 'indicator' are keys and the value is a list of the cooresponding
        mappings.  This needs to be cleaned up, but for now that content
        type skips through the serialization method.

        '''

        if self.content_type != 'document_review':
            serialized = [self.clean_row_result(row) for row in data]

            return None, serialized

        else:
            return None, data



    def clean_row_result(self, row_data):
        '''
        When Serializing, everything but Int and List are converted to string.
        In this case the List (in the case of indicators), is a json array.

        If it is a raw queryset, first convert the row to a dict using the
        built in __dict__ method.

        This just returns a list of dict.  The JsonResponse in the view
        does the actual json conversion.

        Also get rid of the _state attribute ( see POLIO-801)

        '''

        cleaned_row_data = {}

        # if raw queryset, convert to dict
        if isinstance(row_data,Model):
            row_data = dict(row_data.__dict__)
            del row_data['_state']

        # serialize various data type as requirements change and expand #
        for k,v in row_data.iteritems():
            if isinstance(v, int):
                cleaned_row_data[k] = v
            elif k in ['longitude','latitude'] and v:
                cleaned_row_data[k] = float(v)
            elif k == 'bound_json':
                cleaned_row_data[k] = v
            elif k == 'tag_json':
                cleaned_row_data[k] = v
            elif k == 'dashboard_json' and v is None:
                cleaned_row_data[k] = None
            elif k == 'dashboard_json' and v == '':
                cleaned_row_data[k] = None
            elif k == 'dashboard_json':
                cleaned_row_data[k] = v
            else:
                cleaned_row_data[k] = smart_str(v)

        return cleaned_row_data
