from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product

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