from django.conf import settings
from django.contrib.auth.models import User, Group
from tastypie.test import ResourceTestCase

import random

# this is set up for get
# change it to test post

# http://django-tastypie.readthedocs.org/en/latest/testing.html

class CreateUserTest(ResourceTestCase):

    fixtures = ['test_data.json',]

    def setUp(self):
        super(CreateUserTestCase, self).setUp()

        self.username = bfontecc_test
        self.password = test_pass_123
        # TODO: make an administrator, or get one
        self.user = User.objects.create_user(self.username,
            'bfontecc_test@seedscientific.com', self.password)
        # create their api key?
        self.post_url = "/api/v1/create_user/"
        self.get_url = "/api/v1/entity/users/"
        self.user_update = "/api/v1/entity/users/update"
        self.admin_update = "/api/v1/entity/users/admin_update" # TODO: put hash here
        _username = 'test_user'+str(int(random.random() * 100000))
        self.post_data = {
            'username': _username,
            'first_name': 'Bret',
            'last_name': 'Fontecchio',
            'email': _username+'@seedscientific.com'
        }

    def setup_session(self):
        self.api_client.client.login(username=self.username,
            password=self.password)

    def test_get_detail_json(self):
        pass
        # this tests the get
        # it needs to be changed
        # https://plus.google.com/+ScottAnderson42/posts/TpyAXYQaeiy
        '''
        self.setup_session()

        resp = self.api_client.get(self.get_url, format='json')
        self.assertValidJSONResponse(resp)

        # key this differently?
        data = self.deserialize(resp)['objects'][0]
        self.assertEqual(data.get('username'), )
        '''

    def test_post_list(self):
        self.setup_session()

        # Check how many are there first.
        initial_count = Entry.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/v1/entries/',
            format='json', data=self.post_data))
        # Verify a new one has been added.
        self.assertEqual(Entry.objects.count(), initial_count+1)

    def test_get_list_json(self):
        pass

    def test_get_list_xml(self):
        pass

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.get_url, format='json'))
