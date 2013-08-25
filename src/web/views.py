# Create your views here.
from django.core import urlresolvers
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from web.forms import ModuleForm
from web.models import Module


def get_redirect_to_edit_page(module):
    return HttpResponseRedirect(
            urlresolvers.reverse('edit',  
                kwargs={ 'uuid' : module.guid.__str__(),
                         'auth_code' : module.auth_code.__str__()})) 
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
            return get_redirect_to_edit_page(moduleform.instance)
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

def edit_without_auth(request, uuid):
    M = get_object_or_404(Module.objects, guid=uuid, finished=False)
    if request.method == "POST":
        if M.auth_code == request.POST['auth_code']:
            return get_redirect_to_edit_page(M) 
    return render(request, 'web/views/edit_without_auth.html',
                  {'module': M})
    
    
def edit(request, uuid, auth_code):
    M = get_object_or_404(Module.objects, guid=uuid, finished=False, auth_code=auth_code)
    if request.method == "POST" \
        and (request.POST.has_key('savemodule') \
             or request.POST.has_key('finishmodule')):
        moduleform = ModuleForm(request.POST, instance=M)
        if moduleform.is_valid():
            M = moduleform.save()
            if request.POST.has_key('finishmodule'):
                M.finished = True;
                M.save()
                return HttpResponseRedirect(
                    urlresolvers.reverse('show',  
                    kwargs={ 'uuid' : M.guid.__str__()}))
            return get_redirect_to_edit_page(M)
    else:
        moduleform = ModuleForm(instance = M)
    return render(request, 
                  'web/views/edit.html', 
                  {'module': M,
                   'moduleform': moduleform})
    
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