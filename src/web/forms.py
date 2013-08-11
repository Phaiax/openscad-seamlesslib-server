from django.core.validators import RegexValidator
from django.forms import ModelForm
from web.models import Module
import re


class ModuleForm(ModelForm):
    def clean_sourcecode(self):
        self.validate_sourcecode_contains_module_definition()
        return self.cleaned_data['sourcecode']
        
    def validate_sourcecode_contains_module_definition(self):
        regex = r"^\s*" + re.escape("module") + "\s+" + re.escape(self.data['modulename']) + r"\s*\("
        RegexValidator(regex, message=
            "Your sourcecode should contain a module with the same "
             "name as you defined in the \"%s\" field: \n %s" % 
             (self.fields['modulename'].label, self.data['modulename'])) (self.cleaned_data['sourcecode'])

    class Meta:
        model = Module
        fields = ['title', 'modulename', 'author', 'author_acronym', 'sourcecode', 'documentation', 'description']