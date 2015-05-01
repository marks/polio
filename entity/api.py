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
from tastypie.authentication import Authentication as SessionAuthentication
from tastypie.authorization import Authorization as DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted

import re
import json

models.signals.post_save.connect(create_api_key, sender=User)

#TODO: set to false
TASTYPIE_FULL_DEBUG = True
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

#TODO
ALPHA_NUM_UNDERSCORE_ONLY = ''

#TODO
PROBABLY_AN_EMAIL = ''

def valid_password(password):

    if re.match(REGEX_VALID_PASSWORD, password):
        return True
    return False


class UserApiBadRequest(ImmediateHttpResponse):

    def __init__(self, message="", field=""):
        ImmediateHttpResponse.__init__(self, HttpBadRequest(content=json.dumps({
            'error': message, 'error_fields': [field], 'success': False}),
            content_type="application/json; charset=utf-8"))

class UserPasswordError(UserApiBadRequest):

    def __init__(self):
        UserApiBadRequest.__init__(self, message="Invalid Password. Please Enter a password at least 8 characters long with no spaces, at least one digit, at least one uppercase letter, and at least one special character such as: *%$#@!?)(",
            field='password')

class UserCannotEditError(UserApiBadRequest):

    def __init__(self, field):
        UserApiBadRequest.__init__(self, message="Cannot be edited by user",
            field=field)

class BadFormattingException(UserApiBadRequest):

    def __init__(self, field):
        UserApiBadRequest.__init__(self, message="Bad Formatting",
            field=field)

class UserResource(ModelResource):


    class Meta:
        allowed_methods = ['post', 'put']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        queryset = User.objects.all()
        resource_name = 'entity/user'
        always_return_data = True


    def hydrate(self, bundle):

        print 'hydrate'
        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username")
        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")
        return bundle

    def dehydrate(self, bundle):

        user = User.objects.get(username=bundle.obj.username)
        groups = Group.objects.raw(
            '''
            SELECT * FROM auth_user_groups aug
            JOIN auth_group ag
                ON ag.id = aug.group_id
            WHERE aug.user_id = %s;
            ''', [user.pk]
        )
        group_names = [ g.name for g in groups ]
        bundle.data = {
            'error': None,
            'success': True,
            'error_fields': None,
            'user': {
                'id': user.pk,
                'email': bundle.obj.email,
                'username': bundle.obj.username,
                'first_name': bundle.obj.first_name,
                'last_name': bundle.obj.last_name,
                'groups': group_names
            }
        }

        return bundle

    def obj_create(self, bundle, **kwargs):

        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username",
            "password")

        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")

        email = bundle.data['user']['email']
        first_name = bundle.data['user']['first_name']
        last_name = bundle.data['user']['last_name']
        username = bundle.data['user']['username']
        password = bundle.data['user']['password']
        groups = bundle.data['user']['groups']

        if valid_password(password) == False:
            raise UserPasswordError()
        try:
            if User.objects.filter(email=email):
                raise UserApiBadRequest(field="email",
                    message="A user with that email is already enrolled")
            if User.objects.filter(username=username):
                raise UserApiBadRequest(field="username",
                    message="A user with that username is already enrolled")
        except User.DoesNotExist:
            pass

        try:
            # wrap with auth_filter
            user = User.objects.create_user(username, first_name=first_name,
                last_name=last_name, email=email, password=password)
            for group_name in groups:
                try:
                    group = Group.objects.get(name=group_name)
                except:
                    raise UserApiBadRequest(field='groups',
                        message='Invalid Group name: '+group_name)
                try:
                    group.user_set.add(user)
                    pass
                except:
                    raise UserApiBadRequest(field='groups',
                        message='Could not add user to group: '+group.name)
            bundle.obj = user

        except IntegrityError:

            raise UserApiBadRequest(message='A user with that username is already enrolled',
                field='username')

        return bundle



    def obj_update(self, bundle, **kwargs):

        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username",
            "password")

        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")

        email = bundle.data['user']['email']
        first_name = bundle.data['user']['first_name']
        last_name = bundle.data['user']['last_name']
        username = bundle.data['user']['username']
        new_groups = bundle.data['user']['groups']
        pk = bundle.data['user']['id']

        user = User.objects.get(pk=pk)

        # if bundle.request.user.id != pk:
        #   raise UserApiBadRequest(field='id', message="User can only edit self")

        user.first_name = first_name
        user.last_name = last_name

        if user.email != email:
            if not user.is_superuser:
                raise UserCannotEditError(field='email')
            else:
                user.email = email
            if user.username != username:
                raise UserCannotEditError(field='username')

        current_groups = [g.name for g in user.groups.all()]
        for cg in current_groups:
            if cg not in new_groups:
                if not user.is_superuser:
                    raise UserCannotEditError(field='groups')
                group.user_set.remove(user)
        for ng in new_groups:
            if ng not in current_groups:
                if not user.is_superuser:
                    raise UserCannotEditError(field='groups')
                group.user_set.add(user)

        user.save()
        bundle.obj = user

        return bundle
