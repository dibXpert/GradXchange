from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('services', views.services, name='services'),

]