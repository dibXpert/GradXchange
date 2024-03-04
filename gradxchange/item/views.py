from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#class based view
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Item


class IndexClassView(ListView):
    model = Item
    template_name = 'item/index.html'
    context_object_name = 'item_list'
    
class ItemDetail(DetailView):
    model = Item
    template_name = 'item/detail.html'