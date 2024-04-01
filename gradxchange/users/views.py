from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from .models import Profile, Message
from .forms import UserEditForm, ProfileEditForm, MessageForm
from django.contrib.auth.models import User

#item
from item.models import Item 
#service
from service.models import Service



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account are created')
            return redirect('login')
    else:
        form = SignupForm()
    return render (request, 'users/signup.html',{'form':form})

@login_required
def accountPage(request,username):
    user = get_object_or_404(User, username= username)
    user_items = Item.objects.filter(user_name= user)  # Query items belonging to the logged-in user
    user_services = Service.objects.filter(user_name= user)
    profile = get_object_or_404(Profile, user=user)
    # Check if the currently logged-in user is viewing their own account
    is_own_account = request.user == user
    
    context = {
        'user':user,
        'user_items':user_items,
        'user_services':user_services,
        'is_own_account': is_own_account,  # Pass the flag to the template
        'profile_id': profile.id,  # Add the profile ID to the context
    }
    
    return render(request,'users/account.html', context)


#edit profile
@login_required
def edit(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user,data=request.POST) # data from posted data, instance from form data
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES) #  profile from currently logged in user
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account')
    
    else:
        #request method is "GET", data from currently logged in user
        user_form = UserEditForm(instance=request.user) 
        profile_form = ProfileEditForm(instance=request.user.profile ) 
    
    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})
        
@login_required  
def inbox(request):
    profile =  request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':  messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required  
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    #create date read 
    context = {'message':message}
    return render(request, 'users/message.html' , context)

@login_required
def createMessage(request, profile_id):
    recipient = get_object_or_404(Profile, id=profile_id)
    form = MessageForm()  # Initialize the form outside the POST check to handle GET requests

   # if request.user.profile.id == recipient.id:
      #  messages.error(request, "You cannot send a message to yourself.")
       # return redirect('error')  # Adjust with your own redirect target

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            #  want to use the User's first and last name as the sender's name
            message.name = request.user.first_name + " " + request.user.last_name
            message.email = request.user.email  # User's email as the sender's email
            message.sender = request.user.profile
            message.recipient = recipient
            message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('item:index')  # Redirect to a confirmation page

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)

