from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#profile
from .models import Profile, Message

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
        fields = ('image','location','phone',)

#edit about me
class AboutEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('about_me',)

#create message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject','body']