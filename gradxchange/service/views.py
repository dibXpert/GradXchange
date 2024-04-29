from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Service
from .forms import ServiceForm
from .forms import CommentForm
from django.contrib import messages
from datetime import datetime, timedelta
#pagination
from django.core.paginator import Paginator
#login required
from django.contrib.auth.decorators import login_required

def index(request):
    service_list = Service.objects.select_related('user_name').all().order_by('-created')  # Include related user data

    # Retrieve the tag from the URL parameter
    tag = request.GET.get('tag')
    if tag:
        service_list = service_list.filter(tags__name__in=[tag])

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    show_my_services = request.GET.get('show_my_services', 'off')

    search_type = request.GET.get('search_type')
    search_query = request.GET.get('search_query')

    # To store the active filter name and value for displaying in the template
    active_filter_name = None
    active_filter_value = None

    if search_type == 'service_name' and search_query:
        service_list = service_list.filter(service_name__icontains=search_query)
        active_filter_name = 'service Name'
        active_filter_value = search_query
    elif search_type == 'seller_name' and search_query:
        service_list = service_list.filter(user_name__username__icontains=search_query)
        active_filter_name = 'Seller Name'
        active_filter_value = search_query

    if min_price and max_price:
        service_list = service_list.filter(service_price__gte=min_price, service_price__lte=max_price)
        active_filter_name = 'Price Range'
        active_filter_value = f"{min_price} to {max_price}"

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        service_list = service_list.filter(created__gte=start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
        service_list = service_list.filter(created__lt=end_date)  # Using __lt to include "just before midnight"

    if show_my_services == 'on':
        service_list = service_list.filter(user_name=request.user)
        active_filter_name = 'My Services'
        active_filter_value = 'My services'
    

   # Ensure pagination works with the current filters
    page_number = request.GET.get('page')
    paginator = Paginator(service_list, 12)  # Assuming 12 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'service_list': page_obj,
        'result_count': page_obj.paginator.count,
        'show_my_services': show_my_services,
        'active_filter_name': active_filter_name,
        'active_filter_value': active_filter_value,
        'tag': tag  # Optionally pass the tag to highlight it or use it in the template
    }
    return render(request, 'service/index.html', context)


def detail(request,pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.service = service
            new_comment.commented_by = request.user  # Ensure this is an authenticated user
            new_comment.save()
            messages.success(request, 'Your comment was added successfully!')

            return redirect(service.get_absolute_url())  # Redirect to the same page to show the new comment
        else:
            # If the form is not valid
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
        
    profile_id = service.user_name.profile.pk  # This gets the profile ID of the item owner to send a message
    
    # Find related service based on tags
    related_items = Service.objects.filter(tags__name__in=service.tags.names()).exclude(id=service.id).distinct()
    
    context = {
        'service':service,
        'comment_form': comment_form ,
        'profile_id': profile_id, 
        'related_services': related_items,
    }
    return render(request, 'service/detail.html', context)

@login_required
def create_service(request):
    
   # Initialize form variable outside the if statement
    form = ServiceForm()  # Create an instance of the form for GET requests
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)  # Re-create instance for POST
        
        if form.is_valid():
            new_service = form.save(commit=False)  # Save the form temporarily without committing to the database
            new_service.user_name = request.user  # Set the user_name field to the currently logged in user
            new_service.save()  
            messages.success(request, 'Service created successfully!')
            return redirect(reverse('account', kwargs={'username': request.user.username}))
        else:
            context = {'form': form}
            return render(request, 'service/service-form.html', context)


    return render(request, 'service/service-form.html', {'form': form})

@login_required
def update_service(request, id):
    # Use get_object_or_404 to handle cases where the service doesn't exist
    service = get_object_or_404(Service, id=id)

    # Check if the request is POST to handle form submission
    if request.method == 'POST':
        # Initialize the form with POST data and files, using the service instance
        form = ServiceForm(request.POST, request.FILES, instance=service)
        
        if form.is_valid():
            # Save the updated service and associated file(s) if any
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect(reverse('account', kwargs={'username': request.user.username}))

    else:
        # If not POST, initialize the form with the service instance for editing
        form = ServiceForm(instance=service)
    
    # Render the page with the form for both GET requests and invalid form submissions
    return render(request, 'service/service-form.html', {'form': form, 'service': service})

@login_required
def delete_service(request,id):
    service = Service.objects.get(id=id)
    
    if request.method =='POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect(reverse('account', kwargs={'username': request.user.username}))

    
    return render (request, 'service/service-delete.html', {'service':service})