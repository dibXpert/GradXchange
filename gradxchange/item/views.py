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
from django.utils.dateparse import parse_date

from django.contrib.auth.models import User
from datetime import datetime, timedelta

def index(request):
    item_list = Item.objects.select_related('user_name').all().order_by('-created')  # Include related user data

    # Retrieve the tag from the URL parameter
    tag = request.GET.get('tag')
    if tag:
        item_list = item_list.filter(tags__name__in=[tag])

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    show_my_items = request.GET.get('show_my_items', 'off')

    search_type = request.GET.get('search_type')
    search_query = request.GET.get('search_query')

    # To store the active filter name and value for displaying in the template
    active_filter_name = None
    active_filter_value = None

    if search_type == 'item_name' and search_query:
        item_list = item_list.filter(item_name__icontains=search_query)
        active_filter_name = 'Item Name'
        active_filter_value = search_query
    elif search_type == 'seller_name' and search_query:
        item_list = item_list.filter(user_name__username__icontains=search_query)
        active_filter_name = 'Seller Name'
        active_filter_value = search_query

    if min_price and max_price:
        item_list = item_list.filter(item_price__gte=min_price, item_price__lte=max_price)
        active_filter_name = 'Price Range'
        active_filter_value = f"{min_price} to {max_price}"

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        item_list = item_list.filter(created__gte=start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
        item_list = item_list.filter(created__lt=end_date)  # Using __lt to include "just before midnight"

    if show_my_items == 'on':
        item_list = item_list.filter(user_name=request.user)
        active_filter_name = 'My Items'
        active_filter_value = 'My items'
    

   # Ensure pagination works with the current filters
    page_number = request.GET.get('page')
    paginator = Paginator(item_list, 12)  # Assuming 12 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'item_list': page_obj,
        'result_count': page_obj.paginator.count,
        'show_my_items': show_my_items,
        'active_filter_name': active_filter_name,
        'active_filter_value': active_filter_value,
        'tag': tag  # Optionally pass the tag to highlight it or use it in the template
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
    