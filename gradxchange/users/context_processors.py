from django.contrib.auth.models import User
from .models import Message  # Adjust the import according to your models

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user.profile, is_read=False).count()
        return {'unread_message_count': count}
    return {}