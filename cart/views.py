from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product
from django.core.mail import send_mail
from django.conf import settings
from store.models import Notification, Order, OrderItem
import logging

logger = logging.getLogger(__name__)

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
    """Page de validation avec demande d'ID Free Fire si nécessaire"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Votre panier est vide !')
        return redirect('cart:cart_view')
    
    # Vérifier si des produits nécessitent l'ID Free Fire
    requires_free_fire_id = any(
        item.product.category and 
        ('free fire diamant' in item.product.category.name.lower() or 
         item.product.category.slug == 'free-fire-diamant')
        for item in cart_items
    )
    
    cart_total = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST' and requires_free_fire_id:
        free_fire_id = request.POST.get('free_fire_id', '').strip()
        if not free_fire_id:
            messages.error(request, '❌ ID Free Fire requis pour les recharges automatiques!')
        else:
            # Stocker l'ID dans la session temporairement
            request.session['free_fire_id'] = free_fire_id
            return redirect('cart:process_order')
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'requires_free_fire_id': requires_free_fire_id,
        'free_fire_id': request.session.get('free_fire_id', ''),
    }
    return render(request, 'cart/checkout.html', context)

@login_required
def order_success(request, order_id):
    """Page de confirmation"""
    return render(request, 'cart/order_success.html', {'order_id': order_id})

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

def send_redeem_fallback_email(user, product, redeem_code, order, free_fire_id, error_message):
    """Email de fallback pour recharge manuelle"""
    subject = f'🔧 Action Requise - Recharge Free Fire - Commande #{order.id}'
    
    message = f"""
Bonjour {user.username},

Votre commande #{order.id} a été traitée, mais la recharge automatique a rencontré un problème.

📋 DÉTAILS DE LA COMMANDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produit: {product.name}
ID Free Fire: {free_fire_id}
Code REDEEM: {redeem_code}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ PROBLÈME RENCONTRÉ:
{error_message}

🔧 ACTION REQUISE:

1. Rendez-vous sur : https://shop2game.com/?channel=299999
2. Entrez votre ID Free Fire: {free_fire_id}
3. Cliquez sur "Redeem"
4. Entrez votre code: {redeem_code}
5. Validez la transaction

⚠️ IMPORTANT:
- Cette opération doit être faite dans les 24h
- Conservez ce code précieusement
- En cas de difficulté, contactez-nous immédiatement

Nous restons à votre disposition pour toute assistance.

