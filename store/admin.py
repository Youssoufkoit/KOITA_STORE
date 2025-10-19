from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration des catégories avec image"""
    list_display = ['name', 'slug', 'image_preview', 'products_count', 'icon_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Informations Principales', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('icon', 'image', 'image_preview', 'order'),
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def products_count(self, obj):
        count = obj.get_products_count()
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} produit(s)</span>',
            color, count
        )
    products_count.short_description = 'Nombre de produits'
    
    def icon_preview(self, obj):
        return format_html(
            '<i class="{}" style="font-size: 1.5rem; color: #ff6b35;"></i>',
            obj.icon
        )
    icon_preview.short_description = 'Icône'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; border-radius: 10px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Aucune image</span>')
    image_preview.short_description = 'Aperçu Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'stock_status', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    
    actions = ['mark_as_sold', 'mark_as_available']
    
    def price_display(self, obj):
        return format_html(
            '<span style="color: #ff6b35; font-weight: bold;">{:,.0f} FCFA</span>',
            float(obj.price)
        )
    price_display.short_description = 'Prix'
    
    def stock_status(self, obj):
        status = obj.get_stock_status()
        if status == 'out_of_stock':
            return format_html('<span style="color: red;">❌ Rupture</span>')
        elif status == 'low_stock':
            return format_html('<span style="color: orange;">⚠️ Stock bas</span>')
        return format_html('<span style="color: green;">✅ En stock</span>')
    stock_status.short_description = 'Stock'
    
    def mark_as_sold(self, request, queryset):
        queryset.update(stock=0, is_active=False)
        self.message_user(request, f'{queryset.count()} compte(s) marqué(s) comme vendu(s).')
    mark_as_sold.short_description = "💰 Marquer comme VENDU"
    
    def mark_as_available(self, request, queryset):
        queryset.update(stock=1, is_active=True)
        self.message_user(request, f'{queryset.count()} compte(s) marqué(s) comme disponible(s).')
    mark_as_available.short_description = "✅ Marquer comme DISPONIBLE"


admin.site.site_header = "🎮 KOITA_STORE - Administration"
admin.site.site_title = "KOITA_STORE Admin"
admin.site.index_title = "Tableau de bord"