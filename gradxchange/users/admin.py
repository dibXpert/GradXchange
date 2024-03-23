from django.contrib import admin
from .models import Profile
from .models import Message
# Register your models here.

admin.site.site_header = "GradXchange Marketplace Web Application"
admin.site.site_title = "GradXchange"
admin.site.index_title = "Manage GradXchange Marketplace"




admin.site.register(Profile)
admin.site.register(Message)