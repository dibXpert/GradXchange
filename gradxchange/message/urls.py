from . import views
from django.urls import path

app_name='message'

urlpatterns = [

    path('', views.index, name='index'),
    path('<slug:slug>/', views.chat, name= 'chat'),
]