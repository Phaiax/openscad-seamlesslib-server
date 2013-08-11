from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
import uuid

class Tag(models.Model):
    name = models.CharField(max_length = 30)


# Create your models here.
class Module(models.Model):
    guid = models.CharField(max_length = 36)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    author = models.CharField(max_length = 40)
    author_acronym = models.CharField(max_length = 6)
    created = models.DateTimeField(auto_now_add = True)
    finished = models.BooleanField(default = False)
    sourcecode = models.TextField()
    documentation = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="tagged_modules")
    version = models.IntegerField(default = 1)
    modulename = models.CharField(max_length = 40, validators=[RegexValidator(r"^[a-zA-Z]{1}[a-zA-Z0-9]*$")])
    auth_code = models.CharField(max_length = 36)
    average_rating = models.FloatField(default = 0)
    number_of_ratings = models.IntegerField(default = 0)
    uniquename = models.CharField(max_length = 100, default='')
     
    class Admin(admin.ModelAdmin):
        list_display = ['modulename', 'version', 'author_acronym', 'finished']
    def save(self, *args, **kwargs):
        if not self.pk:
            self.guid = uuid.uuid4().__str__()
            self.auth_code = uuid.uuid4().__str__()
        if not self.finished:
            random_tail = ''
            while True:
                self.uniquename = self.generate_uniquename(random_tail)
                try:
                    Module.objects.get(uniquename=self.uniquename)
                    random_tail = uuid.uuid4().__str__()
                except Module.DoesNotExist:
                    break
        super(Module, self).save(*args, **kwargs)

    def generate_uniquename(self, tail = ''):
        if tail is not '':
            tail = '-' + tail
        if len(tail) > 5:
            tail = tail[0:5]
        # max 100 chars: 1 + 6 + 1 + 40 + 2 + 10 + 5 = 65
        # 012345678901234567890123456789012345678901234567890123456789012345
        return "~%s-%s-v%d%s" % (self.author_acronym, self.modulename, self.version, tail) 

    def clean(self):
        super(Module, self).clean()
        
    def get_absolute_url(self):
        return reverse('show', kwargs={'uuid': self.guid})
        
        