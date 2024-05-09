from django.contrib.auth.models import User
from .models import Message  # Adjust the import according to your models

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user.profile, is_read=False).count()
        return {'unread_message_count': count}
    return {}

#Context processors in Django are Python functions that add context variables to the context dictionary for use in rendering templates. Essentially, they allow you to make certain data available globally to all templates without needing to manually pass those variables to each template in every view function.