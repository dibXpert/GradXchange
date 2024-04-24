from django import forms
from .models import Service, Comment
from taggit.forms import TagField
from django.core.exceptions import ValidationError

class ServiceForm(forms.ModelForm):
    tags = TagField(required=False, help_text="Enter comma-separated tags")


    class Meta:
        model = Service
        fields = ['service_name', 'service_desc', 'service_detail','service_price','service_image','tags']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'service_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'service_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'service_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
        def clean_service_price(self):
            service_price = self.cleaned_data['service_price']
            if service_price < 0:
                 raise ValidationError('Price cannot be negative.')
            return service_price
    
        labels = {
            'service_name': "Service's Name",
            'service_desc': "Service's Description",
            'service_detail': "Service's Details",
            'service_price': "Service's Price",
            'service_image': "Service's Image",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
       