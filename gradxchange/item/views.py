from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
# #class based view
# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView

from .models import Item
from .forms import ItemForm

# #class based view
# class IndexClassView(ListView):
#     model = Item
#     template_name = 'item/index.html'
#     context_object_name = 'item_list'
    
    
# class ItemDetail(DetailView):
#     model = Item
#     template_name = 'item/detail.html'
    
# class CreateItem(CreateView):
#     model = Item
#     fields = ['item_name','item_desc','item_price','item_image']
#     template_name = 'item/item-form.html'
    
#     def form_valid(self, form):
#         form.instance.user_name = self.request.user
        
#         return super().form_valid(form)
    

from django.core.paginator import Paginator

# Function based view
def index(request):
    item_list =  Item.objects.all().order_by('item_name') #change to -created_at later
    
    #search
    item_name = request.GET.get('item_name')
    
    if item_name != '' and item_name is not None:
        item_list = item_list.filter(item_name__icontains=item_name)

    #pagination
    paginator = Paginator(item_list,4)
    page = request.GET.get('page')
    item_list = paginator.get_page(page)
        
    return render(request, 'item/index.html', {
        'item_list':item_list  })

def detail(request,pk):
    item = Item.objects.get(pk=pk)
    context = {
        'item':item,
    }
    return render(request, 'item/detail.html', context)

def create_item(request):
    form = ItemForm(request.POST or None)
    
    if  form.is_valid():
        form.save()
        return redirect('item:index')
    
    return render(request, 'item/item-form.html', {'form':form})


def update_item(request,id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)
    
    if form.is_valid():
        form.save()
        return redirect('item:index')
    
    return render(request, 'item/item-form.html', {'form':form, 'item':item})

    
def delete_item(request,id):
    item = Item.objects.get(id=id)
    
    if request.method =='POST':
        item.delete()
        return redirect('item:index')
    
    return render (request, 'item/item-delete.html', {'item':item})
