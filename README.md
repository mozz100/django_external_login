# django_external_login

Allow your users to log in using the same username/password they already use on another Django site.

You've got one Django site, with registered users.  You want to run another one, at a different domain, but don't
want your users to have to remember multiple logins (even though most of them probably use the same username/password
everywhere, right?).  This code is how I did it.

Requires you to allow access to the 'master' database to a set of credentials that can be used by the 'slave'.
Read-only access to the auth_user table is all that's required, and all that I'd recommend you to allow.

If you can't arrange that, you'll have to find some other way to achieve 'external authentication'.

Make sure you read the limitations section below.

## How it works (briefly)

Provides a new authentication backend.  See https://docs.djangoproject.com/en/1.4/topics/auth/#writing-an-authentication-backend

Accesses the 'master' database when users authenticate, fetching their (hashed)
password by looking it up using the username supplied.  If the supplied password passes Django's normal checks, *against
the details from the master database*, the user is treated as authenticated.

The first time each user logs in this way, a *local* User object is created, so that your 'slave' app can create
objects belonging to the users, and foreign key relationships can be set up, etc.

## To install

Place the code into your project. If you track your project in git, here's how to add this repo as a submodule.

    cd /root/of/your/django_project
    git submodule add git://github.com/mozz100/django_external_login.git external_login
    
If you don't use git, clone this repo and then copy its contents to your django project directory as `external_login`.

Then make changes to `settings.py` to use the new auth backend and provide connection details to the 'master' Django installation:

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

## Limitations:

* Only tried with Django 1.4 so far.
* Can't reset password - need to do that at the external source.
* Can't detect logged-in-ness at external site because of cookie domain restrictions.  Even if currently logged in there, must log in locally.
* No sync of data - if you change your username or email in the remote DB, no way to find out here.  That would be easy to script but might cause confusion.
* Currently, no intelligent behaviour if external authentication fails.  Future versions could fall back and try authentication in the *local* database, or do so for users with x permission.
* Probably (almost certainly) will go screwy if you use different versions of Django in the two sites.
