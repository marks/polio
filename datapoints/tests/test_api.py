import requests

from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User

from datapoints.models import Indicator
from source_data.models import Source, Document


class IndicatorResourceTest(ResourceTestCase):

     def setUp(self):
        super(IndicatorResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
            'john@john.com', self.password)

        # create their api_key
        self.api_key = ApiKey.objects.create(user=self.user)

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.document_id = Document.objects.create(
            doc_text = 'test',
            created_by_id = self.user.id,
            guid = 'test').id

        # # create create an indicator
        self.indicator = Indicator.objects.create(name='First Indicator',
            description='First Indicator Description',source=self.source)


     def test_indicator_get(self):

        resp = self.api_client.get('/api/v1/indicator', format='json',\
            username='john',api_key=self.api_key)

        # self.assertValidJSONRespons(resp)
