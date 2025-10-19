from django.db import models
from django.utils.text import slugify


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
    # NOUVEAU: Champ image ajouté
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
    """Modèle pour les produits"""
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