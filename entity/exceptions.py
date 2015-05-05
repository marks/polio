from tastypie.exceptions import TastypieError, ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted

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
