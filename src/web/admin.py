

from django.contrib import admin
from web.models import Tag, Module

admin.site.register(Tag)
admin.site.register(Module, Module.Admin)