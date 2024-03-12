from django import forms
from .models import Item, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_price','item_image']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'commented_by']