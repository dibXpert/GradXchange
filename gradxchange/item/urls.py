from . import views
from django.urls import path

app_name='item'
urlpatterns = [
 
    
    path('', views.index, name='index'),
    #detail
    path('<int:pk>/', views.detail, name='detail'),
    #add item
    path('add', views.create_item, name='create_item'),
    #edit item
    path('edit/<int:id>/', views.update_item,name='update_item'),
    #delete item
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    
    #like
    path('like',views.like_item, name='like'),
    
    path('change_status/<int:item_id>/<str:new_status>/', views.change_status, name='change_status'),
    
    path('item/relist/<int:pk>/', views.relist_item, name='relist_item'),

    
       # #/item/ 
    # path('', views.IndexClassView.as_view(), name='index'),
    # #/item/1
    # path('<int:pk>/', views.ItemDetail.as_view(), name='detail'),
    # #add item
    # path('add/', views.CreateItem.as_view(), name='create_item'),

]

