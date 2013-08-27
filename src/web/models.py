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
    guid = models.CharField(db_index=True, max_length = 36)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    author = models.CharField(max_length = 40, help_text="The acronym should be a little two or three character shortcut for your name. It is used to generate the unique name (~acronym-modulename-version) later.")
    
    author_acronym = models.CharField(max_length = 6)
    created = models.DateTimeField(db_index=True, auto_now_add = True)
    finished = models.BooleanField(default = False)
    sourcecode = models.TextField(help_text="""
        <strong>Commiting this sourcecode you irrevocably agree to release your contribution under the CC-BY-SA 3.0 License and the GPLv2.</strong>
        <p>
        Some tips to make a good and reusable module:
        <ul><li>Don't use global variables! They can cause confusion if they override variables used in the calling script.</li>
        <li>If your sourcecode contains multiple modules, it's probably the best to move them into your main module (yes, that's possible).</li>
        <li>Use parameters to make your module more flexible.</li>
        <li>Parameters like spacing for bores or $fn for detailism are always welcome.</li>
        </ul></p> 
    """)
    documentation = models.TextField(help_text = "You can use your own module name for examples or copy the new unique module name (~author-modulename-version) from above to simplify work for the users of your work.")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tagged_modules")
    version = models.IntegerField(default = 1)
    modulename = models.CharField(max_length = 40, 
                                  validators=[RegexValidator(r"^[a-zA-Z]{1}[a-zA-Z0-9_]*$")],
                                  help_text='The module name is used to find your module in the sourcecode and replace it with its unique name (~author-modulename-version) later.')
    auth_code = models.CharField(max_length = 36)
    average_rating = models.FloatField(db_index=True, default = 0)
    number_of_ratings = models.IntegerField(default = 0)
    uniquename = models.CharField(db_index=True, max_length = 100, default='')
     
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
                    m = Module.objects.get(uniquename=self.uniquename)
                    if m.pk == self.pk:
                        raise Module.DoesNotExist
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
        
    def get_rating_url(self, rate):
        return reverse('rate', kwargs={'uuid': self.guid, 'rating' : rate.__str__()})
        
    def __str__(self):
        return "%s (%s)" % (self.uniquename, self.title)