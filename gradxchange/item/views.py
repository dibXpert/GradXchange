from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from django.template import loader


def index(request):
    item_list =  Item.objects.all()
    context = {
        'item_list':item_list,
    }
    return render(request, 'item/index.html', context)


def item(request):
    return HttpResponse("This is item page")

def detail(request,item_id):
    item = Item.objects.get(pk=item_id)
    context = {
        'item':item,
    }
    return render(request, 'item/detail.html', context)
    