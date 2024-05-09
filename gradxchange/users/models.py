from django.db import models
from  django.contrib.auth.models import User
import uuid
from django.core.validators import RegexValidator


#This model extends the default user model by attaching a one-to-one field to the Django User model. It includes additional fields like image, location, about_me, phone, and whatsapp, each with specific validators where needed (e.g., phone and WhatsApp number validation for Malaysian format). This model is essential for storing extended user information that the default Django User model does not handle.
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

# Defines a Message class where each message has a sender and recipient, both linked to user profiles. Messages are stored with attributes like text content, read status, creation time, and a unique identifier. The model also anticipates grouping by conversations, indicated by a conversation_id.
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages')
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')
    text = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    # Ensure conversation_id is defined if you're grouping by conversations
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=True)

    def __str__(self):
        return f'From: {self.sender.user.username if self.sender else "Unknown"} - To: {self.recipient.user.username if self.recipient else "Unknown"}'
    
    class Meta:
        ordering = ['is_read', '-created'] 
    
    



    