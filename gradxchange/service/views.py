from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service
from django.template import loader
from .forms import ServiceForm

#pagination
from django.core.paginator import Paginator
#login required
from django.contrib.auth.decorators import login_required

# Function based view

def index(request):
    service_list =  Service.objects.all().order_by('service_name')
    
    #search
    service_name = request.GET.get('service_name')
    
    if service_name != '' and service_name is not None:
        service_list = service_list.filter(service_name__icontains=service_name)

    #pagination
    paginator = Paginator(service_list,4)
    page = request.GET.get('page')
    service_list = paginator.get_page(page)
        
    return render(request, 'service/index.html', {
        'service_list':service_list  })

def detail(request,pk):
    service = Service.objects.get(pk=pk)
    context = {
        'service':service,
    }
    return render(request, 'service/detail.html', context)

@login_required
def create_service(request):
    form = ServiceForm(request.POST or None)
    
    if  form.is_valid():
        form.save()
        return redirect('service:index')
    
    return render(request, 'service/service-form.html', {'form':form})

@login_required
def update_service(request,id):
    service = Service.objects.get(id=id)
    form = ServiceForm(request.POST or None, instance=service)
    
    if form.is_valid():
        form.save()
        return redirect('service:index')
    
    return render(request, 'service/service-form.html', {'form':form, 'service':service})

@login_required
def delete_service(request,id):
    service = Service.objects.get(id=id)
    
    if request.method =='POST':
        service.delete()
        return redirect('service:index')
    
    return render (request, 'service/service-delete.html', {'service':service})