from django.contrib import admin
from .models import Item,Comment

class ItemAdmin(admin.ModelAdmin):
    
    def change_to_default(self,request,queryset):
        queryset.update(item_desc="default")
        
    change_to_default.short_description ="Default"
    actions = ('change_to_default',)
    
    list_display = ('item_name','item_desc','item_price')
    search_fields = ('item_name',)
    
   # fields = ('item_name', 'item_price')
    list_editable = ('item_price','item_desc')
    
class CommentAdmin(admin.ModelAdmin):
      search_fields = ('body',)
    
    
# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin )
