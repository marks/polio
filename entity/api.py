from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views import generic
from django.contrib.auth.models import User,Group
from django.template import RequestContext
from django.db import IntegrityError

from django.utils.translation import ugettext as _
from django.db import models
from tastypie.models import create_api_key
from tastypie.exceptions import TastypieError
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import SessionAuthentication
#from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted

import re
import json

models.signals.post_save.connect(create_api_key, sender=User)

TASTYPIE_FULL_DEBUG = True


'''
MINIMUM_PASSWORD_LENGTH = 6
REGEX_VALID_PASSWORD = (
    ## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
    r'^(?!.*[\s])'
    ## Check for a digit
    '((?=.*[\d])'
    ## Check for an uppercase letter
    '(?=.*[A-Z])'
    ## check for special characters. Something which is not word, digit or
    ## space will be treated as special character
    '(?=.*[^\w\d\s])).'
    ## Minimum 8 characters
    '{' + str(MINIMUM_PASSWORD_LENGTH) + ',}$')

def validate_password(password):
    if re.match(REGEX_VALID_PASSWORD, password):
        return True
    return False
'''

class UserApiBadRequest(ImmediateHttpResponse):
    def __init__(self, message="", field=""):
        ImmediateHttpResponse.__init__(self, HttpBadRequest(content=json.dumps({
            'error': message, 'error_fields': [field]}),
            content_type="application/json; charset=utf-8"))

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['password']
        always_return_data = True
        authorization = Authorization()
        authentication = Authentication()

class CreateUserResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    #groups = fields.ToManyField(GroupResource, full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True #change this?
        #authentication = SessionAuthentication()
        authentication = Authentication()
        #authorization = DjangoAuthorization()   #TODO
        authorization = Authorization()
        queryset = User.objects.all()
        resource_name = 'create_user'
        always_return_data = True

    def hydrate(self, bundle):
        print 'hydrate called'
        #TODO: add groups
        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username")
        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")
        return bundle

    def obj_create(self, bundle, **kwargs):
        print 'obj create called'
        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username")
        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")
        email = bundle.data['user']['email']
        first_name = bundle.data['user']['first_name']
        last_name = bundle.data['user']['last_name']
        username = bundle.data['user']['username']
        try:
            if User.objects.filter(email=email):
                print 'email already there'
                raise UserApiBadRequest(field="email",
                    message="A user with that email is already enrolled")
            if User.objects.filter(username=username):
                print 'username already there'
                raise UserApiBadRequest(field="username",
                    message="A user with that username is already enrolled")
        except User.DoesNotExist:
            pass
        #self._meta.resource_name = UserProfileResource._meta.resource_name
        try:
            bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
        except IntegrityError:
            raise
            '''
            raise UserApiBadRequest(message='Username already taken.',
                field='username')
            '''
        return bundle
