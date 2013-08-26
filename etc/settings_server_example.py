
from settings import *
import os.path

DEBUG = False
TEMPLATE_DEBUG = DEBUG




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "/home/MMMMMMMMMMM/html/static"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q34tJ/(oTzQ$34t&$/5ue6sFghS4%56uw5wgSDfghk78W%h24%z2$z3689089=P'

import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': '/home/MMMMMMMMMMMM/xapian_index',
    },
}
