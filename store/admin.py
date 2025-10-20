from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Notification


# ============================================
# ADMIN DES CATÉGORIES
# ============================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration des catégories"""
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


# ============================================
# PROXY MODELS
# ============================================

class RechargeProduct(Product):
    """Proxy model pour les Recharges uniquement"""
    class Meta:
        proxy = True
        verbose_name = "Recharge"
        verbose_name_plural = "📱 Recharges (Diamants, etc.)"


class AccountProduct(Product):
    """Proxy model pour les Comptes uniquement"""
    class Meta:
        proxy = True
        verbose_name = "Compte de Jeu"
        verbose_name_plural = "🎮 Comptes de Jeux"


# ============================================
# ADMIN DES RECHARGES AVEC SUPPORT REDEEM
# ============================================

@admin.register(RechargeProduct)
class RechargeProductAdmin(admin.ModelAdmin):
    """Administration des RECHARGES avec support REDEEM CODE"""
    
    list_display = [
        'name', 
        'category', 
        'price_display', 
        'stock_status', 
        'redeem_status',
        'is_featured', 
        'is_active'
    ]
    list_editable = ['is_featured', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured', 'is_redeem_product', 'redeem_code_used']
    search_fields = ['name', 'description', 'redeem_code']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'category', 'description')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock'),
            'description': 'Stock = nombre d\'unités disponibles'
        }),
        ('🎁 CODE REDEEM (Si applicable)', {
            'fields': (
                'is_redeem_product',
                'redeem_code',
                'redeem_code_used',
            ),
            'description': '⚠️ IMPORTANT : Si c\'est un produit REDEEM, cochez la case et entrez le code unique',
            'classes': ('wide',),
        }),
        ('Image', {
            'fields': ('image',),
        }),
        ('Options', {
            'fields': ('is_active', 'is_featured'),
        }),
    )
    
    actions = ['mark_as_featured', 'unmark_as_featured', 'add_stock', 'reset_redeem_codes']
    
    def get_queryset(self, request):
        """Afficher UNIQUEMENT les produits qui NE SONT PAS des comptes"""
        qs = super().get_queryset(request)
        return qs.exclude(category__slug__icontains='compte').exclude(category__name__icontains='compte')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limiter les catégories aux recharges seulement"""
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.exclude(
                slug__icontains='compte'
            ).exclude(
                name__icontains='compte'
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def price_display(self, obj):
        price_formatted = f"{float(obj.price):,.0f}"
        return format_html(
            '<span style="color: #ff6b35; font-weight: bold;">{} FCFA</span>',
            price_formatted
        )
    price_display.short_description = 'Prix'
    
    def stock_status(self, obj):
        status = obj.get_stock_status()
        if status == 'out_of_stock':
            return format_html('<span style="color: red;">❌ Rupture ({} unités)</span>', obj.stock)
        elif status == 'low_stock':
            return format_html('<span style="color: orange;">⚠️ Stock bas ({} unités)</span>', obj.stock)
        return format_html('<span style="color: green;">✅ En stock ({} unités)</span>', obj.stock)
    stock_status.short_description = 'Stock'
    
    def redeem_status(self, obj):
        """Afficher le statut du code REDEEM"""
        if not obj.is_redeem_product:
            return format_html('<span style="color: #999;">➖ Non REDEEM</span>')
        
        if obj.redeem_code_used:
            return format_html(
                '<span style="background: #e74c3c; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-weight: bold;">'
                '❌ CODE UTILISÉ'
                '</span>'
            )
        elif obj.redeem_code:
            return format_html(
                '<span style="background: #2ecc71; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-weight: bold;">'
                '✅ CODE DISPO: {}'
                '</span>',
                obj.redeem_code[:8] + '...' if len(obj.redeem_code) > 8 else obj.redeem_code
            )
        else:
            return format_html(
                '<span style="background: #f39c12; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-weight: bold;">'
                '⚠️ PAS DE CODE'
                '</span>'
            )
    redeem_status.short_description = 'Statut REDEEM'
    
    # ACTIONS
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'✅ {updated} recharge(s) mise(s) en vedette.')
    mark_as_featured.short_description = "⭐ Mettre en VEDETTE"
    
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} recharge(s) retirée(s) de la vedette.')
    unmark_as_featured.short_description = "Retirer de la VEDETTE"
    
    def add_stock(self, request, queryset):
        for product in queryset:
            product.stock += 10
            product.save()
        self.message_user(request, f'✅ Stock augmenté de 10 unités pour {queryset.count()} produit(s).')
    add_stock.short_description = "📦 Ajouter +10 au stock"
    
    def reset_redeem_codes(self, request, queryset):
        """Réinitialiser les codes REDEEM utilisés"""
        updated = queryset.filter(is_redeem_product=True).update(redeem_code_used=False)
        self.message_user(
            request, 
            f'🔄 {updated} code(s) REDEEM réinitialisé(s).',
            level='success'
        )
    reset_redeem_codes.short_description = "🔄 Réinitialiser codes REDEEM"


# ============================================
# ADMIN DES COMPTES (INCHANGÉ)
# ============================================

@admin.register(AccountProduct)
class AccountProductAdmin(admin.ModelAdmin):
    """Administration des COMPTES DE JEUX uniquement"""
    
    list_display = ['name', 'category', 'price_display', 'availability_status', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured', 'stock']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Informations du Compte', {
            'fields': ('name', 'category', 'description')
        }),
        ('Caractéristiques du Compte', {
            'fields': (
                'account_level',
                'account_rank',
                'has_elite_pass',
                'diamonds_included',
                'account_region',
            ),
            'description': '🎮 Informations spécifiques au compte de jeu'
        }),
        ('Skins, Armes et Items', {
            'fields': (
                'skins_list',
                'weapons_list',
                'vehicles_list',
                'pets_list',
            ),
            'classes': ('collapse',),
            'description': '📦 Listez les items disponibles (un par ligne)'
        }),
        ('Statistiques', {
            'fields': (
                'total_matches',
                'win_rate',
            ),
            'classes': ('collapse',),
        }),
        ('Sécurité', {
            'fields': (
                'email_changeable',
                'phone_linked',
                'facebook_linked',
            ),
            'description': '🔒 Informations de sécurité du compte'
        }),
        ('Prix et Disponibilité', {
            'fields': ('price', 'stock'),
            'description': '⚠️ Pour les comptes: Stock = 1 (disponible) ou 0 (vendu)'
        }),
        ('Image', {
            'fields': ('image',),
            'description': 'Screenshot du compte recommandé'
        }),
        ('Options', {
            'fields': ('is_active', 'is_featured'),
        }),
        ('Notes Internes', {
            'fields': ('internal_notes',),
            'classes': ('collapse',),
            'description': '📝 Notes visibles uniquement par vous'
        }),
    )
    
    actions = ['mark_as_sold', 'mark_as_available', 'mark_as_featured', 'unmark_as_featured']
    
    def get_queryset(self, request):
        """Afficher UNIQUEMENT les comptes"""
        qs = super().get_queryset(request)
        from django.db.models import Q
        return qs.filter(
            Q(category__slug__icontains='compte') | 
            Q(category__name__icontains='compte')
        )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limiter les catégories aux comptes seulement"""
        if db_field.name == "category":
            from django.db.models import Q
            kwargs["queryset"] = Category.objects.filter(
                Q(slug__icontains='compte') | 
                Q(name__icontains='compte')
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def price_display(self, obj):
        price_formatted = f"{float(obj.price):,.0f}"
        return format_html(
            '<span style="color: #667eea; font-weight: bold;">{} FCFA</span>',
            price_formatted
        )
    price_display.short_description = 'Prix'
    
    def availability_status(self, obj):
        """Statut spécifique pour les comptes"""
        if obj.stock > 0 and obj.is_active:
            return format_html(
                '<span style="background: #2ecc71; color: white; padding: 0.4rem 0.8rem; border-radius: 15px; font-weight: bold;">'
                '✅ DISPONIBLE'
                '</span>'
            )
        else:
            return format_html(
                '<span style="background: #e74c3c; color: white; padding: 0.4rem 0.8rem; border-radius: 15px; font-weight: bold;">'
                '❌ VENDU'
                '</span>'
            )
    availability_status.short_description = 'Statut'
    
    def mark_as_sold(self, request, queryset):
        updated = queryset.update(stock=0, is_active=False)
        self.message_user(request, f'💰 {updated} compte(s) marqué(s) comme VENDU(S).', level='success')
    mark_as_sold.short_description = "💰 Marquer comme VENDU"
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(stock=1, is_active=True)
        self.message_user(request, f'✅ {updated} compte(s) marqué(s) comme DISPONIBLE(S).', level='success')
    mark_as_available.short_description = "✅ Marquer comme DISPONIBLE"
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'⭐ {updated} compte(s) mis en vedette.')
    mark_as_featured.short_description = "⭐ Mettre en VEDETTE"
    
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} compte(s) retiré(s) de la vedette.')
    unmark_as_featured.short_description = "Retirer de la VEDETTE"


# ============================================
# ADMIN DES COMMANDES
# ============================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'redeem_code']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations Commande', {
            'fields': ('user', 'total_amount', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']


# ============================================
# PERSONNALISATION DU SITE ADMIN
# ============================================

admin.site.site_header = "🎮 KOITA_STORE - Administration"
admin.site.site_title = "KOITA_STORE Admin"
admin.site.index_title = "📊 Tableau de bord"