from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as authentication_views
from django.conf import settings
from django.conf.urls.static import static

#item (homepage)
from item import views as item_views

urlpatterns = [

    #landing page
    path('', item_views.index, name='index'),
    #admin site
    path('admin/', admin.site.urls),
    
    #item / service
    path('item/', include('item.urls')),
    path('service/', include('service.urls')),
   
    #authentication
    path('signup/',user_views.signup, name='signup'),
    path('login/',authentication_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    #profiles
    path('account/<str:username>/',user_views.accountPage, name='account'),
    #edit profile
    path('edit/',user_views.edit, name='edit'),
  
    #password change
    path('password_change/',authentication_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done',authentication_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    #password reset
    path('password_reset/', authentication_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),name="password_reset"),
    path('password_reset/done', authentication_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>', authentication_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',authentication_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    #messages
    path('inbox/', user_views.inbox, name='inbox'),
    path('message/<str:pk>/', user_views.viewMessage, name='message'),
    path('create_message/<int:profile_id>/', user_views.createMessage, name='create_message'),
  

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