L'équipe KOITA_STORE
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def handle_automatic_recharge(user, product, redeem_code, order, free_fire_id):
    """
    Gère la recharge automatique avec gestion robuste des erreurs
    """
    try:
        from scripts.shop2game_redeem import Shop2GameRedeemer
        redeemer = Shop2GameRedeemer()
        
        logger.info(f"🔄 Tentative de recharge automatique - Produit: {product.name}, ID: {free_fire_id}")
        
        # Tentative de recharge automatique
        success, message = redeemer.redeem_diamonds(free_fire_id, redeem_code)
        
        if success:
            logger.info(f"✅ Recharge automatique réussie - {message}")
            
            # Notification de succès
            Notification.objects.create(
                user=user,
                notification_type='redeem',
                title='✅ Diamants ajoutés avec succès!',
                message=f'Vos {product.name} ont été ajoutés à votre compte Free Fire (ID: {free_fire_id})',
                redeem_code=redeem_code,
                order=order
            )
            
            # Email de confirmation
            send_mail(
                f'✅ Recharge réussie - {product.name}',
                f'Vos {product.name} ont été ajoutés avec succès à votre compte Free Fire (ID: {free_fire_id}).',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
        else:
            logger.warning(f"⚠️ Recharge automatique échouée - {message}")
            
            # Fallback manuel
            handle_manual_fallback(user, product, redeem_code, order, free_fire_id, message)
            
    except Exception as e:
        logger.error(f"❌ Erreur critique lors de la recharge automatique: {str(e)}", exc_info=True)
        
        # Fallback manuel en cas d'erreur critique
        handle_manual_fallback(user, product, redeem_code, order, free_fire_id, f"Erreur système: {str(e)}")

def handle_manual_fallback(user, product, redeem_code, order, free_fire_id, error_message):
    """
    Gère le fallback manuel en cas d'échec de la recharge automatique
    """
    try:
        logger.info(f"🔄 Activation du mode manuel - Raison: {error_message}")
        
        # Email de fallback avec instructions manuelles
        send_redeem_fallback_email(user, product, redeem_code, order, free_fire_id, error_message)
        
        # Notification pour l'utilisateur
        Notification.objects.create(
            user=user,
            notification_type='redeem',
            title='🔧 Action Manuelle Requise - Recharge Free Fire',
            message=f'Utilisez votre code REDEEM: {redeem_code} avec votre ID: {free_fire_id} sur shop2game.com. Raison: {error_message}',
            redeem_code=redeem_code,
            order=order
        )
        
        logger.info("✅ Fallback manuel configuré avec succès")
        
    except Exception as fallback_error:
        logger.critical(f"💥 ERREUR CRITIQUE: Échec du fallback manuel - {str(fallback_error)}", exc_info=True)
        
        # Dernier recours - notification admin
        send_mail(
            '🚨 ERREUR CRITIQUE - Système de recharge KOITA_STORE',
            f'Erreur critique dans le système de recharge:\n\n'
            f'Utilisateur: {user.username}\n'
            f'Commande: #{order.id}\n'
            f'Produit: {product.name}\n'
            f'Erreur initiale: {error_message}\n'
            f'Erreur fallback: {str(fallback_error)}\n\n'
            f'Action requise IMMÉDIATEMENT!',
            settings.DEFAULT_FROM_EMAIL,
            ['admin@koitastore.com'],  # Remplacez par votre email admin
            fail_silently=False,
        )

@login_required
def process_order(request):
    """Traiter la commande avec support des deux catégories"""
    
    # Début du traitement
    logger.info(f"🚀 Début du traitement de commande - Utilisateur: {request.user.username}")
    
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        logger.info(f"📦 Panier contenant {len(cart_items)} articles - Utilisateur: {request.user.username}")
        
        if not cart_items:
            logger.warning("❌ Tentative de commande avec panier vide")
            messages.error(request, 'Votre panier est vide!')
            return redirect('cart:cart_view')
        
        # Récupérer l'ID Free Fire si nécessaire
        free_fire_id = request.session.pop('free_fire_id', '')
        logger.info(f"🎮 ID Free Fire récupéré: {free_fire_id}")
        
        # Créer la commande
        total = sum(item.total_price() for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            free_fire_id=free_fire_id,
            status='processing'
        )
        
        logger.info(f"✅ Commande #{order.id} créée - Montant: {total} FCFA")
        
        # Traiter chaque article
        for index, cart_item in enumerate(cart_items):
            product = cart_item.product
            logger.info(f"📋 Traitement article {index+1}/{len(cart_items)}: {product.name} (x{cart_item.quantity})")
            
            # Vérifier le stock
            if product.stock < cart_item.quantity:
                logger.error(f"❌ Stock insuffisant: {product.name} (stock: {product.stock}, demande: {cart_item.quantity})")
                order.delete()
                messages.error(request, f'Stock insuffisant pour {product.name}')
                return redirect('cart:cart_view')
            
            # Gérer selon la catégorie
            category_name = product.category.name.lower() if product.category else ""
            redeem_code_sent = ''
            
            logger.info(f"🏷️ Catégorie produit: {category_name}")
            
            if product.is_redeem_product and product.redeem_code and not product.redeem_code_used:
                redeem_code_sent = product.redeem_code
                product.redeem_code_used = True
                product.save()
                logger.info(f"🎁 Code REDEEM utilisé: {redeem_code_sent} pour {product.name}")
            
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
            logger.info(f"📦 Stock mis à jour: {product.name} -> {product.stock} unités")
            
            # === TRAITEMENT SPÉCIFIQUE PAR CATÉGORIE ===
            
            # Catégorie "Free Fire Diamant" - Recharge automatique
            if 'free fire diamant' in category_name and free_fire_id and redeem_code_sent:
                logger.info(f"🔄 Déclenchement recharge automatique pour {product.name}")
                handle_automatic_recharge(request.user, product, redeem_code_sent, order, free_fire_id)
            
            # Catégorie "Code Diamant FF" - Envoi simple du code
            elif 'code diamant' in category_name and redeem_code_sent:
                logger.info(f"📧 Envoi simple code REDEEM pour {product.name}")
                try:
                    send_redeem_code_email(request.user, product, redeem_code_sent, order)
                    logger.info("✅ Email de code REDEEM envoyé")
                    
                    Notification.objects.create(
                        user=request.user,
                        notification_type='redeem',
                        title=f'🎁 Code REDEEM pour {product.name}',
                        message=f'Votre code REDEEM : {redeem_code_sent}',
                        redeem_code=redeem_code_sent,
                        order=order
                    )
                    
                except Exception as e:
                    logger.error(f"❌ Erreur envoi email code: {str(e)}", exc_info=True)
                    # Fallback - notification uniquement
                    Notification.objects.create(
                        user=request.user,
                        notification_type='redeem',
                        title=f'🎁 Code REDEEM pour {product.name}',
                        message=f'Votre code REDEEM : {redeem_code_sent} (Erreur envoi email: {str(e)})',
                        redeem_code=redeem_code_sent,
                        order=order
                    )
        
        # Vider le panier
        cart_items_count = cart_items.count()
        cart_items.delete()
        logger.info(f"🛒 Panier vidé - {cart_items_count} articles supprimés")
        
        # Marquer la commande comme complétée
        order.status = 'completed'
        order.save()
        logger.info(f"✅ Commande #{order.id} marquée comme complétée")
        
        messages.success(request, f'✅ Commande #{order.id} validée!')
        logger.info(f"🎉 Processus de commande terminé avec succès - Commande #{order.id}")
        
        return redirect('cart:order_success', order_id=order.id)
    
    logger.warning("❌ Méthode non POST pour process_order")
    return redirect('cart:checkout')