
from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # in memory db with tests
    }
}

ALLOWED_HOSTS.append('testserver')