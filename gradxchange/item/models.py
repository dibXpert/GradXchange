from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal

class Item(models.Model):
    
    def __str__(self):
        return self.item_name
    
    tags = TaggableManager()


    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_detail = models.CharField(max_length=2000)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    item_image = models.ImageField(upload_to='images_item', default="notfound.png")
    created =  models.DateTimeField(auto_now_add=True)
    #user's item
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    
    #people that liked the item
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='item_liked',blank= True)
   
    #item's detail view for new created item
    def get_absolute_url(self):
       return reverse("item:detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField() #short comments no paragraph
    created = models.DateTimeField(auto_now=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.body