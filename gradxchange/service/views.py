from django.shortcuts import render
from django.http import HttpResponse
from .models import Service
from django.template import loader


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
    