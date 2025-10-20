from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product
from django.core.mail import send_mail
from django.conf import settings
from store.models import Notification, Order, OrderItem

def get_or_create_cart(request):
    """Récupère ou crée un panier pour l'utilisateur"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_view(request):
    """Affiche le panier - CORRECTION: le nom doit être cart_view et non cart_detail"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    cart_total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    """Ajoute un produit au panier avec vérification du stock"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Vérifier si le produit est disponible
        if not product.is_available():
            messages.error(request, f'Désolé, {product.name} n\'est plus disponible !')
            return redirect('store:home')
        
        cart = get_or_create_cart(request)
        
        # Vérifier la quantité en stock
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # Vérifier si on peut ajouter plus d'unités
            if cart_item.quantity + 1 > product.stock:
                messages.error(request, f'Stock insuffisant pour {product.name} ! Stock disponible : {product.stock}')
                return redirect('cart:cart_view')
            
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'{product.name} ajouté au panier !')
        return redirect('cart:cart_view')
    
    return redirect('store:home')

def update_cart(request, item_id):
    """Met à jour la quantité avec vérification du stock"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Vérifier le stock disponible
        if quantity > cart_item.product.stock:
            messages.error(request, f'Stock insuffisant ! Disponible : {cart_item.product.stock}')
            return redirect('cart:cart_view')
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Panier mis à jour !')
        else:
            cart_item.delete()
            messages.success(request, 'Article retiré du panier')
    
    return redirect('cart:cart_view')

def remove_from_cart(request, item_id):
    """Supprime un article du panier"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        messages.success(request, 'Article retiré du panier')
    
    return redirect('cart:cart_view')

@login_required
def checkout(request):
    """Page de validation (réservé aux connectés)"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Votre panier est vide !')
        return redirect('cart:cart_view')
    
    cart_total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart/checkout.html', context)

@login_required
def order_success(request, order_id):
    """Page de confirmation"""
    return render(request, 'cart/order_success.html', {'order_id': order_id})

# cart/views.py - AJOUTER CES FONCTIONS

from django.core.mail import send_mail
from django.conf import settings
from store.models import Notification, Order, OrderItem

@login_required
def process_order(request):
    """Traiter la commande et envoyer les codes REDEEM"""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.error(request, 'Votre panier est vide!')
            return redirect('cart:cart_view')
        
        # Créer la commande
        total = sum(item.total_price() for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='processing'
        )
        
        # Créer les items de commande et gérer les codes REDEEM
        for cart_item in cart_items:
            product = cart_item.product
            
            # Vérifier le stock
            if product.stock < cart_item.quantity:
                order.delete()
                messages.error(request, f'Stock insuffisant pour {product.name}')
                return redirect('cart:cart_view')
            
            # Code REDEEM si applicable
            redeem_code_sent = ''
            if product.is_redeem_product and product.redeem_code and not product.redeem_code_used:
                redeem_code_sent = product.redeem_code
                product.redeem_code_used = True
                product.save()
            
            # Créer l'item de commande
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price,
                redeem_code=redeem_code_sent
            )
            
            # Réduire le stock
            product.stock -= cart_item.quantity
            product.save()
            
            # Envoyer le code REDEEM par email si disponible
            if redeem_code_sent:
                send_redeem_code_email(request.user, product, redeem_code_sent, order)
                
                # Créer une notification
                Notification.objects.create(
                    user=request.user,
                    notification_type='redeem',
                    title=f'🎁 Code REDEEM pour {product.name}',
                    message=f'Votre code REDEEM : {redeem_code_sent}',
                    redeem_code=redeem_code_sent,
                    order=order
                )
        
        # Vider le panier
        cart_items.delete()
        
        # Marquer la commande comme complétée
        order.status = 'completed'
        order.save()
        
        messages.success(request, f'✅ Commande #{order.id} validée! Consultez vos emails et notifications.')
        return redirect('cart:order_success', order_id=order.id)
    
    return redirect('cart:checkout')


def send_redeem_code_email(user, product, redeem_code, order):
    """Envoyer le code REDEEM par email"""
    subject = f'🎁 Votre code REDEEM pour {product.name} - KOITA_STORE'
    
    message = f"""
Bonjour {user.username},

Merci pour votre achat sur KOITA_STORE!

🎁 VOTRE CODE REDEEM :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{redeem_code}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Produit : {product.name}
💰 Prix : {product.price} FCFA
📅 Commande #{order.id}

💡 COMMENT UTILISER VOTRE CODE :

1. Rendez-vous sur : https://shop2game.com
2. Connectez-vous avec votre compte Free Fire
3. Entrez votre code REDEEM
4. Validez - Vos diamants seront ajoutés immédiatement !

⚠️ IMPORTANT :
- Ce code est à usage UNIQUE
- Conservez-le précieusement
- Il est également disponible dans votre espace "Mes Commandes"

Besoin d'aide ? Contactez-nous : contact@koitastore.com

Merci de votre confiance !
L'équipe KOITA_STORE
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )