from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
# #class based view
# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView

from django.urls import reverse

from .models import Item
from .forms import ItemForm
from .forms import CommentForm

from django.core.paginator import Paginator

# Function based view
def index(request):

    item_list =  Item.objects.all().order_by('-created',) 
    
    #search
    item_name = request.GET.get('item_name')
    
    if item_name != '' and item_name is not None:
        item_list = item_list.filter(item_name__icontains=item_name)


    # Count the results after filtering
    result_count = item_list.count()
    
    #pagination
    paginator = Paginator(item_list,12)
    page = request.GET.get('page')
    item_list = paginator.get_page(page)
        
    context = {
         'item_list':item_list, 'result_count': result_count,'item_name': item_name,
        
    }
    return render(request, 'item/index.html', context)

def detail(request,pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = item
            new_comment.commented_by = request.user  # Ensure this is an authenticated user
            new_comment.save()
            messages.success(request, 'Your comment was added successfully!')

            return redirect(item.get_absolute_url())  # Redirect to the same page to show the new comment
        else:
            # If the form is not valid
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
        
    profile_id = item.user_name.profile.pk  # This gets the profile ID of the item owner to send a message
    
    # Find related items based on tags
    related_items = Item.objects.filter(tags__name__in=item.tags.names()).exclude(id=item.id).distinct()
    
    context = {
        'item':item,
        'comment_form': comment_form ,
        'profile_id': profile_id, 
        'related_items': related_items,
    }
    return render(request, 'item/detail.html', context)

@login_required
def create_item(request):
    form = ItemForm()  # Create an instance of the form for GET requests
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Re-create instance for POST
        
        if form.is_valid():
            new_item = form.save(commit=False)  # Save the form temporarily without committing to the database
            new_item.user_name = request.user  # Set the user_name field to the currently logged in user
            new_item.save()  # Now save the item to the database
            # form.save_m2m()  # Save the many-to-many data for the form
            messages.success(request, 'Item created successfully!')
             # Redirect the user back to their account page
            return redirect(reverse('account', kwargs={'username': request.user.username}))
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
            form.save()
            messages.success(request, 'Item updated successfully!')  # Add success message

            # Instead of redirecting, re-render the page with the form
            # This keeps the user on the current page and shows the success message
            return render(request, 'item/item-form.html', {'form': form, 'item': item})
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
        messages.success(request, 'Item deleted successfully!')
        return redirect(reverse('account', kwargs={'username': request.user.username}))

    
    return render (request, 'item/item-delete.html', {'item':item})

#liked by users
@login_required
def like_item(request):
    item_id = request.POST.get('item_id')
    item= get_object_or_404(Item,id=item_id)
    
    if item.liked_by.filter(id=request.user.id).exists():
        item.liked_by.remove(request.user)
    else:
        item.liked_by.add(request.user)
    return redirect('item:index')



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
    