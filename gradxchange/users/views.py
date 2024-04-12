from django.shortcuts import redirect,render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from .models import Profile, Message
from .forms import UserEditForm, ProfileEditForm, AboutEditForm,MessageForm
from django.contrib.auth.models import User
from .forms import CustomAuthenticationForm
from django.contrib.auth import authenticate, login
#item
from item.models import Item 
#service
from service.models import Service


def custom_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

#home page
def home(request):
    return render (request, 'users/home.html')
    

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
            messages.success(request, "Your Profile was updated successfully!")
            return redirect(reverse('account', kwargs={'username': request.user.username}))
    else:
        #request method is "GET", data from currently logged in user
        user_form = UserEditForm(instance=request.user) 
        profile_form = ProfileEditForm(instance=request.user.profile ) 
    
    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})

#edit-about me 
@login_required
def edit_about(request):
    if request.method=='POST':
        about_form = AboutEditForm(instance=request.user.profile,data=request.POST) # data from posted data, instance from form data
        
        if about_form.is_valid() :
            about_form.save()  
            messages.success(request, "Your About Me was updated successfully!")
            return redirect(reverse('account', kwargs={'username': request.user.username}))


    else:       
        about_form = AboutEditForm(instance=request.user.profile) 
    return render(request,'users/edit.html',{'about_form':about_form,})
        


@login_required  
def inbox(request):
    request.session['last_page'] = 'inbox'
    profile = request.user.profile
    messageRequests = Message.objects.filter(recipient=profile)
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount
    }
    return render(request, 'users/inbox.html', context)

@login_required  
def viewMessage(request, pk):
    message = get_object_or_404(Message, pk=pk)
    # Mark as read only if the current user is the recipient and not the sender
    if message.recipient == request.user.profile and not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)

@login_required
def createMessage(request, profile_id):
    recipient = get_object_or_404(Profile, id=profile_id)
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = recipient
            message.is_read = False  # Ensure the message is marked as unread
            message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect(reverse('inbox'))  # Or any other appropriate redirect
    else:
        form = MessageForm()

    context = {
        'form': form,
        'recipient': recipient
    }
    return render(request, 'users/message_form.html', context)

@login_required
def send_message(request, profile_id):
    recipient = get_object_or_404(Profile, id=profile_id)
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = recipient
            message.is_read = False  # Ensure the message is marked as unread
            message.save()
            messages.success(request, "Your reply has been sent successfully!")
            return redirect('inbox')  # Redirect to the inbox after sending
    else:
        form = MessageForm()

    context = {
        'form': form,
        'recipient': recipient
    }
    return render(request, 'users/message_form.html', context)

@login_required
def sent_messages(request):
    request.session['last_page'] = 'sent_messages'
    current_user_profile = request.user.profile  # Access the user's profile
    sent_messages = Message.objects.filter(sender=current_user_profile).order_by('-created')  # Get all sent messages

    context = {
        'sent_messages': sent_messages
    }
    return render(request, 'users/sent_messages.html', context)