from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Service
from .forms import ServiceForm
from .forms import CommentForm
from django.contrib import messages

#pagination
from django.core.paginator import Paginator
#login required
from django.contrib.auth.decorators import login_required

# Function based view

def index(request):
    service_list =  Service.objects.all().order_by('-created')
    
    #search
    service_name = request.GET.get('service_name')
    
    if service_name != '' and service_name is not None:
        service_list = service_list.filter(service_name__icontains=service_name)

    # Count the results after filtering
    result_count = service_list.count()
    
    #pagination
    paginator = Paginator(service_list,12)
    page = request.GET.get('page')
    service_list = paginator.get_page(page)
    
    context = {
         'service_list':service_list, 'result_count': result_count,'service_name': service_name,
        
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