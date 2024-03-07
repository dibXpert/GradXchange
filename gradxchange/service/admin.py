from django.contrib import admin
from .models import Service

class ServiceAdmin(admin.ModelAdmin):
    
    def change_to_default(self,request,queryset):
        queryset.update(service_desc="default")
        
    change_to_default.short_description ="Default"
    actions = ('change_to_default',)
    
    list_display = ('service_name','service_desc','service_price')
    search_fields = ('service_name',)
    
    fields = ('service_name', 'service_price',)
    list_editable = ('service_price','service_desc')

admin.site.register(Service, ServiceAdmin)