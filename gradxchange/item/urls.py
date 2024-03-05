from . import views
from django.urls import path

app_name='item'
urlpatterns = [
    #/item/ 
    path('', views.IndexClassView.as_view(), name='index'),
    #/item/1
    path('<int:pk>/', views.ItemDetail.as_view(), name='detail'),
    #add item
    path('add/', views.CreateItem.as_view(), name='create_item'),
    
    #delete item
    path('delete/<int:id>/', views.delete_item, name='delete_item'),

]

