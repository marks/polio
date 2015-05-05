from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User,Group
from django.template import RequestContext
from django.db import IntegrityError
from django.db import models
from django.db.models import Q

from tastypie import fields
from tastypie.models import create_api_key
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication as SessionAuthentication
from tastypie.authorization import Authorization as DjangoAuthorization
from tastypie.http import HttpBadRequest, HttpAccepted

from .exceptions import *

import re
import json

models.signals.post_save.connect(create_api_key, sender=User)

#TODO:
# custom authorization:
 # http://django-tastypie.readthedocs.org/en/latest/authorization.html

#TODO: set to false
TASTYPIE_FULL_DEBUG = True
MINIMUM_PASSWORD_LENGTH = 6
ALPHA_NUM = '[A-Za-z0-9 _]{3,30}$'
EMAIL = '^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{3,}$'
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

class GroupResource(ModelResource):

    class Meta:
        queryset = Group.objects.all()
        resource_name = 'auth/group'

class UserShowResource(ModelResource):

    groups = fields.ManyToManyField(GroupResource, 'groups', null=True, full=True)

    class Meta:

        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        queryset = User.objects.all()
        excludes = ['password']
        resource_name = 'entity/users'
        filtering = {
            'username': ALL,
            'id': ALL,
            'first_name': ALL,
            'last_name': ALL
        }

    def dehydrate(self, bundle):

        return {
            'error': None,
            'success': True,
            'error_fields': None,
            'user': {
                'id': bundle.obj.id,
                'email': bundle.obj.email,
                'username': bundle.obj.username,
                'first_name': bundle.obj.first_name,
                'last_name': bundle.obj.last_name,
                'groups': [ g.name for g in bundle.obj.groups.all() ]
            }
        }

    def build_filters(self, filters=None):

        if filters is None:
            filters = {}
        orm_filters = super(UserShowResource, self).build_filters(filters)

        if('search' in filters):
            query = filters['search']
            qset = (
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )
            orm_filters.update({'custom': qset})

        return orm_filters

    def apply_filters(self, request, applicable_filters):

        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(UserShowResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

class UserResource(ModelResource):

    groups = fields.ManyToManyField(GroupResource, 'groups', null=True, full=True)

    class Meta:

        allowed_methods = ['post', 'put']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        queryset = User.objects.all()
        resource_name = 'entity/user'
        always_return_data = True

    def hydrate(self, bundle):

        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username")
        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")
        return bundle

    def dehydrate(self, bundle):
        '''
        user = User.objects.get(username=bundle.obj.username)
        # why is this here get rid of it use groups foreign key
        groups = Group.objects.raw(
            ###
            SELECT * FROM auth_user_groups aug
            JOIN auth_group ag
                ON ag.id = aug.group_id
            WHERE aug.user_id = %s;
            ###
            , [user.pk]
        )
        '''
        group_names = [ g.name for g in bundle.obj.groups.all() ]
        bundle.data = {
            'error': None,
            'success': True,
            'error_fields': None,
            'user': {
                'id': bundle.obj.id,
                'email': bundle.obj.email,
                'username': bundle.obj.username,
                'first_name': bundle.obj.first_name,
                'last_name': bundle.obj.last_name,
                'groups': group_names
            }
        }

        return bundle

    def obj_create(self, bundle, **kwargs):

        def retrieve_valid(data, fieldname, pattern):

            if re.match(pattern, data[fieldname]) == False:
                raise BadFormattingException(fieldname)
            return data[fieldname]

        REQUIRED_FIELDS = ("first_name", "last_name", "email", "username",
            "password")

        for field in REQUIRED_FIELDS:
            if field not in bundle.data['user']:
                raise UserApiBadRequest(field=field, message="Missing Parameter")

        userdata = bundle.data['user']
        email = retrieve_valid(userdata, 'email', EMAIL)
        first_name = retrieve_valid(userdata, 'first_name', ALPHA_NUM)
        last_name = retrieve_valid(userdata, 'last_name', ALPHA_NUM)
        username = retrieve_valid(userdata, 'username', ALPHA_NUM)
        password = retrieve_valid(userdata, 'email', REGEX_VALID_PASSWORD)
        groups = userdata['groups']

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

        #TODO: replace with custom auth
        superuser = False
        if bundle.request.user.is_superuser:
           superuser = True

        user = User.objects.get(pk=pk)

        #TODO:
        # move this to custom auth
        # if not superuser:
            # if bundle.request.user.id != pk:
            #   raise UserApiBadRequest(field='id', message="User can only edit self")

        user.first_name = first_name
        user.last_name = last_name

        if user.email != email:
            if not superuser:
                raise UserCannotEditError(field='email')
            else:
                user.email = email
            if user.username != username:
                raise UserCannotEditError(field='username')

        current_groups = [g.name for g in user.groups.all()]
        for cg in current_groups:
            if cg not in new_groups:
                if not superuser:
                    raise UserCannotEditError(field='groups')
                group.user_set.remove(user)
        for ng in new_groups:
            if ng not in current_groups:
                if not superuser:
                    raise UserCannotEditError(field='groups')
                group.user_set.add(user)

        user.save()
        bundle.obj = user

        return bundle
