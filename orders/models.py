from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Order(models.Model):
    """Modèle de commande séparé"""
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

# Create your models here.
