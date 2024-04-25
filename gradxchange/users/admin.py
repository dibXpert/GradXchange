from django.contrib import admin
from .models import Profile
from .models import Message
# Register your models here.

admin.site.site_header = "GradXchange Marketplace Web Application"
admin.site.site_title = "GradXchange"
admin.site.index_title = "Manage GradXchange Marketplace"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('display_sender', 'display_recipient', 'text', 'is_read', 'created')
    search_fields = ('text',)

    def display_sender(self, obj):
        return obj.sender.user.username if obj.sender else "Unknown"
    display_sender.short_description = 'Sender'

    def display_recipient(self, obj):
        return obj.recipient.user.username if obj.recipient else "Unknown"
    display_recipient.short_description = 'Recipient'


admin.site.register(Profile)
admin.site.register(Message, MessageAdmin)