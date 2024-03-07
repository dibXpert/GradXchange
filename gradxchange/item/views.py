from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
#class based view
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Item
from .forms import ItemForm

#class based view
class IndexClassView(ListView):
    model = Item
    template_name = 'item/index.html'
    context_object_name = 'item_list'
    
    
class ItemDetail(DetailView):
    model = Item
    template_name = 'item/detail.html'
    
class CreateItem(CreateView):
    model = Item
    fields = ['item_name','item_desc','item_price','item_image']
    template_name = 'item/item-form.html'
    
    def form_valid(self, form):
        form.instance.user_name = self.request.user
        
        return super().form_valid(form)
    
        
    

    
def delete_item(request,id):
    item = Item.objects.get(id=id)
    
    if request.method =='POST':
        item.delete()
        return redirect('item:index')
    
    return render (request, 'item/item-delete.html', {'item':item})
