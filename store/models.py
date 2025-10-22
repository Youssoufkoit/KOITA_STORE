from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    """Modèle pour les catégories de produits avec image"""
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Classe CSS de l'icône (ex: fas fa-gamepad)",
        verbose_name="Icône"
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name="Image de la catégorie",
        help_text="Image d'illustration de la catégorie (recommandé: 400x300px)"
    )
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_products_count(self):
        """Compte le nombre de produits liés à cette catégorie"""
        return self.products.count()


class Product(models.Model):
    """Modèle pour les produits (recharges ET comptes)"""
    class Product(models.Model):
    # ... champs existants ...
    
    # ===== NOUVEAU CHAMP =====
     requires_player_id = models.BooleanField(
        default=False,
        verbose_name='Requiert ID joueur',
        help_text='Afficher le champ ID joueur pour ce produit'
    )
    
    # ... reste des champs existants ...
    
    def requires_free_fire_id(self):
        """Vérifie si le produit nécessite un ID Free Fire (pour recharges automatiques)"""
        return self.requires_player_id
    # Champs communs
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA)")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
        related_name='products'
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    stock = models.IntegerField(default=0, verbose_name="Stock disponible")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_featured = models.BooleanField(default=False, verbose_name="Produit vedette")
    requires_player_id = models.BooleanField(
        default=False,
        verbose_name='Requiert ID joueur',
        help_text='Afficher le champ ID joueur pour ce produit'
    )
    # ===== CHAMPS SPÉCIFIQUES POUR LES COMPTES =====
    
    # Informations du compte
    account_level = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="Niveau du compte",
        help_text="Ex: 50, 65, 80, etc."
    )
    
    account_rank = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Rang/Grade",
        help_text="Ex: Héroïque, Grand Maître, Conqueror, etc."
    )
    
    has_elite_pass = models.BooleanField(
        default=False,
        verbose_name="Elite Pass actif"
    )
    
    diamonds_included = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Diamants inclus",
        help_text="Nombre de diamants sur le compte"
    )
    
    # Skins et bundles
    skins_list = models.TextField(
        blank=True,
        verbose_name="Liste des skins/bundles",
        help_text="Listez les skins rares (un par ligne)"
    )
    
    # Armes
    weapons_list = models.TextField(
        blank=True,
        verbose_name="Liste des armes",
        help_text="Listez les armes disponibles (un par ligne)"
    )
    
    # Véhicules
    vehicles_list = models.TextField(
        blank=True,
        verbose_name="Liste des véhicules/skyboards",
        help_text="Listez les véhicules disponibles (un par ligne)"
    )
    
    # Pets/Familiers
    pets_list = models.TextField(
        blank=True,
        verbose_name="Liste des pets",
        help_text="Listez les pets disponibles (un par ligne)"
    )
    
    # Sécurité
    email_changeable = models.BooleanField(
        default=True,
        verbose_name="Email changeable"
    )
    
    phone_linked = models.BooleanField(
        default=False,
        verbose_name="Numéro de téléphone lié"
    )
    
    facebook_linked = models.BooleanField(
        default=False,
        verbose_name="Facebook lié"
    )
    
    # Informations additionnelles
    account_region = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Région du compte",
        help_text="Ex: Afrique, Europe, Asie, etc.",
        choices=[
            ('', 'Non spécifié'),
            ('afrique', 'Afrique'),
            ('europe', 'Europe'),
            ('asie', 'Asie'),
            ('amerique', 'Amérique'),
            ('oceanie', 'Océanie'),
        ]
    )
    
    total_matches = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nombre total de matchs"
    )
    
    win_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taux de victoire (%)",
        help_text="Ex: 65.50 pour 65.50%"
    )
    
    # Notes internes
    internal_notes = models.TextField(
        blank=True,
        verbose_name="Notes internes",
        help_text="Notes visibles uniquement par l'admin (non affichées sur le site)"
    )
    
    # ===== CHAMPS REDEEM CODE =====
    is_redeem_product = models.BooleanField(
        default=False,
        verbose_name='Produit REDEEM',
        help_text='Cocher si ce produit nécessite un code REDEEM'
    )
    redeem_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Code REDEEM',
        help_text='Code unique à fournir après achat (pour produits REDEEM uniquement)'
    )
    redeem_code_used = models.BooleanField(
        default=False,
        verbose_name='Code REDEEM utilisé',
        help_text='Indique si le code a déjà été vendu'
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"
    
    def is_available(self):
        return self.stock > 0 and self.is_active
    
    def get_stock_status(self):
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock <= 5:
            return 'low_stock'
        else:
            return 'in_stock'
    
    def is_account(self):
        """Vérifie si c'est un compte de jeu"""
        if self.category:
            return 'compte' in self.category.slug.lower() or 'compte' in self.category.name.lower()
        return False
    
    def get_features_list(self):
        """Retourne une liste formatée des caractéristiques du compte"""
        features = []
        
        if self.account_level:
            features.append(f"Niveau {self.account_level}")
        
        if self.account_rank:
            features.append(f"Rang: {self.account_rank}")
        
        if self.has_elite_pass:
            features.append("Elite Pass actif")
        
        if self.diamonds_included:
            features.append(f"{self.diamonds_included} diamants inclus")
        
        if self.email_changeable:
            features.append("Email changeable")
        
        if self.win_rate:
            features.append(f"Win rate: {self.win_rate}%")
        
        return features
    
def requires_free_fire_id(self):
    """Vérifie si le produit nécessite un ID Free Fire (pour recharges automatiques)"""
    # Vérifier d'abord le champ booléen spécifique
    if self.requires_player_id:
        return True
    
    # Ensuite vérifier la catégorie pour la rétrocompatibilité
    if self.category:
        return 'free fire diamant' in self.category.name.lower()
    return False

class Order(models.Model):
    """Modèle de commande"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours'),
        ('completed', 'Complétée'),
        ('cancelled', 'Annulée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant total')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    free_fire_id = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name='ID Free Fire',
        help_text='ID Free Fire du joueur pour les recharges automatiques'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"
    
    def contains_free_fire_diamonds(self):
        """Vérifie si la commande contient des produits Free Fire Diamant"""
        return self.order_items.filter(
            product__category__name__icontains='free fire diamant'
        ).exists()
    
    def contains_diamond_codes(self):
        """Vérifie si la commande contient des codes diamants"""
        return self.order_items.filter(
            product__category__name__icontains='code diamant'
        ).exists()


class OrderItem(models.Model):
    """Articles d'une commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    redeem_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Code REDEEM fourni'
    )
    
    class Meta:
        verbose_name = 'Article de commande'
        verbose_name_plural = 'Articles de commande'
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def total_price(self):
        return self.price * self.quantity


class Notification(models.Model):
    """Notifications utilisateur"""
    TYPE_CHOICES = [
        ('order', 'Commande'),
        ('redeem', 'Code REDEEM'),
        ('info', 'Information'),
        ('warning', 'Avertissement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    redeem_code = models.CharField(max_length=50, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


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

