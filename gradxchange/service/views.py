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
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone


def index(request):
    service_list = Service.objects.select_related('user_name').filter(status=Service.Status.AVAILABLE).annotate(likes_count=Count('liked_by')).order_by('-created')  # Include related user data

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

    # Adjust price filter to allow independent min and max 
    if min_price:
        service_list = service_list.filter(service_price__gte=min_price)
        active_filter_name = 'Minimum Price'
        active_filter_value = f"RM {min_price}+"
    if max_price:
        service_list = service_list.filter(service_price__lte=max_price)
        active_filter_name = 'Maximum Price'
        active_filter_value = f"Up to RM {max_price}"
        

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        service_list = service_list.filter(created__gte=start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = timezone.make_aware(end_date, timezone.get_default_timezone())
        end_date = end_date+ timedelta(days=1) - timedelta(seconds=1)
        service_list = service_list.filter(created__lt=end_date)

    if show_my_services == 'on':
        service_list = service_list.filter(user_name=request.user)
        active_filter_name = 'My Services'
        active_filter_value = 'My services'
    

   # Ensure pagination works with the current filters
    page_number = request.GET.get('page')
    paginator = Paginator(service_list, 12)  # Assuming 12 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'service_list': page_obj,# Make sure pagination still works with the annotated queryset
        'result_count': page_obj.paginator.count,
        'show_my_services': show_my_services,
        'active_filter_name': active_filter_name,
        'active_filter_value': active_filter_value,
        'tag': tag,  # Optionally pass the tag to highlight it or use it in the template
        'start_date': start_date,  # Pass start_date to the template
        'end_date': end_date,  # Pass end_date to the template
        'min_price': min_price,  # Pass min_price to the template
        'max_price': max_price,  # Pass max_price to the template
    }
    return render(request, 'service/index.html', context)


def detail(request,pk):
    service = get_object_or_404(Service, pk=pk)
    
    update_breadcrumb(request, service.service_name, request.path)

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
    
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = service.liked_by.filter(id=request.user.id).exists()
    
    context = {
        'service':service,
        'comment_form': comment_form ,
        'profile_id': profile_id, 
        'related_services': related_items,
        'user_has_liked':  user_has_liked,
    }
    return render(request, 'service/detail.html', context)

def update_breadcrumb(request, name, url):
    # Get the current breadcrumb list from session, or initialize it if it doesn't exist
    breadcrumb = request.session.get('breadcrumb', [])
    
    # Check if the current URL already exists in the breadcrumb trail
    if breadcrumb and breadcrumb[-1]['url'] == url:
        # Avoid duplicating the last entry if the page was refreshed
        pass
    else:
        # Check for existing entries and remove the oldest if length is already 5
        breadcrumb.append({'name': name, 'url': url})
        if len(breadcrumb) > 5:
            breadcrumb = breadcrumb[-5:]  # Keep only the last 5 elements
    
    # Update the session
    request.session['breadcrumb'] = breadcrumb

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
            form.save_m2m()  # Save the many-to-many data for the form, including tags
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
            return render(request, 'service/service-form.html', {'form': form, 'service': service})

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

#liked by users
@login_required
def like_service(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        
        if service.liked_by.filter(id=request.user.id).exists():
            service.liked_by.remove(request.user)
            liked = False
        else:
            service.liked_by.add(request.user)
            liked = True

        print(f"User {request.user.username} {'liked' if liked else 'unliked'} the service.")
        print(f"Total likes now: {service.liked_by.count()}")

        return JsonResponse({
            'liked': liked,
            'total_likes': service.liked_by.count()
        })
    else:
        return HttpResponse(status=405)  # Method not allowed
    
def change_status(request, service_id, new_status):
    service = get_object_or_404(Service, id=service_id)
    if request.user == service.user_name:
        service.status = new_status
        service.save()
    else:
        messages.error(request, 'You are not authorized to change the status of this service.')
    # return redirect('item:detail', pk=item.pk)
    return redirect(reverse('account', kwargs={'username': request.user.username}))

def relist_service(request, pk):
    original_service = get_object_or_404(Service, pk=pk)
    
    if request.user != original_service.user_name:
        messages.error(request, "You are not authorized to re-list this item.")
        return redirect('service:index', pk=pk)

    # Clone the item
    new_service = Service.objects.get(pk=pk)
    new_service.pk = None  # Reset the primary key to create a new object
    new_service.status = Service.Status.AVAILABLE  # Set status to available
    new_service.save()

    messages.success(request, "Service re-listed successfully. A new listing has been created.")
    # return redirect('item:detail', pk=new_item.pk)  # Redirect to the new item's detail page
    return redirect(reverse('account', kwargs={'username': request.user.username}))