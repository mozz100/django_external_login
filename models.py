from django.contrib.auth.models import User

class ExternalUser(User):

    class Meta:
        app_label = 'auth'
        db_table = 'auth_user'
        proxy = True # see https://docs.djangoproject.com/en/1.4/topics/db/models/#proxy-models
