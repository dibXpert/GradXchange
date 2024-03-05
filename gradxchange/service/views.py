from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service
from django.template import loader
from .forms import ServiceForm


# Function based view
app_name='service'
def index(request):
    service_list =  Service.objects.all()
    context = {
        'service_list':service_list,
    }
    return render(request, 'service/index.html', context)

def detail(request,service_id):
    service = Service.objects.get(pk=service_id)
    context = {
        'service':service,
    }
    return render(request, 'service/detail.html', context)

def create_service(request):
    form = ServiceForm(request.POST or None)
    
    if  form.is_valid():
        form.save()
        return redirect('service:index')
    
    return render(request, 'service/service-form.html', {'form':form})

def update_service(request,id):
    service = Service.objects.get(id=id)
    form = ServiceForm(request.POST or None, instance=service)
    
    if form.is_valid():
        form.save()
        return redirect('service:index')
    
    return render(request, 'service/service-form.html', {'form':form, 'service':service})
    
def delete_service(request,id):
    service = Service.objects.get(id=id)
    
    if request.method =='POST':
        service.delete()
        return redirect('service:index')
    
    return render (request, 'service/service-delete.html', {'service':service})