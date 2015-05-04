from django.conf import settings
from django.contrib.auth.models import User, Group
from tastypie.test import ResourceTestCase

import random

# this is set up for get
# change it to test post

# http://django-tastypie.readthedocs.org/en/latest/testing.html

class CreateUserTestCase(ResourceTestCase):

    #fixtures = ['test_data.json',]

    def setUp(self):

        super(CreateUserTestCase, self).setUp()
        self.username = 'test_admin'
        self.password = '2938472@#$@#'
        # TODO: make an administrator, or get one
        self.user = User.objects.create_user(self.username,
            'bfontecc_test@seedscientific.com', self.password)
        # create their api key?
        self.post_url = "/api/v2/entity/user/"
        self.get_url = "/api/v1/entity/users/"
        self.user_update = "/api/v1/entity/users/update"
        self.admin_update = "/api/v1/entity/users/admin_update" # TODO: put hash here
        self._username = 'test_user'+str(int(random.random() * 100000))
        self.put_to_id = 1
        self.put_url = self.post_url+self.put_to_id


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

        # key this differently
        data = self.deserialize(resp)['objects'][0]
        self.assertEqual(data.get('username'), )
        '''

    def test_user_post_unauthenticated(self):
        pass
        '''
        self.assertHttpUnauthorized(self.api_client.post(self.post_url,
            format='json', data=self.post_data))
        '''

    def test_user_put_unauthenticated(self):
        pass
        '''
        self.assertHttpUnauthorized(self.api_client.put(self.put_url,
            format='json', data=self.post_data))
        '''

    def test_user_post_badpassword(self):

        bad_data = {
            'user': {
                'username': self._username,
                'first_name': 'Bret',
                'last_name': 'Fontecchio',
                'email': self._username+'@seedscientific.com',
                'password': 'password',
                'groups': 'unicef_hq'
            }
        }
        self.setup_session()
        initial_count = User.objects.count()
        self.assertHttpBadRequest(self.api_client.post(self.post_url,
            format='json', data=bad_data))
        self.assertEqual(User.objects.count(), initial_count)

    def test_user_post_missingfield(self):

        bad_data = {
            'user': {
                'username': self._username,
                'first_name': 'Bret',
                'last_name': 'Fontecchio',
                'password': 'Unicef2015!$#',
                'groups': 'unicef_hq'
            }
        }
        self.setup_session()
        initial_count = User.objects.count()
        self.assertHttpBadRequest(self.api_client.post(self.post_url,
            format='json', data=bad_data))
        self.assertEqual(User.objects.count(), initial_count)


    def test_user_post(self):

        good_data = {
            'user': {
                'username': self._username,
                'first_name': 'Bret',
                'last_name': 'Fontecchio',
                'email': self._username+'@seedscientific.com',
                'password': 'Unicef2015$$##',
                'groups': []
            }
        }
        # there are no groups in the test database
        self.setup_session()

        # Check how many are there first.
        initial_count = User.objects.count()
        self.assertHttpCreated(self.api_client.post(self.post_url,
            format='json', data=good_data))
        # Verify a new one has been added.
        self.assertEqual(User.objects.count(), initial_count+1)

    def test_user_put_missingfield(self):
        pass

    def test_user_put_badformat(self):
        pass

    def test_user_put(self):
        pass

    def test_get_detail_unauthenticated(self):

        '''
        self.assertHttpUnauthorized(self.api_client.get(self.get_url, format='json'))
        '''
