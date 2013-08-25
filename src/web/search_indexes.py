import datetime
from haystack import indexes
from web.models import Module

class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    created = indexes.DateTimeField(model_attr='created')
    #tags = indexes.ManyToManyField(Tag, related_name="tagged_modules")
    version = indexes.IntegerField(model_attr='version')
    average_rating = indexes.IntegerField(model_attr='average_rating')
    uniquename = indexes.CharField(model_attr='uniquename')
    modulename = indexes.CharField(model_attr='modulename')
    

    def get_model(self):
        return Module

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(finished=True)