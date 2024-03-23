"""
URL configuration for gradxchange project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as authentication_views
from django.conf import settings
from django.conf.urls.static import static
#item (homepage)
from item import views as item_views



urlpatterns = [

#first page 
    path('', item_views.index, name='index'),

    path('admin/', admin.site.urls),
    path('message/', include('message.urls')),
    
    path('service/', include('service.urls')),
    path('item/', include('item.urls')),
    
    path('signup/',user_views.signup, name='signup'),
    path('login/',authentication_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    #profile
    path('account/',user_views.accountPage, name='account'),
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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

