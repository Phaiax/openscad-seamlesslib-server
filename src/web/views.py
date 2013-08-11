# Create your views here.
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from web.forms import ModuleForm
from django.core import urlresolvers
from web.models import Module

def home(request):
    top_rated_modules = Module.objects.order_by('-average_rating')[0:10]
    last_added_modules = Module.objects.order_by('-created')[0:10]
    return render(request, 'web/views/index.html', {'top_rated_modules' : top_rated_modules,
                                                    'last_added_modules' : last_added_modules})

def add(request):
    if request.method == "POST":
        moduleform = ModuleForm(request.POST)
        if moduleform.is_valid():
            moduleform.save()
            return HttpResponseRedirect(
                        urlresolvers.reverse('show',  
                        kwargs={ 'uuid' : moduleform.instance.guid.__str__()}))
    else:
        moduleform = ModuleForm()
    return render(request, 'web/views/add.html', {'newmoduleform' : moduleform})

def show(request, uuid):
    M = get_object_or_404(Module.objects, guid=uuid)
    return render(request, 'web/views/show.html', {'module':M})
