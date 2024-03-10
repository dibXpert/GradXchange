from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
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

@login_required
def create_item(request):
    
   # Initialize form variable outside the if statement
    form = ItemForm()  # Create an instance of the form for GET requests
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Re-create instance for POST
        
        if form.is_valid():
            new_item = form.save(commit=False)  # Save the form temporarily without committing to the database
            new_item.user_name = request.user  # Set the user_name field to the currently logged in user
            new_item.save()  # Now save the item to the database
            return redirect('item:index') 
        else:
            context = {'form': form}
            return render(request, 'item/item-form.html', context)

    # This will now always be defined for GET requests
    return render(request, 'item/item-form.html', {'form': form})

@login_required
def update_item(request, id):
    # Use get_object_or_404 to handle cases where the item doesn't exist
    item = get_object_or_404(Item, id=id)

    # Check if the request is POST to handle form submission
    if request.method == 'POST':
        # Initialize the form with POST data and files, using the item instance
        form = ItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            # Save the updated item and associated file(s) if any
            form.save()
            # Redirect to a success page or item index
            return redirect('item:index')
    else:
        # If not POST, initialize the form with the item instance for editing
        form = ItemForm(instance=item)
    
    # Render the page with the form for both GET requests and invalid form submissions
    return render(request, 'item/item-form.html', {'form': form, 'item': item})

# def update_item(request,id):
#     item = Item.objects.get(id=id)
#     form = ItemForm(request.POST or None, instance=item)
    
#     if form.is_valid():
#         form.save()
#         return redirect('item:index')
    
#     return render(request, 'item/item-form.html', {'form':form, 'item':item})


@login_required
def delete_item(request,id):
    item = Item.objects.get(id=id)
    
    if request.method =='POST':
        item.delete()
        return redirect('item:index')
    
    return render (request, 'item/item-delete.html', {'item':item})
