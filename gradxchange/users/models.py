from django.db import models
from  django.contrib.auth.models import User
import uuid
from django.core.validators import RegexValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_picture')
    location =models.CharField(max_length=100)
    # about me 
    about_me = models.CharField(max_length=200, null=True, blank=True)
    # Phone number validator for Malaysian format
    phone_regex = RegexValidator(
        regex=r'^\+?60?\d{9,10}$',
        message="Phone number must be entered in the format: '+60123456789'. With country code +60 and up to 10 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Optional: adjust max_length as needed


    # whatsapp number validator for Malaysian format
    whatsapp_regex = RegexValidator(
        regex=r'^\+?60?\d{9,10}$',
        message="Whatsapp number must be entered in the format: '+60123456789'. With country code +60 and up to 10 digits allowed."
    )
    whatsapp = models.CharField(validators=[whatsapp_regex], max_length=17, blank=True)


    
    
    
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
        return self.subject if self.subject is not None else "No Subject"

    
    class Meta:
        ordering = ['is_read', '-created'] 
    
    



    