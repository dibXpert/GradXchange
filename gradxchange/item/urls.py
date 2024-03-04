from . import views
from django.urls import path

app_name='item'
urlpatterns = [
    #/item/ 
    path('', views.IndexClassView.as_view(), name='index'),
    #/item/1
    path('<int:pk>/', views.ItemDetail.as_view(), name='detail'),

]

