from django.shortcuts import render
from django.http import HttpResponse
from .models import Service
from django.template import loader


# Create your views here.


def index(request):
    service_list = Service.objects.all()
    template = loader.get_template('service/index.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))


def services(request):
    return HttpResponse("this is an services view")
