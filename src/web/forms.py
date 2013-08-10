from django.forms import ModelForm
from web.models import Module


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'modulename', 'author', 'author_acronym', 'sourcecode', 'documentation', 'description']