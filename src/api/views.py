# Create your views here.
from django.shortcuts import get_object_or_404
from web.models import Module
from django.http.response import HttpResponse
from django.utils import simplejson
from seamless.version import versioninfo

def get_by_uniquename(request, uniquename):
    module = get_object_or_404(Module, uniquename=uniquename)
    jsonresponse = {
        'guid' : module.guid,
        'title' : module.title,
        'description' : module.description,
        'author' : module.author,
        'author_acronym' : module.author_acronym,
        'created' : module.created.isoformat(),
        'finished' : module.finished,
        'sourcecode' : module.sourcecode,
        'documentation' : module.documentation,
        'version' : module.version,
        'modulename' : module.modulename,
        'average_rating' : module.average_rating,
        'number_of_ratings' : module.number_of_ratings,
        'uniquename' : module.uniquename
    }
    return HttpResponse(simplejson.dumps(jsonresponse, encoding="UTF-8"), content_type="application/json")

def version_info(request):
    return HttpResponse(simplejson.dumps(versioninfo, encoding="UTF-8"), content_type="application/json")