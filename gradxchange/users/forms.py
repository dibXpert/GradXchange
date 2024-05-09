from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea
from .models import Profile, Message
from django.contrib.auth import get_user_model

User = get_user_model()

#This form inherits from Django's UserCreationForm and adds additional fields such as email, first_name, and last_name. This extended form is used to collect extra information during the user registration process, facilitating a more detailed user profile from the outset.
class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

#edit user
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        
        
#edit user profile
class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('location','phone','whatsapp')

#edit about me
class AboutEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('image','about_me',)
        widgets = {
            'about_me': Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust the size as needed
        }

#create message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']