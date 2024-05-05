from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as authentication_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    #home page
    path('', user_views.home, name='home'),
    #admin site
    path('admin/', admin.site.urls),
    
    #item / service
    path('item/', include('item.urls')),
    path('service/', include('service.urls')),
   
    #authentication
    path('signup/',user_views.signup, name='signup'),
    path('login/', user_views.custom_login, name='login'),

    # path('login/',authentication_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    #profiles
    path('account/<str:username>/',user_views.accountPage, name='account'),
    #edit profile
    path('edit/',user_views.edit, name='edit'),
    #edit about me
    path('edit_about/',user_views.edit_about, name='edit_about'),
    
    #whatsapp 
    path('redirect_to_whatsapp/<str:whatsapp_number>/', user_views.redirectToWhatsApp, name='redirect_to_whatsapp'),

  
    #password change
    path('password_change/',authentication_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done',authentication_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    #password reset
    #submit email form
    path('password_reset/', authentication_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),name="password_reset"),
    #Email sent success message
    path('password_reset/done', authentication_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name="password_reset_done"),
    #Link to password rest form in email
    path('reset/<uidb64>/<token>', authentication_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    #Password successfully changed message
    path('reset/done/',authentication_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    #messages
    path('inbox/', user_views.inbox, name='inbox'),
    path('chat/<int:profile_id>/', user_views.chat, name='chat'),

   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


