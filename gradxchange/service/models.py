from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal
from django.conf import settings
import datetime


class Service(models.Model):
    
    def __str__(self):
        return self.service_name
    
    tags = TaggableManager()
    service_name = models.CharField(max_length=200)
    service_desc = models.CharField(max_length=200)
    service_detail = models.CharField(max_length=2000)
    service_price = models.IntegerField()
    service_image = models.ImageField(upload_to='images_service', default="notfound.png")
    created =  models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='service_liked',blank= True)

   
    #service's detail view for new created service
    def get_absolute_url(self):
       return reverse("service:detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_comments')
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.body
   
