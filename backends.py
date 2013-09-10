from django.conf import settings
from django.contrib.auth.models import User, check_password
from models import ExternalUser

class ExternalDBBackend(object):
    """
    Authenticate against external database, instead of local, but return a local User object.
    Based on https://docs.djangoproject.com/en/1.4/topics/auth/#writing-an-authentication-backend
    """

    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        # Use our connection to the external database to authenticate the user
        credentials_valid = False # let's assume the worst, it's more secure that way
        try:
            # look up user in the external database, and attempt password check
            external_user = ExternalUser.objects.using("external_login").get(username=username)
            credentials_valid = check_password(password, external_user.password)
        except ExternalUser.DoesNotExist:
            external_user = None
            credentials_valid = False

        if credentials_valid:
            try:
                # look for local user, create if necessary
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from the external database will.
                user = User(username=username)
                # in fact, let's set the password to Django's proper 'unusable' one
                user.set_unusable_password()
                # TODO: copy attributes from the remote database to the local User model
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None