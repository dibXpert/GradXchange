from . import views
from django.urls import path

app_name='item'
urlpatterns = [
    #/item/ 
    path('', views.index, name='index'),
    path('item', views.item, name='item'),
    #/item/1
    path('<int:item_id>/', views.detail, name='detail'),

]

