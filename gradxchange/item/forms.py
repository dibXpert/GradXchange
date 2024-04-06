from django import forms
from .models import Item, Comment
from taggit.forms import TagField


class ItemForm(forms.ModelForm):
    tags = TagField(required=False, help_text="Enter comma-separated tags")


    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_detail','item_price','item_image','tags']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'item_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'item_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'item_name': "Item's Name",
            'item_desc': "Item's Description",
            'item_detail': "Item's Details",
            'item_price': "Item's Price",
            'item_image': "Item's Image",
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
       