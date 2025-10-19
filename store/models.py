from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('recharge', 'Recharge Free Fire'),
        ('account', 'Compte de Jeu'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Catégorie")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    stock = models.IntegerField(default=0, verbose_name="Stock disponible")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
    
    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"
    
    def is_available(self):
        """Vérifie si le produit est en stock"""
        return self.stock > 0 and self.is_active