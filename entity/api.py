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

from django.utils.translation import ugettext as _
from django.db import models
from tastypie.models import create_api_key
from tastypie.exceptions import TastypieError
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

import re
import json

models.signals.post_save.connect(create_api_key, sender=User)

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

class UserApiException(TastypieError):
    def __init__(self, message="", field=""):
        self._response = {
            "error": message,
            "error_fields": [ field ]
        }
    @property
    def response(self):
        return HttpResponse(json.dumps(self._response),
                content_type='application/json')

class CreateUserResource(ModelResource):
    user = fields.ForeignKey('core.api.UserResource', 'user', full=True)
    #groups = fields.ToManyField(GroupResource, full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authentication = Authentication() #TODO
        authorization = Authorization()   #TODO
        queryset = User.objects.all()
        resource_name = 'create_user'
        always_return_data = True

    def hydrate(self, bundle):
        print 'hydrate called'
        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username",
            "groups")
        for field in REQUIRED_FIELDS:
            if field not in bundle.data["user"]:
                raise UserApiException(field=field, message="Missing Parameter")
        return bundle

    def obj_create(self, bundle, **kwargs):
        print 'obj create called'
        try:
            email = bundle.data['user']['email']
            first_name = bundle.data['user']['first_name']
            last_name = bundle.data['user']['last_name']
            username = bundle.data['user']['username']
        except KeyError as missing_key:
            raise UserApiException(field=missing_key,
                message="Missing Parameter")
        try:
            if User.objects.filter(email=email):
                raise UserApiException(field="email",
                    message="A user with that email is already enrolled")
            if User.objects.filter(username=username):
                raise UserApiException(field="username",
                    message="A user with that username is already enrolled")
        except User.DoesNotExist:
            pass
        #self._meta.resource_name = UserProfileResource._meta.resource_name
        #return super(CreateUserResource, self).obj_create(bundle, **kwargs)
