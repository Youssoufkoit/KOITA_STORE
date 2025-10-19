from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration des catégories"""
    list_display = ['name', 'slug', 'products_count', 'icon_preview', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Informations Principales', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('icon', 'order')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def products_count(self, obj):
        """Affiche le nombre de produits dans la catégorie"""
        count = obj.get_products_count()
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} produits</span>',
            color, count
        )
    products_count.short_description = 'Nombre de produits'
    
    def icon_preview(self, obj):
        """Prévisualise l'icône"""
        return format_html(
            '<i class="{}" style="font-size: 1.5rem; color: #ff6b35;"></i>',
            obj.icon
        )
    icon_preview.short_description = 'Icône'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administration des produits"""
    list_display = [
        'name', 
        'category', 
        'price_display', 
        'stock_status', 
        'is_featured', 
        'is_active',
        'created_at'
    ]
    list_editable = ['is_featured', 'is_active']
    list_filter = [
        'category', 
        'is_active', 
        'is_featured', 
        'created_at',
        'updated_at'
    ]
    search_fields = ['name', 'description', 'category__name']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations Principales', {
            'fields': ('name', 'description', 'category')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock'),
            'description': 'Gérez le prix en FCFA et le stock disponible'
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Options', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        """Affiche le prix formaté"""
        return format_html(
            '<span style="color: #ff6b35; font-weight: bold; font-size: 1.1rem;">{:,.0f} FCFA</span>',
            obj.price
        )
    price_display.short_description = 'Prix'
    
    def stock_status(self, obj):
        """Affiche le statut du stock avec couleur"""
        status = obj.get_stock_status()
        
        if status == 'out_of_stock':
            color = 'red'
            icon = '❌'
            text = f'Rupture ({obj.stock})'
        elif status == 'low_stock':
            color = 'orange'
            icon = '⚠️'
            text = f'Stock bas ({obj.stock})'
        else:
            color = 'green'
            icon = '✅'
            text = f'En stock ({obj.stock})'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, text
        )
    stock_status.short_description = 'Statut Stock'
    
    def image_preview(self, obj):
        """Prévisualise l'image du produit"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Aucune image</span>')
    image_preview.short_description = 'Aperçu Image'
    
    actions = [
        'mark_as_active',
        'mark_as_inactive',
        'mark_as_featured',
        'mark_as_not_featured',
        'reset_stock'
    ]
    
    def mark_as_active(self, request, queryset):
        """Active les produits sélectionnés"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} produit(s) activé(s).')
    mark_as_active.short_description = "✅ Activer les produits sélectionnés"
    
    def mark_as_inactive(self, request, queryset):
        """Désactive les produits sélectionnés"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} produit(s) désactivé(s).')
    mark_as_inactive.short_description = "❌ Désactiver les produits sélectionnés"
    
    def mark_as_featured(self, request, queryset):
        """Marque les produits comme vedette"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} produit(s) marqué(s) en vedette.')
    mark_as_featured.short_description = "⭐ Marquer comme vedette"
    
    def mark_as_not_featured(self, request, queryset):
        """Retire le statut vedette"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} produit(s) retiré(s) de la vedette.')
    mark_as_not_featured.short_description = "⭐ Retirer de la vedette"
    
    def reset_stock(self, request, queryset):
        """Remet le stock à 0"""
        updated = queryset.update(stock=0)
        self.message_user(request, f'Stock remis à 0 pour {updated} produit(s).')
    reset_stock.short_description = "🔄 Remettre le stock à 0"


# Personnalisation du titre de l'admin
admin.site.site_header = "🎮 RealGames - Administration"
admin.site.site_title = "RealGames Admin"
admin.site.index_title = "Tableau de bord"