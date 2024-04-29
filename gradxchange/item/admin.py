from django.contrib import admin
from .models import Item,Comment

class ItemAdmin(admin.ModelAdmin):
    
    def change_to_default(self,request,queryset):
        queryset.update(item_desc="default")
        
    list_display = ('item_name', 'like_count', 'display_likers')
    search_fields = ['item_name']
    filter_horizontal = ('liked_by',)

    def like_count(self, obj):
        return obj.liked_by.count()
    like_count.short_description = 'Likes'

    def display_likers(self, obj):
        return ", ".join([user.username for user in obj.liked_by.all()])
    display_likers.short_description = 'Liked By'
    
class CommentAdmin(admin.ModelAdmin):
      search_fields = ('body',)
    
    
# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin )
