from . import views
from django.urls import path

app_name='service'
urlpatterns = [
    path('', views.index, name='index'),
    #detail
    path('<int:pk>/', views.detail, name='detail'),
    #add service
    path('add', views.create_service, name='create_service'),
    #edit service
    path('edit/<int:id>/', views.update_service,name='update_service'),
    #delete service
    path('delete/<int:id>/', views.delete_service,name='delete_service'),
    
    path('like',views.like_service, name='like_service'),

]