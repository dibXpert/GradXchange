from django.db import models
from  django.contrib.auth.models import User
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_picture')
    location =models.CharField(max_length=100)
    
    
    
    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    #relationship with Profile
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True, editable=False)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created'] 
    
    



    