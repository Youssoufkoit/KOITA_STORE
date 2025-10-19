from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at', 'is_available')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    
    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True
    is_available.short_description = 'Disponible'