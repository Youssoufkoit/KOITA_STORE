from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Paramètres
    email_notifications = models.BooleanField(default=True)
    order_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile de {self.user.username}"
    
    def get_total_orders(self):
        """Retourne le nombre total de commandes"""
        return self.user.user_orders.count() if hasattr(self.user, 'user_orders') else 0  # CORRIGÉ: user_orders
    
    def get_total_spent(self):
        """Retourne le montant total dépensé"""
        from django.db.models import Sum
        if not hasattr(self.user, 'user_orders'):  # CORRIGÉ: user_orders
            return 0
        total = self.user.user_orders.filter(  # CORRIGÉ: user_orders
            status__in=['completed', 'processing']
        ).aggregate(Sum('total_amount'))['total_amount__sum']
        return total if total else 0

# Signaux pour créer automatiquement un profil
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()