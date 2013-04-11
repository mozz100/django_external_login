To install

    cd /root/of/your/django_project
    git submodule add git://github.com/mozz100/django_external_login.git external_login

In settings.py:

    # Use alternative authentication provider instead of default ('django.contrib.auth.backends.ModelBackend',)
    AUTHENTICATION_BACKENDS = ('external_login.backends.ExternalDBBackend',)

You should only give READ access to the credentials used.  Giving WRITE access is unecessary, and asking for trouble.

    # Provide connection details so this app can access the external database
    DATABASES['external_login'] = {
        'ENGINE': 'django.db.backends.xyz',     # Whatever you need to use - depends on the external DB
        'NAME': 'external_database_name',       # Or path to database file if using sqlite3.
        'USER': 'read_only_user',               # Not used with sqlite3.
        'PASSWORD': 'abracadabra',              # Not used with sqlite3.
        'HOST': 'external.db.provider.com',     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }

That should be it.

Limitations:

* Can't reset password - need to do that at the external source.
* Can't detect logged-in-ness at external site because of cookie domain restrictions.  Even if currently logged in there, must log in locally.
* No sync of data - if you change your username or email in the remote DB, no way to find out here.  That would be easy to script but might cause confusion.
