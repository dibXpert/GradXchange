from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea
from .models import Profile, Message
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username", error_messages={'required': 'Username is required'})
    password = forms.CharField(label="Password", widget=forms.PasswordInput, error_messages={'required': 'Password is required'})

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
        fields = ('image','location','phone','whatsapp')

#edit about me
class AboutEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('about_me',)
        widgets = {
            'about_me': Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust the size as needed
        }

#create message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']