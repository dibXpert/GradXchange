from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# A signal receiver connected to the post_save signal of the Django User model. It automatically creates a Profile instance whenever a new User is created. This is crucial for maintaining a one-to-one relationship between User and Profile, ensuring that each user has exactly one associated profile.
@receiver(post_save,sender=User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
#Also a receiver for the post_save signal but it focuses on saving the profile instance whenever the User instance is saved. This ensures that changes to the user model trigger updates in the related profile model, keeping data consistent across the application.
@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()
    
    
#Signal Setup: The post_save signal from Django’s User model is used. This signal is triggered every time a User object is saved, which includes when a new user is created.
#Signal Receiver: The build_profile function is marked as a receiver for the post_save signal, specifically listening to changes from the User model. It checks whether the user has been created (if created:) and not just updated. If it's a new user, Profile.objects.create(user=instance) executes, which creates a new Profile instance associated with the new user.
#Automatic Execution: Because this process is connected to the post_save signal of the User model and is configured to run when a new user is created, it guarantees that a Profile will exist for every user immediately after their user record is created during registration
