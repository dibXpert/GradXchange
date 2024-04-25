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

from django.db.models import Q, Max


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
        
def redirectToWhatsApp(request, whatsapp_number):
    # Construct the WhatsApp URL
    whatsapp_url = f'https://wa.me/{whatsapp_number}'
    return redirect(whatsapp_url)


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
            # Stay on the chat page by redirecting to the current chat page
            return redirect(reverse('chat', kwargs={'profile_id': profile_id}))
    else:
        form = MessageForm()

    context = {
        'form': form,
        'recipient': recipient
    }
    return render(request, 'users/message_form.html', context)

@login_required
def inbox(request):
    profile = request.user.profile
    search_query = request.GET.get('search', '')

    # Fetching other users based on conversations
    other_users = Profile.objects.filter(
        Q(sent_messages__recipient=profile) | Q(received_messages__sender=profile)
    ).distinct().exclude(id=profile.id)

    # Apply search filter if present
    if search_query:
        other_users = other_users.filter(user__username__icontains=search_query)

    # Collect conversations
    conversations = []
    for user in other_users:
        try:
            last_message = Message.objects.filter(
                Q(sender=profile, recipient=user) | Q(sender=user, recipient=profile)
            ).latest('created')
            conversations.append({
                'other_party': user,
                'last_message': last_message
            })
        except Message.DoesNotExist:
            continue  # Continue if no messages are found, although unlikely

    unread_count = Message.objects.filter(recipient=profile, is_read=False).count()

    context = {
        'conversations': conversations,
        'unreadCount': unread_count,
        'search_query': search_query
    }
    return render(request, 'users/inbox.html', context)


@login_required
def chat(request, profile_id):
    user_A = request.user.profile  # Current logged-in user
    user_B = get_object_or_404(Profile, id=profile_id)  # Recipient obtained from URL parameter

    # Get all messages between user_A and user_B
    messages = Message.objects.filter(
        Q(sender=user_A, recipient=user_B) | Q(sender=user_B, recipient=user_A)
    ).order_by('created')

    # Mark messages as read when the chat is opened
    Message.objects.filter(sender=user_B, recipient=user_A, is_read=False).update(is_read=True)

    context = {
        'messages': messages,
        'user_A': user_A,
        'user_B': user_B,
        'profile_id': profile_id,  # Pass the profile_id to the template
    }
    return render(request, 'users/chat.html', context)

