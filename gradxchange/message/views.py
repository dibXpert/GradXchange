from django.shortcuts import render
from .models import Message

# Create your views here.
def index(request):
    message_list =  Message.objects.all()


    return render(request, 'message/index.html', {
        'message_list':message_list })

def chat(request, slug):
    message = Message.objects.get(slug=slug)
    return render(request, 'message/chat.html', {'message':message})
    