# Create your views here.
from django.core import urlresolvers
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from web.forms import ModuleForm
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
    rating_links = [(i, M.get_rating_url(i)) for i in range(0,11)]
    return render(request, 'web/views/show.html',
                  {'module':M, 
                   'rating_links' : rating_links
                   })

def rate(request, uuid, rating):
    try:
        rating = int(float(rating))
    except:
        raise Http404
    if rating < 0 or 10 < rating:
        raise Http404 
    M = get_object_or_404(Module.objects, guid=uuid)
    M.average_rating = ( (M.average_rating * M.number_of_ratings) + rating ) / (M.number_of_ratings + 1)
    M.number_of_ratings = M.number_of_ratings + 1
    M.save()
    return redirect(M)